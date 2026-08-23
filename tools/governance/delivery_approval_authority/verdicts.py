from __future__ import annotations

import re
from typing import Any

from .canonical import CanonicalizationError, canonical_json_bytes
from .crypto import digest, instant
from .schemas import SchemaSet


SCOPE = "DSGEOREF-DELIVERY-APPROVAL-AUTHORITY-V1"
ROLE_DECISIONS = {"Executor": "DELIVERED", "QA": "APPROVE", "Reviewer": "APPROVE"}
ZERO_SHA = "0" * 40
EPOCH = "1970-01-01T00:00:00Z"


def fail_context(
    task: Any,
    candidate_sha: Any,
    verification_time: Any,
) -> tuple[dict[str, Any], str, str]:
    safe_task = task if isinstance(task, dict) else {}
    try:
        canonical_json_bytes(safe_task)
    except (CanonicalizationError, TypeError, ValueError):
        safe_task = {}
    safe_sha = candidate_sha if isinstance(candidate_sha, str) else ""
    if re.fullmatch(r"[0-9a-f]{40}", safe_sha) is None:
        safe_sha = ZERO_SHA
    safe_time = verification_time if isinstance(verification_time, str) else EPOCH
    try:
        instant(safe_time)
    except ValueError:
        safe_time = EPOCH
    return safe_task, safe_sha, safe_time


def verdict(
    schemas: SchemaSet,
    status: str,
    code: str,
    task: dict[str, Any],
    candidate_sha: str,
    profile: dict[str, Any],
    verification_time: str,
    subjects: dict[str, set[str]] | None = None,
) -> dict[str, Any]:
    accountable = subjects or {role: set() for role in ROLE_DECISIONS}
    result = {
        "schema_version": "1.0.0",
        "status": status,
        "code": code,
        "trust_scope": SCOPE,
        "profile": {
            "profile_id": profile.get("profile_id", "invalid"),
            "profile_version": profile.get("profile_version", "invalid"),
        },
        "task_envelope": {
            "task_id": task.get("task_id", "INVALID"),
            "digest_sha256": digest(task),
        },
        "candidate_sha": candidate_sha,
        "verification_time": verification_time,
        "validated_roles": list(ROLE_DECISIONS) if status == "PASS" else [],
        "accountable_subjects": {
            role: sorted(accountable[role]) if status == "PASS" else []
            for role in ROLE_DECISIONS
        },
    }
    schemas.validate_verdict(result)
    return result
