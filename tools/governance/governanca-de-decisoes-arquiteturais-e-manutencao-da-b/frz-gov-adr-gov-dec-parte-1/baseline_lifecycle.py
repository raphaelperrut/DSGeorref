from __future__ import annotations

import hashlib
import re
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any

from canonical_json import CanonicalizationError, canonical_json_bytes, load_json_bytes
from contract_validation import schema_findings
from foundation_validation_types import Finding, require_valid


TASK_PATH = ".codex/tasks/TASK-0688.json"
ZERO_DIGEST = "0" * 64
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True, order=True)
class CoverageEntry:
    path: str
    content_sha256: str

    def as_dict(self) -> dict[str, str]:
        return {"path": self.path, "content_sha256": self.content_sha256}


@dataclass(frozen=True)
class EvidenceArtifact:
    content: bytes
    reviewed_candidate_commit: str | None = None
    merged_commit: str | None = None


class AppendOnlyRecordLedger:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str], bytes] = {}

    def append(self, record: Mapping[str, Any]) -> None:
        record_type = record.get("record_type")
        identity_fields = {
            "FOUNDATION_BASELINE": "baseline_id",
            "FOUNDATION_BASELINE_SUPERSESSION": "supersession_id",
            "FOUNDATION_CLOSURE_EVIDENCE_SET": "evidence_set_id",
            "FOUNDATION_CLOSURE": "closure_id",
            "FOUNDATION_REOPENING": "reopening_id",
        }
        identity_field = identity_fields.get(str(record_type))
        if identity_field is None or not isinstance(record.get(identity_field), str):
            raise ValueError("record has no recognized immutable identity")
        identity = str(record[identity_field])
        if record_type == "FOUNDATION_BASELINE":
            version = record.get("baseline_version")
            if not isinstance(version, str):
                raise ValueError("baseline record has no immutable version")
            identity = f"{identity}@{version}"
        key = (str(record_type), identity)
        encoded = canonical_json_bytes(record)
        existing = self._records.get(key)
        if existing is not None and existing != encoded:
            raise ValueError("silent replacement of an immutable record is forbidden")
        self._records[key] = encoded

    def contains_exactly(self, record: Mapping[str, Any]) -> bool:
        try:
            record_type = str(record["record_type"])
            field = {
                "FOUNDATION_BASELINE": "baseline_id",
                "FOUNDATION_BASELINE_SUPERSESSION": "supersession_id",
                "FOUNDATION_CLOSURE_EVIDENCE_SET": "evidence_set_id",
                "FOUNDATION_CLOSURE": "closure_id",
                "FOUNDATION_REOPENING": "reopening_id",
            }[record_type]
            identity = str(record[field])
            if record_type == "FOUNDATION_BASELINE":
                identity = f"{identity}@{record['baseline_version']}"
            return self._records[(record_type, identity)] == canonical_json_bytes(record)
        except (KeyError, CanonicalizationError):
            return False


