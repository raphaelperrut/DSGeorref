from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


class PolicyValidationError(ValueError):
    def __init__(self, findings: list[Finding] | tuple[Finding, ...]) -> None:
        self.findings = tuple(sorted(findings))
        message = "; ".join(
            f"{finding.code} at {finding.field}: {finding.detail}"
            for finding in self.findings
        )
        super().__init__(message)


EXPECTED_POLICY: dict[str, Any] = {
    "schema_version": "1.0.0",
    "policy_id": "ENGINEERING-FOUNDATION-PORTFOLIO-RUNTIME",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "controls": {
        "materialization_evidence": {
            "evidence_type": "PortfolioMaterializationEvidenceSet",
            "before_operational_convergence": "REQUIRED",
            "missing_evidence": "REJECT",
        },
        "sync_run_record": {
            "record_type": "PortfolioSyncRunRecord",
            "every_execution": "REQUIRED",
            "immutability": "REQUIRED",
            "sanitization": "REQUIRED",
            "missing_or_mutable_record": "REJECT",
        },
        "wave_recovery": {
            "snapshot": "REQUIRED",
            "safe_compensations": "REQUIRED",
            "reconciliation": "FORWARD",
            "unsafe_recovery": "REJECT",
        },
        "service_identity": {
            "identity": "DEDICATED",
            "privileges": "LEAST_PRIVILEGE",
            "credentials": "SHORT_LIVED",
            "shared_or_long_lived_credentials": "REJECT",
        },
        "domain_io_boundary": {
            "domain_core": "SYNCHRONOUS",
            "asynchronous_io": "BOUNDARIES_ONLY",
            "asynchronous_domain_core": "REJECT",
        },
        "composition": {
            "composition_roots": "EXPLICIT",
            "dependency_injection": "CONSTRUCTOR",
            "implicit_composition": "REJECT",
        },
        "settings": {
            "typing": "TYPED",
            "sources": "STRATIFIED",
            "required_values": "FAIL_CLOSED",
            "missing_required_value": "REJECT",
        },
        "command_transactions": {
            "unit_of_work": "EXPLICIT",
            "transactions": "SHORT",
            "implicit_or_long_transaction": "REJECT",
        },
        "repeatable_mutations": {
            "idempotency": "PERSISTENT",
            "volatile_idempotency": "REJECT",
        },
        "logging": {
            "envelope": "STRUCTURED",
            "correlation_ids": "REQUIRED",
            "redaction": "CENTRALIZED",
            "uncorrelated_or_unredacted": "REJECT",
        },
    },
    "requirement_evidence": {
        "REQ-PRM-007": "test_portfolio_materialization_decision_07",
        "REQ-PRM-008": "test_portfolio_materialization_decision_08",
        "REQ-PRM-009": "test_portfolio_materialization_decision_09",
        "REQ-PRM-010": "test_portfolio_materialization_decision_10",
        "REQ-RUN-002": "test_req_run_002",
        "REQ-RUN-003": "test_req_run_003",
        "REQ-RUN-004": "test_req_run_004",
        "REQ-RUN-005": "test_req_run_005",
        "REQ-RUN-007": "test_req_run_007",
        "REQ-RUN-009": "test_req_run_009",
    },
}


def _finding_code(field: str) -> str:
    mappings = {
        "materialization_evidence": "MATERIALIZATION_EVIDENCE_INVALID",
        "sync_run_record": "SYNC_RUN_RECORD_INVALID",
        "wave_recovery": "WAVE_RECOVERY_INVALID",
        "service_identity": "SERVICE_IDENTITY_INVALID",
        "domain_io_boundary": "DOMAIN_IO_BOUNDARY_INVALID",
        "composition": "COMPOSITION_INVALID",
        "settings": "SETTINGS_INVALID",
        "command_transactions": "COMMAND_TRANSACTION_INVALID",
        "repeatable_mutations": "IDEMPOTENCY_INVALID",
        "logging": "LOGGING_INVALID",
    }
    for control, code in mappings.items():
        if field.startswith(f"$.controls.{control}"):
            return code
    if field.startswith("$.requirement_evidence"):
        return "REQUIREMENT_EVIDENCE_INVALID"
    return "POLICY_STRUCTURE_INVALID"


def _compare(actual: object, expected: object, field: str) -> list[Finding]:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [Finding(_finding_code(field), field, "expected object")]
        findings: list[Finding] = []
        for key in sorted(actual.keys() - expected.keys()):
            findings.append(
                Finding("POLICY_STRUCTURE_INVALID", f"{field}.{key}", "unknown field")
            )
        for key in sorted(expected.keys() - actual.keys()):
            target = f"{field}.{key}"
            findings.append(Finding(_finding_code(target), target, "missing field"))
        for key in sorted(actual.keys() & expected.keys()):
            findings.extend(_compare(actual[key], expected[key], f"{field}.{key}"))
        return findings
    if type(actual) is not type(expected) or actual != expected:
        return [Finding(_finding_code(field), field, f"expected {expected!r}")]
    return []


def validate_policy(policy: object) -> list[Finding]:
    return sorted(_compare(policy, EXPECTED_POLICY, "$"))


def require_valid(policy: object) -> None:
    findings = validate_policy(policy)
    if findings:
        raise PolicyValidationError(findings)


def load_policy(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PolicyValidationError(
            [Finding("POLICY_UNREADABLE", "$", str(error))]
        ) from error
    require_valid(loaded)
    return loaded
