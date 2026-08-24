from __future__ import annotations

import copy
import csv
import json
from functools import cache
from pathlib import Path
from typing import Any

import yaml
import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "repositorio-privado-project-central-views-campos-label"
    / "worker-parte-2"
)
SCHEMA_PATH = CONTRACT_ROOT / "worker-governance-conformance.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/worker-governance-conformance.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


@cache
def _manifest() -> dict[str, Any]:
    loaded = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


@cache
def _validator() -> Draft202012Validator:
    schema = _load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


@cache
def _profile() -> dict[str, Any]:
    profile = _load_json(EXAMPLE_PATH)
    _validator().validate(profile)
    return profile


def _assert_rejected(profile: dict[str, Any]) -> None:
    assert list(_validator().iter_errors(profile)), "invalid profile was silently accepted"


def _validate_task_envelope_schema(envelope_schema: dict[str, Any] | None) -> None:
    assert envelope_schema is not None, "TASK_ENVELOPE_CONTRACT_MISSING"
    assert envelope_schema.get("$id", "").endswith(
        "/task-envelope/1.6.0"
    ), "UNVERSIONED_TASK_ENVELOPE"
    Draft202012Validator.check_schema(envelope_schema)


def _validate_task_envelope_reference(profile: dict[str, Any], root: Path) -> None:
    contract = profile["controls"]["task_envelope"]["contract"]
    contract_path = root / contract
    envelope_schema = _load_json(contract_path) if contract_path.is_file() else None
    _validate_task_envelope_schema(envelope_schema)


def _manifest_entry(requirement: str, test: str) -> dict[str, Any]:
    entries = [item for item in _manifest()["requirements"] if item["id"] == requirement]
    assert len(entries) == 1
    assert entries[0]["test"] == test
    assert entries[0]["failure_modes"]
    return entries[0]


def test_req_worker_001() -> None:
    profile = _profile()
    control = profile["controls"]["task_envelope"]
    assert profile["profile_version"] == _manifest()["contract_version"] == "1.0.0"
    assert control == {
        "contract": ".codex/tasks/TASK_ENVELOPE.schema.json",
        "versioning": "EXPLICIT",
        "content_policy": "IDS_VERSION_AND_INDISPENSABLE_TECHNICAL_CONTEXT_ONLY",
        "unknown_content": "REJECT",
        "contradiction": "STOP",
    }

    _validate_task_envelope_reference(profile, ROOT)
    assert _manifest()["status"] == "FROZEN"
    assert {item["id"] for item in _manifest()["requirements"]} == {
        "REQ-WORKER-001",
        "REQ-WORKER-010",
    }
    entry = _manifest_entry("REQ-WORKER-001", "test_req_worker_001")
    assert "ENVELOPE_CONTAINS_NONESSENTIAL_CONTENT" in entry["failure_modes"]

    permissive = copy.deepcopy(profile)
    permissive["controls"]["task_envelope"]["unknown_content"] = "IGNORE"
    _assert_rejected(permissive)
    unknown = copy.deepcopy(profile)
    unknown["controls"]["task_envelope"]["payload"] = "INLINE"
    _assert_rejected(unknown)

    published = {
        MANIFEST_PATH.relative_to(ROOT).as_posix(),
        SCHEMA_PATH.relative_to(ROOT).as_posix(),
        EXAMPLE_PATH.relative_to(ROOT).as_posix(),
    }
    with OWNERSHIP_PATH.open(encoding="utf-8", newline="") as registry_file:
        registered = {
            row["contract"]
            for row in csv.DictReader(registry_file)
            if row["owner_context"] == "BC-001" and row["status"] == "VERSIONED"
        }
    assert published <= registered


def test_task_envelope_contract_missing_is_fail_closed() -> None:
    entry = _manifest_entry("REQ-WORKER-001", "test_req_worker_001")
    assert "TASK_ENVELOPE_CONTRACT_MISSING" in entry["failure_modes"]
    with pytest.raises(AssertionError) as error:
        _validate_task_envelope_schema(None)
    assert str(error.value).splitlines()[0] == "TASK_ENVELOPE_CONTRACT_MISSING"


@pytest.mark.parametrize("schema_id", [None, "https://dsgeorref.local/task-envelope/1.5.0"])
def test_unversioned_task_envelope_is_fail_closed(
    schema_id: str | None,
) -> None:
    entry = _manifest_entry("REQ-WORKER-001", "test_req_worker_001")
    assert "UNVERSIONED_TASK_ENVELOPE" in entry["failure_modes"]
    envelope_schema = _load_json(ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json")
    if schema_id is None:
        envelope_schema.pop("$id")
    else:
        envelope_schema["$id"] = schema_id

    with pytest.raises(AssertionError) as error:
        _validate_task_envelope_schema(envelope_schema)
    assert str(error.value).splitlines()[0] == "UNVERSIONED_TASK_ENVELOPE"


def test_req_worker_0010() -> None:
    lifecycle = _profile()["controls"]["worker_lifecycle"]
    assert lifecycle["readiness"]["unverified_dependency"] == "NOT_READY"
    assert lifecycle["drain"] == {
        "new_work": "REJECT",
        "in_flight_work_units": "RECONCILE",
    }
    assert lifecycle["shutdown"] == {
        "mode": "COOPERATIVE",
        "in_flight_work_units": "CHECKPOINT_AND_RECONCILE",
    }
    assert lifecycle["resume"]["checkpoint"] == "COMPATIBLE_ONLY"
    assert lifecycle["resume"]["compatibility"] == [
        "HASHES",
        "SCHEMAS",
        "INPUTS",
        "VERSIONS",
    ]
    assert lifecycle["fault_injection"]["silent_fallback"] == "PROHIBITED"
    assert len(lifecycle["fault_injection"]["required_scenarios"]) == 4
    entry = _manifest_entry("REQ-WORKER-010", "test_req_worker_0010")
    assert "SILENT_LIFECYCLE_FALLBACK" in entry["failure_modes"]

    mutations = [
        ("readiness", "unverified_dependency", "READY"),
        ("drain", "new_work", "ACCEPT"),
        ("shutdown", "mode", "IMMEDIATE"),
        ("resume", "checkpoint", "LATEST"),
        ("fault_injection", "silent_fallback", "ALLOWED"),
    ]
    for section, field, value in mutations:
        invalid = copy.deepcopy(_profile())
        invalid["controls"]["worker_lifecycle"][section][field] = value
        _assert_rejected(invalid)

    missing_scenario = copy.deepcopy(_profile())
    missing_scenario["controls"]["worker_lifecycle"]["fault_injection"][
        "required_scenarios"
    ].pop()
    _assert_rejected(missing_scenario)


def test_shutdown_abandoning_in_flight_work_is_fail_closed() -> None:
    entry = _manifest_entry("REQ-WORKER-010", "test_req_worker_0010")
    assert "SHUTDOWN_ABANDONS_IN_FLIGHT_WORK" in entry["failure_modes"]
    abandoning = copy.deepcopy(_profile())
    abandoning["controls"]["worker_lifecycle"]["shutdown"][
        "in_flight_work_units"
    ] = "ABANDON"

    errors = list(_validator().iter_errors(abandoning))
    assert len(errors) == 1
    assert list(errors[0].absolute_path) == [
        "controls",
        "worker_lifecycle",
        "shutdown",
        "in_flight_work_units",
    ]
    assert errors[0].validator == "const"
    assert errors[0].validator_value == "CHECKPOINT_AND_RECONCILE"
