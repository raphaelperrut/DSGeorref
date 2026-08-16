from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from canonical_json import CanonicalizationError, canonical_json_bytes
from foundation_validation_types import Finding
from governed_artifacts import (
    resolve_governed_artifact,
    revision_first_parent,
    role_authorizes_path,
    task_authorizes_artifact,
)


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _governed_records(
    repository_root: Path,
    references: Iterable[Mapping[str, Any]],
    *,
    record_type: str,
    finding_code: str,
    expected_role: str | None = None,
) -> tuple[list[dict[str, Any]], list[Finding]]:
    records: list[dict[str, Any]] = []
    findings: list[Finding] = []
    for position, reference in enumerate(references):
        field = f"{record_type}[{position}]"
        try:
            artifact = resolve_governed_artifact(repository_root, reference)
            record = artifact.json_object()
        except ValueError as error:
            findings.append(Finding(finding_code, field, str(error)))
            continue
        if record.get("record_type") != record_type:
            findings.append(Finding(finding_code, field, "governed record has wrong type"))
            continue
        if expected_role is not None and not role_authorizes_path(
            repository_root,
            artifact.source_revision,
            expected_role,
            artifact.path,
        ):
            findings.append(
                Finding(
                    finding_code,
                    field,
                    f"record path is not governed for role {expected_role}",
                )
            )
            continue
        if expected_role == "Product Owner":
            authority_revision = revision_first_parent(
                repository_root, artifact.source_revision
            )
            authorized = authority_revision is not None and task_authorizes_artifact(
                repository_root,
                authority_revision,
                expected_role,
                artifact.path,
                record,
                required_reference="REQ-ISM-010",
            )
            if not authorized:
                findings.append(
                    Finding(
                        finding_code,
                        field,
                        "approval is not bound to a pre-existing governed Product Owner TaskEnvelope",
                    )
                )
                continue
        records.append(record)
    return records, findings


def _snapshot_findings(
    snapshots: Iterable[tuple[str, Mapping[str, Any]]]
) -> list[Finding]:
    findings: list[Finding] = []
    observed: dict[str, str] = {}
    for snapshot_id, snapshot in snapshots:
        try:
            digest = _digest(snapshot)
        except CanonicalizationError as error:
            findings.append(Finding("SNAPSHOT_INVALID", snapshot_id, str(error)))
            continue
        previous_digest = observed.get(snapshot_id)
        if previous_digest is not None and previous_digest != digest:
            findings.append(Finding("SNAPSHOT_MUTATED", snapshot_id, "snapshot identity changed content"))
        observed[snapshot_id] = digest
    return findings


def _snapshot_endpoint_findings(
    snapshots: tuple[tuple[str, Mapping[str, Any]], ...],
    previous_items: Mapping[str, Any],
    current_items: Mapping[str, Any],
) -> list[Finding]:
    if len(snapshots) < 2 or snapshots[0][0] == snapshots[-1][0]:
        return [
            Finding(
                "SNAPSHOT_HISTORY_INVALID",
                "snapshots",
                "distinct prior and current governed snapshot identities are required",
            )
        ]
    findings: list[Finding] = []
    if snapshots[0][1] != previous_items:
        findings.append(
            Finding("SNAPSHOT_HISTORY_INVALID", "previous_items", "prior state is not the first snapshot")
        )
    if snapshots[-1][1] != current_items:
        findings.append(
            Finding("SNAPSHOT_HISTORY_INVALID", "current_items", "current state is not the last snapshot")
        )
    return findings


def _expected_changes(
    previous_items: Mapping[str, Any], current_items: Mapping[str, Any]
) -> dict[str, dict[str, Any]]:
    return {
        item_id: {"item_id": item_id, "before": previous_items.get(item_id), "after": current_items.get(item_id)}
        for item_id in sorted(set(previous_items) | set(current_items))
        if previous_items.get(item_id) != current_items.get(item_id)
    }


def _delta_changes(
    deltas: list[dict[str, Any]], findings: list[Finding]
) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    changes: dict[str, dict[str, Any]] = {}
    digests: dict[str, str] = {}
    for delta in deltas:
        delta_id = delta.get("delta_id")
        rows = delta.get("changes")
        if not isinstance(delta_id, str) or not delta_id or not isinstance(rows, list):
            findings.append(Finding("DELTA_INVALID", "delta", "delta identity/changes are malformed"))
            continue
        if delta_id in digests:
            findings.append(Finding("DELTA_DUPLICATE", delta_id, "delta identity is applied more than once"))
            continue
        digests[delta_id] = _digest(delta)
        for row in rows:
            item_id = row.get("item_id") if isinstance(row, dict) else None
            if not isinstance(item_id, str) or item_id in changes:
                findings.append(Finding("DELTA_CHANGE_DUPLICATE", str(item_id), "item transition is missing or duplicated"))
                continue
            changes[item_id] = row
    return changes, digests


