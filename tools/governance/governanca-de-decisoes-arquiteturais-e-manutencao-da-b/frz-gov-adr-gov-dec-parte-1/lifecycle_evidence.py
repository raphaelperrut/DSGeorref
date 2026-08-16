from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from canonical_json import canonical_json_bytes
from contract_validation import schema_findings
from foundation_validation_types import Finding
from governed_artifacts import (
    resolve_governed_artifact,
    revision_is_ancestor,
    revision_parent_count,
    role_authorizes_path,
)
from lifecycle_records import AppendOnlyRecordLedger


ADR_AUTHORITY_PATH = "docs/02-architecture/adrs/ADR-057-release-train-publicacao-e-gates-de-distribuicao.md"
CLOSURE_AUTHORITY_PATH = "docs/00-governance/DEFINITION_OF_DONE.md"


def baseline_reference(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "baseline_id": record.get("baseline_id"),
        "baseline_version": record.get("baseline_version"),
        "baseline_digest": record.get("baseline_digest"),
    }


def normative_authority_findings(
    repository_root: Path,
    reference: object,
    *,
    field: str,
    expected_path: str,
    expected_markers: tuple[str, ...],
) -> list[Finding]:
    if not isinstance(reference, Mapping):
        return [Finding("AUTHORITY_INVALID", field, "authority reference is malformed")]
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        text = artifact.content.decode("utf-8")
    except (UnicodeDecodeError, ValueError) as error:
        return [Finding("AUTHORITY_INVALID", field, str(error))]
    if artifact.path != expected_path or any(marker not in text for marker in expected_markers):
        return [
            Finding(
                "AUTHORITY_INVALID",
                field,
                "reference does not resolve to the accepted normative authority",
            )
        ]
    return []


def _proof_findings(
    repository_root: Path,
    proof_name: str,
    reference: Mapping[str, Any],
    baseline: Mapping[str, Any],
    candidate: str,
    merged: str,
) -> list[Finding]:
    field = f"$.proofs.{proof_name}"
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        payload = artifact.json_object()
    except ValueError as error:
        return [Finding("EVIDENCE_INVALID", field, str(error))]
    expected = {
        "record_type": "FOUNDATION_CLOSURE_PROOF",
        "proof_type": proof_name,
        "result": "PASS",
        "baseline": dict(baseline),
        "reviewed_candidate_commit": candidate,
    }
    if any(payload.get(key) != value for key, value in expected.items()):
        return [Finding("EVIDENCE_INVALID", field, "proof payload/linkage is not substantive")]
    if not revision_is_ancestor(repository_root, candidate, artifact.source_revision):
        return [Finding("COMMIT_LINK_MISMATCH", field, "proof predates reviewed candidate")]
    if proof_name == "HUMAN_MERGE":
        if payload.get("merged_commit") != merged or not revision_is_ancestor(
            repository_root, merged, artifact.source_revision
        ):
            return [Finding("COMMIT_LINK_MISMATCH", field, "human merge is not governed history")]
    elif "merged_commit" in payload:
        return [Finding("EVIDENCE_INVALID", field, "non-merge proof asserts merged_commit")]
    return _proof_authority_findings(
        repository_root,
        proof_name,
        payload,
        artifact.path,
        candidate,
        merged,
        field,
    )


def _proof_authority_findings(
    repository_root: Path,
    proof_name: str,
    payload: Mapping[str, Any],
    artifact_path: str,
    candidate: str,
    merged: str,
    field: str,
) -> list[Finding]:
    required_roles = {
        "QA_APPROVAL": "QA",
        "REVIEWER_APPROVAL": "Reviewer",
        "HUMAN_MERGE": "Autoridade Humana",
        "FIRST_SLICE_AUTHORIZATION": "Product Owner",
    }
    role = required_roles.get(proof_name)
    if role is not None and payload.get("authority_role") != role:
        return [Finding("EVIDENCE_AUTHORITY_INVALID", field, f"proof requires role {role}")]
    governed_roles = {"QA", "Reviewer", "Product Owner"}
    if role in governed_roles and not role_authorizes_path(
        repository_root, candidate, str(role), artifact_path
    ):
        return [
            Finding(
                "EVIDENCE_AUTHORITY_INVALID",
                field,
                f"proof path is not governed for role {role}",
            )
        ]
    if proof_name == "HUMAN_MERGE" and revision_parent_count(repository_root, merged) < 2:
        return [Finding("EVIDENCE_AUTHORITY_INVALID", field, "merged_commit is not a Git merge")]
    return []


