from __future__ import annotations

import copy
import csv
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw"
)
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
SCHEMA_PATH = CONTRACT_ROOT / "walking-skeleton.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/walking-skeleton.json"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0534.json"
DESIGN_REVIEW_PATH = (
    ROOT
    / "docs/02-architecture/design-reviews"
    / "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw"
    / "ISSUE-0644-DESIGN-REVIEW.md"
)

PUBLISHED_PATHS = {
    path.relative_to(ROOT).as_posix()
    for path in (MANIFEST_PATH, SCHEMA_PATH, EXAMPLE_PATH)
}
EXPECTED_OPERATIONS = {
    "post_projects_projectid_jobs",
    "get_jobs_jobid",
    "get_attempts_attemptid_diagnostics",
    "get_artifact_sets_artifactsetid_manifest",
}
EXPECTED_STAGES = [
    "FRONTEND",
    "API",
    "POSTGRESQL",
    "RABBITMQ_CELERY",
    "WORKER",
    "DIAGNOSTIC_ARTIFACT",
]
EXPECTED_TESTS = {
    "test_executable_foundation_gate_clean_room_end_to_end",
    "test_sprint_zero_baseline_decision_04",
    "test_epic_086_contrato",
    "test_walking_skeleton_fail_closed_paths",
}


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _validator() -> Draft202012Validator:
    schema = _load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _assert_rejected(profile: dict[str, Any]) -> None:
    assert list(_validator().iter_errors(profile)), "invalid profile was silently accepted"


def _openapi_operation_ids() -> set[str]:
    openapi = _load_yaml(ROOT / "contracts/http/openapi.yaml")
    operations: set[str] = set()
    for path_item in openapi["paths"].values():
        for method, operation in path_item.items():
            if method in {"get", "post", "put", "patch", "delete"}:
                operations.add(operation["operationId"])
    return operations


def _assert_contract_sources(profile: dict[str, Any]) -> None:
    sources = profile["contract_sources"]
    assert set(sources["operations"]) == EXPECTED_OPERATIONS
    assert _openapi_operation_ids() >= EXPECTED_OPERATIONS
    file_references = {
        value
        for key, value in sources.items()
        if key != "operations" and isinstance(value, str)
    }
    assert all((ROOT / reference).is_file() for reference in file_references)


def test_executable_foundation_gate_clean_room_end_to_end() -> None:
    schema = json.loads(SCHEMA_PATH.read_bytes())
    profile = json.loads(EXAMPLE_PATH.read_bytes())
    assert isinstance(schema, dict)
    assert isinstance(profile, dict)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(profile)

    assert [item["order"] for item in profile["flow"]] == list(range(1, 7))
    assert [item["stage"] for item in profile["flow"]] == EXPECTED_STAGES
    assert profile["data_authority"]["state"] == "POSTGRESQL_POSTGIS"
    assert profile["data_authority"]["broker"] == "TRANSPORT_ONLY"
    assert profile["data_authority"]["outbox"] == (
        "TRANSACTIONAL_WITH_AUTHORITATIVE_STATE"
    )
    assert profile["state_model"]["walking_skeleton_job_states"] == [
        "queued",
        "running",
        "succeeded",
        "failed",
    ]
    assert profile["state_model"]["transition_authority"] == "POSTGRESQL_POSTGIS"
    assert profile["state_model"]["other_states"] == (
        "NOT_EXERCISED_AND_NOT_IMPLICITLY_MAPPED"
    )
    assert profile["public_observation"]["telemetry_is_authority"] is False
    assert profile["delivery_gate"]["runtime_implementation"] == (
        "DOWNSTREAM_STORIES_ONLY"
    )
    _assert_contract_sources(profile)

    job_schema = _load_json(ROOT / profile["contract_sources"]["job"])
    assert job_schema["$id"].endswith("/1.0.0")
    job_states = set(job_schema["properties"]["state"]["enum"])
    assert {"queued", "running", "succeeded", "failed"} <= job_states

    openapi = _load_yaml(ROOT / profile["contract_sources"]["http"])
    assert openapi["info"]["version"] == profile["state_model"]["http_contract_version"]

    diagnostic_schema = _load_json(ROOT / profile["contract_sources"]["diagnostic"])
    assert {"code", "stage", "evidence", "remediations"} <= set(
        diagnostic_schema["required"]
    )


