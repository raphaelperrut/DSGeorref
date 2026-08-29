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
CAPABILITY_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "openapi-cliente-typescript-e-contratos-cli-jobs-evento"
)
CONTRACT_ROOT = CAPABILITY_ROOT / "consolidacao"
SCHEMA_PATH = CONTRACT_ROOT / "slice-consolidation.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/slice-consolidation.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
GRAPH_PATH = ROOT / "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
REVIEW_PATH = ROOT / "docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
CHECKPOINT_SUFFIX = "schema-compatibility-checkpoint.json"


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


def test_story_0016_slice_consolidation() -> None:
    schema = _load_json(SCHEMA_PATH)
    profile = _load_json(EXAMPLE_PATH)
    manifest = _load_yaml(MANIFEST_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(profile)

    assert manifest["identity"] == {
        "epic_id": "EPIC-004",
        "story_id": "STORY-0016",
        "issue_id": "ISSUE-0126",
        "task_id": "TASK-0016",
    }
    assert manifest["status"] == "FROZEN"
    assert manifest["contract_version"] == profile["contract_version"] == "1.0.0"
    assert manifest["proof"]["required_tests"] == [
        "test_story_0016_slice_consolidation"
    ]

    assert {item["story_id"] for item in profile["slices"]} == _graph_edges(
        target="STORY-0016"
    ) == {"STORY-0701", "STORY-0702"}
    assert {item["task_id"] for item in profile["slices"]} == {
        "TASK-0701",
        "TASK-0702",
    }
    _validate_artifact_lineage(profile)

    declared: set[str] = set()
    for slice_record in profile["slices"]:
        requirements = set(slice_record["requirements"])
        assert not declared.intersection(requirements)
        assert requirements == _reviewed_requirements(slice_record["issue_id"])
        declared.update(requirements)
    assert declared == set(profile["coverage"]["requirement_ids"])
    assert profile["coverage"]["duplicates"] == []
    assert profile["coverage"]["unassigned"] == []

    contracts = [_child_contract(item) for item in profile["slices"]]
    contract_ids = {item[0]["contract"]["id"] for item in contracts}
    profile_ids = [item[1]["profile_id"] for item in contracts]
    control_names = [set(item[1]["controls"]) for item in contracts]
    assert len(contract_ids) == len(set(profile_ids)) == 2
    assert control_names[0].isdisjoint(control_names[1])
    assert profile["integration"]["profile_namespaces"] == profile_ids
    assert contracts[1][0]["contract"]["extends"] == contracts[0][0]["contract"][
        "example"
    ]

    relationship = profile["integration"]["extension_relationship"]
    assert relationship["base_profile"] == profile_ids[0]
    assert relationship["extension_profile"] == profile_ids[1]
    assert _load_yaml(ROOT / relationship["declared_by"])["contract"]["extends"] == (
        contracts[0][0]["contract"]["example"]
    )
    assert profile["integration"]["contract_collisions"] == []
    assert profile["integration"]["redundant_implementations"] == []
    assert profile["integration"]["runtime_materialization"] == (
        "DOWNSTREAM_STORIES_ONLY"
    )

    checkpoint_paths = {
        artifact["path"]
        for slice_record in profile["slices"]
        for artifact in slice_record["artifacts"]
        if artifact["path"].endswith(CHECKPOINT_SUFFIX)
    }
    assert len(checkpoint_paths) == 1
    checkpoint = _load_json(ROOT / checkpoint_paths.pop())
    assert checkpoint["status"] == "FROZEN"
    assert {entry["category"] for entry in checkpoint["entries"]} == {
        "DATABASE",
        "API",
        "EVENT",
        "MANIFEST",
        "ARTIFACT",
    }

    gate = profile["review_gate"]
    assert set(gate["eligible_dependents"]) == _graph_edges(source="STORY-0016")
    assert gate["candidate_state"] == "READY_FOR_INDEPENDENT_REVIEW"
    assert gate["authority_role"] == "Reviewer"
    assert gate["same_candidate_commit"] is True
    assert gate["residual_risks_required"] is True
    assert gate["self_approval"] == "PROHIBITED"
    assert gate["released_dependents"] == []


def test_consolidation_rejects_implicit_or_self_release() -> None:
    schema = _load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    self_released = copy.deepcopy(_load_json(EXAMPLE_PATH))
    self_released["review_gate"]["candidate_state"] = "RELEASED"
    self_released["review_gate"]["released_dependents"] = ["STORY-0703"]

    errors = list(validator.iter_errors(self_released))
    assert {error.validator for error in errors} == {"const", "maxItems"}


def test_consolidation_rejects_untracked_extension() -> None:
    schema = _load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    untracked = copy.deepcopy(_load_json(EXAMPLE_PATH))
    untracked["integration"]["extension_relationship"]["declared_by"] = (
        "contracts/untracked.yaml"
    )

    errors = list(validator.iter_errors(untracked))
    assert {error.validator for error in errors} == {"const"}


def test_consolidation_contract_is_registered() -> None:
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
