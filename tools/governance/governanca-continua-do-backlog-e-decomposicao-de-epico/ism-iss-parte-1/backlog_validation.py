from __future__ import annotations

import re
from collections.abc import Mapping, Sequence

from policy_validation import Finding, strict_fields

STABLE_ID = re.compile(r"^(?:EPIC|STORY|ISSUE)-[0-9]{4}$")
REFERENCE_ID = re.compile(r"^(?:ADR|REQ|RISK|GATE)-[A-Z0-9][A-Z0-9._-]*$")


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _reference_findings(value: object, field: str, known_sources: set[str]) -> list[Finding]:
    if not isinstance(value, Mapping):
        return [Finding("ISSUE_TRACEABILITY_INVALID", field, "expected object")]
    expected = {"adrs", "requirements", "risks", "gates"}
    if set(value) != expected:
        return [
            Finding(
                "ISSUE_TRACEABILITY_INVALID",
                field,
                "ADR, requirement, risk and gate reference lists are required",
            )
        ]
    findings: list[Finding] = []
    for kind, references in value.items():
        if not isinstance(references, list) or any(
            not isinstance(reference, str)
            or REFERENCE_ID.fullmatch(reference) is None
            or reference not in known_sources
            for reference in references
        ):
            findings.append(
                Finding(
                    "ISSUE_TRACEABILITY_INVALID",
                    f"{field}.{kind}",
                    "references must use canonical identifiers",
                )
            )
    return findings


def validate_work_item(
    item: object, canonical_domains: set[str], known_sources: set[str]
) -> list[Finding]:
    expected = {
        "stable_id",
        "title",
        "github_number",
        "primary_domain",
        "affected_domains",
        "references",
        "local_decision",
    }
    record, findings = strict_fields(item, expected, "$", "WORK_ITEM_INVALID")
    if record is None:
        return findings
    stable_id = record.get("stable_id")
    if not isinstance(stable_id, str) or STABLE_ID.fullmatch(stable_id) is None:
        findings.append(Finding("STABLE_ID_INVALID", "$.stable_id", "invalid stable id"))
    github_number = record.get("github_number")
    if not _text(record.get("title")) or type(github_number) is not int or github_number < 1:
        findings.append(Finding("WORK_ITEM_INVALID", "$", "title/number are invalid"))
    primary = record.get("primary_domain")
    affected = record.get("affected_domains")
    if not isinstance(primary, str) or primary not in canonical_domains:
        findings.append(Finding("DOMAIN_UNKNOWN", "$.primary_domain", "unknown domain"))
    if not isinstance(affected, list) or any(
        not isinstance(domain, str) or domain not in canonical_domains for domain in affected
    ):
        findings.append(Finding("DOMAIN_UNKNOWN", "$.affected_domains", "unknown domain"))
    elif len(set(affected)) != len(affected) or primary in affected:
        findings.append(
            Finding(
                "DOMAIN_TAXONOMY_INVALID",
                "$.affected_domains",
                "affected domains must be unique and exclude the primary domain",
            )
        )
    findings.extend(_reference_findings(record.get("references"), "$.references", known_sources))
    references = record.get("references")
    has_reference = isinstance(references, Mapping) and any(references.values())
    decision = record.get("local_decision")
    valid_decision = (
        isinstance(decision, Mapping)
        and set(decision) == {"justification", "reversible"}
        and _text(decision.get("justification"))
        and decision.get("reversible") is True
    )
    if decision is not None and not valid_decision:
        findings.append(
            Finding("LOCAL_DECISION_INVALID", "$.local_decision", "reversible reason required")
        )
    if not has_reference and not valid_decision:
        findings.append(Finding("ORPHAN_ISSUE", "$", "reference or reversible decision required"))
    return sorted(set(findings))


def validate_issue_set(
    items: Sequence[object], canonical_domains: set[str], known_sources: set[str]
) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[str] = set()
    for position, item in enumerate(items):
        findings.extend(validate_work_item(item, canonical_domains, known_sources))
        if not isinstance(item, Mapping):
            continue
        stable_id = item.get("stable_id")
        if isinstance(stable_id, str):
            if stable_id in seen:
                findings.append(
                    Finding("DUPLICATE_ISSUE", f"$[{position}].stable_id", "duplicate stable ID")
                )
            seen.add(stable_id)
    return sorted(set(findings))


def validate_identity_update(before: object, after: object) -> list[Finding]:
    if not isinstance(before, Mapping) or not isinstance(after, Mapping):
        return [Finding("STABLE_ID_INVALID", "$", "expected objects")]
    before_id = before.get("stable_id")
    after_id = after.get("stable_id")
    if (
        not isinstance(before_id, str)
        or STABLE_ID.fullmatch(before_id) is None
        or not isinstance(after_id, str)
        or STABLE_ID.fullmatch(after_id) is None
    ):
        return [Finding("STABLE_ID_INVALID", "$.stable_id", "invalid stable ID")]
    if before_id != after_id:
        return [
            Finding(
                "STABLE_ID_CHANGED",
                "$.stable_id",
                "GitHub number/title changes cannot replace repository identity",
            )
        ]
    return []


