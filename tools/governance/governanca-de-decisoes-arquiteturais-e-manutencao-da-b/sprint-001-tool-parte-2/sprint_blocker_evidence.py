from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from governed_authority import authority_findings
from record_contract import reference_findings, strict_fields
from slice_one import Finding, resolve_governed_artifact, revision_is_ancestor


BLOCKER_FIELDS = frozenset(
    {
        "record_type",
        "blocked_story_id",
        "blocker_story_id",
        "state",
        "reason",
        "observed_revision",
        "observation",
    }
)
OBSERVATION_FIELDS = frozenset(
    {
        "record_type",
        "blocked_story_id",
        "blocker_story_id",
        "observed_revision",
        "status",
        "authority_role",
        "task_id",
        "issue_id",
        "story_id",
        "reviewed_candidate_commit",
    }
)


def blocker_payload(
    repository_root: Path,
    reference: object,
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> tuple[Mapping[str, Any] | None, list[Finding]]:
    if not isinstance(reference, Mapping):
        return None, [Finding("EXTENSION_BLOCKER_INVALID", "$.blocker_evidence", "reference required")]
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        payload = artifact.json_object()
    except ValueError as error:
        return None, [Finding("EXTENSION_BLOCKER_INVALID", "$.blocker_evidence", str(error))]
    findings = strict_fields(payload, BLOCKER_FIELDS, "$.blocker_evidence")
    if payload.get("record_type") != "SPRINT_BLOCKER_EVIDENCE" or payload.get("state") != "ACTIVE":
        findings.append(Finding("EXTENSION_BLOCKER_INVALID", "$.blocker_evidence", "active blocker evidence required"))
    observed = payload.get("observed_revision")
    if not isinstance(observed, str) or not revision_is_ancestor(repository_root, observed, artifact.source_revision):
        findings.append(Finding("EXTENSION_BLOCKER_INVALID", "$.blocker_evidence", "revision linkage invalid"))
    findings.extend(
        _blocker_observation_findings(
            repository_root,
            payload.get("observation"),
            payload,
            artifact.source_revision,
            delivery_gate,
        )
    )
    return payload, findings


def _blocker_observation_findings(
    repository_root: Path,
    reference: object,
    blocker: Mapping[str, Any],
    blocker_revision: str,
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    field = "$.blocker_evidence.observation"
    findings = reference_findings(reference, field)
    if not isinstance(reference, Mapping):
        return findings
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        observation = artifact.json_object()
    except ValueError as error:
        return findings + [Finding("EXTENSION_BLOCKER_INVALID", field, str(error))]
    findings.extend(strict_fields(observation, OBSERVATION_FIELDS, field))
    expected = {
        "record_type": "BLOCKER_OBSERVATION_EVIDENCE",
        "blocked_story_id": blocker.get("blocked_story_id"),
        "blocker_story_id": blocker.get("blocker_story_id"),
        "observed_revision": blocker.get("observed_revision"),
        "status": "ACTIVE",
        "authority_role": "QA",
        "reviewed_candidate_commit": blocker.get("observed_revision"),
    }
    if any(observation.get(name) != value for name, value in expected.items()) or not revision_is_ancestor(
        repository_root, artifact.source_revision, blocker_revision
    ):
        findings.append(Finding("EXTENSION_BLOCKER_INVALID", field, "governed observation mismatch"))
    findings.extend(
        authority_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=observation,
            expected_role="QA",
            required_reference=str(blocker.get("blocked_story_id")),
            field=field,
        )
    )
    return findings
