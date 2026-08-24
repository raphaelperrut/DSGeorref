from __future__ import annotations

import copy
import importlib.util
import sys
from functools import cache
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/repositorio-privado-project-central-views-campos-label/"
    "native-pln-parte-3"
)
VALIDATOR_PATH = MODULE_ROOT / "policy_validation.py"
VALIDATOR_MODULE_NAME = "native_planning_policy_validation"
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "native-pln-parte-3/foundation-policy.json"
)
_validator_spec = importlib.util.spec_from_file_location(
    VALIDATOR_MODULE_NAME, VALIDATOR_PATH
)
if _validator_spec is None or _validator_spec.loader is None:
    raise ImportError(f"cannot load validator from {VALIDATOR_PATH}")
_validator = importlib.util.module_from_spec(_validator_spec)
sys.modules[VALIDATOR_MODULE_NAME] = _validator
_validator_spec.loader.exec_module(_validator)

PolicyValidationError = _validator.PolicyValidationError
load_policy = _validator.load_policy
validate_policy = _validator.validate_policy


@cache
def _policy() -> dict[str, Any]:
    return load_policy(POLICY_PATH)


def _codes(policy: object) -> set[str]:
    return {finding.code for finding in validate_policy(policy)}


def _replace(control: str, field: str, value: object) -> dict[str, Any]:
    invalid = copy.deepcopy(_policy())
    invalid["controls"][control][field] = value
    return invalid


def test_req_native_005() -> None:
    control = _policy()["controls"]["classic_descriptor"]
    assert control == {
        "descriptor": "ROOTSIFT",
        "numeric_representation": "FLOAT32",
        "promotion": "CANONICAL",
    }
    invalid = _replace("classic_descriptor", "descriptor", "SIFT")
    assert "CLASSIC_DESCRIPTOR_INVALID" in _codes(invalid)


def test_req_native_006() -> None:
    control = _policy()["controls"]["classic_matcher"]
    assert control == {
        "ann": "FLANN_KD_TREE",
        "ann_status": "REQUIRED",
        "calibration_oracle": "BF_EXACT",
        "oracle_mode": "CONTROLLED",
    }
    invalid = _replace("classic_matcher", "oracle_mode", "DEFAULT")
    assert "CLASSIC_MATCHER_INVALID" in _codes(invalid)


def test_req_native_007() -> None:
    control = _policy()["controls"]["robust_estimator"]
    assert control["library"] == "OPENCV"
    assert control["estimator"] == "USAC_MAGSAC"
    assert control["versioning"] == "OCI_DIGEST_PINNED"
    assert control["boundary"] == "ENCAPSULATED"
    assert control["silent_fallback"] == "PROHIBITED"
    invalid = _replace("robust_estimator", "silent_fallback", "RANSAC")
    assert "ROBUST_ESTIMATOR_INVALID" in _codes(invalid)


def test_req_native_008() -> None:
    control = _policy()["controls"]["cog"]
    assert control["writer"] == "GDAL_NATIVE_STACK"
    assert control["validation_path"] == "INDEPENDENT"
    assert control["validation_dimensions"] == ["STRUCTURAL", "SPATIAL", "CONTENT"]
    assert control["invalid_output"] == "REJECT"
    invalid = _replace("cog", "validation_path", "WRITER_SELF_CHECK")
    assert "COG_INVALID" in _codes(invalid)


def test_req_native_009() -> None:
    control = _policy()["controls"]["native_stack"]
    assert control["promotion_unit"] == "OCI_ABI"
    assert control["members"] == [
        "GDAL",
        "PROJ",
        "GEOS",
        "OPENCV",
        "GRIDS",
        "BINDINGS",
    ]
    assert control["pin"] == "NATIVE_OCI_STACK_DIGEST"
    assert control["abi_smoke"] == "REQUIRED"
    invalid = _replace("native_stack", "promotion_unit", "INDEPENDENT_PACKAGES")
    assert "NATIVE_STACK_INVALID" in _codes(invalid)


def test_req_native_0010() -> None:
    control = _policy()["controls"]["native_io"]
    assert control["drivers"] == "ALLOWLIST"
    assert control["vsi"] == "ALLOWLIST"
    assert control["network_vsi"] == "DISABLED_BY_DEFAULT"
    assert control["external_files"] == "HOSTILE"
    assert control["dataset_handles"] == "WORK_UNIT_LOCAL"
    assert control["process_isolation"] == "REQUIRED"
    invalid = _replace("native_io", "dataset_handles", "SHARED")
    assert "NATIVE_IO_INVALID" in _codes(invalid)


def test_roadmap_horizons_outcomes_gates_and_date_exception() -> None:
    control = _policy()["controls"]["roadmap"]
    assert control["structure"] == ["HORIZON", "OUTCOME", "GATE"]
    assert control["dates"] == "EXCEPTION_ONLY"
    assert control["date_justification"] == "REAL_COMMITMENT_REQUIRED"
    assert control["unjustified_date"] == "REJECT"
    invalid = _replace("roadmap", "date_justification", "OPTIONAL")
    assert "ROADMAP_INVALID" in _codes(invalid)


def test_layered_milestones_gate_release_mapping() -> None:
    control = _policy()["controls"]["milestones"]
    assert control == {
        "outcome_gate": "SEPARATE_LAYER",
        "release": "SEPARATE_LAYER",
        "iteration": "SEPARATE_LAYER",
        "mapping": "EXPLICIT_REQUIRED",
    }
    invalid = _replace("milestones", "mapping", "IMPLICIT")
    assert "MILESTONES_INVALID" in _codes(invalid)


def test_sequence_gates_dependencies_priority_override_audit() -> None:
    control = _policy()["controls"]["sequencing"]
    assert control["order_by"] == [
        "BLOCKER",
        "GATE",
        "DEPENDENCY",
        "EXPLAINABLE_PRIORITY",
    ]
    assert control["priority_override"] == "AUDIT_REQUIRED"
    assert control["unaudited_override"] == "REJECT"
    invalid = _replace("sequencing", "unaudited_override", "ALLOW")
    assert "SEQUENCING_INVALID" in _codes(invalid)


def test_critical_enablers_uncertain_dependencies_and_risk_buffers() -> None:
    control = _policy()["controls"]["critical_dependencies"]
    assert control["classifications"] == [
        "ENABLER",
        "HIGH_FAN_OUT",
        "SINGLE_POINT_OF_FAILURE",
        "UNCERTAIN_DEPENDENCY",
    ]
    assert control["uncertain_dependency"] == "RISK_BUFFER_REQUIRED"
    assert control["unclassified_critical_dependency"] == "REJECT"
    invalid = _replace("critical_dependencies", "uncertain_dependency", "IGNORE")
    assert "CRITICAL_DEPENDENCIES_INVALID" in _codes(invalid)


def test_policy_rejects_unknown_fields_and_unreadable_input() -> None:
    invalid = copy.deepcopy(_policy())
    invalid["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(invalid)

    with pytest.raises(PolicyValidationError) as captured:
        load_policy(POLICY_PATH.parent / "missing-policy.json")
    assert captured.value.findings[0].code == "POLICY_UNREADABLE"
