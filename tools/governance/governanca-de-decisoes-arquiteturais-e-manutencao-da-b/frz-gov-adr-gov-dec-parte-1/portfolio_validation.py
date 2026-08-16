from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping
from typing import Any

from canonical_json import CanonicalizationError, canonical_json_bytes
from foundation_validation_types import Finding


def validate_snapshot_tombstone_delta_history(
    snapshots: Iterable[tuple[str, Mapping[str, Any]]],
    *,
    previous_item_ids: Iterable[str],
    current_item_ids: Iterable[str],
    tombstoned_item_ids: Iterable[str],
    applied_delta_ids: Iterable[str],
    approved_delta_ids: Iterable[str],
) -> list[Finding]:
    findings: list[Finding] = []
    observed_digests: dict[str, str] = {}
    for snapshot_id, snapshot in snapshots:
        try:
            digest = hashlib.sha256(canonical_json_bytes(snapshot)).hexdigest()
        except CanonicalizationError as error:
            findings.append(Finding("SNAPSHOT_INVALID", snapshot_id, str(error)))
            continue
        previous_digest = observed_digests.get(snapshot_id)
        if previous_digest is not None and previous_digest != digest:
            findings.append(
                Finding(
                    "SNAPSHOT_MUTATED",
                    snapshot_id,
                    "historical snapshot identity resolves to different content",
                )
            )
        observed_digests[snapshot_id] = digest

    previous = frozenset(previous_item_ids)
    current = frozenset(current_item_ids)
    tombstones = frozenset(tombstoned_item_ids)
    missing_tombstones = sorted((previous - current) - tombstones)
    if missing_tombstones:
        findings.append(
            Finding(
                "TOMBSTONE_REQUIRED",
                "tombstoned_item_ids",
                f"removed items lack tombstones: {', '.join(missing_tombstones)}",
            )
        )

    applied = frozenset(applied_delta_ids)
    approved = frozenset(approved_delta_ids)
    unapproved = sorted(applied - approved)
    if unapproved:
        findings.append(
            Finding(
                "DELTA_NOT_APPROVED",
                "applied_delta_ids",
                f"applied deltas lack approval: {', '.join(unapproved)}",
            )
        )
    return sorted(findings)
