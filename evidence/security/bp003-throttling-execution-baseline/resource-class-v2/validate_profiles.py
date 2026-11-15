"""Document-only validation. No runtime, network or workload execution."""

import copy
import fnmatch
import graphlib
import hashlib
import json
from pathlib import Path
import re
import subprocess

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[4]
BASE = "5d465868b23e283f3baed530c98931322cc839ed"
DIRECTORY = Path(__file__).resolve().parent
PREFIX = "docs/04-quality/benchmark-profiles/"
PATHS = [PREFIX + "BP-003-throttling-hardware-reference.yaml",
         PREFIX + "BP-003-throttling-threat-workload.yaml"]
checks = {}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def check(name, condition):
    checks[name] = "PASS" if condition else "FAIL"
    if not condition:
        raise ValueError(name)


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def digest(data):
    payload = {key: data[key] for key in ("profile_id", "version", "spec")}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node):
    pairs = loader.construct_pairs(node, deep=True)
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate YAML mapping key")
    return dict(pairs)


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                             unique_mapping)
new = [yaml.load((ROOT / p).read_text(encoding="utf-8"), Loader=UniqueLoader)
       for p in PATHS]
old = [yaml.load(git("show", BASE + ":" + p), Loader=UniqueLoader) for p in PATHS]
check("yaml_valid_unique_keys", all(isinstance(p["spec"], dict) for p in new))
check("approved_v1_inputs_preserved_in_baseline", all(
    git("show", "4b634381328bd969679abe48ee6936aaf8fe4319:" + p)
    == git("show", BASE + ":" + p) and digest(d) == d["definition_sha256"]
    for p, d in zip(PATHS, old)))
for i, profile in enumerate(new):
    peer = new[1 - i]
    check(f"version_and_id_{i}", profile["version"] == "2.0.0"
          and old[i]["version"] == "1.0.0"
          and profile["profile_id"] == old[i]["profile_id"])
    check(f"canonical_digest_{i}", digest(profile) == profile["definition_sha256"])
    companion = profile["companion"]
    check(f"companion_{i}", companion["path"] == PATHS[1 - i]
          and companion["profile_id"] == peer["profile_id"]
          and companion["version"] == peer["version"]
          and companion["definition_sha256"] == digest(peer))
    check(f"approval_not_inherited_{i}",
          profile["approval_state"] == "PENDING_INDEPENDENT_REVIEW")

expected = copy.deepcopy(old[1]["spec"])
expected["hardware_profile_version"] = "2.0.0"
check("entire_workload_unchanged_except_hardware_version", new[1]["spec"] == expected)
for section in ("security_acceptance", "resource_and_dos_acceptance", "traffic",
                "fixtures", "reproduction", "observables_minimum"):
    check(section + "_identical", new[1]["spec"][section] == old[1]["spec"][section])
hardware = new[0]["spec"]
check("no_exact_sku_or_clock_requirement", not any(
    key in hardware["cpu"] for key in ("processor_model", "physical_cores_allocated",
                                      "nominal_frequency_mhz", "threads_per_core_used"))
    and not re.search(r"7313|EPYC|3000 MHz", json.dumps(hardware)))
cpu = hardware["cpu"]
check("four_cpu_reference_budget", cpu["architecture"] == "x86_64"
      and cpu["vendors"] == ["Intel", "AMD"]
      and cpu["execution_cpus_available_min"] == 4
      and cpu["reference_execution_cpus_reserved"] == 4
      and cpu["api_execution_cpu_budget"] + cpu["postgresql_execution_cpu_budget"] == 4)
ram = hardware["ram"]
check("ram_reference_budget", ram["target_available_or_reservable_bytes_min"] == 16 * 2**30
      and ram["reference_target_reserved_bytes"] == 16 * 2**30
      and ram["api_cgroup_max_bytes"] == 4 * 2**30
      and ram["postgresql_cgroup_max_bytes"] == 8 * 2**30
      and ram["os_and_measurement_reserve_bytes"] == 4 * 2**30)
check("storage_capacity_and_durability_preserved",
      hardware["storage"]["free_bytes_before_each_repetition_min"] == 100 * 2**30
      and hardware["storage"]["durability"] == old[0]["spec"]["storage"]["durability"])
for key in ("python", "postgresql_family", "deployment", "exact_pins", "transport", "api_processes"):
    check("runtime_preserved_" + key, hardware["runtime"][key] == old[0]["spec"]["runtime"][key])
check("minimum_supported_false", hardware["minimum_supported_claim"] is False)
document = ROOT / PREFIX / "BP-003-security-runtime-calibration.md"
links = re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8"))
check("bp003_document_links", bool(links) and all(
    (document.parent / link).resolve().is_file() for link in links))
manifest = json.loads((DIRECTORY / "artifact-manifest.json").read_text(encoding="utf-8"))
check("manifest_artifact_digests", all(
    hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest() == item["file_sha256"]
    for item in manifest["artifacts"]))
task = load(".codex/tasks/TASK-0770.json")
jsonschema.Draft202012Validator(load(".codex/tasks/TASK_ENVELOPE.schema.json")).validate(task)
check("task_schema", True)
index = load("docs/06-delivery/STORY_INDEX.json")["stories"]
matches = [s for s in index if s["story_id"] == task["story_id"]]
check("unique_identity_index", len(matches) == 1 and matches[0]["task_id"] == task["task_id"]
      and matches[0]["issue_id"] == task["issue_id"]
      and matches[0]["dependencies"] == task["dependencies"])
graph = load("docs/06-delivery/STORY_DEPENDENCY_GRAPH.json")
dependencies = {node["id"]: set() for node in graph["nodes"]}
for edge in graph["edges"]:
    check("dag_endpoints_exist", edge["from"] in dependencies and edge["to"] in dependencies)
    dependencies[edge["to"]].add(edge["from"])
list(graphlib.TopologicalSorter(dependencies).static_order())
check("dag_acyclic_and_predecessors", dependencies[task["story_id"]] == set(task["dependencies"]))
changed = git("diff", BASE, "--name-only").decode().splitlines()
untracked = git("ls-files", "--others", "--exclude-standard").decode().splitlines()
relevant_untracked = [p for p in untracked if p != "src/frontend/debug.log"]
check("write_scope", all(any(fnmatch.fnmatchcase(p, a) for a in task["allow_paths"])
                         for p in changed + relevant_untracked))
check("historical_evidence_unchanged", all(
    not p.startswith("evidence/security/bp003-throttling-execution-baseline/")
    or "/resource-class-v2/" in p for p in changed))
subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
check("whitespace", True)
report = {"baseline_sha": BASE, "checks": checks,
          "benchmark_executed": False, "independent_approval": False,
          "profile_schema": "No normative profile schema supplied; unique-key YAML, semantic invariants and canonical bindings checked.",
          "artifacts": [{"path": p, "version": n["version"],
                         "definition_sha256": digest(n),
                         "file_sha256": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()}
                        for p, n in zip(PATHS, new)]}
(DIRECTORY / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(report, indent=2))