def validate_evidence_set(
    repository_root: Path,
    record: dict[str, Any],
    baseline: Mapping[str, Any],
) -> list[Finding]:
    findings = schema_findings(repository_root, record)
    if findings or record.get("record_type") != "FOUNDATION_CLOSURE_EVIDENCE_SET":
        return sorted(findings)
    if record.get("baseline") != baseline_reference(baseline):
        findings.append(Finding("BASELINE_REFERENCE_MISMATCH", "$.baseline", "wrong baseline"))
    candidate = record["reviewed_candidate_commit"]
    merged = record["merged_commit"]
    if not revision_is_ancestor(repository_root, candidate, merged):
        findings.append(
            Finding("COMMIT_LINK_MISMATCH", "$.merged_commit", "merge does not contain candidate")
        )
    for proof_name, proof in sorted(record["proofs"].items()):
        findings.extend(
            _proof_findings(
                repository_root,
                proof_name,
                proof["artifact"],
                record["baseline"],
                candidate,
                merged,
            )
        )
    return sorted(findings)


def validate_closure(
    repository_root: Path,
    closure: dict[str, Any],
    evidence_set: Mapping[str, Any],
    baseline: Mapping[str, Any],
) -> list[Finding]:
    findings = schema_findings(repository_root, closure)
    if findings or closure.get("record_type") != "FOUNDATION_CLOSURE":
        return sorted(findings)
    if closure.get("baseline") != baseline_reference(baseline):
        findings.append(Finding("BASELINE_REFERENCE_MISMATCH", "$.baseline", "wrong baseline"))
    if closure.get("evidence_set_id") != evidence_set.get("evidence_set_id"):
        findings.append(Finding("EVIDENCE_SET_MISMATCH", "$.evidence_set_id", "wrong evidence set"))
    try:
        linked = resolve_governed_artifact(repository_root, closure["evidence_set"])
    except ValueError:
        linked = None
    if linked is None or linked.content != canonical_json_bytes(evidence_set):
        findings.append(Finding("EVIDENCE_SET_INVALID", "$.evidence_set", "unverifiable evidence set"))
    findings.extend(
        normative_authority_findings(
            repository_root,
            closure.get("closure_authority"),
            field="$.closure_authority",
            expected_path=CLOSURE_AUTHORITY_PATH,
            expected_markers=(
                "# Definition of Done",
                "QA registrou aprovação independente",
                "autoridade humana realizou o merge",
            ),
        )
    )
    findings.extend(validate_evidence_set(repository_root, dict(evidence_set), baseline))
    return sorted(findings)


def validate_reopening(
    repository_root: Path,
    reopening: dict[str, Any],
    prior_closure: Mapping[str, Any],
    prior_baseline: Mapping[str, Any],
    prior_evidence_set: Mapping[str, Any],
    ledger: AppendOnlyRecordLedger,
) -> list[Finding]:
    findings = schema_findings(repository_root, reopening)
    if findings or reopening.get("record_type") != "FOUNDATION_REOPENING":
        return sorted(findings)
    findings.extend(
        validate_closure(
            repository_root,
            dict(prior_closure),
            prior_evidence_set,
            prior_baseline,
        )
    )
    if not ledger.contains_exactly(prior_closure) or not ledger.contains_exactly(prior_evidence_set):
        findings.append(Finding("HISTORY_NOT_PRESERVED", "$", "prior closure/evidence changed or missing"))
    if reopening.get("prior_closure_id") != prior_closure.get("closure_id"):
        findings.append(Finding("CLOSURE_REFERENCE_MISMATCH", "$.prior_closure_id", "wrong closure"))
    if reopening.get("prior_baseline") != baseline_reference(prior_baseline):
        findings.append(Finding("BASELINE_REFERENCE_MISMATCH", "$.prior_baseline", "wrong baseline"))
    _validate_reopening_references(repository_root, reopening, prior_closure, findings)
    if reopening.get("new_candidate_id") in {
        prior_evidence_set.get("evidence_set_id"),
        prior_evidence_set.get("reviewed_candidate_commit"),
    }:
        findings.append(Finding("CANDIDATE_REUSED", "$.new_candidate_id", "new candidate required"))
    if reopening.get("new_evidence_set_id") == prior_evidence_set.get("evidence_set_id"):
        findings.append(Finding("EVIDENCE_SET_REUSED", "$.new_evidence_set_id", "new evidence set required"))
    return sorted(findings)


