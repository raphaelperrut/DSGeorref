from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = (
    ROOT
    / "docs/03-engineering/contexts/engineering_governance"
    / "migrations-ci-secret-dependency-scan-e-telemetria-mini"
    / "consolidacao/CONSOLIDATION.json"
)
GRAPH_PATH = ROOT / "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
REVIEW_PATH = ROOT / "docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0022.json"
TASK_SCHEMA_PATH = ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json"

EXPECTED_PREDECESSORS = {
    "STORY-0708": ("ISSUE-0818", "TASK-0708"),
    "STORY-0709": ("ISSUE-0819", "TASK-0709"),
    "STORY-0710": ("ISSUE-0820", "TASK-0710"),
    "STORY-0711": ("ISSUE-0821", "TASK-0711"),
}


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _git_blob(revision: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{revision}:{path}"],
        check=True,
        capture_output=True,
    )
    return completed.stdout


def _is_ancestor(ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", ancestor, descendant],
        check=False,
    )
    return completed.returncode == 0


def _reviewed_requirements(issue_id: str) -> set[str]:
    with REVIEW_PATH.open(encoding="utf-8", newline="") as review_file:
        rows = [row for row in csv.DictReader(review_file) if row["issue_id"] == issue_id]
    assert len(rows) == 1
    row = rows[0]
    assert row["status"] == "PASS"
    assert row["conflicts"] == row["redundancies"] == "0"
    assert row["missing"] == row["impossible"] == row["cycles"] == "0"
    return set(row["requirements"].split("/"))


def test_story_0022_slice_consolidation() -> None:
    manifest = _load_json(MANIFEST_PATH)
    assert manifest["schema_version"] == "1.0.0"
    assert manifest["identity"] == {
        "epic_id": "EPIC-005",
        "story_id": "STORY-0022",
        "issue_id": "ISSUE-0132",
        "task_id": "TASK-0022",
        "owner_context": "BC-001",
    }

    graph = _load_json(GRAPH_PATH)
    incoming = {
        edge["from"]
        for edge in graph["edges"]
        if edge["relation"] == "blocks" and edge["to"] == "STORY-0022"
    }
    outgoing = {
        edge["to"]
        for edge in graph["edges"]
        if edge["relation"] == "blocks" and edge["from"] == "STORY-0022"
    }
    records = {record["story_id"]: record for record in manifest["predecessors"]}
    assert set(records) == incoming == set(EXPECTED_PREDECESSORS)

    baseline = manifest["integration_base_commit"]
    assert _is_ancestor(baseline, "HEAD")
    all_requirements: set[str] = set()
    all_artifacts: set[str] = set()
    all_tests: set[str] = set()

    for story_id, record in records.items():
        issue_id, task_id = EXPECTED_PREDECESSORS[story_id]
        assert (record["issue_id"], record["task_id"]) == (issue_id, task_id)
        assert _is_ancestor(record["evidence_commit"], record["merge_commit"])
        assert _is_ancestor(record["merge_commit"], baseline)

        evidence_blob = _git_blob(baseline, record["evidence_path"])
        assert hashlib.sha256(evidence_blob).hexdigest() == record["evidence_sha256"]
        assert _git_blob("HEAD", record["evidence_path"]) == evidence_blob
        evidence = yaml.safe_load(evidence_blob)
        assert evidence["identity"] == {
            "epic_id": "EPIC-005",
            "story_id": story_id,
            "issue_id": issue_id,
            "task_id": task_id,
        }
        assert evidence["candidate"]["state"] in {
            "READY_FOR_QA",
            "READY_FOR_SENTINEL_QA",
        }
        assert evidence["candidate"]["independent_review"] == "NOT_PERFORMED"
        assert evidence["candidate"]["approval_claimed"] is False
        assert evidence["contract_impact"]["existing_frozen_contract_changed"] is False
        assert evidence["contract_impact"]["new_public_contract"] is False
        assert evidence["contract_impact"]["http_changed"] is False
        assert evidence["contract_impact"]["persistence_changed"] is False

        requirements = {entry["requirement"] for entry in evidence["coverage"]}
        tests = {entry["test"] for entry in evidence["coverage"]}
        assert requirements == _reviewed_requirements(issue_id)
        assert all_requirements.isdisjoint(requirements)
        assert all_tests.isdisjoint(tests)
        all_requirements.update(requirements)
        all_tests.update(tests)

        artifacts = set(evidence["implementation_artifacts"])
        assert artifacts
        assert all_artifacts.isdisjoint(artifacts)
        for artifact in artifacts:
            baseline_artifact = _git_blob(baseline, artifact)
            assert _git_blob("HEAD", artifact) == baseline_artifact
        all_artifacts.update(artifacts)

    assert len(all_requirements) == len(all_tests) == 40
    assert len(all_artifacts) == 28
    assert manifest["coverage"]["requirement_count"] == 40
    assert manifest["coverage"]["duplicates"] == []
    assert manifest["coverage"]["unassigned"] == []
    assert manifest["integration"] == {
        "predecessor_outputs_reused_unchanged": True,
        "artifact_path_collisions": [],
        "normative_requirement_overlaps": [],
        "duplicate_test_proofs": [],
        "shared_contract_changes": [],
        "redundant_implementations": [],
        "runtime_materialization": "DOWNSTREAM_STORY_0024_ONLY",
        "migration_required_for_this_diff": False,
    }

    gate = manifest["review_gate"]
    assert set(gate["eligible_dependents"]) == outgoing == {"STORY-0024"}
    assert gate["candidate_state"] == "READY_FOR_SENTINEL_QA"
    assert gate["authority_role"] == "Reviewer"
    assert gate["residual_risks_required"] is True
    assert gate["self_approval"] == "PROHIBITED"
    assert gate["released_dependents"] == []

    task = _load_json(TASK_PATH)
    task_schema = _load_json(TASK_SCHEMA_PATH)
    Draft202012Validator.check_schema(task_schema)
    Draft202012Validator(task_schema).validate(task)
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in task["allow_paths"]
    assert "evidence/implementation/epic-005/story-0022/**" in task["allow_paths"]
    assert ".codex/tasks/TASK-0022.json" in task["allow_paths"]
    assert not any(path.startswith("src/") for path in task["allow_paths"])
