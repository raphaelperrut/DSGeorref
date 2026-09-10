from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "consolidacao/CONSOLIDATION.json"
)
GRAPH_PATH = ROOT / "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
REVIEW_PATH = ROOT / "docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0535.json"
TASK_SCHEMA_PATH = ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json"
EVIDENCE_PATH = ROOT / "evidence/implementation/epic-086/story-0535/IMPLEMENTATION_EVIDENCE.json"

EXPECTED_PREDECESSORS = {
    "STORY-0752": ("ISSUE-0862", "TASK-0752", 1),
    "STORY-0753": ("ISSUE-0863", "TASK-0753", 2),
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
        capture_output=True,
    )
    return completed.returncode == 0


def _is_unchanged_from(revision: str, path: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "--quiet", revision, "--", path],
        check=False,
        capture_output=True,
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


def _test_functions(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}


def _contract_binding(policy: dict[str, Any]) -> dict[str, str]:
    contract = policy["contract"]
    return {
        "path": contract["path"],
        "version": contract["version"],
        "sha256": contract["sha256"],
    }


def test_story_0535_slice_consolidation() -> None:
    manifest = _load_json(MANIFEST_PATH)
    assert manifest["schema_version"] == "1.0.0"
    assert manifest["identity"] == {
        "epic_id": "EPIC-086",
        "story_id": "STORY-0535",
        "issue_id": "ISSUE-0645",
        "task_id": "TASK-0535",
        "owner_context": "BC-001",
    }

    graph = _load_json(GRAPH_PATH)
    incoming = {
        edge["from"]
        for edge in graph["edges"]
        if edge["relation"] == "blocks" and edge["to"] == "STORY-0535"
    }
    outgoing = {
        edge["to"]
        for edge in graph["edges"]
        if edge["relation"] == "blocks" and edge["from"] == "STORY-0535"
    }
    records = {record["story_id"]: record for record in manifest["predecessors"]}
    assert set(records) == incoming == set(EXPECTED_PREDECESSORS)

    baseline = manifest["integration_base_commit"]
    assert _is_ancestor(baseline, "HEAD")
    all_requirements: set[str] = set()
    all_checkpoints: set[str] = set()
    all_outputs: set[str] = set()
    contract_bindings: list[dict[str, str]] = []

    for story_id, record in records.items():
        issue_id, task_id, slice_number = EXPECTED_PREDECESSORS[story_id]
        assert (record["issue_id"], record["task_id"]) == (issue_id, task_id)

        blobs = {}
        for output in ("policy", "evidence", "validator", "test"):
            path = record[f"{output}_path"]
            blobs[output] = _git_blob(baseline, path)
            assert hashlib.sha256(blobs[output]).hexdigest() == record[
                f"{output}_sha256"
            ]
            assert _is_unchanged_from(baseline, path)

        policy = json.loads(blobs["policy"])
        evidence = json.loads(blobs["evidence"])["payload"]
        task = _load_json(ROOT / f".codex/tasks/{task_id}.json")
        assert policy["foundation_id"] == "EXECUTABLE-FOUNDATION-WALKING-SKELETON"
        assert policy["owner"] == evidence["owner"] == "BC-001"
        assert policy["status"] == evidence["status"] == "CANDIDATE"
        assert policy["slice"]["number"] == slice_number
        assert policy["slice"]["total"] == 2
        assert evidence["acceptance_criteria"] == task["acceptance_criterion_ids"]
        assert policy["failure_policy"] == {
            "mode": "FAIL_CLOSED",
            "silent_fallback": False,
            "publication_on_error": "PROHIBITED",
        }

        requirements = set(policy["requirement_evidence"])
        assert requirements == set(evidence["requirements"])
        assert requirements == _reviewed_requirements(issue_id)
        assert all_requirements.isdisjoint(requirements)
        all_requirements.update(requirements)

        checkpoints = {
            item["checkpoint"] for item in policy["requirement_evidence"].values()
        }
        assert len(checkpoints) == len(requirements)
        assert all_checkpoints.isdisjoint(checkpoints)
        for item in policy["requirement_evidence"].values():
            assert item["checkpoint"] == f'{item["test_path"]}::{item["test_id"]}'
            assert item["test_id"] in _test_functions(ROOT / item["test_path"])
        all_checkpoints.update(checkpoints)

        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / record["validator_path"]),
                "--policy",
                str(ROOT / record["policy_path"]),
                "--repository-root",
                str(ROOT),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr
        assert json.loads(completed.stdout)["status"] == "PASS"

        outputs = {
            record[f"{output}_path"]
            for output in ("policy", "evidence", "validator", "test")
        }
        assert all_outputs.isdisjoint(outputs)
        all_outputs.update(outputs)
        contract_bindings.append(_contract_binding(policy))

    assert len(all_requirements) == len(all_checkpoints) == 12
    assert len(all_outputs) == 8
    assert contract_bindings == [manifest["integration"]["shared_contract"]] * 2
    assert manifest["coverage"] == {
        "requirement_count": 12,
        "duplicates": [],
        "unassigned": [],
    }
    assert manifest["integration"] == {
        "predecessor_outputs_reused_unchanged": True,
        "artifact_path_collisions": [],
        "normative_requirement_overlaps": [],
        "duplicate_test_proofs": [],
        "shared_contract": contract_bindings[0],
        "shared_contract_changes": [],
        "redundant_implementations": [],
        "validation_composition": "ISOLATED_PROCESS_PER_SLICE",
        "runtime_materialization": "DOWNSTREAM_STORIES_ONLY",
        "migration_required_for_this_diff": False,
    }

    gate = manifest["review_gate"]
    assert set(gate["eligible_dependents"]) == outgoing == {"STORY-0537"}
    assert gate == {
        "candidate_state": "READY_FOR_REVIEW",
        "authority_role": "Reviewer",
        "residual_risks_required": True,
        "self_approval": "PROHIBITED",
        "eligible_dependents": ["STORY-0537"],
        "released_dependents": [],
    }

    task = _load_json(TASK_PATH)
    task_schema = _load_json(TASK_SCHEMA_PATH)
    Draft202012Validator.check_schema(task_schema)
    Draft202012Validator(task_schema).validate(task)
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in task["allow_paths"]
    assert "evidence/implementation/epic-086/story-0535/**" in task["allow_paths"]
    assert ".codex/tasks/TASK-0535.json" in task["allow_paths"]
    assert not any(path.startswith("src/") for path in task["allow_paths"])

    implementation_evidence = _load_json(EVIDENCE_PATH)
    assert implementation_evidence["identity"] == {
        "epic_id": "EPIC-086",
        "story_id": "STORY-0535",
        "issue_id": "ISSUE-0645",
        "task_id": "TASK-0535",
    }
    assert implementation_evidence["candidate"] == {
        "integration_base_commit": baseline,
        "state": "READY_FOR_REVIEW",
        "independent_review": "NOT_PERFORMED",
        "approval_claimed": False,
    }
    assert implementation_evidence["coverage"] == {
        "predecessors": ["STORY-0752", "STORY-0753"],
        "requirement_count": 12,
        "duplicates": [],
        "unassigned": [],
        "test": (
            "tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
            "test_slice_consolidation.py::test_story_0535_slice_consolidation"
        ),
    }
    assert implementation_evidence["contract_impact"] == {
        "existing_frozen_contract_changed": False,
        "new_public_contract": False,
        "http_changed": False,
        "persistence_changed": False,
        "migration_required": False,
    }
    assert implementation_evidence["integration"] == {
        "validation_composition": "ISOLATED_PROCESS_PER_SLICE",
        "residual_risks": [
            "TOP_LEVEL_VALIDATOR_MODULE_NAMES_REQUIRE_PROCESS_ISOLATION"
        ],
    }
    assert implementation_evidence["validation"] == {
        "result": "PASS",
        "pytest_cases_passed": 15,
        "commands": [
            "pytest -q -p no:cacheprovider tests/fnd/"
            "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
            "test_slice_consolidation.py",
            "pytest -q -p no:cacheprovider tests/fnd/"
            "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
            "test_implementation.py",
            "pytest -q -p no:cacheprovider tests/fnd/"
            "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
            "test_completion.py",
        ],
    }
    assert implementation_evidence["review_gate"] == {
        "authority_role": "Reviewer",
        "residual_risks_required": True,
        "eligible_dependents": ["STORY-0537"],
        "released_dependents": [],
    }
    assert implementation_evidence["rollback"] == (
        "REVERT_CANDIDATE_COMMIT_NO_DATA_ACTION"
    )
    for artifact in implementation_evidence["implementation_artifacts"]:
        assert (ROOT / artifact).is_file()
