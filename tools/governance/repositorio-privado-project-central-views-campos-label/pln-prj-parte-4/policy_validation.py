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
    "policy_id": "ENGINEERING-FOUNDATION-PLANNING-PROJECT",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "controls": {
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
        "issue_types": {
            "taxonomy": "VERSIONED_CANONICAL",
            "form_per_registered_type": "REQUIRED",
            "unknown_type": "REJECT",
        },
        "mandatory_fields": {
            "core": "REQUIRED",
            "per_type_extensions": "REQUIRED",
            "missing_applicable_field": "REJECT",
        },
        "hierarchy": {
            "primary_parent": "EXACTLY_ONE",
            "operational_hierarchy": "LIMITED",
            "multiple_primary_parents": "REJECT",
        },
        "ready_gate": {
            "definition": "docs/00-governance/DEFINITION_OF_READY.md",
            "applicability": "PROPORTIONAL",
            "unsatisfied": "REJECT",
        },
        "done_gate": {
            "definition": "docs/00-governance/DEFINITION_OF_DONE.md",
            "evidence": "REQUIRED",
            "applicable_checks": "REQUIRED",
            "unsatisfied": "REJECT",
        },
    },
    "requirement_evidence": {
        "REQ-PLN-005": "test_wip_class_limits_global_cap_and_emergency_reserve",
        "REQ-PLN-006": (
            "test_capacity_ranges_availability_throughput_and_no_deadline_conversion"
        ),
        "REQ-PLN-007": (
            "test_pull_iteration_objective_and_carryover_reason_classification"
        ),
        "REQ-PLN-008": (
            "test_accountable_owner_collaborator_reviewer_and_gate_approver"
        ),
        "REQ-PLN-010": (
            "test_versioned_reforecast_snapshot_variance_classification_and_delta_report"
        ),
        "REQ-PRJ-001": "test_issue_type_forms",
        "REQ-PRJ-002": "test_mandatory_core_type_fields",
        "REQ-PRJ-003": "test_single_parent_limited_hierarchy",
        "REQ-PRJ-005": "test_definition_of_ready_gate",
        "REQ-PRJ-006": "test_evidence_based_definition_of_done",
    },
}


def _finding_code(field: str) -> str:
    mappings = {
        "wip_limits": "WIP_LIMITS_INVALID",
        "capacity": "CAPACITY_INVALID",
        "pull_flow": "PULL_FLOW_INVALID",
        "roles": "ROLE_SEPARATION_INVALID",
        "reforecast": "REFORECAST_INVALID",
        "issue_types": "ISSUE_TYPES_INVALID",
        "mandatory_fields": "MANDATORY_FIELDS_INVALID",
        "hierarchy": "HIERARCHY_INVALID",
        "ready_gate": "READY_GATE_INVALID",
        "done_gate": "DONE_GATE_INVALID",
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
