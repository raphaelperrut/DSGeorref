from __future__ import annotations

import copy
import csv
import json
from functools import cache
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "openapi-cliente-typescript-e-contratos-cli-jobs-evento"
    / "crs-dbschema-epic-parte-1"
)
SCHEMA_PATH = CONTRACT_ROOT / "contract-foundation.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/contract-foundation.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0701.json"
OPENAPI_PATH = ROOT / "contracts/http/openapi.yaml"
PROCESSING_PLAN_PATH = ROOT / "contracts/domain/processing-plan.schema.json"
PROBLEM_DETAILS_PATH = ROOT / "contracts/errors/problem-details.schema.json"
FOUNDATION_PROFILE_PATH = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "repositorio-privado-project-central-views-campos-label"
    / "classicprofile-iss-native-parte-1/examples/foundation-conformance.json"
)

REQUIREMENT_TESTS = {
    "REQ-CRS-002": "test_explicit_axis_order_and_adapter_normalization",
    "REQ-DBSCHEMA-007": "test_req_dbschema_007",
    "REQ-DBSCHEMA-008": "test_req_dbschema_008",
    "REQ-EPIC-031": "generated_client_component_accessibility_e2e",
    "REQ-FS1-001": "test_first_functional_slice_decision_01",
    "REQ-FS1-004": "test_first_functional_slice_decision_04",
    "REQ-RUN-001": "test_req_run_001",
    "REQ-RUN-006": "test_req_run_006",
    "REQ-RUN-008": "test_req_run_008",
    "REQ-RUN-010": "test_req_run_0010",
}


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
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


def _assert_control_rejected(control: str, field: str, value: object) -> None:
    invalid = copy.deepcopy(_profile())
    invalid["controls"][control][field] = value
    _assert_rejected(invalid)


def _manifest_entry(requirement: str) -> dict[str, Any]:
    manifest = _load_yaml(MANIFEST_PATH)
    entries = [item for item in manifest["requirements"] if item["id"] == requirement]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["test"] == REQUIREMENT_TESTS[requirement]
    assert entry["failure_modes"]
    return entry


def test_explicit_axis_order_and_adapter_normalization() -> None:
    control = _profile()["controls"]["coordinate_boundary"]
    assert control == {
        "scope": "COORDINATES_OUTSIDE_CLOSED_SPACE",
        "crs": "EXPLICIT",
        "axis_convention": "EXPLICIT",
        "unit": "EXPLICIT",
        "precision": "FLOAT64",
        "adapter_normalization": "ALWAYS_XY",
        "invalid_crs": "REJECT",
    }
    assert "CRS_OR_AXIS_CONVENTION_MISSING" in _manifest_entry("REQ-CRS-002")[
        "failure_modes"
    ]
    _assert_control_rejected("coordinate_boundary", "adapter_normalization", "NATIVE")
    _assert_control_rejected("coordinate_boundary", "invalid_crs", "BEST_EFFORT")


def test_req_dbschema_007() -> None:
    control = _profile()["controls"]["versioned_extensions"]
    assert control["jsonb_usage"] == "VERSIONED_EXTENSIBILITY_ONLY"
    assert control["relational_invariants"] == "REQUIRED"
    assert control["unknown_extension"] == "REJECT"
    _assert_control_rejected("versioned_extensions", "relational_invariants", "OPTIONAL")


def test_req_dbschema_008() -> None:
    control = _profile()["controls"]["state_transitions"]
    assert control == {
        "state_catalog": "VERSIONED_TYPED",
        "transition_policy": "REGISTERED_ONLY",
        "unknown_state": "REJECT",
        "invalid_transition": "REJECT",
    }
    _assert_control_rejected("state_transitions", "invalid_transition", "ACCEPT")


def generated_client_component_accessibility_e2e() -> None:
    control = _profile()["controls"]["generated_client_quality"]
    assert control["source"] == "contracts/http/openapi.yaml"
    assert control["generation"] == "EXCLUSIVE"
    assert control["critical_flow_gates"] == ["COMPONENT", "ACCESSIBILITY", "E2E"]
    assert control["missing_gate"] == "REJECT"

    openapi = _load_yaml(OPENAPI_PATH)
    assert openapi["openapi"] == "3.1.0"
    assert openapi["info"]["version"] == "2.6.0"
    _assert_control_rejected("generated_client_quality", "missing_gate", "WARN")


