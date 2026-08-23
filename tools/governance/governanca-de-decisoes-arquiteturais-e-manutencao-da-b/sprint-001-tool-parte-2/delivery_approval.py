from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from tools.governance.delivery_approval_authority import verify_delivery_approval

from slice_one import Finding, canonical_json_bytes


REQUIRED_ROLES = frozenset({"Executor", "QA", "Reviewer"})


@dataclass(frozen=True)
class VerifiedDeliveryApproval:
    candidate_sha: str
    task_id: str
    accountable_subjects: Mapping[str, tuple[str, ...]]


class DeliveryApprovalGate:
    """Adapter to the operational verifier published by ISSUE-0871.

    The operational boundary resolves its repository, revision, anchors and profile
    internally. This adapter accepts only untrusted records plus trusted decision
    context and cannot be configured with a caller-selected verifier or trust set.
    """

    def __init__(self) -> None:
        self._cache: dict[
            str, tuple[VerifiedDeliveryApproval | None, tuple[Finding, ...]]
        ] = {}

    def verify(
        self,
        *,
        evidence: Mapping[str, Any],
        task_envelope: Mapping[str, Any],
        candidate_sha: str,
        verification_time: str,
    ) -> tuple[VerifiedDeliveryApproval | None, list[Finding]]:
        cache_key = hashlib.sha256(
            canonical_json_bytes(
                {
                    "candidate_sha": candidate_sha,
                    "evidence": evidence,
                    "task_envelope": task_envelope,
                    "verification_time": verification_time,
                }
            )
        ).hexdigest()
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached[0], list(cached[1])
        try:
            verdict = verify_delivery_approval(
                evidence=dict(evidence),
                task_envelope=dict(task_envelope),
                expected_candidate_sha=candidate_sha,
                verification_time=verification_time,
            )
        except (AssertionError, KeyError, TypeError, ValueError) as error:
            return None, [_finding(f"DAA verification failed closed: {error}")]
        expected_task = task_envelope.get("task_id")
        if not _complete_verdict(verdict, expected_task, candidate_sha):
            code = verdict.get("code") if isinstance(verdict, Mapping) else "INVALID"
            return None, [_finding(f"DAA rejected approval set: {code}")]
        subjects = verdict["accountable_subjects"]
        approval = VerifiedDeliveryApproval(
                candidate_sha=candidate_sha,
                task_id=str(expected_task),
                accountable_subjects={
                    role: tuple(sorted(subjects[role])) for role in sorted(REQUIRED_ROLES)
                },
            )
        self._cache[cache_key] = (approval, ())
        return approval, []

def _complete_verdict(
    verdict: object, expected_task: object, candidate_sha: str
) -> bool:
    if not isinstance(verdict, Mapping):
        return False
    task = verdict.get("task_envelope")
    subjects = verdict.get("accountable_subjects")
    return bool(
        verdict.get("status") == "PASS"
        and verdict.get("code") == "APPROVAL_AUTHORITY_VERIFIED"
        and verdict.get("candidate_sha") == candidate_sha
        and isinstance(task, Mapping)
        and task.get("task_id") == expected_task
        and set(verdict.get("validated_roles", [])) == REQUIRED_ROLES
        and isinstance(subjects, Mapping)
        and set(subjects) == REQUIRED_ROLES
        and all(isinstance(subjects[role], list) and subjects[role] for role in REQUIRED_ROLES)
    )


def _finding(detail: str) -> Finding:
    return Finding("DELIVERY_APPROVAL_INVALID", "delivery_approval", detail)
