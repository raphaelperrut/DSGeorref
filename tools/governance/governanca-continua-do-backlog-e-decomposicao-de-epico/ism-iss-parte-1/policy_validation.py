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
                f"{finding.code} at {finding.field}: {finding.detail}" for finding in self.findings
            )
        )


def strict_fields(
    value: object, expected: set[str], field: str, code: str
) -> tuple[Mapping[str, Any] | None, list[Finding]]:
    if not isinstance(value, Mapping):
        return None, [Finding(code, field, "expected object")]
    actual = set(value)
    findings = [
        Finding(code, f"{field}.{name}", "missing field") for name in sorted(expected - actual)
    ]
    findings.extend(
        Finding(code, f"{field}.{name}", "unknown field") for name in sorted(actual - expected)
    )
    return value, findings


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


EXPECTED_POLICY: dict[str, Any] = {
    "schema_version": "1.0.0",
    "policy_id": "BACKLOG-GOVERNANCE-FOUNDATION",
    "owner": "BC-001",
    "contract_binding": {
        "source": (
            "contracts/contexts/engineering_governance/fnd/"
            "governanca-continua-do-backlog-e-decomposicao-de-epico/"
            "contract-manifest.yaml"
        ),
        "contract_version": "1.0.0",
        "status": "FROZEN",
    },
    "controls": {
        "domain_taxonomy": {
            "source": "CANONICAL_REGISTRY",
            "primary_domain_count": 1,
            "affected_domains": "ZERO_OR_MORE_UNIQUE",
            "primary_in_affected": "REJECT",
            "unknown_domain": "REJECT",
        },
        "epic_outcome": {
            "outcome": "REQUIRED",
            "verification_evidence": "REQUIRED",
            "closure": "EVIDENCE_ONLY",
        },
        "vertical_slices": {
            "maximum_requirements": 10,
            "result": "VERIFIABLE",
            "write_scope": "PRIMARY_REQUIRED",
            "integration": "SEQUENCED",
        },
        "stable_identity": {
            "source": "VERSIONED_REPOSITORY",
            "github_number": "NON_AUTHORITATIVE",
            "github_title": "NON_AUTHORITATIVE",
            "identity_change": "REJECT",
        },
        "acceptance_evidence": {
            "accepted_sources": ["ADR", "REQUIREMENT", "RISK", "GATE"],
            "explicit_mapping": "REQUIRED",
            "unresolved_source": "REJECT",
        },
        "cross_domain_work": {
            "issue_identity": "SINGLE",
            "primary_domain_count": 1,
            "affected_domains": "REQUIRED_WHEN_CROSS_DOMAIN",
            "duplicate_issue": "REJECT",
        },
        "research_spike": {
            "question": "REQUIRED",
            "budget": "REQUIRED",
            "evidence": "REQUIRED",
            "exit_decision": "REQUIRED",
        },
        "baseline_history": {
            "snapshots": "IMMUTABLE",
            "removal_tombstone": "REQUIRED",
            "delta": "EXACT",
            "delta_approval": "REQUIRED",
            "history_rewrite": "REJECT",
        },
        "work_packages": {
            "epic_issue": "REQUIRED",
            "implementable_slice_skeleton": "REQUIRED",
            "traceability": "REQUIRED",
        },
        "issue_traceability": {
            "accepted_references": ["ADR", "REQUIREMENT", "RISK", "GATE"],
            "local_decision": "REVERSIBLE_JUSTIFICATION",
            "orphan_issue": "REJECT",
        },
    },
    "requirement_evidence": {
        "REQ-ISM-001": "test_canonical_domain_taxonomy_primary_and_affected_domains",
        "REQ-ISM-002": "test_work_package_epics_outcome_evidence_and_closure",
        "REQ-ISM-003": "test_thin_vertical_integrable_slices_and_pr_sequence",
        "REQ-ISM-005": "test_stable_portfolio_ids_independent_github_numbers_titles",
        "REQ-ISM-007": "test_req_ism_007",
        "REQ-ISM-008": "test_single_primary_cross_domain_issue_contracts",
        "REQ-ISM-009": "test_req_ism_009",
        "REQ-ISM-010": "test_portfolio_snapshot_tombstone_approved_delta",
        "REQ-ISS-001": "test_all_work_packages_have_parent_issue_and_slice_skeleton",
        "REQ-ISS-003": ("test_no_orphan_issue_without_adr_or_local_decision_justification"),
    },
}


def _finding_code(field: str) -> str:
    if field.startswith("$.controls."):
        control = field.split(".")[2].upper()
        return f"{control}_INVALID"
    if field.startswith("$.requirement_evidence"):
        return "REQUIREMENT_EVIDENCE_INVALID"
    if field.startswith("$.contract_binding"):
        return "CONTRACT_BINDING_INVALID"
    return "POLICY_STRUCTURE_INVALID"


def _compare(actual: object, expected: object, field: str) -> list[Finding]:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [Finding(_finding_code(field), field, "expected object")]
        findings: list[Finding] = []
        for key in sorted(actual.keys() - expected.keys()):
            findings.append(Finding("POLICY_STRUCTURE_INVALID", f"{field}.{key}", "unknown field"))
        for key in sorted(expected.keys() - actual.keys()):
            path = f"{field}.{key}"
            findings.append(Finding(_finding_code(path), path, "missing field"))
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
        loaded = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, ValueError) as error:
        raise PolicyValidationError([Finding("POLICY_UNREADABLE", "$", str(error))]) from error
    require_valid(loaded)
    return cast(dict[str, Any], loaded)
