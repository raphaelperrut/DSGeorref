from __future__ import annotations

from pathlib import Path
from typing import Any

from .crypto import digest
from .repository import GovernedTrustError, resolve_governed_trust
from .schemas import SchemaSet
from .verdicts import EPOCH, SCOPE, ZERO_SHA, fail_context
from .verifier import OperationalVerifier


def _unresolved_verdict(task: Any, candidate_sha: Any, verification_time: Any) -> dict[str, Any]:
    safe_task, safe_sha, safe_time = fail_context(task, candidate_sha, verification_time)
    return {
        "schema_version": "1.0.0",
        "status": "FAIL",
        "code": "TRUST_ANCHOR_INVALID",
        "trust_scope": SCOPE,
        "profile": {"profile_id": "invalid", "profile_version": "invalid"},
        "task_envelope": {
            "task_id": safe_task.get("task_id", "INVALID"),
            "digest_sha256": digest(safe_task),
        },
        "candidate_sha": safe_sha or ZERO_SHA,
        "verification_time": safe_time or EPOCH,
        "validated_roles": [],
        "accountable_subjects": {"Executor": [], "QA": [], "Reviewer": []},
    }


def verify_delivery_approval(
    *,
    repository: Path,
    revision: str,
    task_envelope: Any,
    expected_candidate_sha: Any,
    verification_time: Any,
    evidence: Any,
) -> dict[str, Any]:
    """Return only a fail-closed DAA verdict for one governed repository revision.

    Trust profile, anchors, schemas, issuers and keys are never accepted as parameters.
    """
    try:
        schemas = SchemaSet(repository, revision)
        trust = resolve_governed_trust(repository, revision)
    except (GovernedTrustError, OSError, ValueError):
        return _unresolved_verdict(task_envelope, expected_candidate_sha, verification_time)
    safe_task, safe_sha, safe_time = fail_context(
        task_envelope,
        expected_candidate_sha,
        verification_time,
    )
    return OperationalVerifier(trust, schemas).verify(
        evidence=evidence,
        task_envelope=safe_task,
        candidate_sha=safe_sha,
        verification_time=safe_time,
    )