def _git_blob(repository_root: Path, revision: str, path: str) -> bytes:
    resolved = subprocess.run(
        ["git", "-C", str(repository_root), "rev-parse", f"{revision}:{path}"],
        check=False,
        capture_output=True,
    )
    if resolved.returncode != 0:
        raise ValueError(f"coverage path is missing at source revision: {path}")
    blob_id = resolved.stdout.decode("ascii").strip()
    completed = subprocess.run(
        ["git", "-C", str(repository_root), "cat-file", "blob", blob_id],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise ValueError(f"coverage blob is unreadable at source revision: {path}")
    return completed.stdout


def _validate_repository_path(path: object) -> str:
    if not isinstance(path, str) or not path:
        raise ValueError("coverage path must be a non-empty string")
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts or "\\" in path:
        raise ValueError(f"coverage path is not repository-relative: {path!r}")
    return path


@lru_cache(maxsize=16)
def resolve_coverage(repository_root: Path, source_revision: str) -> tuple[CoverageEntry, ...]:
    if COMMIT_PATTERN.fullmatch(source_revision) is None:
        raise ValueError("source_revision must be one full lowercase Git commit SHA")
    task_bytes = _git_blob(repository_root, source_revision, TASK_PATH)
    try:
        task = load_json_bytes(task_bytes)
    except CanonicalizationError as error:
        raise ValueError(f"invalid coverage authority: {error}") from error
    references = task.get("references") if isinstance(task, dict) else None
    if not isinstance(references, list):
        raise ValueError("TaskEnvelope references must be an array")
    paths = [_validate_repository_path(item) for item in references]
    paths.append(TASK_PATH)
    if len(paths) != len(set(paths)):
        raise ValueError("coverage contains a duplicate path")
    entries = []
    for path in sorted(paths):
        content = task_bytes if path == TASK_PATH else _git_blob(repository_root, source_revision, path)
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
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": "1.0.0",
        "record_type": "FOUNDATION_BASELINE",
        "baseline_id": baseline_id,
        "baseline_version": baseline_version,
        "owner": "BC-001",
        "source_revision": source_revision,
        "coverage_authority": {
            "task_id": "TASK-0688",
            "task_envelope_path": TASK_PATH,
            "references_field": "references",
            "include_task_envelope": True,
        },
        "coverage": [entry.as_dict() for entry in resolve_coverage(repository_root, source_revision)],
        "canonicalization_profile": "SPEC-001-JCS",
        "digest_algorithm": "SHA-256",
        "baseline_digest": ZERO_DIGEST,
    }
    record["baseline_digest"] = hashlib.sha256(canonical_json_bytes(record)).hexdigest()
    require_valid(validate_baseline(repository_root, record))
    return record


def _baseline_reference(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "baseline_id": record.get("baseline_id"),
        "baseline_version": record.get("baseline_version"),
        "baseline_digest": record.get("baseline_digest"),
    }


