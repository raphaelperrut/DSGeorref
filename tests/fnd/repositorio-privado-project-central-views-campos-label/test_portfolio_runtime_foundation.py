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
    "prm-run-parte-6"
)
VALIDATOR_PATH = MODULE_ROOT / "policy_validation.py"
VALIDATOR_MODULE_NAME = "portfolio_runtime_foundation_policy_validation"
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "prm-run-parte-6/foundation-policy.json"
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


def test_portfolio_materialization_decision_07() -> None:
    control = _policy()["controls"]["materialization_evidence"]
    assert control["evidence_type"] == "PortfolioMaterializationEvidenceSet"
    assert control["before_operational_convergence"] == "REQUIRED"
    assert control["missing_evidence"] == "REJECT"
    invalid = _replace("materialization_evidence", "missing_evidence", "ALLOW")
    assert "MATERIALIZATION_EVIDENCE_INVALID" in _codes(invalid)


def test_portfolio_materialization_decision_08() -> None:
    control = _policy()["controls"]["sync_run_record"]
    assert control["record_type"] == "PortfolioSyncRunRecord"
    assert control["every_execution"] == "REQUIRED"
    assert control["immutability"] == "REQUIRED"
    assert control["sanitization"] == "REQUIRED"
    invalid = _replace("sync_run_record", "sanitization", "OPTIONAL")
    assert "SYNC_RUN_RECORD_INVALID" in _codes(invalid)


def test_portfolio_materialization_decision_09() -> None:
    control = _policy()["controls"]["wave_recovery"]
    assert control["snapshot"] == "REQUIRED"
    assert control["safe_compensations"] == "REQUIRED"
    assert control["reconciliation"] == "FORWARD"
    assert control["unsafe_recovery"] == "REJECT"
    invalid = _replace("wave_recovery", "safe_compensations", "OPTIONAL")
    assert "WAVE_RECOVERY_INVALID" in _codes(invalid)


def test_portfolio_materialization_decision_10() -> None:
    control = _policy()["controls"]["service_identity"]
    assert control["identity"] == "DEDICATED"
    assert control["privileges"] == "LEAST_PRIVILEGE"
    assert control["credentials"] == "SHORT_LIVED"
    assert control["shared_or_long_lived_credentials"] == "REJECT"
    invalid = _replace("service_identity", "credentials", "LONG_LIVED")
    assert "SERVICE_IDENTITY_INVALID" in _codes(invalid)


def test_req_run_002() -> None:
    control = _policy()["controls"]["domain_io_boundary"]
    assert control["domain_core"] == "SYNCHRONOUS"
    assert control["asynchronous_io"] == "BOUNDARIES_ONLY"
    assert control["asynchronous_domain_core"] == "REJECT"
    invalid = _replace("domain_io_boundary", "asynchronous_io", "DOMAIN_CORE")
    assert "DOMAIN_IO_BOUNDARY_INVALID" in _codes(invalid)


def test_req_run_003() -> None:
    control = _policy()["controls"]["composition"]
    assert control["composition_roots"] == "EXPLICIT"
    assert control["dependency_injection"] == "CONSTRUCTOR"
    assert control["implicit_composition"] == "REJECT"
    invalid = _replace("composition", "dependency_injection", "GLOBAL")
    assert "COMPOSITION_INVALID" in _codes(invalid)


def test_req_run_004() -> None:
    control = _policy()["controls"]["settings"]
    assert control["typing"] == "TYPED"
    assert control["sources"] == "STRATIFIED"
    assert control["required_values"] == "FAIL_CLOSED"
    assert control["missing_required_value"] == "REJECT"
    invalid = _replace("settings", "required_values", "BEST_EFFORT")
    assert "SETTINGS_INVALID" in _codes(invalid)


def test_req_run_005() -> None:
    control = _policy()["controls"]["command_transactions"]
    assert control["unit_of_work"] == "EXPLICIT"
    assert control["transactions"] == "SHORT"
    assert control["implicit_or_long_transaction"] == "REJECT"
    invalid = _replace("command_transactions", "transactions", "UNBOUNDED")
    assert "COMMAND_TRANSACTION_INVALID" in _codes(invalid)


def test_req_run_007() -> None:
    control = _policy()["controls"]["repeatable_mutations"]
    assert control["idempotency"] == "PERSISTENT"
    assert control["volatile_idempotency"] == "REJECT"
    invalid = _replace("repeatable_mutations", "idempotency", "IN_MEMORY")
    assert "IDEMPOTENCY_INVALID" in _codes(invalid)


def test_req_run_009() -> None:
    control = _policy()["controls"]["logging"]
    assert control["envelope"] == "STRUCTURED"
    assert control["correlation_ids"] == "REQUIRED"
    assert control["redaction"] == "CENTRALIZED"
    assert control["uncorrelated_or_unredacted"] == "REJECT"
    invalid = _replace("logging", "redaction", "LOCAL_OPTIONAL")
    assert "LOGGING_INVALID" in _codes(invalid)


def test_policy_rejects_unknown_fields_and_unreadable_input() -> None:
    invalid = copy.deepcopy(_policy())
    invalid["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(invalid)

    with pytest.raises(PolicyValidationError) as captured:
        load_policy(POLICY_PATH.parent / "missing-policy.json")
    assert captured.value.findings[0].code == "POLICY_UNREADABLE"
