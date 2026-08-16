from __future__ import annotations

import csv
import re
from collections.abc import Iterable
from io import StringIO
from pathlib import Path, PurePosixPath

from foundation_validation_types import Finding
from governed_artifacts import git_blob, revision_is_ancestor


DECISION_CLASSIFICATIONS = frozenset(
    {"NEW_ADR", "REFINE_EXISTING", "APPLICATION_PROFILE", "BENCHMARK_PROFILE", "ISSUE_DETAIL"}
)
LOCAL_CLASSIFICATIONS = DECISION_CLASSIFICATIONS - {"NEW_ADR"}
ADR_INDEX_PATH = "docs/00-governance/ADR_INDEX.csv"
ADR_DIRECTORY = PurePosixPath("docs/02-architecture/adrs")
APPLICATION_PROFILE_DIRECTORY = PurePosixPath("docs/03-engineering/application-profiles")
BENCHMARK_PROFILE_DIRECTORY = PurePosixPath("docs/03-engineering/benchmark-profiles")
ISSUE_DIRECTORY = PurePosixPath("docs/06-delivery/issues")
ADR_ID_PATTERN = re.compile(r"^ADR-[0-9]{3}$")
REQUIREMENT_ID_PATTERN = re.compile(r"\bREQ-[A-Z0-9-]+\b")


def _try_blob(repository_root: Path, revision: str, path: str) -> bytes | None:
    try:
        return git_blob(repository_root, revision, path)
    except ValueError:
        return None


def _is_under(path: PurePosixPath, directory: PurePosixPath) -> bool:
    return path != directory and directory in path.parents


def derive_normative_classification(
    repository_root: Path,
    *,
    base_revision: str,
    candidate_revision: str,
    proposal_path: str,
) -> str:
    if not revision_is_ancestor(repository_root, base_revision, candidate_revision):
        raise ValueError("candidate does not preserve the classification base")
    path = PurePosixPath(proposal_path)
    if path.is_absolute() or ".." in path.parts or "\\" in proposal_path:
        raise ValueError("proposal path is not repository-relative")
    if _try_blob(repository_root, candidate_revision, proposal_path) is None:
        raise ValueError("proposal does not exist in governed candidate revision")
    if _is_under(path, ADR_DIRECTORY):
        return (
            "REFINE_EXISTING"
            if _try_blob(repository_root, base_revision, proposal_path) is not None
            else "NEW_ADR"
        )
    if _is_under(path, APPLICATION_PROFILE_DIRECTORY):
        return "APPLICATION_PROFILE"
    if _is_under(path, BENCHMARK_PROFILE_DIRECTORY):
        return "BENCHMARK_PROFILE"
    if _is_under(path, ISSUE_DIRECTORY):
        return "ISSUE_DETAIL"
    raise ValueError("proposal path has no authoritative classification rule")


def _identifier_from_path(proposal_path: str) -> str | None:
    prefix = PurePosixPath(proposal_path).name.split("-", 2)
    if len(prefix) >= 2 and prefix[0] == "ADR" and prefix[1].isdigit():
        candidate = f"ADR-{prefix[1]}"
        return candidate if ADR_ID_PATTERN.fullmatch(candidate) else None
    return None


def validate_classification_before_identifier(
    repository_root: Path,
    *,
    base_revision: str,
    candidate_revision: str,
    proposal_path: str,
    declared_classification: str | None,
    allocated_identifier: str | None,
) -> list[Finding]:
    findings: list[Finding] = []
    try:
        authoritative = derive_normative_classification(
            repository_root,
            base_revision=base_revision,
            candidate_revision=candidate_revision,
            proposal_path=proposal_path,
        )
    except ValueError as error:
        return [Finding("CLASSIFICATION_AUTHORITY_INVALID", proposal_path, str(error))]
    if declared_classification not in DECISION_CLASSIFICATIONS:
        findings.append(Finding("CLASSIFICATION_INVALID", "declared_classification", "classification is outside the closed set"))
    elif declared_classification != authoritative:
        findings.append(Finding("CLASSIFICATION_MISMATCH", "declared_classification", "claim differs from repository-derived classification"))
    path_identifier = _identifier_from_path(proposal_path)
    if allocated_identifier != path_identifier:
        findings.append(Finding("IDENTIFIER_MISMATCH", "allocated_identifier", "identifier differs from governed artifact identity"))
    if authoritative == "NEW_ADR" and path_identifier is not None:
        findings.append(
            Finding(
                "IDENTIFIER_ALLOCATED_EARLY",
                "allocated_identifier",
                "no governed pre-allocation classification record exists in the base revision",
            )
        )
    return sorted(findings)