def _acceptance_findings(
    value: object, known_sources: set[str], known_evidence: set[str]
) -> list[Finding]:
    if not isinstance(value, list) or not value:
        return [Finding("ACCEPTANCE_EVIDENCE_INVALID", "$.acceptance_evidence", "required")]
    findings: list[Finding] = []
    for position, entry in enumerate(value):
        field = f"$.acceptance_evidence[{position}]"
        record, row_findings = strict_fields(
            entry, {"criterion", "sources", "evidence"}, field, "ACCEPTANCE_EVIDENCE_INVALID"
        )
        findings.extend(row_findings)
        if record is None:
            continue
        sources = record.get("sources")
        if (
            not _text(record.get("criterion"))
            or not isinstance(record.get("evidence"), str)
            or record["evidence"] not in known_evidence
        ):
            findings.append(
                Finding("ACCEPTANCE_EVIDENCE_INVALID", field, "unverified criterion/evidence")
            )
        if (
            not isinstance(sources, list)
            or not sources
            or any(
                not isinstance(source, str)
                or REFERENCE_ID.fullmatch(source) is None
                or source not in known_sources
                for source in sources
            )
        ):
            findings.append(
                Finding("ACCEPTANCE_EVIDENCE_INVALID", f"{field}.sources", "invalid source")
            )
    return findings


def validate_epic(epic: object, known_sources: set[str], known_evidence: set[str]) -> list[Finding]:
    expected = {"outcome", "closure_evidence", "epic_issue", "slices", "acceptance_evidence"}
    record, findings = strict_fields(epic, expected, "$", "EPIC_INVALID")
    if record is None:
        return findings
    if not _text(record.get("outcome")):
        findings.append(Finding("EPIC_OUTCOME_MISSING", "$.outcome", "required"))
    evidence = record.get("closure_evidence")
    if (
        not isinstance(evidence, list)
        or not evidence
        or any(not isinstance(item, str) or item not in known_evidence for item in evidence)
    ):
        findings.append(Finding("EPIC_CLOSURE_EVIDENCE_MISSING", "$.closure_evidence", "required"))
    epic_issue = record.get("epic_issue")
    if (
        not isinstance(epic_issue, str)
        or not epic_issue.startswith("ISSUE-")
        or STABLE_ID.fullmatch(epic_issue) is None
    ):
        findings.append(Finding("EPIC_ISSUE_MISSING", "$.epic_issue", "required"))
    slices = record.get("slices")
    if not isinstance(slices, list) or not slices:
        findings.append(Finding("SLICE_SKELETON_MISSING", "$.slices", "required"))
    else:
        findings.extend(_slice_findings(slices, known_sources))
    findings.extend(
        _acceptance_findings(record.get("acceptance_evidence"), known_sources, known_evidence)
    )
    return sorted(set(findings))


def _slice_findings(slices: Sequence[object], known_sources: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    observed_ids: set[str] = set()
    observed_sequence: list[int] = []
    for position, item in enumerate(slices):
        field = f"$.slices[{position}]"
        row, row_findings = strict_fields(
            item,
            {"stable_id", "requirement_ids", "write_scope", "integration_sequence"},
            field,
            "SLICE_INVALID",
        )
        findings.extend(row_findings)
        if row is None:
            continue
        stable_id = row.get("stable_id")
        requirements = row.get("requirement_ids")
        sequence = row.get("integration_sequence")
        if (
            not isinstance(stable_id, str)
            or not stable_id.startswith("STORY-")
            or STABLE_ID.fullmatch(stable_id) is None
            or stable_id in observed_ids
        ):
            findings.append(Finding("SLICE_INVALID", f"{field}.stable_id", "invalid or duplicate"))
        else:
            observed_ids.add(stable_id)
        if (
            not isinstance(requirements, list)
            or not 1 <= len(requirements) <= 10
            or any(
                not isinstance(requirement, str)
                or not requirement.startswith("REQ-")
                or requirement not in known_sources
                for requirement in requirements
            )
            or len(set(requirements)) != len(requirements)
        ):
            findings.append(
                Finding("SLICE_TOO_LARGE", f"{field}.requirement_ids", "expected 1..10")
            )
        if not _text(row.get("write_scope")):
            findings.append(Finding("SLICE_INVALID", f"{field}.write_scope", "required"))
        if type(sequence) is not int:
            findings.append(
                Finding(
                    "SLICE_SEQUENCE_INVALID", f"{field}.integration_sequence", "integer required"
                )
            )
        else:
            observed_sequence.append(sequence)
    if observed_sequence != list(range(1, len(slices) + 1)):
        findings.append(
            Finding("SLICE_SEQUENCE_INVALID", "$.slices", "sequence must be contiguous")
        )
    return findings


def validate_spike(spike: object) -> list[Finding]:
    record, findings = strict_fields(
        spike,
        {"question", "budget", "evidence", "exit_decision"},
        "$",
        "SPIKE_INVALID",
    )
    if record is None:
        return findings
    for field in ("question", "budget", "evidence", "exit_decision"):
        if not _text(record.get(field)):
            findings.append(Finding("SPIKE_INVALID", f"$.{field}", "required"))
    return sorted(set(findings))
