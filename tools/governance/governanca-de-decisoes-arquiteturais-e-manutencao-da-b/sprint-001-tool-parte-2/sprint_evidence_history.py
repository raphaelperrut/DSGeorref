from __future__ import annotations

import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from slice_one import (
    AppendOnlyRecordLedger,
    Finding,
    canonical_json_bytes,
    git_blob,
    load_json_bytes,
    resolve_governed_artifact,
)


class SprintEvidenceLedger:
    def __init__(self) -> None:
        self._ledger = AppendOnlyRecordLedger()

    @staticmethod
    def _envelope(record: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "record_type": "FOUNDATION_CLOSURE_EVIDENCE_SET",
            "evidence_set_id": record.get("evidence_set_id"),
            "sprint_evidence_record": dict(record),
        }

    def append(self, record: Mapping[str, Any]) -> None:
        self._ledger.append(self._envelope(record))

    def contains_exactly(self, record: Mapping[str, Any]) -> bool:
        return self._ledger.contains_exactly(self._envelope(record))


def governed_sprint_evidence(
    repository_root: Path,
    reference: Mapping[str, Any],
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> tuple[dict[str, Any] | None, list[Finding]]:
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        record = artifact.json_object()
    except ValueError as error:
        return None, [Finding("GOVERNED_SPRINT_EVIDENCE_INVALID", "$", str(error))]
    from sprint_evidence import validate_sprint_evidence_set

    findings = validate_sprint_evidence_set(
        repository_root, record, delivery_gate=delivery_gate
    )
    if artifact.content != canonical_json_bytes(record):
        findings.append(
            Finding("GOVERNED_SPRINT_EVIDENCE_INVALID", "$", "record is not canonical JSON")
        )
    findings.extend(
        _append_only_history_findings(
            repository_root,
            artifact.source_revision,
            artifact.path,
            record,
        )
    )
    return record, sorted(findings)


def _append_only_history_findings(
    repository_root: Path,
    source_revision: str,
    path: str,
    current: Mapping[str, Any],
) -> list[Finding]:
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(repository_root),
            "log",
            "--format=@@%H",
            "--name-only",
            "--diff-filter=AM",
            "--reverse",
            source_revision,
        ],
        check=False,
        capture_output=True,
        encoding="ascii",
    )
    if completed.returncode != 0:
        return [Finding("EVIDENCE_HISTORY_INVALID", path, "Git history is unavailable")]
    ledger = SprintEvidenceLedger()
    observed_current = False
    revision: str | None = None
    locations: set[str] = set()
    for line in completed.stdout.splitlines():
        if line.startswith("@@"):
            revision = line.removeprefix("@@")
            continue
        historical_path = line.strip()
        if revision is None or not historical_path.endswith(".json"):
            continue
        try:
            historical = load_json_bytes(
                git_blob(repository_root, revision, historical_path)
            )
        except ValueError:
            continue
        if not isinstance(historical, Mapping) or historical.get("evidence_set_id") != current.get(
            "evidence_set_id"
        ):
            continue
        locations.add(historical_path)
        try:
            ledger.append(historical)
        except ValueError as error:
            return [Finding("EVIDENCE_HISTORY_INVALID", path, str(error))]
        if (
            revision == source_revision
            and historical_path == path
            and canonical_json_bytes(historical) == canonical_json_bytes(current)
        ):
            observed_current = True
    if len(locations) != 1:
        return [
            Finding(
                "EVIDENCE_HISTORY_INVALID",
                path,
                "evidence identity must have one immutable governed path",
            )
        ]
    if not observed_current or not ledger.contains_exactly(current):
        return [Finding("EVIDENCE_HISTORY_INVALID", path, "current record is absent from history")]
    return []