def _adr_index(repository_root: Path, revision: str) -> dict[str, dict[str, str]]:
    try:
        text = git_blob(repository_root, revision, ADR_INDEX_PATH).decode("utf-8")
    except (UnicodeDecodeError, ValueError) as error:
        raise ValueError(f"ADR index is unavailable or invalid: {error}") from error
    rows: dict[str, dict[str, str]] = {}
    for row in csv.DictReader(StringIO(text)):
        adr_id = row.get("adr_id")
        if not isinstance(adr_id, str) or not ADR_ID_PATTERN.fullmatch(adr_id) or adr_id in rows:
            raise ValueError("ADR index contains invalid or duplicate identity")
        rows[adr_id] = row
    return rows


def _adr_text(repository_root: Path, revision: str, proposal_path: str) -> str:
    try:
        return git_blob(repository_root, revision, proposal_path).decode("utf-8")
    except (UnicodeDecodeError, ValueError) as error:
        raise ValueError(f"ADR proposal is unavailable or invalid: {error}") from error


def _metadata_value(text: str, label: str) -> str | None:
    pattern = rf"^- \*\*{re.escape(label)}:\*\* `?([^`\r\n]+)`?\s*$"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else None


def validate_new_adr_eligibility(
    repository_root: Path,
    *,
    base_revision: str,
    candidate_revision: str,
    proposal_path: str,
    declared_classification: str,
) -> list[Finding]:
    findings = validate_classification_before_identifier(
        repository_root,
        base_revision=base_revision,
        candidate_revision=candidate_revision,
        proposal_path=proposal_path,
        declared_classification=declared_classification,
        allocated_identifier=_identifier_from_path(proposal_path),
    )
    try:
        authoritative = derive_normative_classification(
            repository_root,
            base_revision=base_revision,
            candidate_revision=candidate_revision,
            proposal_path=proposal_path,
        )
        if authoritative != "NEW_ADR":
            if declared_classification == "NEW_ADR":
                findings.append(Finding("ARTIFICIAL_ADR_PROMOTION", "declared_classification", "governed path/history classifies proposal as local"))
            return sorted(set(findings))
        adr_id = _identifier_from_path(proposal_path)
        row = _adr_index(repository_root, candidate_revision).get(str(adr_id))
        text = _adr_text(repository_root, candidate_revision, proposal_path)
    except ValueError as error:
        findings.append(Finding("ADR_AUTHORITY_INVALID", proposal_path, str(error)))
        return sorted(set(findings))
    eligible = (
        row is not None
        and row.get("file") == PurePosixPath(proposal_path).name
        and row.get("independent_boundary") == "true"
        and _metadata_value(text, "Boundary independente") == "SIM"
        and "alto impacto e alto custo de reversão" in text
        and _metadata_value(text, "Status") == "Accepted"
    )
    if not eligible:
        findings.append(
            Finding(
                "NEW_ADR_INELIGIBLE",
                proposal_path,
                "ADR index/document do not establish independent, durable, high-reversal-cost eligibility",
            )
        )
    return sorted(set(findings))


def _explicit_superseded_ids(text: str) -> frozenset[str]:
    value = _metadata_value(text, "Substitui") or _metadata_value(text, "Supersedes")
    if value is None or value == "Nenhuma":
        return frozenset()
    return frozenset(item.strip() for item in value.split(",") if item.strip())


def _section_bullets(text: str, heading: str) -> frozenset[str]:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        return frozenset()
    return frozenset(
        re.sub(r"\s+", " ", line[2:].strip()).casefold()
        for line in match.group("body").splitlines()
        if line.startswith("- ") and line[2:].strip()
    )


