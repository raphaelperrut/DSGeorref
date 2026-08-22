from __future__ import annotations

from typing import Any

from .crypto import digest, instant
from .records import attestation_code, profile_code
from .repository import GovernedTrust
from .schemas import SchemaSet
from .verdicts import ROLE_DECISIONS, verdict


class OperationalVerifier:
    """Verifier bound to trust loaded from one governed repository revision."""

    def __init__(self, trust: GovernedTrust, schemas: SchemaSet) -> None:
        self._trust = trust
        self._schemas = schemas

    def verify(
        self,
        *,
        evidence: Any,
        task_envelope: dict[str, Any],
        candidate_sha: str,
        verification_time: str,
    ) -> dict[str, Any]:
        try:
            return self._verify(
                evidence=evidence,
                task=task_envelope,
                candidate_sha=candidate_sha,
                verification_time=verification_time,
            )
        except (KeyError, TypeError, ValueError):
            return self._failure(
                "SCHEMA_INVALID",
                task_envelope,
                candidate_sha,
                verification_time,
            )

    def _failure(
        self,
        code: str,
        task: dict[str, Any],
        candidate_sha: str,
        verification_time: str,
    ) -> dict[str, Any]:
        return verdict(
            self._schemas,
            "FAIL",
            code,
            task,
            candidate_sha,
            self._trust.profile,
            verification_time,
        )

    def _verify(
        self,
        *,
        evidence: Any,
        task: dict[str, Any],
        candidate_sha: str,
        verification_time: str,
    ) -> dict[str, Any]:
        if not isinstance(evidence, dict) or set(evidence) != {"bindings", "attestations"}:
            return self._failure("SCHEMA_INVALID", task, candidate_sha, verification_time)
        bindings, attestations = evidence["bindings"], evidence["attestations"]
        if not isinstance(bindings, list) or not isinstance(attestations, list):
            return self._failure("SCHEMA_INVALID", task, candidate_sha, verification_time)
        if not all(isinstance(record, dict) for record in (*bindings, *attestations)):
            return self._failure("SCHEMA_INVALID", task, candidate_sha, verification_time)
        checked_at = instant(verification_time)
        code = profile_code(
            self._schemas,
            self._trust.anchors,
            self._trust.profile,
            checked_at,
        )
        if code is not None:
            return self._failure(code, task, candidate_sha, verification_time)
        if self._schemas.code("task", task) is not None:
            return self._failure("TASK_ENVELOPE_INVALID", task, candidate_sha, verification_time)
        task_id, task_digest = task["task_id"], digest(task)
        subjects = {role: set() for role in ROLE_DECISIONS}
        for record in attestations:
            code = attestation_code(
                self._schemas,
                record,
                bindings,
                self._trust.profile,
                task_id,
                task_digest,
                candidate_sha,
                checked_at,
            )
            if code is not None:
                return self._failure(code, task, candidate_sha, verification_time)
            subjects[record["role"]].add(record["accountable_subject"])
        if any(not subjects[role] for role in ROLE_DECISIONS):
            return self._failure("APPROVAL_MISSING", task, candidate_sha, verification_time)
        pairs = (("Executor", "QA"), ("Executor", "Reviewer"), ("QA", "Reviewer"))
        if any(subjects[left] & subjects[right] for left, right in pairs):
            return self._failure("INDEPENDENCE_VIOLATION", task, candidate_sha, verification_time)
        return verdict(
            self._schemas,
            "PASS",
            "APPROVAL_AUTHORITY_VERIFIED",
            task,
            candidate_sha,
            self._trust.profile,
            verification_time,
            subjects,
        )
