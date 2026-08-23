from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from slice_one import (
    COMMIT_PATTERN,
    Finding,
    revision_first_parent,
    revision_is_ancestor,
    role_authorizes_path,
    task_authorizes_artifact,
    git_blob,
    load_json_bytes,
)


AUTHORITY_FIELDS = frozenset(
    {
        "authority_role",
        "task_id",
        "issue_id",
        "story_id",
        "reviewed_candidate_commit",
    }
)


def authority_findings(
    repository_root: Path,
    *,
    delivery_gate: DeliveryApprovalGate | None,
    artifact_path: str,
    artifact_revision: str,
    payload: Mapping[str, Any],
    expected_role: str,
    required_reference: str,
    field: str,
    approval_revision: str | None = None,
) -> list[Finding]:
    candidate = payload.get("reviewed_candidate_commit")
    if not isinstance(candidate, str) or COMMIT_PATTERN.fullmatch(candidate) is None:
        return [Finding("EVIDENCE_AUTHORITY_INVALID", field, "candidate commit is invalid")]
    checkpoint = revision_first_parent(repository_root, candidate)
    if checkpoint is None:
        return [Finding("EVIDENCE_AUTHORITY_INVALID", field, "control-plane checkpoint is absent")]
    valid_history = candidate != artifact_revision and revision_is_ancestor(
        repository_root, candidate, artifact_revision
    )
    valid_role = payload.get("authority_role") == expected_role and role_authorizes_path(
        repository_root, checkpoint, expected_role, artifact_path
    )
    valid_task = task_authorizes_artifact(
        repository_root,
        checkpoint,
        expected_role,
        artifact_path,
        payload,
        required_reference=required_reference,
    )
    approval_findings = _delivery_approval_findings(
        repository_root,
        delivery_gate=delivery_gate,
        task_id=payload.get("task_id"),
        checkpoint=checkpoint,
        candidate=candidate,
        artifact_revision=approval_revision or artifact_revision,
    )
    if valid_history and valid_role and valid_task and not approval_findings:
        return []
    return approval_findings or [
        Finding(
            "EVIDENCE_AUTHORITY_INVALID",
            field,
            "artifact lacks pre-existing role/TaskEnvelope authority or independent provenance",
        )
    ]


def _delivery_approval_findings(
    repository_root: Path,
    *,
    delivery_gate: DeliveryApprovalGate | None,
    task_id: object,
    checkpoint: str,
    candidate: str,
    artifact_revision: str,
) -> list[Finding]:
    if type(delivery_gate) is not DeliveryApprovalGate or not isinstance(task_id, str):
        return [
            Finding(
                "DELIVERY_APPROVAL_INVALID",
                "delivery_approval",
                "trusted DAA gate and TaskEnvelope identity are required",
            )
        ]
    path = f"evidence/delivery-approval-authority/{task_id}/{candidate}.json"
    try:
        evidence = load_json_bytes(git_blob(repository_root, artifact_revision, path))
        task = load_json_bytes(
            git_blob(repository_root, checkpoint, f".codex/tasks/{task_id}.json")
        )
    except ValueError as error:
        return [Finding("DELIVERY_APPROVAL_INVALID", path, str(error))]
    if not isinstance(evidence, Mapping) or not isinstance(task, Mapping):
        return [Finding("DELIVERY_APPROVAL_INVALID", path, "DAA records are invalid")]
    _approval, findings = delivery_gate.verify(
        evidence=evidence,
        task_envelope=task,
        candidate_sha=candidate,
    )
    return findings
