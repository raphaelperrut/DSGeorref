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
    def __init__(self, findings: list[Finding]) -> None:
        self.findings = tuple(sorted(findings))
        message = "; ".join(
            f"{finding.code} at {finding.field}: {finding.detail}"
            for finding in self.findings
        )
        super().__init__(message)


class _DuplicateKeyError(ValueError):
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(key)


EXPECTED_POLICY: dict[str, Any] = {
    "schema_version": "1.0.0",
    "policy_id": "ENGINEERING-BACKLOG-PROJECT-GOVERNANCE",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "controls": {
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
    },
    "requirement_evidence": {
        "REQ-PRJ-001": "test_issue_type_forms",
        "REQ-PRJ-002": "test_mandatory_core_type_fields",
        "REQ-PRJ-003": "test_single_parent_limited_hierarchy",
        "REQ-PRJ-005": "test_definition_of_ready_gate",
        "REQ-PRJ-006": "test_evidence_based_definition_of_done",
        "REQ-PRJ-007": "test_typed_dependency_cycle_detection",
        "REQ-PRJ-008": "test_derived_priority_dimensions",
        "REQ-PRJ-009": "test_relative_size_uncertainty_split",
        "REQ-PRJ-010": "test_guarded_project_automation",
        "REQ-PRM-001": "test_portfolio_materialization_decision_01",
    },
}


_CONTROL_CODES = {
    "issue_types": "ISSUE_TYPES_INVALID",
    "mandatory_fields": "MANDATORY_FIELDS_INVALID",
    "hierarchy": "HIERARCHY_INVALID",
    "ready_gate": "READY_GATE_INVALID",
    "done_gate": "DONE_GATE_INVALID",
    "typed_dependencies": "DEPENDENCY_GRAPH_INVALID",
    "priority": "PRIORITY_INVALID",
    "relative_size": "RELATIVE_SIZE_INVALID",
    "guarded_automation": "AUTOMATION_GUARD_INVALID",
    "staging_materialization": "STAGING_MATERIALIZATION_INVALID",
}


def _finding_code(field: str) -> str:
    for control, code in _CONTROL_CODES.items():
        if field.startswith(f"$.controls.{control}"):
            return code
    if field.startswith("$.requirement_evidence"):
        return "REQUIREMENT_EVIDENCE_INVALID"
    return "POLICY_STRUCTURE_INVALID"


def _compare(actual: object, expected: object, field: str) -> list[Finding]:
    if not isinstance(expected, dict):
        if type(actual) is type(expected) and actual == expected:
            return []
        return [Finding(_finding_code(field), field, f"expected {expected!r}")]
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


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(key)
        result[key] = value
    return result


def validate_policy(policy: object) -> list[Finding]:
    return sorted(_compare(policy, EXPECTED_POLICY, "$"))


def require_valid(policy: object) -> None:
    findings = validate_policy(policy)
    if findings:
        raise PolicyValidationError(findings)


def load_policy(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object
        )
    except _DuplicateKeyError as error:
        raise PolicyValidationError(
            [Finding("POLICY_DUPLICATE_KEY", f"$.{error.key}", "duplicate key")]
        ) from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PolicyValidationError(
            [Finding("POLICY_UNREADABLE", "$", str(error))]
        ) from error
    require_valid(loaded)
    return loaded
