from __future__ import annotations

import copy
import importlib.util
import sys
from functools import cache
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[4]
MODULE_ROOT = Path(__file__).resolve().parent
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico/"
    "prm-sprint-001-parte-4/foundation-policy.json"
)
_SPEC = importlib.util.spec_from_file_location(
    "portfolio_materialization_slice_policy_validation",
    MODULE_ROOT / "policy_validation.py",
)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError("cannot load portfolio materialization policy validator")
_VALIDATOR = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _VALIDATOR
_SPEC.loader.exec_module(_VALIDATOR)

PolicyValidationError = _VALIDATOR.PolicyValidationError
load_policy = _VALIDATOR.load_policy
validate_policy = _VALIDATOR.validate_policy


@cache
def _policy() -> dict[str, Any]:
    return load_policy(POLICY_PATH)


def _codes(policy: object) -> set[str]:
    return {finding.code for finding in validate_policy(policy)}


def _replace(control: str, field: str, value: object) -> dict[str, Any]:
    invalid = copy.deepcopy(_policy())
    invalid["controls"][control][field] = value
    return invalid


def test_portfolio_materialization_decision_02() -> None:
    control = _policy()["controls"]["bounded_waves"]
    assert control == {
        "dependency_bound": "REQUIRED",
        "gate_bound": "REQUIRED",
        "risk_bound": "REQUIRED",
        "unbounded_import": "REJECT",
    }
    assert "MATERIALIZATION_WAVES_INVALID" in _codes(
        _replace("bounded_waves", "risk_bound", "OPTIONAL")
    )


def test_portfolio_materialization_decision_03() -> None:
    control = _policy()["controls"]["field_sync"]
    assert control["authority_per_field"] == "REQUIRED"
    assert control["direction_per_field"] == "REQUIRED"
    assert control["undefined_field_governance"] == "REJECT"
    assert "FIELD_SYNC_INVALID" in _codes(
        _replace("field_sync", "direction_per_field", "IMPLICIT")
    )


def test_portfolio_materialization_decision_04() -> None:
    control = _policy()["controls"]["drift_reconciliation"]
    assert control["comparison"] == "THREE_WAY"
    assert control["conflict_classification"] == "REQUIRED"
    assert control["silent_conflict_overwrite"] == "REJECT"
    assert "DRIFT_RECONCILIATION_INVALID" in _codes(
        _replace("drift_reconciliation", "comparison", "TWO_WAY")
    )


def test_portfolio_materialization_decision_05() -> None:
    control = _policy()["controls"]["destructive_changes"]
    assert control["approved_changeset"] == "REQUIRED"
    assert control["tombstones"] == "REQUIRED"
    assert control["direct_destructive_mutation"] == "REJECT"
    assert "DESTRUCTIVE_CHANGE_INVALID" in _codes(
        _replace("destructive_changes", "tombstones", "OPTIONAL")
    )


def test_portfolio_materialization_decision_06() -> None:
    control = _policy()["controls"]["resumable_operations"]
    assert control["idempotency"] == "REQUIRED"
    assert control["checkpoints"] == "REQUIRED"
    assert control["backoff"] == "REQUIRED"
    assert control["safe_resume"] == "REQUIRED"
    assert control["incompatible_resume"] == "REJECT"
    assert "RESUMABLE_OPERATION_INVALID" in _codes(
        _replace("resumable_operations", "safe_resume", "BEST_EFFORT")
    )


def test_portfolio_materialization_decision_07() -> None:
    control = _policy()["controls"]["materialization_evidence"]
    assert control["evidence_type"] == "PortfolioMaterializationEvidenceSet"
    assert control["before_operational_convergence"] == "REQUIRED"
    assert control["missing_evidence"] == "REJECT"
    assert "MATERIALIZATION_EVIDENCE_INVALID" in _codes(
        _replace("materialization_evidence", "missing_evidence", "ALLOW")
    )


def test_portfolio_materialization_decision_08() -> None:
    control = _policy()["controls"]["sync_run_record"]
    assert control["record_type"] == "PortfolioSyncRunRecord"
    assert control["every_execution"] == "REQUIRED"
    assert control["immutability"] == "REQUIRED"
    assert control["sanitization"] == "REQUIRED"
    assert control["missing_or_mutable_record"] == "REJECT"
    assert "SYNC_RUN_RECORD_INVALID" in _codes(
        _replace("sync_run_record", "sanitization", "OPTIONAL")
    )


def test_portfolio_materialization_decision_09() -> None:
    control = _policy()["controls"]["wave_recovery"]
    assert control["snapshot"] == "REQUIRED"
    assert control["safe_compensations"] == "REQUIRED"
    assert control["reconciliation"] == "FORWARD"
    assert control["unsafe_recovery"] == "REJECT"
    assert "WAVE_RECOVERY_INVALID" in _codes(
        _replace("wave_recovery", "safe_compensations", "OPTIONAL")
    )


def test_portfolio_materialization_decision_10() -> None:
    control = _policy()["controls"]["service_identity"]
    assert control["identity"] == "DEDICATED"
    assert control["privileges"] == "LEAST_PRIVILEGE"
    assert control["credentials"] == "SHORT_LIVED"
    assert control["shared_or_long_lived_credentials"] == "REJECT"
    assert "SERVICE_IDENTITY_INVALID" in _codes(
        _replace("service_identity", "credentials", "LONG_LIVED")
    )


def test_sprint_zero_baseline_decision_01() -> None:
    control = _policy()["controls"]["sprint_minimum_scope"]
    assert control["selection"] == "MINIMUM_ONLY"
    assert len(control["capabilities"]) == 7
    assert control["capabilities"][-1] == "SprintEvidenceSet machine-readable"
    assert control["scope_expansion"] == "REJECT"
    assert "SPRINT_MINIMUM_SCOPE_INVALID" in _codes(
        _replace("sprint_minimum_scope", "scope_expansion", "ALLOW")
    )


def test_policy_input_is_strict_and_fail_closed() -> None:
    unknown = copy.deepcopy(_policy())
    unknown["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(unknown)

    missing = copy.deepcopy(_policy())
    del missing["controls"]["service_identity"]["credentials"]
    assert "SERVICE_IDENTITY_INVALID" in _codes(missing)

    missing_evidence = copy.deepcopy(_policy())
    del missing_evidence["requirement_evidence"]["REQ-PRM-008"]
    assert "REQUIREMENT_EVIDENCE_INVALID" in _codes(missing_evidence)
    assert "POLICY_STRUCTURE_INVALID" in _codes([])

    duplicate_text = '{"schema_version":"1.0.0","schema_version":"1.0.0"}'
    with (
        patch.object(Path, "read_text", return_value=duplicate_text),
        pytest.raises(PolicyValidationError) as duplicate_error,
    ):
        load_policy(POLICY_PATH)
    assert duplicate_error.value.findings[0].code == "POLICY_DUPLICATE_KEY"

    with pytest.raises(PolicyValidationError) as missing_file_error:
        load_policy(POLICY_PATH.with_name("missing-policy.json"))
    assert missing_file_error.value.findings[0].code == "POLICY_UNREADABLE"
