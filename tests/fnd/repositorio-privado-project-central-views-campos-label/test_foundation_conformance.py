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
    / "repositorio-privado-project-central-views-campos-label"
    / "classicprofile-iss-native-parte-1"
)
SCHEMA_PATH = CONTRACT_ROOT / "foundation-conformance.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/foundation-conformance.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"

REQUIREMENT_TESTS = {
    "REQ-CLASSICPROFILE-004": "test_req_classicprofile_004",
    "REQ-ISS-007": "test_acceptance_evidence_derivation_and_contract_change_review",
    "REQ-NATIVE-002": "test_req_native_002",
    "REQ-PLN-009": "test_cross_domain_contract_checkpoint_and_walking_skeleton_integration",
    "REQ-PRJ-004": "test_canonical_workflow_transitions",
    "REQ-RUN-001": "test_req_run_001",
    "REQ-RUN-006": "test_req_run_006",
    "REQ-RUN-008": "test_req_run_008",
    "REQ-RUN-010": "test_req_run_0010",
    "REQ-SPRINT-001-004": "test_sprint_zero_baseline_decision_04",
}


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


@cache
def _load_manifest() -> dict[str, Any]:
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


def _assert_control_rejected(control: str, field: str, value: object) -> None:
    invalid = copy.deepcopy(_profile())
    invalid["controls"][control][field] = value
    _assert_rejected(invalid)


def _manifest_entry(requirement: str) -> dict[str, Any]:
    manifest = _load_manifest()
    entries = [item for item in manifest["requirements"] if item["id"] == requirement]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["test"] == REQUIREMENT_TESTS[requirement]
    assert entry["failure_modes"]
    return entry


def test_req_classicprofile_004() -> None:
    control = _profile()["controls"]["classic_profile"]
    assert control == {
        "descriptor": "ROOTSIFT",
        "numeric_representation": "FLOAT32",
        "versioning": "PROFILE_PINNED",
        "ann": "FLANN_KD_TREE",
        "calibration_oracle": "BF",
        "execution_order": "CLASSIC_BEFORE_ELIGIBLE_AI",
    }
    assert "NON_FLOAT32_DESCRIPTOR" in _manifest_entry("REQ-CLASSICPROFILE-004")[
        "failure_modes"
    ]
    _assert_control_rejected("classic_profile", "numeric_representation", "FLOAT64")


def test_acceptance_evidence_derivation_and_contract_change_review() -> None:
    control = _profile()["controls"]["acceptance_evidence"]
    assert control["derivation_source"] == "PUBLISHED_CONTRACT"
    assert control["contract_change_review"] == "EXPLICIT_REQUIRED"
    entry = _manifest_entry("REQ-ISS-007")
    assert "UNREVIEWED_CONTRACT_CHANGE" in entry["failure_modes"]
    _assert_control_rejected("acceptance_evidence", "contract_change_review", "OPTIONAL")

    manifest = _load_manifest()
    assert manifest["status"] == "FROZEN"
    assert manifest["compatibility"]["breaking_change"] == "NEW_MAJOR_AND_ARCHITECT_REVIEW"
    assert {item["id"] for item in manifest["requirements"]} == set(REQUIREMENT_TESTS)
    assert len(manifest["requirements"]) == len(REQUIREMENT_TESTS)

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


def test_req_native_002() -> None:
    control = _profile()["controls"]["crs_operations"]
    assert control["library"] == "PYPROJ"
    assert control["typed_crs"] == "REQUIRED"
    assert control["always_xy"] is True
    assert control["precision"] == "FLOAT64"
    _assert_control_rejected("crs_operations", "always_xy", False)


def test_cross_domain_contract_checkpoint_and_walking_skeleton_integration() -> None:
    control = _profile()["controls"]["integration_checkpoints"]
    assert control["producer_contract"] == "REQUIRED"
    assert control["consumer_contract"] == "REQUIRED"
    assert control["compatibility"] == {
        "schema": "EXACT_OR_COMPATIBLE",
        "inputs": "EXACT",
        "versions": "EXACT_OR_COMPATIBLE",
        "hashes": "EXACT",
    }
    _assert_control_rejected("integration_checkpoints", "producer_contract", "OPTIONAL")


def test_canonical_workflow_transitions() -> None:
    control = _profile()["controls"]["workflow"]
    assert control["state_catalog"] == "VERSIONED_CANONICAL"
    assert control["transition_policy"] == "REGISTERED_ONLY"
    assert control["unknown_state"] == "REJECT"
    assert control["invalid_transition"] == "REJECT"
    _assert_control_rejected("workflow", "invalid_transition", "ACCEPT")


def test_req_run_001() -> None:
    control = _profile()["controls"]["application_boundaries"]
    assert control["namespace"] == "dsgeorref"
    assert control["application_services"] == "SHARED"
    assert control["surfaces"] == {
        "cli": "THIN_ADAPTER",
        "api": "THIN_ADAPTER",
        "worker": "THIN_ADAPTER",
    }
    _assert_control_rejected("application_boundaries", "namespace", "dsgeorref_worker")


def test_req_run_006() -> None:
    control = _profile()["controls"]["domain_errors"]
    assert control["typed"] == "REQUIRED"
    assert control["mapping"] == "VERSIONED_PROBLEM_DETAILS"
    assert control["schema"] == "contracts/errors/problem-details.schema.json"
    assert control["unmapped_error"] == "REJECT"
    _assert_control_rejected("domain_errors", "unmapped_error", "GENERIC_FALLBACK")


def test_req_run_008() -> None:
    control = _profile()["controls"]["typescript_client"]
    assert control["source"] == "contracts/http/openapi.yaml"
    assert control["generation"] == "EXCLUSIVE"
    assert control["semantic_diff_gate"] == "DETERMINISTIC_REQUIRED"
    assert control["manual_dto_duplication"] == "PROHIBITED"
    _assert_control_rejected("typescript_client", "generation", "MANUAL_ALLOWED")


def test_req_run_0010() -> None:
    control = _profile()["controls"]["capability_registry"]
    assert control["scope"] == "LOCAL"
    assert control["versioned"] is True
    assert control["auditable"] is True
    assert control["fail_closed"] is True
    assert all(value is False for value in control["bypass"].values())
    _assert_control_rejected("capability_registry", "fail_closed", False)


def test_sprint_zero_baseline_decision_04() -> None:
    control = _profile()["controls"]["foundation_boundaries"]
    assert control["required"] == ["CORE", "API", "RUNNERS"]
    assert control["separation"] == "MANDATORY"
    assert control["runtime_materialization"] == "DECLARATIVE_ONLY"

    referenced_schema = ROOT / control["contract"]
    referenced_example = referenced_schema.parent / "examples/foundation-boundaries.json"
    schema = _load_json(referenced_schema)
    decision = _load_json(referenced_example)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(decision)
    assert set(decision["boundaries"]) == {"core", "api", "runners"}

    _assert_control_rejected("foundation_boundaries", "separation", "OPTIONAL")
