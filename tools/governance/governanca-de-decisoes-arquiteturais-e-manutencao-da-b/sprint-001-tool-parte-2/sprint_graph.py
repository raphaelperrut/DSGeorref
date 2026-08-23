from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from governed_authority import AUTHORITY_FIELDS, authority_findings
from record_contract import reference_findings, strict_fields
from sprint_graph_evidence import blocker_payload, completion_story_ids
from slice_one import (
    Finding,
    canonical_json_bytes,
    derive_canonical_sprint_selection,
    git_blob,
    load_json_bytes,
    resolve_governed_artifact,
)


GRAPH_PATH = "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
WAVE_FIELDS = frozenset(
    {
        "wave_id",
        "graph_revision",
        "story_ids",
        "completion_evidence",
        "evidence_oriented",
        "authority",
    }
)
EXTENSION_FIELDS = frozenset(
    {"record_type", "extension_id", "sprint_id", "blocker_evidence", "graph", "authority"}
)


def validate_wave(
    repository_root: Path,
    wave: Mapping[str, Any],
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> list[Finding]:
    findings = strict_fields(wave, WAVE_FIELDS, "$")
    if findings:
        return sorted(findings)
    story_ids = wave.get("story_ids")
    if not _unique_strings(story_ids):
        findings.append(Finding("WAVE_INVALID", "$.story_ids", "must be non-empty and unique"))
        return sorted(findings)
    completed, completion_findings = completion_story_ids(
        repository_root,
        wave.get("completion_evidence"),
        delivery_gate=delivery_gate,
    )
    findings.extend(completion_findings)
    if wave.get("evidence_oriented") is not True:
        findings.append(Finding("WAVE_NOT_EVIDENCE_ORIENTED", "$.evidence_oriented", "must be true"))
    findings.extend(_wave_authority_findings(repository_root, wave, delivery_gate))
    try:
        selected = set(derive_canonical_sprint_selection(repository_root))
        edges = _edges(_graph(repository_root, str(wave.get("graph_revision"))))
    except ValueError as error:
        findings.append(Finding("WAVE_AUTHORITY_INVALID", "$.graph_revision", str(error)))
        return sorted(findings)
    if not set(story_ids).issubset(selected) or not set(completed).issubset(selected):
        findings.append(Finding("WAVE_SELECTION_INVALID", "$", "story is outside canonical selection"))
    if len(selected) > 1 and set(story_ids) == selected:
        findings.append(
            Finding(
                "WAVE_NOT_SMALL",
                "$.story_ids",
                "a vertical wave must be a proper subset of the canonical selection",
            )
        )
    if set(story_ids) & set(completed):
        findings.append(Finding("WAVE_SELECTION_INVALID", "$", "wave and completed sets overlap"))
    for story_id in story_ids:
        missing = sorted(
            source
            for source, target in edges
            if target == story_id and source not in completed
        )
        if missing:
            findings.append(
                Finding("WAVE_GRAPH_MISMATCH", story_id, f"direct blockers not completed: {', '.join(missing)}")
            )
    return sorted(findings)


def _wave_authority_findings(
    repository_root: Path,
    wave: Mapping[str, Any],
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    reference = wave.get("authority")
    findings = reference_findings(reference, "$.authority")
    if not isinstance(reference, Mapping):
        return findings
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        payload = artifact.json_object()
    except ValueError as error:
        return findings + [Finding("WAVE_AUTHORITY_INVALID", "$.authority", str(error))]
    expected_fields = frozenset({"record_type", "wave_sha256"}) | AUTHORITY_FIELDS
    findings.extend(strict_fields(payload, expected_fields, "$.authority"))
    projection = {key: value for key, value in wave.items() if key != "authority"}
    expected_digest = hashlib.sha256(canonical_json_bytes(projection)).hexdigest()
    if payload.get("record_type") != "SPRINT_WAVE_AUTHORIZATION" or payload.get(
        "wave_sha256"
    ) != expected_digest or payload.get("reviewed_candidate_commit") != wave.get(
        "graph_revision"
    ):
        findings.append(Finding("WAVE_AUTHORITY_INVALID", "$.authority", "wave authorization mismatch"))
    findings.extend(
        authority_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=payload,
            expected_role="Tech Lead",
            required_reference="REQ-SPRINT-001-003",
            field="$.authority",
        )
    )
    return findings


def validate_sprint_extension(
    repository_root: Path,
    extension: Mapping[str, Any],
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> list[Finding]:
    findings = strict_fields(extension, EXTENSION_FIELDS, "$")
    if extension.get("record_type") != "SPRINT_EXTENSION" or extension.get("sprint_id") != "SPRINT-001":
        findings.append(Finding("EXTENSION_IDENTITY_INVALID", "$", "extension identity is invalid"))
    blocker_reference = extension.get("blocker_evidence")
    graph_reference = extension.get("graph")
    findings.extend(reference_findings(blocker_reference, "$.blocker_evidence"))
    findings.extend(reference_findings(graph_reference, "$.graph"))
    findings.extend(
        _record_authority_findings(
            repository_root,
            extension,
            reference=extension.get("authority"),
            record_type="SPRINT_EXTENSION_AUTHORIZATION",
            digest_field="extension_sha256",
            expected_role="Product Owner",
            required_reference="REQ-SPRINT-001-009",
            expected_candidate=(
                blocker_reference.get("source_revision")
                if isinstance(blocker_reference, Mapping)
                else None
            ),
            field="$.authority",
            delivery_gate=delivery_gate,
        )
    )
    if isinstance(graph_reference, Mapping):
        findings.extend(_resolve(repository_root, graph_reference, "$.graph"))
    blocker, blocker_findings = blocker_payload(
        repository_root, blocker_reference, delivery_gate=delivery_gate
    )
    findings.extend(blocker_findings)
    if blocker is None:
        return sorted(findings)
    if not isinstance(blocker.get("reason"), str) or not blocker["reason"].strip():
        findings.append(Finding("EXTENSION_BLOCKER_INVALID", "$.blocker_evidence.reason", "direct reason is required"))
    try:
        edges = _edges(_graph(repository_root, str(blocker.get("observed_revision"))))
    except ValueError as error:
        findings.append(Finding("EXTENSION_BLOCKER_INVALID", "$.blocker_evidence", str(error)))
        return sorted(findings)
    pair = (blocker.get("blocker_story_id"), blocker.get("blocked_story_id"))
    if pair not in edges:
        findings.append(Finding("EXTENSION_NOT_DIRECTLY_BLOCKED", "$.blocker_evidence", "no direct graph edge justifies extension"))
    if isinstance(graph_reference, Mapping) and (
        graph_reference.get("path") != GRAPH_PATH
        or graph_reference.get("source_revision") != blocker.get("observed_revision")
    ):
        findings.append(
            Finding(
                "EXTENSION_EVIDENCE_DIVERGENT",
                "$.graph",
                "evidence must bind the exact canonical graph revision",
            )
        )
    return sorted(findings)


def _record_authority_findings(
    repository_root: Path,
    record: Mapping[str, Any],
    *,
    reference: object,
    record_type: str,
    digest_field: str,
    expected_role: str,
    required_reference: str,
    expected_candidate: object,
    field: str,
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    findings = reference_findings(reference, field)
    if not isinstance(reference, Mapping):
        return findings
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        payload = artifact.json_object()
    except ValueError as error:
        return findings + [Finding("RECORD_AUTHORITY_INVALID", field, str(error))]
    findings.extend(
        strict_fields(payload, frozenset({"record_type", digest_field}) | AUTHORITY_FIELDS, field)
    )
    projection = {key: value for key, value in record.items() if key != "authority"}
    digest = hashlib.sha256(canonical_json_bytes(projection)).hexdigest()
    if (
        payload.get("record_type") != record_type
        or payload.get(digest_field) != digest
        or payload.get("reviewed_candidate_commit") != expected_candidate
    ):
        findings.append(Finding("RECORD_AUTHORITY_INVALID", field, "authorization mismatch"))
    findings.extend(
        authority_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=payload,
            expected_role=expected_role,
            required_reference=required_reference,
            field=field,
        )
    )
    return findings


def _graph(repository_root: Path, revision: str) -> Mapping[str, Any]:
    try:
        graph = load_json_bytes(git_blob(repository_root, revision, GRAPH_PATH))
    except ValueError as error:
        raise ValueError(f"canonical graph is unavailable: {error}") from error
    if not isinstance(graph, Mapping) or graph.get("semantics") != (
        "Only hard blockers; edge from prerequisite to dependent."
    ):
        raise ValueError("canonical graph semantics are invalid")
    return graph


def _edges(graph: Mapping[str, Any]) -> set[tuple[str, str]]:
    raw_edges = graph.get("edges")
    if not isinstance(raw_edges, list):
        raise ValueError("canonical graph edges are invalid")
    edges: set[tuple[str, str]] = set()
    for edge in raw_edges:
        if not isinstance(edge, Mapping) or edge.get("relation") != "blocks":
            raise ValueError("canonical graph contains an invalid edge")
        source, target = edge.get("from"), edge.get("to")
        if not isinstance(source, str) or not isinstance(target, str):
            raise ValueError("canonical graph edge identity is invalid")
        edges.add((source, target))
    return edges


def _resolve(repository_root: Path, reference: Mapping[str, Any], field: str) -> list[Finding]:
    try:
        resolve_governed_artifact(repository_root, reference)
    except ValueError as error:
        return [Finding("GOVERNED_ARTIFACT_INVALID", field, str(error))]
    return []


def _unique_strings(value: object, *, allow_empty: bool = False) -> bool:
    return isinstance(value, list) and (allow_empty or bool(value)) and all(
        isinstance(item, str) and item for item in value
    ) and len(value) == len(set(value))
