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
    "prj-prm-parte-5"
)
VALIDATOR_PATH = MODULE_ROOT / "policy_validation.py"
VALIDATOR_MODULE_NAME = "project_portfolio_materialization_policy_validation"
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "prj-prm-parte-5/foundation-policy.json"
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


def test_typed_dependency_cycle_detection() -> None:
    control = _policy()["controls"]["typed_dependencies"]
    assert control["edge_type"] == "REQUIRED"
    assert control["material_cycle_detection"] == "REQUIRED"
    assert control["material_cycle"] == "REJECT"
    invalid = _replace("typed_dependencies", "material_cycle", "ALLOW")
    assert "DEPENDENCY_GRAPH_INVALID" in _codes(invalid)


def test_derived_priority_dimensions() -> None:
    control = _policy()["controls"]["priority"]
    assert control["dimensions"] == ["IMPACT", "URGENCY", "RISK", "GATE"]
    assert control["derivation"] == "EXPLICIT"
    assert control["collapsed_dimension"] == "REJECT"
    invalid = _replace("priority", "dimensions", ["PRIORITY"])
    assert "PRIORITY_INVALID" in _codes(invalid)


def test_relative_size_uncertainty_split() -> None:
    control = _policy()["controls"]["relative_size"]
    assert control["estimate"] == "RELATIVE_BAND"
    assert control["confidence"] == "REQUIRED"
    assert control["split_rule"] == "REQUIRED"
    assert control["uncertain_without_split_rule"] == "REJECT"
    invalid = _replace("relative_size", "confidence", "OPTIONAL")
    assert "RELATIVE_SIZE_INVALID" in _codes(invalid)


def test_guarded_project_automation() -> None:
    control = _policy()["controls"]["guarded_automation"]
    assert control["integrity_preservation"] == "REQUIRED"
    assert control["material_decision_approval"] == "PROHIBITED"
    assert control["material_decision_gate"] == "HUMAN_REQUIRED"
    assert control["silent_approval"] == "REJECT"
    invalid = _replace("guarded_automation", "material_decision_approval", "ALLOW")
    assert "AUTOMATION_GUARD_INVALID" in _codes(invalid)


def test_portfolio_materialization_decision_01() -> None:
    control = _policy()["controls"]["staging_materialization"]
    assert control["first_target"] == "REPRESENTATIVE_STAGING"
    assert control["operational_project_after_staging"] == "REQUIRED"
    assert control["direct_first_operational_materialization"] == "REJECT"
    invalid = _replace(
        "staging_materialization", "direct_first_operational_materialization", "ALLOW"
    )
    assert "STAGING_MATERIALIZATION_INVALID" in _codes(invalid)


def test_portfolio_materialization_decision_02() -> None:
    control = _policy()["controls"]["bounded_waves"]
    assert control["dependency_bound"] == "REQUIRED"
    assert control["gate_bound"] == "REQUIRED"
    assert control["risk_bound"] == "REQUIRED"
    assert control["unbounded_import"] == "REJECT"
    invalid = _replace("bounded_waves", "risk_bound", "OPTIONAL")
    assert "MATERIALIZATION_WAVES_INVALID" in _codes(invalid)


def test_portfolio_materialization_decision_03() -> None:
    control = _policy()["controls"]["field_sync"]
    assert control["authority_per_field"] == "REQUIRED"
    assert control["direction_per_field"] == "REQUIRED"
    assert control["undefined_field_governance"] == "REJECT"
    invalid = _replace("field_sync", "direction_per_field", "IMPLICIT")
    assert "FIELD_SYNC_INVALID" in _codes(invalid)


def test_portfolio_materialization_decision_04() -> None:
    control = _policy()["controls"]["drift_reconciliation"]
    assert control["comparison"] == "THREE_WAY"
    assert control["conflict_classification"] == "REQUIRED"
    assert control["silent_conflict_overwrite"] == "REJECT"
    invalid = _replace("drift_reconciliation", "comparison", "TWO_WAY")
    assert "DRIFT_RECONCILIATION_INVALID" in _codes(invalid)


def test_portfolio_materialization_decision_05() -> None:
    control = _policy()["controls"]["destructive_changes"]
    assert control["approved_changeset"] == "REQUIRED"
    assert control["tombstones"] == "REQUIRED"
    assert control["direct_destructive_mutation"] == "REJECT"
    invalid = _replace("destructive_changes", "tombstones", "OPTIONAL")
    assert "DESTRUCTIVE_CHANGE_INVALID" in _codes(invalid)


def test_portfolio_materialization_decision_06() -> None:
    control = _policy()["controls"]["resumable_operations"]
    assert control["idempotency"] == "REQUIRED"
    assert control["checkpoints"] == "REQUIRED"
    assert control["backoff"] == "REQUIRED"
    assert control["safe_resume"] == "REQUIRED"
    assert control["incompatible_resume"] == "REJECT"
    invalid = _replace("resumable_operations", "safe_resume", "BEST_EFFORT")
    assert "RESUMABLE_OPERATION_INVALID" in _codes(invalid)


def test_policy_rejects_unknown_fields_and_unreadable_input() -> None:
    invalid = copy.deepcopy(_policy())
    invalid["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(invalid)

    with pytest.raises(PolicyValidationError) as captured:
        load_policy(POLICY_PATH.parent / "missing-policy.json")
    assert captured.value.findings[0].code == "POLICY_UNREADABLE"
