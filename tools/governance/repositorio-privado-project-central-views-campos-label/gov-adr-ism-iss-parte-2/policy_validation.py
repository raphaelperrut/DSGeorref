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
    "policy_id": "ENGINEERING-FOUNDATION-ISM-ISS-NATIVE",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "controls": {
        "adr_governance": {
            "local_kinds": ["REFINEMENT", "PROFILE", "BENCHMARK", "LOCAL_DETAIL"],
            "local_promotion": "REJECT",
            "overlap_check": "REQUIRED",
            "normative_owner": "REQUIRED",
            "owner_decision_gate": "REQUIRED",
            "eligibility_validator": (
                "decision_governance.validate_new_adr_eligibility"
            ),
            "change_validator": (
                "decision_governance.validate_adr_change_governance"
            ),
        },
        "domain_taxonomy": {
            "source": "CANONICAL_REGISTRY",
            "primary_domain_count": 1,
            "affected_domains": "ZERO_OR_MORE_UNIQUE",
            "primary_in_affected": "REJECT",
            "unknown_domain": "REJECT",
        },
        "issue_sync": {
            "default_mode": "DRY_RUN",
            "dry_run_writes": "PROHIBITED",
            "managed_field_registry": "REQUIRED",
            "unmanaged_field_mutation": "REJECT",
            "repeat_convergence": "NO_CHANGES",
        },
        "cross_domain_work": {
            "issue_identity": "SINGLE",
            "primary_domain_count": 1,
            "affected_domains": "REQUIRED_WHEN_CROSS_DOMAIN",
            "duplicate_issue": "REJECT",
        },
        "portfolio": {
            "epic_issue": "REQUIRED",
            "implementable_slice_skeleton": "REQUIRED",
            "traceability": "REQUIRED",
            "complete_skeleton": "REQUIRED",
            "future_detailing": "PROGRESSIVE",
        },
        "research_spike": {
            "budget": "REQUIRED",
            "verifiable_question": "REQUIRED",
            "decision_output": "REQUIRED",
            "objective_exit_criterion": "REQUIRED",
        },
        "geometry_boundary": {
            "domain_library": "SHAPELY",
            "io_adapters": "EXPLICIT",
            "domain_parsing": "PROHIBITED",
            "domain_serialization": "PROHIBITED",
        },
    },
    "requirement_evidence": {
        "REQ-GOV-ADR-003": "test_adr_governance_overlap",
        "REQ-GOV-ADR-018": "test_adr_governance_overlap",
        "REQ-ISM-001": (
            "test_canonical_domain_taxonomy_primary_and_affected_domains"
        ),
        "REQ-ISM-006": "test_req_ism_006",
        "REQ-ISM-008": "test_single_primary_cross_domain_issue_contracts",
        "REQ-ISS-001": (
            "test_all_work_packages_have_parent_issue_and_slice_skeleton"
        ),
        "REQ-ISS-004": (
            "test_complete_portfolio_skeleton_and_progressive_detailing_rules"
        ),
        "REQ-ISS-006": "test_idempotent_dry_run_managed_field_issue_sync",
        "REQ-ISS-009": "test_bounded_research_spike_exit_decision",
        "REQ-NATIVE-003": "test_req_native_003",
    },
}


def _finding_code(field: str) -> str:
    if field.startswith("$.controls.adr_governance"):
        return "ADR_GOVERNANCE_INVALID"
    if field.startswith("$.controls.domain_taxonomy"):
        return "DOMAIN_TAXONOMY_INVALID"
    if field.startswith("$.controls.issue_sync"):
        return "ISSUE_SYNC_INVALID"
    if field.startswith("$.controls.cross_domain_work"):
        return "CROSS_DOMAIN_WORK_INVALID"
    if field.startswith("$.controls.portfolio"):
        return "PORTFOLIO_INVALID"
    if field.startswith("$.controls.research_spike"):
        return "RESEARCH_SPIKE_INVALID"
    if field.startswith("$.controls.geometry_boundary"):
        return "GEOMETRY_BOUNDARY_INVALID"
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
            findings.append(
                Finding(_finding_code(f"{field}.{key}"), f"{field}.{key}", "missing field")
            )
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
