from __future__ import annotations

import copy
import importlib.util
import json
import sys
from functools import cache
from pathlib import Path
from typing import Any, cast

import pytest

ROOT = Path(__file__).resolve().parents[4]
MODULE_ROOT = Path(__file__).resolve().parent
VALIDATOR_PATH = MODULE_ROOT / "policy_validation.py"
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico/"
    "iss-pln-parte-2/foundation-policy.json"
)
MODULE_NAME = "backlog_planning_policy_validation"
SPEC = importlib.util.spec_from_file_location(MODULE_NAME, VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"cannot load validator from {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[MODULE_NAME] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

PolicyValidationError = VALIDATOR.PolicyValidationError
load_policy = VALIDATOR.load_policy
validate_policy = VALIDATOR.validate_policy


@cache
def _policy() -> dict[str, Any]:
    return cast(dict[str, Any], load_policy(POLICY_PATH))


def _codes(policy: object) -> set[str]:
    return {finding.code for finding in validate_policy(policy)}


def _replace(control: str, field: str, value: object) -> dict[str, Any]:
    invalid = copy.deepcopy(_policy())
    invalid["controls"][control][field] = value
    return invalid


def test_complete_portfolio_skeleton_and_progressive_detailing_rules() -> None:
    assert _policy()["controls"]["portfolio"] == {
        "complete_skeleton": "REQUIRED",
        "future_detailing": "PROGRESSIVE",
    }
    invalid = _replace("portfolio", "future_detailing", "FULL_UPFRONT")
    assert "PORTFOLIO_INVALID" in _codes(invalid)


def test_roadmap_horizons_outcomes_gates_and_date_exception() -> None:
    control = _policy()["controls"]["roadmap"]
    assert control["structure"] == ["HORIZON", "OUTCOME", "GATE"]
    assert control["dates"] == "EXCEPTION_ONLY"
    assert control["date_justification"] == "REAL_COMMITMENT_REQUIRED"
    assert control["unjustified_date"] == "REJECT"
    invalid = _replace("roadmap", "date_justification", "OPTIONAL")
    assert "ROADMAP_INVALID" in _codes(invalid)


def test_layered_milestones_gate_release_mapping() -> None:
    assert _policy()["controls"]["milestones"] == {
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


def test_wip_class_limits_global_cap_and_emergency_reserve() -> None:
    control = _policy()["controls"]["wip_limits"]
    assert control["scopes"] == ["CLASS", "GLOBAL"]
    assert control["reservations"] == ["P0", "SECURITY", "MAINTENANCE"]
    assert control["over_limit"] == "REJECT"
    invalid = _replace("wip_limits", "reservations", ["P0"])
    assert "WIP_LIMITS_INVALID" in _codes(invalid)


def test_capacity_ranges_availability_throughput_and_no_deadline_conversion() -> None:
    control = _policy()["controls"]["capacity"]
    assert control["estimate"] == "RANGE"
    assert control["categories"] == ["AVAILABILITY", "THROUGHPUT"]
    assert control["confidence"] == "REQUIRED"
    assert control["automatic_deadline_conversion"] == "PROHIBITED"
    assert control["invalid_range"] == "REJECT"
    invalid = _replace("capacity", "automatic_deadline_conversion", "ALLOW")
    assert "CAPACITY_INVALID" in _codes(invalid)


def test_pull_iteration_objective_and_carryover_reason_classification() -> None:
    assert _policy()["controls"]["pull_flow"] == {
        "system": "PULL",
        "iteration_objective": "REQUIRED",
        "carryover_reason": "CLASSIFICATION_REQUIRED",
        "unclassified_carryover": "REJECT",
    }
    invalid = _replace("pull_flow", "unclassified_carryover", "ALLOW")
    assert "PULL_FLOW_INVALID" in _codes(invalid)


def test_accountable_owner_collaborator_reviewer_and_gate_approver() -> None:
    control = _policy()["controls"]["roles"]
    assert control["accountable_owner"] == "EXACTLY_ONE"
    assert control["collaborator"] == "SEPARATE"
    assert control["reviewer"] == "SEPARATE"
    assert control["gate_approver"] == "SEPARATE"
    assert control["self_approval"] == "PROHIBITED"
    invalid = _replace("roles", "reviewer", "ACCOUNTABLE_OWNER")
    assert "ROLE_SEPARATION_INVALID" in _codes(invalid)


def test_versioned_reforecast_snapshot_variance_classification_and_delta_report() -> None:
    control = _policy()["controls"]["reforecast"]
    assert control["snapshots"] == "VERSIONED_IMMUTABLE"
    assert control["material_variance"] == "CLASSIFICATION_REQUIRED"
    assert control["delta_report"] == "REQUIRED"
    assert control["overwrite"] == "REJECT"
    assert control["unclassified_material_variance"] == "REJECT"
    invalid = _replace("reforecast", "overwrite", "ALLOW")
    assert "REFORECAST_INVALID" in _codes(invalid)


def test_policy_input_fails_closed(tmp_path: Path) -> None:
    unknown = copy.deepcopy(_policy())
    unknown["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(unknown)

    missing = copy.deepcopy(_policy())
    del missing["controls"]["portfolio"]
    assert "PORTFOLIO_INVALID" in _codes(missing)

    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"schema_version":"1","schema_version":"2"}', encoding="utf-8")
    with pytest.raises(PolicyValidationError, match="duplicate JSON key"):
        load_policy(duplicate)

    non_finite = tmp_path / "non-finite.json"
    non_finite.write_text('{"schema_version":NaN}', encoding="utf-8")
    with pytest.raises(PolicyValidationError, match="non-finite JSON constant"):
        load_policy(non_finite)

    unreadable = tmp_path / "missing.json"
    with pytest.raises(PolicyValidationError) as captured:
        load_policy(unreadable)
    assert captured.value.findings[0].code == "POLICY_UNREADABLE"

    assert json.loads(POLICY_PATH.read_text(encoding="utf-8")) == _policy()
