from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from governed_authority import authority_findings
from record_contract import reference_findings, strict_fields
from sprint_blocker_evidence import blocker_payload
from slice_one import (
    Finding,
    git_blob,
    load_json_bytes,
    resolve_governed_artifact,
    revision_is_ancestor,
)


COMPLETION_FIELDS = frozenset(
    {
        "record_type",
        "story_id",
        "task_id",
        "state",
        "candidate_revision",
        "assurance_evidence",
    }
)
ASSURANCE_FIELDS = frozenset(
    {
        "record_type",
        "authority_role",
        "task_id",
        "issue_id",
        "story_id",
        "reviewed_story_id",
        "reviewed_candidate_commit",
        "result",
    }
)


def completion_story_ids(
    repository_root: Path,
    references: object,
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> tuple[list[str], list[Finding]]:
    if not isinstance(references, list):
        return [], [
            Finding(
                "COMPLETION_EVIDENCE_INVALID",
                "$.completion_evidence",
                "must be an array",
            )
        ]
    story_ids: list[str] = []
    findings: list[Finding] = []
    for index, reference in enumerate(references):
        field = f"$.completion_evidence[{index}]"
        findings.extend(reference_findings(reference, field))
        if not isinstance(reference, Mapping):
            continue
        try:
            artifact = resolve_governed_artifact(repository_root, reference)
            payload = artifact.json_object()
        except ValueError as error:
            findings.append(Finding("COMPLETION_EVIDENCE_INVALID", field, str(error)))
            continue
        findings.extend(strict_fields(payload, COMPLETION_FIELDS, field))
        if payload.get("record_type") != "STORY_COMPLETION_EVIDENCE" or payload.get(
            "state"
        ) != "COMPLETED":
            findings.append(
                Finding("COMPLETION_EVIDENCE_INVALID", field, "completed evidence required")
            )
            continue
        story_ids.append(str(payload.get("story_id")))
        findings.extend(
            _completion_authority_findings(
                repository_root,
                artifact.source_revision,
                payload,
                field,
                delivery_gate,
            )
        )
    if story_ids != sorted(set(story_ids)):
        findings.append(
            Finding(
                "COMPLETION_EVIDENCE_INVALID",
                "$.completion_evidence",
                "must be sorted and unique",
            )
        )
    return story_ids, findings


def _completion_authority_findings(
    repository_root: Path,
    evidence_revision: str,
    payload: Mapping[str, Any],
    field: str,
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    candidate = payload.get("candidate_revision")
    task_id = payload.get("task_id")
    if not isinstance(candidate, str) or not isinstance(task_id, str):
        return [Finding("COMPLETION_EVIDENCE_INVALID", field, "candidate/task identity is absent")]
    try:
        task = load_json_bytes(
            git_blob(repository_root, candidate, f".codex/tasks/{task_id}.json")
        )
    except ValueError as error:
        return [Finding("COMPLETION_EVIDENCE_INVALID", field, str(error))]
    if not isinstance(task, Mapping) or task.get("story_id") != payload.get("story_id"):
        return [Finding("COMPLETION_EVIDENCE_INVALID", field, "TaskEnvelope/story mismatch")]
    if not _task_review_authorized(task):
        return [
            Finding(
                "COMPLETION_EVIDENCE_INVALID",
                field,
                "TaskEnvelope review authorities are incomplete",
            )
        ]
    if not revision_is_ancestor(repository_root, candidate, evidence_revision):
        return [Finding("COMPLETION_EVIDENCE_INVALID", field, "evidence predates candidate")]
    return _completion_assurance_findings(
        repository_root,
        payload.get("assurance_evidence"),
        candidate,
        evidence_revision,
        str(payload.get("story_id")),
        field,
        delivery_gate,
    )


def _task_review_authorized(task: Mapping[str, Any]) -> bool:
    phase_f = task.get("phase_f_review")
    phase_g = task.get("phase_g_review")
    review = phase_f.get("review") if isinstance(phase_f, Mapping) else None
    required_roles = review.get("required_roles") if isinstance(review, Mapping) else None
    return bool(
        task.get("requirements_review_status") == "PASS"
        and isinstance(phase_g, Mapping)
        and phase_g.get("status") == "PASS"
        and isinstance(required_roles, list)
        and {"QA", "Reviewer"}.issubset(set(required_roles))
    )


def _completion_assurance_findings(
    repository_root: Path,
    references: object,
    candidate: str,
    evidence_revision: str,
    reviewed_story_id: str,
    field: str,
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    if not isinstance(references, list) or len(references) != 2:
        return [Finding("COMPLETION_EVIDENCE_INVALID", field, "QA and Reviewer evidence required")]
    findings: list[Finding] = []
    for index, reference in enumerate(references):
        proof_field = f"{field}.assurance_evidence[{index}]"
        findings.extend(reference_findings(reference, proof_field))
        if not isinstance(reference, Mapping):
            continue
        proof, revision, proof_findings = _assurance_proof(
            repository_root, reference, proof_field
        )
        findings.extend(proof_findings)
        if proof is None or revision is None:
            continue
        expected_role = ("QA", "Reviewer")[index]
        findings.extend(
            _assurance_link_findings(
                repository_root,
                proof,
                revision,
                candidate,
                evidence_revision,
                proof_field,
                expected_role,
                reviewed_story_id,
            )
        )
        findings.extend(
            authority_findings(
                repository_root,
                delivery_gate=delivery_gate,
                artifact_path=reference["path"],
                artifact_revision=revision,
                payload=proof,
                expected_role=expected_role,
                required_reference=reviewed_story_id,
                field=proof_field,
            )
        )
    return findings


def _assurance_proof(
    repository_root: Path, reference: Mapping[str, Any], field: str
) -> tuple[Mapping[str, Any] | None, str | None, list[Finding]]:
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        proof = artifact.json_object()
    except ValueError as error:
        return None, None, [Finding("COMPLETION_EVIDENCE_INVALID", field, str(error))]
    return proof, artifact.source_revision, strict_fields(proof, ASSURANCE_FIELDS, field)


def _assurance_link_findings(
    repository_root: Path,
    proof: Mapping[str, Any],
    proof_revision: str,
    candidate: str,
    evidence_revision: str,
    field: str,
    expected_role: str,
    reviewed_story_id: str,
) -> list[Finding]:
    valid = (
        proof.get("record_type") == "CANDIDATE_ASSURANCE_EVIDENCE"
        and proof.get("authority_role") == expected_role
        and proof.get("reviewed_story_id") == reviewed_story_id
        and proof.get("reviewed_candidate_commit") == candidate
        and proof.get("result") == "PASS"
        and revision_is_ancestor(repository_root, candidate, proof_revision)
        and revision_is_ancestor(repository_root, proof_revision, evidence_revision)
    )
    return [] if valid else [
        Finding("COMPLETION_EVIDENCE_INVALID", field, "assurance proof mismatch")
    ]