def validate_baseline(repository_root: Path, record: dict[str, Any]) -> list[Finding]:
    findings = schema_findings(repository_root, record)
    if findings or record.get("record_type") != "FOUNDATION_BASELINE":
        return sorted(findings)
    try:
        expected_coverage = [
            entry.as_dict()
            for entry in resolve_coverage(repository_root, str(record["source_revision"]))
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
    if supersession.get("predecessor") != _baseline_reference(predecessor):
        findings.append(Finding("LINEAGE_MISMATCH", "$.predecessor", "wrong predecessor"))
    if supersession.get("successor") != _baseline_reference(successor):
        findings.append(Finding("LINEAGE_MISMATCH", "$.successor", "wrong successor"))
    return sorted(findings)


def _verify_reference(
    reference: Mapping[str, Any], artifacts: Mapping[str, EvidenceArtifact]
) -> EvidenceArtifact | None:
    artifact = artifacts.get(str(reference.get("path")))
    if artifact is None:
        return None
    if hashlib.sha256(artifact.content).hexdigest() != reference.get("sha256"):
        return None
    return artifact


def validate_evidence_set(
    repository_root: Path,
    record: dict[str, Any],
    baseline: Mapping[str, Any],
    artifacts: Mapping[str, EvidenceArtifact],
) -> list[Finding]:
    findings = schema_findings(repository_root, record)
    if findings or record.get("record_type") != "FOUNDATION_CLOSURE_EVIDENCE_SET":
        return sorted(findings)
    if record.get("baseline") != _baseline_reference(baseline):
        findings.append(Finding("BASELINE_REFERENCE_MISMATCH", "$.baseline", "wrong baseline"))
    candidate = record["reviewed_candidate_commit"]
    merged = record["merged_commit"]
    for proof_name, proof in sorted(record["proofs"].items()):
        artifact = _verify_reference(proof["artifact"], artifacts)
        if artifact is None:
            findings.append(Finding("EVIDENCE_INVALID", f"$.proofs.{proof_name}", "missing or hash mismatch"))
        elif proof_name == "HUMAN_MERGE":
            if (artifact.reviewed_candidate_commit, artifact.merged_commit) != (candidate, merged):
                findings.append(Finding("COMMIT_LINK_MISMATCH", f"$.proofs.{proof_name}", "wrong merge linkage"))
        elif artifact.reviewed_candidate_commit != candidate:
            findings.append(Finding("COMMIT_LINK_MISMATCH", f"$.proofs.{proof_name}", "wrong candidate linkage"))
    return sorted(findings)


def validate_closure(
    repository_root: Path,
    closure: dict[str, Any],
    evidence_set: Mapping[str, Any],
    baseline: Mapping[str, Any],
    artifacts: Mapping[str, EvidenceArtifact],
) -> list[Finding]:
    findings = schema_findings(repository_root, closure)
    if findings or closure.get("record_type") != "FOUNDATION_CLOSURE":
        return sorted(findings)
    if closure.get("baseline") != _baseline_reference(baseline):
        findings.append(Finding("BASELINE_REFERENCE_MISMATCH", "$.baseline", "wrong baseline"))
    if closure.get("evidence_set_id") != evidence_set.get("evidence_set_id"):
        findings.append(Finding("EVIDENCE_SET_MISMATCH", "$.evidence_set_id", "wrong evidence set"))
    linked = _verify_reference(closure["evidence_set"], artifacts)
    if linked is None or linked.content != canonical_json_bytes(evidence_set):
        findings.append(Finding("EVIDENCE_SET_INVALID", "$.evidence_set", "unverifiable evidence set"))
    if _verify_reference(closure["closure_authority"], artifacts) is None:
        findings.append(Finding("CLOSURE_AUTHORITY_INVALID", "$.closure_authority", "unverifiable authority"))
    return sorted(findings)


def validate_reopening(
    repository_root: Path,
    reopening: dict[str, Any],
    prior_closure: Mapping[str, Any],
    prior_baseline: Mapping[str, Any],
    prior_evidence_set: Mapping[str, Any],
    artifacts: Mapping[str, EvidenceArtifact],
    ledger: AppendOnlyRecordLedger,
) -> list[Finding]:
    findings = schema_findings(repository_root, reopening)
    if findings or reopening.get("record_type") != "FOUNDATION_REOPENING":
        return sorted(findings)
    if not ledger.contains_exactly(prior_closure) or not ledger.contains_exactly(prior_evidence_set):
        findings.append(Finding("HISTORY_NOT_PRESERVED", "$", "prior closure/evidence changed or missing"))
    if reopening.get("prior_closure_id") != prior_closure.get("closure_id"):
        findings.append(Finding("CLOSURE_REFERENCE_MISMATCH", "$.prior_closure_id", "wrong closure"))
    if reopening.get("prior_baseline") != _baseline_reference(prior_baseline):
        findings.append(Finding("BASELINE_REFERENCE_MISMATCH", "$.prior_baseline", "wrong baseline"))
    linked = _verify_reference(reopening["prior_closure"], artifacts)
    if linked is None or linked.content != canonical_json_bytes(prior_closure):
        findings.append(Finding("PRIOR_CLOSURE_INVALID", "$.prior_closure", "unverifiable closure"))
    if _verify_reference(reopening["material_trigger"]["evidence"], artifacts) is None:
        findings.append(Finding("MATERIAL_TRIGGER_INVALID", "$.material_trigger", "unverifiable trigger"))
    if _verify_reference(reopening["authority"], artifacts) is None:
        findings.append(Finding("REOPENING_AUTHORITY_INVALID", "$.authority", "unverifiable authority"))
    if reopening.get("new_candidate_id") in {
        prior_evidence_set.get("evidence_set_id"),
        prior_evidence_set.get("reviewed_candidate_commit"),
    }:
        findings.append(Finding("CANDIDATE_REUSED", "$.new_candidate_id", "new candidate required"))
    if reopening.get("new_evidence_set_id") == prior_evidence_set.get("evidence_set_id"):
        findings.append(Finding("EVIDENCE_SET_REUSED", "$.new_evidence_set_id", "new evidence set required"))
    return sorted(findings)