def test_walking_skeleton_fail_closed_paths() -> None:
    profile = _load_json(EXAMPLE_PATH)
    _validator().validate(profile)

    mutations = []

    missing_stage = copy.deepcopy(profile)
    missing_stage["flow"].pop(3)
    mutations.append(missing_stage)

    reordered = copy.deepcopy(profile)
    reordered["flow"][2], reordered["flow"][3] = reordered["flow"][3], reordered["flow"][2]
    mutations.append(reordered)

    broker_as_authority = copy.deepcopy(profile)
    broker_as_authority["data_authority"]["broker"] = "STATE_AUTHORITY"
    mutations.append(broker_as_authority)

    silent_fallback = copy.deepcopy(profile)
    silent_fallback["failure_policy"]["silent_fallback"] = True
    mutations.append(silent_fallback)

    publish_on_error = copy.deepcopy(profile)
    publish_on_error["failure_policy"]["publication_on_error"] = "ALLOW"
    mutations.append(publish_on_error)

    missing_failure = copy.deepcopy(profile)
    missing_failure["failure_policy"]["paths"].pop()
    mutations.append(missing_failure)

    unsupported_version = copy.deepcopy(profile)
    unsupported_version["contract_version"] = "2.0.0"
    mutations.append(unsupported_version)

    unmapped_state = copy.deepcopy(profile)
    unmapped_state["state_model"]["walking_skeleton_job_states"].append("partial")
    mutations.append(unmapped_state)

    unexpected = copy.deepcopy(profile)
    unexpected["fallback"] = "best-effort"
    mutations.append(unexpected)

    for mutation in mutations:
        _assert_rejected(mutation)


def test_epic_086_contrato() -> None:
    manifest = _load_yaml(MANIFEST_PATH)
    profile = _load_json(EXAMPLE_PATH)
    task = _load_json(TASK_PATH)

    assert manifest["schema_version"] == manifest["contract_version"] == "1.0.0"
    assert manifest["status"] == "FROZEN"
    assert manifest["owner"] == "BC-001"
    assert manifest["identity"] == {
        "epic_id": "EPIC-086",
        "story_id": "STORY-0534",
        "issue_id": "ISSUE-0644",
        "task_id": "TASK-0534",
    }
    assert manifest["contract"]["schema"] == SCHEMA_PATH.relative_to(ROOT).as_posix()
    assert manifest["contract"]["example"] == EXAMPLE_PATH.relative_to(ROOT).as_posix()
    assert {item["id"] for item in manifest["traceability"]["requirements"]} == {
        "REQ-EPIC-001",
        "REQ-SPRINT-001-004",
    }
    assert set(manifest["proof"]["required_tests"]) == EXPECTED_TESTS
    assert set(profile["delivery_gate"]["required_tests"]) == EXPECTED_TESTS
    assert manifest["review"]["self_approval"] == "PROHIBITED"
    assert DESIGN_REVIEW_PATH.is_file()

    with OWNERSHIP_PATH.open(encoding="utf-8", newline="") as ownership_file:
        registered = {
            row["contract"]
            for row in csv.DictReader(ownership_file)
            if row["owner_context"] == "BC-001" and row["status"] == "VERSIONED"
        }
    assert registered >= PUBLISHED_PATHS

    required_allow_paths = {
        "tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_contract.py",
        "evidence/implementation/epic-086/story-0534/**",
        "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv",
    }
    assert required_allow_paths <= set(task["allow_paths"])
    assert required_allow_paths <= set(task["phase_f_review"]["files"]["allow_paths"])