def _approval_findings(
    approvals: list[dict[str, Any]], delta_digests: Mapping[str, str]
) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[str] = set()
    for approval in approvals:
        delta_id = approval.get("delta_id")
        if not isinstance(delta_id, str) or delta_id in seen:
            findings.append(Finding("DELTA_APPROVAL_DUPLICATE", str(delta_id), "approval identity is invalid or duplicate"))
            continue
        seen.add(delta_id)
        valid = (
            delta_id in delta_digests
            and approval.get("delta_sha256") == delta_digests[delta_id]
            and approval.get("status") == "APPROVED"
            and approval.get("authority_role") == "Product Owner"
        )
        if not valid:
            findings.append(Finding("DELTA_APPROVAL_INVALID", delta_id, "approval does not govern exact applied delta"))
    missing = sorted(set(delta_digests) - seen)
    if missing:
        findings.append(Finding("DELTA_NOT_APPROVED", "deltas", ", ".join(missing)))
    return findings


def _tombstone_findings(
    tombstones: list[dict[str, Any]],
    previous_items: Mapping[str, Any],
    current_items: Mapping[str, Any],
    delta_ids: set[str],
) -> list[Finding]:
    findings: list[Finding] = []
    removed = set(previous_items) - set(current_items)
    seen: set[str] = set()
    for tombstone in tombstones:
        item_id = tombstone.get("item_id")
        delta_id = tombstone.get("delta_id")
        valid = (
            isinstance(item_id, str)
            and item_id in removed
            and item_id not in seen
            and delta_id in delta_ids
            and tombstone.get("prior_item_sha256") == _digest(previous_items[item_id])
        )
        if not valid:
            findings.append(Finding("TOMBSTONE_INVALID", str(item_id), "tombstone is malformed, active, duplicate or unexplained"))
        elif isinstance(item_id, str):
            seen.add(item_id)
    missing = sorted(removed - seen)
    if missing:
        findings.append(Finding("TOMBSTONE_REQUIRED", "tombstones", ", ".join(missing)))
    return findings


def validate_snapshot_tombstone_delta_history(
    repository_root: Path,
    snapshots: Iterable[tuple[str, Mapping[str, Any]]],
    *,
    previous_items: Mapping[str, Any],
    current_items: Mapping[str, Any],
    tombstone_references: Iterable[Mapping[str, Any]],
    delta_references: Iterable[Mapping[str, Any]],
    approval_references: Iterable[Mapping[str, Any]],
) -> list[Finding]:
    snapshot_history = tuple(snapshots)
    findings = _snapshot_findings(snapshot_history)
    findings.extend(
        _snapshot_endpoint_findings(snapshot_history, previous_items, current_items)
    )
    deltas, delta_findings = _governed_records(
        repository_root, delta_references, record_type="PORTFOLIO_DELTA", finding_code="DELTA_INVALID"
    )
    approvals, approval_load_findings = _governed_records(
        repository_root,
        approval_references,
        record_type="PORTFOLIO_DELTA_APPROVAL",
        finding_code="DELTA_APPROVAL_INVALID",
        expected_role="Product Owner",
    )
    tombstones, tombstone_load_findings = _governed_records(
        repository_root,
        tombstone_references,
        record_type="PORTFOLIO_TOMBSTONE",
        finding_code="TOMBSTONE_INVALID",
    )
    findings.extend((*delta_findings, *approval_load_findings, *tombstone_load_findings))
    observed_changes, delta_digests = _delta_changes(deltas, findings)
    expected_changes = _expected_changes(previous_items, current_items)
    if observed_changes != expected_changes:
        findings.append(Finding("DELTA_TRANSITION_MISMATCH", "deltas", "deltas do not exactly explain prior-to-current transition"))
    findings.extend(_approval_findings(approvals, delta_digests))
    findings.extend(_tombstone_findings(tombstones, previous_items, current_items, set(delta_digests)))
    return sorted(set(findings))
