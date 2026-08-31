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
    / "migrations-ci-secret-dependency-scan-e-telemetria-mini"
    / "sgvcal-parte-2"
)
SCHEMA_PATH = CONTRACT_ROOT / "sgvcal-conformance.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/sgvcal-conformance.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0707.json"
VERDICT_PATH = ROOT / "contracts/domain/sgv-verdict.schema.json"
BENCHMARK_PATH = ROOT / "docs/04-quality/benchmark-profiles/BP-002-sgv-calibration.md"

REQUIREMENT_TESTS = {
    "REQ-SGVCAL-001": "test_req_sgvcal_001",
    "REQ-SGVCAL-002": "test_req_sgvcal_002",
    "REQ-SGVCAL-003": "test_req_sgvcal_003",
    "REQ-SGVCAL-004": "test_req_sgvcal_004",
    "REQ-SGVCAL-005": "test_req_sgvcal_005",
    "REQ-SGVCAL-006": "test_req_sgvcal_006",
    "REQ-SGVCAL-007": "test_req_sgvcal_007",
    "REQ-SGVCAL-008": "test_req_sgvcal_008",
    "REQ-SGVCAL-009": "test_req_sgvcal_009",
    "REQ-SGVCAL-010": "test_req_sgvcal_0010",
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


def test_req_sgvcal_001() -> None:
    control = _profile()["controls"]["profile_immutability"]
    assert control["scope"] == "PER_STRATUM"
    assert control["hard_invariants"] == "IMMUTABLE"
    assert control["sgv_profile"] == "IMMUTABLE_VERSIONED"
    assert control["evidence"] == "IMMUTABLE_CONTENT_ADDRESSED"
    assert control["digest_algorithm"] == "SHA-256"
    _manifest_entry("REQ-SGVCAL-001")
    _assert_control_rejected("profile_immutability", "missing_or_mutable", "WARN")


def test_req_sgvcal_002() -> None:
    control = _profile()["controls"]["metric_declaration"]
    assert control["required_dimensions"] == [
        "space",
        "unit",
        "direction",
        "normalization",
    ]
    _manifest_entry("REQ-SGVCAL-002")
    _assert_control_rejected("metric_declaration", "required_dimensions", ["unit"])


def test_req_sgvcal_003() -> None:
    control = _profile()["controls"]["robust_error_distribution"]
    assert control["transfer_error"] == "SYMMETRIC"
    assert control["distribution"] == "ROBUST"
    _manifest_entry("REQ-SGVCAL-003")
    _assert_control_rejected("robust_error_distribution", "transfer_error", "FORWARD_ONLY")


def test_req_sgvcal_004() -> None:
    control = _profile()["controls"]["multidimensional_coverage"]
    assert control["required_dimensions"] == ["leverage", "spatial_support"]
    _manifest_entry("REQ-SGVCAL-004")
    _assert_control_rejected("multidimensional_coverage", "required_dimensions", ["leverage"])


def test_req_sgvcal_005() -> None:
    control = _profile()["controls"]["stability_gates"]
    assert control["required_checks"] == [
        "conditioning",
        "degeneracy",
        "leave_one_out_stability",
    ]
    _manifest_entry("REQ-SGVCAL-005")
    _assert_control_rejected("stability_gates", "required_checks", ["conditioning"])


def test_req_sgvcal_006() -> None:
    control = _profile()["controls"]["local_deformation"]
    assert control["measurement"] == "ADAPTIVE_JACOBIAN"
    _manifest_entry("REQ-SGVCAL-006")
    _assert_control_rejected("local_deformation", "measurement", "GLOBAL_ONLY")


def test_req_sgvcal_007() -> None:
    control = _profile()["controls"]["contextual_validity"]
    verdict = _load_json(VERDICT_PATH)
    assert control["required_checks"] == [
        "footprint",
        "topology",
        "crs",
        "contextual_plausibility",
    ]
    assert control["all_checks_required"] is True
    assert control["missing_or_invalid"] == "REJECT"
    assert control["silent_fallback"] == "PROHIBITED"
    assert "hard_gates" in verdict["required"]
    assert "SILENT_CONTEXT_FALLBACK" in _manifest_entry("REQ-SGVCAL-007")[
        "failure_modes"
    ]
    _assert_control_rejected("contextual_validity", "required_checks", ["crs"])
    _assert_control_rejected("contextual_validity", "silent_fallback", "ALLOW")


def test_req_sgvcal_008() -> None:
    control = _profile()["controls"]["calibration_governance"]
    benchmark = BENCHMARK_PATH.read_text(encoding="utf-8")
    assert control["calibration"] == "STRATIFIED"
    assert control["holdout"] == "BLIND_SEPARATE"
    assert control["false_acceptance_budget"] == "BLOCKING"
    assert "holdout cego" in benchmark
    assert "falso aceite crítico como budget bloqueante" in benchmark
    _manifest_entry("REQ-SGVCAL-008")
    _assert_control_rejected("calibration_governance", "missing_or_exceeded", "WARN")


def test_req_sgvcal_009() -> None:
    control = _profile()["controls"]["gray_zone"]
    verdict = _load_json(VERDICT_PATH)
    assert control["outcome"] == "REVIEWABLE"
    assert control["hard_gate_override"] == "PROHIBITED"
    assert control["failed_hard_gate"] == "REJECTED"
    assert "reviewable" in verdict["properties"]["verdict"]["enum"]
    _manifest_entry("REQ-SGVCAL-009")
    _assert_control_rejected("gray_zone", "hard_gate_override", "ALLOW")


def test_req_sgvcal_0010() -> None:
    control = _profile()["controls"]["promotion_and_rollback"]
    assert control["stages"] == ["shadow", "canary"]
    assert control["profile_evidence"] == "IMMUTABLE_CONTENT_ADDRESSED"
    assert control["rollback"] == "REQUIRED"
    _manifest_entry("REQ-SGVCAL-010")
    _assert_control_rejected("promotion_and_rollback", "stages", ["canary"])
    _assert_control_rejected("promotion_and_rollback", "rollback", "OPTIONAL")


def test_contract_package_is_registered_and_envelope_is_contained() -> None:
    manifest = _load_yaml(MANIFEST_PATH)
    assert manifest["status"] == "FROZEN"
    assert manifest["contract_version"] == _profile()["profile_version"] == "1.0.0"
    assert manifest["proof"]["mandatory_story_test"] == "test_req_sgvcal_007"
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
    assert ".codex/tasks/TASK-0707.json" in allow_paths
    assert "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv" in allow_paths
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in allow_paths
    assert any(path.startswith("evidence/implementation/migrations-ci-") for path in allow_paths)
    assert not any(path.startswith("src/") for path in allow_paths)


def test_profile_rejects_missing_unknown_or_permissive_state() -> None:
    missing = copy.deepcopy(_profile())
    del missing["controls"]["contextual_validity"]
    _assert_rejected(missing)

    unknown = copy.deepcopy(_profile())
    unknown["controls"]["silent_fallback"] = {"enabled": True}
    _assert_rejected(unknown)

    permissive = copy.deepcopy(_profile())
    permissive["status"] = "DRAFT"
    _assert_rejected(permissive)
