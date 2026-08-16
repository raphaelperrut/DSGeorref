from __future__ import annotations

from collections.abc import Iterable

from foundation_validation_types import Finding


DECISION_CLASSIFICATIONS = frozenset(
    {
        "NEW_ADR",
        "REFINE_EXISTING",
        "APPLICATION_PROFILE",
        "BENCHMARK_PROFILE",
        "ISSUE_DETAIL",
    }
)
LOCAL_CLASSIFICATIONS = DECISION_CLASSIFICATIONS - {"NEW_ADR"}


def validate_classification_before_identifier(
    classification: str | None, allocated_identifier: str | None
) -> list[Finding]:
    findings: list[Finding] = []
    if classification is None:
        findings.append(
            Finding(
                "CLASSIFICATION_REQUIRED",
                "classification",
                "classification is required before identifier allocation",
            )
        )
    elif classification not in DECISION_CLASSIFICATIONS:
        findings.append(
            Finding(
                "CLASSIFICATION_INVALID",
                "classification",
                "classification is outside the closed normative set",
            )
        )
    if allocated_identifier is not None and findings:
        findings.append(
            Finding(
                "IDENTIFIER_ALLOCATED_EARLY",
                "allocated_identifier",
                "identifier exists without a valid prior classification",
            )
        )
    return sorted(findings)


def validate_new_adr_eligibility(
    declared_classification: str,
    normative_classification: str,
    *,
    boundary_independent: bool,
    durable_impact: bool,
    high_reversal_cost: bool,
) -> list[Finding]:
    findings = validate_classification_before_identifier(declared_classification, None)
    if normative_classification not in DECISION_CLASSIFICATIONS:
        findings.append(
            Finding(
                "NORMATIVE_CLASSIFICATION_INVALID",
                "normative_classification",
                "normative classification is outside the closed set",
            )
        )
        return sorted(findings)
    if declared_classification != normative_classification:
        code = (
            "ARTIFICIAL_ADR_PROMOTION"
            if declared_classification == "NEW_ADR"
            and normative_classification in LOCAL_CLASSIFICATIONS
            else "CLASSIFICATION_MISMATCH"
        )
        findings.append(
            Finding(
                code,
                "declared_classification",
                "declared classification differs from the accepted normative classification",
            )
        )
    eligibility = boundary_independent and durable_impact and high_reversal_cost
    if declared_classification == "NEW_ADR" and not eligibility:
        findings.append(
            Finding(
                "NEW_ADR_INELIGIBLE",
                "declared_classification",
                "NEW_ADR requires independent boundary, durable impact and high reversal cost",
            )
        )
    return sorted(findings)


def validate_adr_change_governance(
    *,
    overlapping_adr_ids: Iterable[str],
    superseded_adr_ids: Iterable[str],
    declared_normative_owner: str | None,
    expected_normative_owner: str,
    owner_approved: bool,
) -> list[Finding]:
    overlaps = tuple(sorted(overlapping_adr_ids))
    superseded = frozenset(superseded_adr_ids)
    findings: list[Finding] = []
    unresolved = [adr_id for adr_id in overlaps if adr_id not in superseded]
    if unresolved:
        findings.append(
            Finding(
                "ADR_OVERLAP_UNRESOLVED",
                "overlapping_adr_ids",
                f"overlap is not resolved by supersession: {', '.join(unresolved)}",
            )
        )
    if not declared_normative_owner or declared_normative_owner != expected_normative_owner:
        findings.append(
            Finding(
                "NORMATIVE_OWNER_INVALID",
                "declared_normative_owner",
                "declared owner does not match the accepted normative owner",
            )
        )
    if not owner_approved:
        findings.append(
            Finding(
                "OWNER_GATE_REQUIRED",
                "owner_approved",
                "new or changed ADR requires the Owner decision gate",
            )
        )
    return sorted(findings)