def _owned_requirements(text: str) -> frozenset[str]:
    match = re.search(r"^- \*\*Requisitos owned:\*\* (?P<value>.+)$", text, re.MULTILINE)
    return (
        frozenset(REQUIREMENT_ID_PATTERN.findall(match.group("value")))
        if match is not None
        else frozenset()
    )


def _derived_overlapping_adr_ids(
    repository_root: Path,
    revision: str,
    proposal_path: str,
    index: dict[str, dict[str, str]],
    candidate_text: str,
    base_text: bytes | None,
) -> frozenset[str]:
    if base_text is not None and base_text == candidate_text.encode("utf-8"):
        return frozenset()
    proposal_id = _identifier_from_path(proposal_path)
    decisions = _section_bullets(candidate_text, "Decisão")
    requirements = _owned_requirements(candidate_text)
    overlaps = set(_explicit_superseded_ids(candidate_text))
    for adr_id, row in index.items():
        if adr_id == proposal_id:
            continue
        path = str(ADR_DIRECTORY / str(row.get("file", "")))
        try:
            other_text = _adr_text(repository_root, revision, path)
        except ValueError:
            continue
        same_decision = bool(decisions & _section_bullets(other_text, "Decisão"))
        same_requirement = bool(requirements & _owned_requirements(other_text))
        if same_decision or same_requirement:
            overlaps.add(adr_id)
    return frozenset(overlaps)


def validate_adr_change_governance(
    repository_root: Path,
    *,
    base_revision: str,
    candidate_revision: str,
    proposal_path: str,
    overlapping_adr_ids: Iterable[str],
    superseded_adr_ids: Iterable[str],
    declared_normative_owner: str | None,
) -> list[Finding]:
    findings: list[Finding] = []
    try:
        index = _adr_index(repository_root, candidate_revision)
        candidate_text = _adr_text(repository_root, candidate_revision, proposal_path)
        base_text = _try_blob(repository_root, base_revision, proposal_path)
        owner_text = base_text.decode("utf-8") if base_text is not None else candidate_text
    except (UnicodeDecodeError, ValueError) as error:
        return [Finding("ADR_AUTHORITY_INVALID", proposal_path, str(error))]
    overlaps = tuple(overlapping_adr_ids)
    superseded = tuple(superseded_adr_ids)
    if len(overlaps) != len(set(overlaps)) or len(superseded) != len(set(superseded)):
        findings.append(Finding("ADR_REFERENCE_DUPLICATE", "overlap/supersession", "ADR references must be unique"))
    unknown = sorted((set(overlaps) | set(superseded)) - set(index))
    if unknown:
        findings.append(Finding("ADR_REFERENCE_UNKNOWN", "overlap/supersession", ", ".join(unknown)))
    explicit = _explicit_superseded_ids(candidate_text)
    if frozenset(superseded) != explicit:
        findings.append(Finding("SUPERSESSION_CLAIM_MISMATCH", "superseded_adr_ids", "claim differs from governed ADR metadata"))
    derived_overlaps = _derived_overlapping_adr_ids(
        repository_root,
        candidate_revision,
        proposal_path,
        index,
        candidate_text,
        base_text,
    )
    unresolved = sorted((set(overlaps) | set(derived_overlaps)) - explicit)
    if unresolved:
        findings.append(Finding("ADR_OVERLAP_UNRESOLVED", "overlapping_adr_ids", ", ".join(unresolved)))
    expected_owner = _metadata_value(owner_text, "Owner normativo")
    if expected_owner is None or declared_normative_owner != expected_owner:
        findings.append(Finding("NORMATIVE_OWNER_INVALID", "declared_normative_owner", "claim differs from accepted owner"))
    owner_gate = (
        base_text is not None
        and _metadata_value(owner_text, "Aprovador") == "Project Owner"
        and _metadata_value(owner_text, "Status") == "Accepted"
    )
    if not owner_gate:
        findings.append(
            Finding(
                "OWNER_GATE_REQUIRED",
                proposal_path,
                "base authority lacks an accepted Project Owner gate",
            )
        )
    return sorted(set(findings))
