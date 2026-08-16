from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any

from canonical_json import CanonicalizationError, canonical_json_bytes, load_json_bytes
from contract_validation import schema_findings
from foundation_validation_types import Finding, require_valid
from governed_artifacts import COMMIT_PATTERN, git_blob
from lifecycle_evidence import (
    ADR_AUTHORITY_PATH,
    baseline_reference,
    normative_authority_findings,
    validate_closure,
    validate_evidence_set,
    validate_reopening,
)
from lifecycle_records import AppendOnlyRecordLedger


ZERO_DIGEST = "0" * 64


@dataclass(frozen=True, order=True)
class CoverageEntry:
    path: str
    content_sha256: str

    def as_dict(self) -> dict[str, str]:
        return {"path": self.path, "content_sha256": self.content_sha256}


def _validate_repository_path(path: object) -> str:
    if not isinstance(path, str) or not path:
        raise ValueError("coverage path must be a non-empty string")
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts or "\\" in path:
        raise ValueError(f"coverage path is not repository-relative: {path!r}")
    return path


@lru_cache(maxsize=16)
def resolve_coverage(
    repository_root: Path, source_revision: str, task_path: str
) -> tuple[CoverageEntry, ...]:
    if COMMIT_PATTERN.fullmatch(source_revision) is None:
        raise ValueError("source_revision must be one full lowercase Git commit SHA")
    normalized_task_path = _validate_repository_path(task_path)
    task_bytes = git_blob(repository_root, source_revision, normalized_task_path)
    try:
        task = load_json_bytes(task_bytes)
    except CanonicalizationError as error:
        raise ValueError(f"invalid coverage authority: {error}") from error
    references = task.get("references") if isinstance(task, dict) else None
    if not isinstance(references, list):
        raise ValueError("TaskEnvelope references must be an array")
    paths = [_validate_repository_path(item) for item in references]
    paths.append(normalized_task_path)
    if len(paths) != len(set(paths)):
        raise ValueError("coverage contains a duplicate path")
    entries = []
    for path in sorted(paths):
        content = (
            task_bytes
            if path == normalized_task_path
            else git_blob(repository_root, source_revision, path)
        )
        try:
            content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(f"coverage is not UTF-8: {path}") from error
        entries.append(CoverageEntry(path, hashlib.sha256(content).hexdigest()))
    return tuple(entries)


def build_baseline(
    repository_root: Path,
    source_revision: str,
    baseline_id: str,
    baseline_version: str,
    task_path: str,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": "2.0.0",
        "record_type": "FOUNDATION_BASELINE",
        "baseline_id": baseline_id,
        "baseline_version": baseline_version,
        "owner": "BC-001",
        "source_revision": source_revision,
        "coverage_authority": {
            "task_id": Path(task_path).stem,
            "task_envelope_path": task_path,
            "references_field": "references",
            "include_task_envelope": True,
        },
        "coverage": [
            entry.as_dict()
            for entry in resolve_coverage(repository_root, source_revision, task_path)
        ],
        "canonicalization_profile": "SPEC-001-JCS",
        "digest_algorithm": "SHA-256",
        "baseline_digest": ZERO_DIGEST,
    }
    record["baseline_digest"] = hashlib.sha256(canonical_json_bytes(record)).hexdigest()
    require_valid(validate_baseline(repository_root, record))
    return record


def validate_baseline(repository_root: Path, record: dict[str, Any]) -> list[Finding]:
    findings = schema_findings(repository_root, record)
    if findings or record.get("record_type") != "FOUNDATION_BASELINE":
        return sorted(findings)
    try:
        expected_coverage = [
            entry.as_dict()
            for entry in resolve_coverage(
                repository_root,
                str(record["source_revision"]),
                str(record["coverage_authority"]["task_envelope_path"]),
            )
        ]
        if record["coverage"] != expected_coverage:
            findings.append(
                Finding("COVERAGE_MISMATCH", "$.coverage", "coverage is not the derived set")
            )
        projection = dict(record)
        projection["baseline_digest"] = ZERO_DIGEST
        expected_digest = hashlib.sha256(canonical_json_bytes(projection)).hexdigest()
        if record["baseline_digest"] != expected_digest:
            findings.append(
                Finding("DIGEST_MISMATCH", "$.baseline_digest", "digest does not match projection")
            )
    except (ValueError, CanonicalizationError) as error:
        findings.append(Finding("BASELINE_INVALID", "$", str(error)))
    return sorted(findings)


def validate_transition(
    repository_root: Path,
    predecessor: dict[str, Any],
    successor: dict[str, Any],
    supersession: dict[str, Any] | None,
) -> list[Finding]:
    findings = validate_baseline(repository_root, predecessor)
    findings.extend(validate_baseline(repository_root, successor))
    if findings:
        return sorted(findings)
    changed = predecessor["baseline_digest"] != successor["baseline_digest"]
    if not changed and supersession is not None:
        findings.append(Finding("SUPERSESSION_REDUNDANT", "$", "unchanged digest cannot supersede"))
    if changed and supersession is None:
        findings.append(Finding("SUPERSESSION_REQUIRED", "$", "changed digest requires lineage"))
        return sorted(findings)
    if supersession is None:
        return []
    findings.extend(schema_findings(repository_root, supersession))
    if supersession.get("record_type") != "FOUNDATION_BASELINE_SUPERSESSION":
        return sorted(findings)
    if predecessor["baseline_id"] != successor["baseline_id"]:
        findings.append(Finding("BASELINE_ID_CHANGED", "$.successor", "stable identity changed"))
    if supersession.get("predecessor") != baseline_reference(predecessor):
        findings.append(Finding("LINEAGE_MISMATCH", "$.predecessor", "wrong predecessor"))
    if supersession.get("successor") != baseline_reference(successor):
        findings.append(Finding("LINEAGE_MISMATCH", "$.successor", "wrong successor"))
    findings.extend(
        normative_authority_findings(
            repository_root,
            supersession.get("authority"),
            field="$.authority",
            expected_path=ADR_AUTHORITY_PATH,
            expected_markers=("# ADR-057", "**Status:** `Accepted`", "**Aprovador:** `Project Owner`"),
        )
    )
    return sorted(findings)