def _validate_reopening_references(
    repository_root: Path,
    reopening: Mapping[str, Any],
    prior_closure: Mapping[str, Any],
    findings: list[Finding],
) -> None:
    try:
        linked = resolve_governed_artifact(repository_root, reopening["prior_closure"])
    except ValueError:
        linked = None
    if linked is None or linked.content != canonical_json_bytes(prior_closure):
        findings.append(Finding("PRIOR_CLOSURE_INVALID", "$.prior_closure", "unverifiable closure"))
    try:
        trigger_artifact = resolve_governed_artifact(
            repository_root, reopening["material_trigger"]["evidence"]
        )
        trigger = trigger_artifact.json_object()
    except ValueError as error:
        findings.append(Finding("MATERIAL_TRIGGER_INVALID", "$.material_trigger", str(error)))
    else:
        expected = {
            "record_type": "FOUNDATION_REOPENING_TRIGGER",
            "kind": reopening["material_trigger"]["kind"],
            "prior_closure_id": reopening["prior_closure_id"],
            "prior_baseline": reopening["prior_baseline"],
            "new_candidate_id": reopening["new_candidate_id"],
            "new_evidence_set_id": reopening["new_evidence_set_id"],
        }
        if any(trigger.get(key) != value for key, value in expected.items()):
            findings.append(
                Finding("MATERIAL_TRIGGER_INVALID", "$.material_trigger", "trigger does not substantiate transition")
            )
        findings.extend(
            _reopening_link_findings(
                repository_root,
                trigger,
                trigger_artifact.source_revision,
                reopening,
            )
        )
    authority = normative_authority_findings(
        repository_root,
        reopening.get("authority"),
        field="$.authority",
        expected_path=ADR_AUTHORITY_PATH,
        expected_markers=("# ADR-057", "**Status:** `Accepted`", "**Aprovador:** `Project Owner`"),
    )
    findings.extend(
        Finding("REOPENING_AUTHORITY_INVALID", item.field, item.detail) for item in authority
    )


def _reopening_link_findings(
    repository_root: Path,
    trigger: Mapping[str, Any],
    trigger_revision: str,
    reopening: Mapping[str, Any],
) -> list[Finding]:
    expectations = (
        (
            "new_candidate",
            {
                "record_type": "FOUNDATION_REOPENING_CANDIDATE",
                "candidate_id": reopening["new_candidate_id"],
                "prior_closure_id": reopening["prior_closure_id"],
                "prior_baseline": reopening["prior_baseline"],
            },
        ),
        (
            "new_evidence_set",
            {
                "record_type": "FOUNDATION_REOPENING_EVIDENCE_SET",
                "evidence_set_id": reopening["new_evidence_set_id"],
                "candidate_id": reopening["new_candidate_id"],
                "status": "OPEN",
            },
        ),
    )
    findings: list[Finding] = []
    for field, expected in expectations:
        reference = trigger.get(field)
        if not isinstance(reference, Mapping):
            findings.append(Finding("MATERIAL_TRIGGER_INVALID", field, "governed link is missing"))
            continue
        try:
            artifact = resolve_governed_artifact(repository_root, reference)
            payload = artifact.json_object()
        except ValueError as error:
            findings.append(Finding("MATERIAL_TRIGGER_INVALID", field, str(error)))
            continue
        if (
            any(payload.get(key) != value for key, value in expected.items())
            or not revision_is_ancestor(repository_root, artifact.source_revision, trigger_revision)
        ):
            findings.append(
                Finding(
                    "MATERIAL_TRIGGER_INVALID",
                    field,
                    "linked candidate/evidence artifact does not substantiate reopening",
                )
            )
    return findings
