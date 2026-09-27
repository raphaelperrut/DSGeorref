from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


class PolicyValidationError(ValueError):
    def __init__(self, findings: list[Finding] | tuple[Finding, ...]) -> None:
        self.findings = tuple(sorted(findings))
        super().__init__(
            "; ".join(
                f"{finding.code} at {finding.field}: {finding.detail}"
                for finding in self.findings
            )
        )


EXPECTED_POLICY: dict[str, Any] = {
    "schema_version": "1.0.0",
    "policy_id": "BACKLOG-PLANNING-GOVERNANCE",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "controls": {
        "portfolio": {
            "complete_skeleton": "REQUIRED",
            "future_detailing": "PROGRESSIVE",
        },
        "roadmap": {
            "structure": ["HORIZON", "OUTCOME", "GATE"],
            "dates": "EXCEPTION_ONLY",
            "date_justification": "REAL_COMMITMENT_REQUIRED",
            "unjustified_date": "REJECT",
        },
        "milestones": {
            "outcome_gate": "SEPARATE_LAYER",
            "release": "SEPARATE_LAYER",
            "iteration": "SEPARATE_LAYER",
            "mapping": "EXPLICIT_REQUIRED",
        },
        "sequencing": {
            "order_by": [
                "BLOCKER",
                "GATE",
                "DEPENDENCY",
                "EXPLAINABLE_PRIORITY",
            ],
            "priority_override": "AUDIT_REQUIRED",
            "unaudited_override": "REJECT",
        },
        "critical_dependencies": {
            "classifications": [
                "ENABLER",
                "HIGH_FAN_OUT",
                "SINGLE_POINT_OF_FAILURE",
                "UNCERTAIN_DEPENDENCY",
            ],
            "uncertain_dependency": "RISK_BUFFER_REQUIRED",
            "unclassified_critical_dependency": "REJECT",
        },
        "wip_limits": {
            "scopes": ["CLASS", "GLOBAL"],
            "reservations": ["P0", "SECURITY", "MAINTENANCE"],
            "over_limit": "REJECT",
        },
        "capacity": {
            "estimate": "RANGE",
            "categories": ["AVAILABILITY", "THROUGHPUT"],
            "confidence": "REQUIRED",
            "automatic_deadline_conversion": "PROHIBITED",
            "invalid_range": "REJECT",
        },
        "pull_flow": {
            "system": "PULL",
            "iteration_objective": "REQUIRED",
            "carryover_reason": "CLASSIFICATION_REQUIRED",
            "unclassified_carryover": "REJECT",
        },
        "roles": {
            "accountable_owner": "EXACTLY_ONE",
            "collaborator": "SEPARATE",
            "reviewer": "SEPARATE",
            "gate_approver": "SEPARATE",
            "self_approval": "PROHIBITED",
        },
        "reforecast": {
            "snapshots": "VERSIONED_IMMUTABLE",
            "material_variance": "CLASSIFICATION_REQUIRED",
            "delta_report": "REQUIRED",
            "overwrite": "REJECT",
            "unclassified_material_variance": "REJECT",
        },
    },
    "requirement_evidence": {
        "REQ-ISS-004": "test_complete_portfolio_skeleton_and_progressive_detailing_rules",
        "REQ-PLN-001": "test_roadmap_horizons_outcomes_gates_and_date_exception",
        "REQ-PLN-002": "test_layered_milestones_gate_release_mapping",
        "REQ-PLN-003": "test_sequence_gates_dependencies_priority_override_audit",
        "REQ-PLN-004": "test_critical_enablers_uncertain_dependencies_and_risk_buffers",
        "REQ-PLN-005": "test_wip_class_limits_global_cap_and_emergency_reserve",
        "REQ-PLN-006": (
            "test_capacity_ranges_availability_throughput_and_no_deadline_conversion"
        ),
        "REQ-PLN-007": "test_pull_iteration_objective_and_carryover_reason_classification",
        "REQ-PLN-008": (
            "test_accountable_owner_collaborator_reviewer_and_gate_approver"
        ),
        "REQ-PLN-010": (
            "test_versioned_reforecast_snapshot_variance_classification_and_delta_report"
        ),
    },
}

CONTROL_CODES = {
    "portfolio": "PORTFOLIO_INVALID",
    "roadmap": "ROADMAP_INVALID",
    "milestones": "MILESTONES_INVALID",
    "sequencing": "SEQUENCING_INVALID",
    "critical_dependencies": "CRITICAL_DEPENDENCIES_INVALID",
    "wip_limits": "WIP_LIMITS_INVALID",
    "capacity": "CAPACITY_INVALID",
    "pull_flow": "PULL_FLOW_INVALID",
    "roles": "ROLE_SEPARATION_INVALID",
    "reforecast": "REFORECAST_INVALID",
}


def _finding_code(field: str) -> str:
    for control, code in CONTROL_CODES.items():
        if field.startswith(f"$.controls.{control}"):
            return code
    if field.startswith("$.requirement_evidence"):
        return "REQUIREMENT_EVIDENCE_INVALID"
    return "POLICY_STRUCTURE_INVALID"


def _compare(actual: object, expected: object, field: str) -> list[Finding]:
    if isinstance(expected, Mapping):
        if not isinstance(actual, Mapping):
            return [Finding(_finding_code(field), field, "expected object")]
        findings = [
            Finding("POLICY_STRUCTURE_INVALID", f"{field}.{key}", "unknown field")
            for key in sorted(actual.keys() - expected.keys())
        ]
        for key in sorted(expected.keys() - actual.keys()):
            target = f"{field}.{key}"
            findings.append(Finding(_finding_code(target), target, "missing field"))
        for key in sorted(actual.keys() & expected.keys()):
            findings.extend(_compare(actual[key], expected[key], f"{field}.{key}"))
        return findings
    if type(actual) is not type(expected) or actual != expected:
        return [Finding(_finding_code(field), field, f"expected {expected!r}")]
    return []


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    decoded: dict[str, Any] = {}
    for key, value in pairs:
        if key in decoded:
            raise ValueError(f"duplicate JSON key: {key}")
        decoded[key] = value
    return decoded


def _reject_non_finite(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def validate_policy(policy: object) -> list[Finding]:
    return sorted(_compare(policy, EXPECTED_POLICY, "$"))


def require_valid(policy: object) -> None:
    findings = validate_policy(policy)
    if findings:
        raise PolicyValidationError(findings)


def load_policy(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_non_finite,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise PolicyValidationError(
            [Finding("POLICY_UNREADABLE", "$", str(error))]
        ) from error
    require_valid(loaded)
    return cast(dict[str, Any], loaded)