def test_generated_client_component_accessibility_e2e() -> None:
    generated_client_component_accessibility_e2e()
    _manifest_entry("REQ-EPIC-031")


def test_first_functional_slice_decision_01() -> None:
    control = _profile()["controls"]["first_functional_slice"]
    assert control == {
        "input_scope": "EXACTLY_ONE_IMAGE",
        "execution": "END_TO_END",
        "contract_shape": "BATCH_COMPATIBLE",
        "scope_expansion": "REJECT",
    }
    _assert_control_rejected("first_functional_slice", "input_scope", "UNBOUNDED_BATCH")


def test_first_functional_slice_decision_04() -> None:
    control = _profile()["controls"]["processing_plan"]
    assert control["contract"] == PROCESSING_PLAN_PATH.relative_to(ROOT).as_posix()
    assert control["persistence"] == "REQUIRED"
    assert control["authority"] == "POSTGRESQL"
    assert control["immutability"] == "REQUIRED"
    assert control["versioning"] == "SCHEMA_AND_DIGEST"

    processing_plan = _load_json(PROCESSING_PLAN_PATH)
    Draft202012Validator.check_schema(processing_plan)
    required = set(processing_plan["required"])
    assert {"schema_version", "strategy", "quality_profile_id", "output_profile_id"} <= required
    assert {"capabilities", "budgets", "digest"} <= required
    _assert_control_rejected("processing_plan", "invalid_plan", "PERSIST_WITH_WARNING")


def test_req_run_001() -> None:
    control = _profile()["controls"]["application_boundaries"]
    foundation = _load_json(FOUNDATION_PROFILE_PATH)["controls"]["application_boundaries"]
    assert control == foundation
    _assert_control_rejected("application_boundaries", "namespace", "dsgeorref_worker")


def test_req_run_006() -> None:
    control = _profile()["controls"]["domain_errors"]
    foundation = _load_json(FOUNDATION_PROFILE_PATH)["controls"]["domain_errors"]
    assert control == foundation
    assert control["schema"] == PROBLEM_DETAILS_PATH.relative_to(ROOT).as_posix()
    problem_details = _load_json(PROBLEM_DETAILS_PATH)
    Draft202012Validator.check_schema(problem_details)
    assert {"type", "title", "status"} <= set(problem_details["required"])
    _assert_control_rejected("domain_errors", "unmapped_error", "GENERIC_FALLBACK")


def test_req_run_008() -> None:
    control = _profile()["controls"]["typescript_client"]
    foundation = _load_json(FOUNDATION_PROFILE_PATH)["controls"]["typescript_client"]
    assert control == foundation
    _assert_control_rejected("typescript_client", "generation", "MANUAL_ALLOWED")


def test_req_run_0010() -> None:
    control = _profile()["controls"]["capability_registry"]
    foundation = _load_json(FOUNDATION_PROFILE_PATH)["controls"]["capability_registry"]
    assert control == foundation
    assert all(value is False for value in control["bypass"].values())
    _assert_control_rejected("capability_registry", "fail_closed", False)


def test_contract_package_is_registered_and_envelope_is_contained() -> None:
    manifest = _load_yaml(MANIFEST_PATH)
    assert manifest["status"] == "FROZEN"
    assert manifest["contract_version"] == _profile()["profile_version"] == "1.0.0"
    assert {item["id"] for item in manifest["requirements"]} == set(REQUIREMENT_TESTS)
    assert manifest["proof"]["required_tests"] == list(REQUIREMENT_TESTS.values())

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

    task = _load_json(TASK_PATH)
    allow_paths = set(task["allow_paths"])
    assert ".codex/tasks/TASK-0701.json" in allow_paths
    assert "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv" in allow_paths
    assert any(path.startswith("tests/fnd/openapi-") for path in allow_paths)
    assert any(path.startswith("evidence/implementation/openapi-") for path in allow_paths)


def test_profile_rejects_missing_or_unknown_control() -> None:
    missing = copy.deepcopy(_profile())
    del missing["controls"]["state_transitions"]
    _assert_rejected(missing)

    unknown = copy.deepcopy(_profile())
    unknown["controls"]["silent_fallback"] = {"enabled": True}
    _assert_rejected(unknown)
