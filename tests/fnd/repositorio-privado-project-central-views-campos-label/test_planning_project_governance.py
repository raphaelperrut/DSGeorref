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
    "pln-prj-parte-4"
)
VALIDATOR_PATH = MODULE_ROOT / "policy_validation.py"
VALIDATOR_MODULE_NAME = "planning_project_policy_validation"
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "pln-prj-parte-4/foundation-policy.json"
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
    control = _policy()["controls"]["pull_flow"]
    assert control == {
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


def test_issue_type_forms() -> None:
    control = _policy()["controls"]["issue_types"]
    assert control == {
        "taxonomy": "VERSIONED_CANONICAL",
        "form_per_registered_type": "REQUIRED",
        "unknown_type": "REJECT",
    }
    invalid = _replace("issue_types", "unknown_type", "GENERIC_FORM")
    assert "ISSUE_TYPES_INVALID" in _codes(invalid)


def test_mandatory_core_type_fields() -> None:
    control = _policy()["controls"]["mandatory_fields"]
    assert control == {
        "core": "REQUIRED",
        "per_type_extensions": "REQUIRED",
        "missing_applicable_field": "REJECT",
    }
    invalid = _replace("mandatory_fields", "per_type_extensions", "OPTIONAL")
    assert "MANDATORY_FIELDS_INVALID" in _codes(invalid)


def test_single_parent_limited_hierarchy() -> None:
    control = _policy()["controls"]["hierarchy"]
    assert control == {
        "primary_parent": "EXACTLY_ONE",
        "operational_hierarchy": "LIMITED",
        "multiple_primary_parents": "REJECT",
    }
    invalid = _replace("hierarchy", "multiple_primary_parents", "ALLOW")
    assert "HIERARCHY_INVALID" in _codes(invalid)


def test_definition_of_ready_gate() -> None:
    control = _policy()["controls"]["ready_gate"]
    assert control["definition"] == "docs/00-governance/DEFINITION_OF_READY.md"
    assert control["applicability"] == "PROPORTIONAL"
    assert control["unsatisfied"] == "REJECT"
    invalid = _replace("ready_gate", "unsatisfied", "READY")
    assert "READY_GATE_INVALID" in _codes(invalid)


def test_evidence_based_definition_of_done() -> None:
    control = _policy()["controls"]["done_gate"]
    assert control["definition"] == "docs/00-governance/DEFINITION_OF_DONE.md"
    assert control["evidence"] == "REQUIRED"
    assert control["applicable_checks"] == "REQUIRED"
    assert control["unsatisfied"] == "REJECT"
    invalid = _replace("done_gate", "evidence", "OPTIONAL")
    assert "DONE_GATE_INVALID" in _codes(invalid)


def test_policy_rejects_unknown_fields_and_unreadable_input() -> None:
    invalid = copy.deepcopy(_policy())
    invalid["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(invalid)

    with pytest.raises(PolicyValidationError) as captured:
        load_policy(POLICY_PATH.parent / "missing-policy.json")
    assert captured.value.findings[0].code == "POLICY_UNREADABLE"
