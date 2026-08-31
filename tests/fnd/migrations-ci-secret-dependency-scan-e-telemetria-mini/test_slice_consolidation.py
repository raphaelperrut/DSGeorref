from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "migrations-ci-secret-dependency-scan-e-telemetria-mini"
    / "consolidacao"
)
SCHEMA_PATH = CONTRACT_ROOT / "slice-consolidation.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/slice-consolidation.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
GRAPH_PATH = ROOT / "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
REVIEW_PATH = ROOT / "docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0021.json"
TASK_SCHEMA_PATH = ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json"


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _git_blob(revision: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{revision}:{path}"],
        check=True,
        capture_output=True,
    )
    return completed.stdout


def _graph_edges(*, source: str | None = None, target: str | None = None) -> set[str]:
    graph = _load_json(GRAPH_PATH)
    values: set[str] = set()
    for edge in graph["edges"]:
        if edge["relation"] != "blocks":
            continue
        if source is not None and edge["from"] == source:
            values.add(edge["to"])
        if target is not None and edge["to"] == target:
            values.add(edge["from"])
    return values


def _reviewed_requirements(issue_id: str) -> set[str]:
    with REVIEW_PATH.open(encoding="utf-8", newline="") as review_file:
        rows = [row for row in csv.DictReader(review_file) if row["issue_id"] == issue_id]
    assert len(rows) == 1
    assert rows[0]["status"] == "PASS"
    assert rows[0]["conflicts"] == rows[0]["redundancies"] == "0"
    assert rows[0]["missing"] == rows[0]["impossible"] == "0"
    requirements = rows[0]["requirements"]
    return set(requirements.split("/")) if requirements else set()


def _child_contract(slice_record: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_path = next(
        artifact["path"]
        for artifact in slice_record["artifacts"]
        if artifact["path"].endswith("contract-manifest.yaml")
    )
    manifest = _load_yaml(ROOT / manifest_path)
    example = _load_json(ROOT / manifest["contract"]["example"])
    return manifest, example


def _validate_artifact_lineage(profile: dict[str, Any]) -> None:
    baseline = profile["baseline"]["candidate_commit"]
    seen_paths: set[str] = set()
    seen_digests: set[str] = set()
    for slice_record in profile["slices"]:
        ancestry = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "merge-base",
                "--is-ancestor",
                slice_record["merge_commit"],
                baseline,
            ],
            check=False,
        )
        assert ancestry.returncode == 0
        for artifact in slice_record["artifacts"]:
            path = artifact["path"]
            digest = hashlib.sha256(_git_blob(baseline, path)).hexdigest()
            assert digest == artifact["sha256"]
            assert path not in seen_paths
            assert digest not in seen_digests
            seen_paths.add(path)
            seen_digests.add(digest)


def test_story_0021_slice_consolidation() -> None:
    schema = _load_json(SCHEMA_PATH)
    profile = _load_json(EXAMPLE_PATH)
    manifest = _load_yaml(MANIFEST_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(profile)

    assert manifest["identity"] == {
        "epic_id": "EPIC-005",
        "story_id": "STORY-0021",
        "issue_id": "ISSUE-0131",
        "task_id": "TASK-0021",
    }
    assert manifest["status"] == "FROZEN"
    assert manifest["contract_version"] == profile["contract_version"] == "1.0.0"
    assert manifest["proof"]["required_tests"] == [
        "test_story_0021_slice_consolidation"
    ]

    slice_story_ids = {item["story_id"] for item in profile["slices"]}
    assert slice_story_ids == _graph_edges(target="STORY-0021") == {
        "STORY-0706",
        "STORY-0707",
    }
    assert {item["task_id"] for item in profile["slices"]} == {
        "TASK-0706",
        "TASK-0707",
    }
    _validate_artifact_lineage(profile)

    declared: set[str] = set()
    for slice_record in profile["slices"]:
        requirements = set(slice_record["requirements"])
        assert not declared.intersection(requirements)
        assert requirements == _reviewed_requirements(slice_record["issue_id"])
        child_manifest, _child_example = _child_contract(slice_record)
        assert requirements <= {
            entry["id"] for entry in child_manifest["requirements"]
        }
        declared.update(requirements)
    assert declared == set(profile["coverage"]["requirement_ids"])
    assert profile["coverage"]["duplicates"] == []
    assert profile["coverage"]["unassigned"] == []

    contracts = [_child_contract(item) for item in profile["slices"]]
    contract_ids = {child_manifest["contract"]["id"] for child_manifest, _ in contracts}
    profile_ids = {example["profile_id"] for _, example in contracts}
    control_names = [set(example["controls"]) for _, example in contracts]
    assert len(contract_ids) == len(profile_ids) == 2
    assert control_names[0].isdisjoint(control_names[1])
    assert set(profile["integration"]["control_namespaces"]) == profile_ids
    assert profile["integration"]["contract_collisions"] == []
    assert profile["integration"]["redundant_implementations"] == []
    assert profile["integration"]["runtime_materialization"] == (
        "DOWNSTREAM_STORIES_ONLY"
    )

    gate = profile["review_gate"]
    assert set(gate["eligible_dependents"]) == _graph_edges(source="STORY-0021")
    assert gate["candidate_state"] == "READY_FOR_INDEPENDENT_REVIEW"
    assert gate["authority_role"] == "Reviewer"
    assert gate["residual_risks_required"] is True
    assert gate["self_approval"] == "PROHIBITED"
    assert gate["released_dependents"] == []


def test_consolidation_rejects_implicit_or_self_release() -> None:
    validator = Draft202012Validator(_load_json(SCHEMA_PATH))
    self_released = copy.deepcopy(_load_json(EXAMPLE_PATH))
    self_released["review_gate"]["candidate_state"] = "RELEASED"
    self_released["review_gate"]["released_dependents"] = ["STORY-0023"]

    errors = list(validator.iter_errors(self_released))
    assert {error.validator for error in errors} == {"const", "maxItems"}


def test_consolidation_contract_is_registered_and_envelope_is_contained() -> None:
    expected = {
        MANIFEST_PATH.relative_to(ROOT).as_posix(),
        SCHEMA_PATH.relative_to(ROOT).as_posix(),
        EXAMPLE_PATH.relative_to(ROOT).as_posix(),
    }
    with OWNERSHIP_PATH.open(encoding="utf-8", newline="") as ownership_file:
        registered = {
            row["contract"]
            for row in csv.DictReader(ownership_file)
            if row["owner_context"] == "BC-001" and row["status"] == "VERSIONED"
        }
    assert expected <= registered

    task = _load_json(TASK_PATH)
    task_schema = _load_json(TASK_SCHEMA_PATH)
    Draft202012Validator.check_schema(task_schema)
    Draft202012Validator(task_schema).validate(task)
    allow_paths = set(task["allow_paths"])
    assert ".codex/tasks/TASK-0021.json" in allow_paths
    assert "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv" in allow_paths
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in allow_paths
    assert "evidence/implementation/epic-005/story-0021/**" in allow_paths
    assert not any(path.startswith("src/") for path in allow_paths)
