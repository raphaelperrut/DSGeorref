"""Disposable Git histories and signed DAA fixtures; no real Stage A evidence."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from tools.governance.delivery_approval_authority.crypto import digest
from tools.governance.delivery_gates.model import GRAPH, REGISTRY, SCHEMA, TASK_SCHEMA, sha256

ROOT = Path(__file__).resolve().parents[3]
GATE_ID = "DG-TASK-0738-A"
SAR = "docs/02-architecture/sar/SAR-120-DELIVERY-DEPENDENCY-VIEW.md"
ADR = (
    "docs/02-architecture/adrs/"
    "ADR-006-prompts-permanentes-taskenvelope-e-precedencia-de-instrucoes.md"
)


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *arguments], check=True, capture_output=True, text=True
    ).stdout.strip()


def write(root: Path, path: str, value: Any) -> dict[str, str]:
    destination = root / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    content = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()
    destination.write_bytes(content)
    return {"path": path, "sha256": sha256(content)}


def commit(root: Path, message: str) -> str:
    git(root, "add", ".")
    git(root, "commit", "--quiet", "-m", message)
    return git(root, "rev-parse", "HEAD")


def planning_fixture(root: Path) -> Path:
    root.mkdir()
    for path in (SCHEMA, REGISTRY, TASK_SCHEMA, SAR, ADR):
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, root / path)
    graph = json.loads((ROOT / GRAPH).read_text(encoding="utf-8"))
    selected = {"STORY-0036", "STORY-0038", "STORY-0185", "STORY-0738"}
    nodes = [node for node in graph["nodes"] if node["id"] in selected]
    edges = [
        {"from": "STORY-0036", "to": "STORY-0038"},
        {"from": "STORY-0038", "to": "STORY-0185"},
        {"from": "STORY-0185", "to": "STORY-0738"},
    ]
    write(root, GRAPH, {"nodes": nodes, "edges": edges})
    for node in nodes:
        path = f".codex/tasks/{node['task_id']}.json"
        task = json.loads((ROOT / path).read_text(encoding="utf-8"))
        task["dependencies"] = [edge["from"] for edge in edges if edge["to"] == node["id"]]
        write(root, path, task)
    index = "story_id,status\nSTORY-0036,done\nSTORY-0038,planned\n"
    index += "STORY-0185,planned\nSTORY-0738,planned\n"
    (root / "docs/06-delivery/STORY_INDEX.csv").write_text(index, encoding="utf-8")
    git(root, "init", "--quiet", "-b", "main")
    git(root, "config", "user.name", "delivery gate test")
    git(root, "config", "user.email", "gate@test.invalid")
    commit(root, "test: planning model")
    return root


def delivery_fixture(root: Path) -> tuple[Path, dict[str, Any], str, str]:
    planning_fixture(root)
    git(root, "switch", "-c", "stage-a")
    gate = json.loads((root / REGISTRY).read_text())["gates"][0]
    outputs = []
    for item in gate["required_outputs"]:
        reference = write(root, item["path"], {"test_output": item["output_id"]})
        outputs.append({"output_id": item["output_id"], **reference})
    candidate = commit(root, "test: synthetic stage A outputs")
    evidence_root = f"evidence/delivery-gates/{GATE_ID}/{candidate}"
    checks = []
    for check in gate["acceptance_checks"]:
        evidence = write(
            root,
            f"{evidence_root}/{check['check_id']}.json",
            {"candidate_sha": candidate, "result": "PASS"},
        )
        checks.append({**check, **evidence, "result": "PASS"})
    task = json.loads((root / ".codex/tasks/TASK-0738.json").read_text(encoding="utf-8"))
    manifest = {
        "schema_version": "1.0.0",
        "gate_id": GATE_ID,
        "definition_sha256": digest(gate),
        "candidate_sha": candidate,
        "owner_task_envelope_sha256": digest(task),
        "outputs": outputs,
        "checks": checks,
    }
    manifest_ref = write(root, evidence_root + "/acceptance-manifest.json", manifest)
    snapshot = copy.deepcopy(task)
    snapshot["delivery_gate_scope"]["acceptance_manifest_sha256"] = manifest_ref["sha256"]
    snapshot_ref = write(root, evidence_root + "/task-envelope.acceptance.json", snapshot)
    from .signed_approval import create_approval

    bundle = create_approval(root, snapshot, candidate)
    daa_ref = write(root, evidence_root + "/daa.json", bundle)
    commit(root, "test: signed partial acceptance")
    git(root, "switch", "main")
    git(root, "merge", "--no-ff", "stage-a", "-m", "test: canonical human merge")
    integration = git(root, "rev-parse", "HEAD")
    human_ref = write(
        root,
        evidence_root + "/human.json",
        {
            "proof_type": "HUMAN_MERGE",
            "authority_role": "Autoridade Humana",
            "result": "PASS",
            "reviewed_candidate_commit": candidate,
            "merged_commit": integration,
        },
    )
    receipt = {
        "schema_version": "1.0.0",
        "gate_id": GATE_ID,
        "definition_sha256": digest(gate),
        "acceptance_manifest": manifest_ref,
        "task_envelope_snapshot": snapshot_ref,
        "daa_evidence": [daa_ref],
        "required_baseline_ref": "refs/heads/main",
        "integration_commit": integration,
        "human_integration_record": human_ref,
    }
    write(root, evidence_root + "/integration-receipt.json", receipt)
    commit(root, "test: integration receipt")
    return root, receipt, candidate, integration
