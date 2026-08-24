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
    "policy_id": "ENGINEERING-FOUNDATION-PROJECT-MATERIALIZATION",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "controls": {
        "typed_dependencies": {
            "edge_type": "REQUIRED",
            "material_cycle_detection": "REQUIRED",
            "material_cycle": "REJECT",
        },
        "priority": {
            "dimensions": ["IMPACT", "URGENCY", "RISK", "GATE"],
            "derivation": "EXPLICIT",
            "collapsed_dimension": "REJECT",
        },
        "relative_size": {
            "estimate": "RELATIVE_BAND",
            "confidence": "REQUIRED",
            "split_rule": "REQUIRED",
            "uncertain_without_split_rule": "REJECT",
        },
        "guarded_automation": {
            "integrity_preservation": "REQUIRED",
            "material_decision_approval": "PROHIBITED",
            "material_decision_gate": "HUMAN_REQUIRED",
            "silent_approval": "REJECT",
        },
        "staging_materialization": {
            "first_target": "REPRESENTATIVE_STAGING",
            "operational_project_after_staging": "REQUIRED",
            "direct_first_operational_materialization": "REJECT",
        },
        "bounded_waves": {
            "dependency_bound": "REQUIRED",
            "gate_bound": "REQUIRED",
            "risk_bound": "REQUIRED",
            "unbounded_import": "REJECT",
        },
        "field_sync": {
            "authority_per_field": "REQUIRED",
            "direction_per_field": "REQUIRED",
            "undefined_field_governance": "REJECT",
        },
        "drift_reconciliation": {
            "comparison": "THREE_WAY",
            "conflict_classification": "REQUIRED",
            "silent_conflict_overwrite": "REJECT",
        },
        "destructive_changes": {
            "approved_changeset": "REQUIRED",
            "tombstones": "REQUIRED",
            "direct_destructive_mutation": "REJECT",
        },
        "resumable_operations": {
            "idempotency": "REQUIRED",
            "checkpoints": "REQUIRED",
            "backoff": "REQUIRED",
            "safe_resume": "REQUIRED",
            "incompatible_resume": "REJECT",
        },
    },
    "requirement_evidence": {
        "REQ-PRJ-007": "test_typed_dependency_cycle_detection",
        "REQ-PRJ-008": "test_derived_priority_dimensions",
        "REQ-PRJ-009": "test_relative_size_uncertainty_split",
        "REQ-PRJ-010": "test_guarded_project_automation",
        "REQ-PRM-001": "test_portfolio_materialization_decision_01",
        "REQ-PRM-002": "test_portfolio_materialization_decision_02",
        "REQ-PRM-003": "test_portfolio_materialization_decision_03",
        "REQ-PRM-004": "test_portfolio_materialization_decision_04",
        "REQ-PRM-005": "test_portfolio_materialization_decision_05",
        "REQ-PRM-006": "test_portfolio_materialization_decision_06",
    },
}


def _finding_code(field: str) -> str:
    mappings = {
        "typed_dependencies": "DEPENDENCY_GRAPH_INVALID",
        "priority": "PRIORITY_INVALID",
        "relative_size": "RELATIVE_SIZE_INVALID",
        "guarded_automation": "AUTOMATION_GUARD_INVALID",
        "staging_materialization": "STAGING_MATERIALIZATION_INVALID",
        "bounded_waves": "MATERIALIZATION_WAVES_INVALID",
        "field_sync": "FIELD_SYNC_INVALID",
        "drift_reconciliation": "DRIFT_RECONCILIATION_INVALID",
        "destructive_changes": "DESTRUCTIVE_CHANGE_INVALID",
        "resumable_operations": "RESUMABLE_OPERATION_INVALID",
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
