from __future__ import annotations

from typing import Any

from .crypto import digest, instant
from .records import attestation_code, profile_code
from .repository import GovernedTrust
from .schemas import SchemaSet
from .verdicts import ROLE_DECISIONS, SOLO_ROLES, solo_verdict, verdict


class OperationalVerifier:
    """Verifier bound to trust loaded from one governed repository revision."""

    def __init__(self, trust: GovernedTrust, schemas: SchemaSet) -> None:
        self._trust = trust
        self._schemas = schemas.for_contract_version(trust.contract_version)

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
        if self._trust.contract_version == "2.0.0":
            return solo_verdict(
                self._schemas,
                "FAIL",
                code,
                task,
                candidate_sha,
                self._trust.profile,
                verification_time,
            )
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
        if self._trust.contract_version == "2.0.0":
            return self._verify_solo(
                bindings,
                attestations,
                task,
                candidate_sha,
                verification_time,
                checked_at,
            )
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

    def _verify_solo(
        self,
        bindings: list[dict[str, Any]],
        attestations: list[dict[str, Any]],
        task: dict[str, Any],
        candidate_sha: str,
        verification_time: str,
        checked_at: Any,
    ) -> dict[str, Any]:
        task_envelope = {"task_id": task["task_id"], "digest_sha256": digest(task)}
        policies = [
            policy
            for policy in self._trust.profile["governance_policies"]
            if policy["task_envelope"] == task_envelope
        ]
        if len(policies) != 1:
            return self._failure(
                "GOVERNANCE_MODE_UNAUTHORIZED", task, candidate_sha, verification_time
            )
        policy = policies[0]
        if (
            policy["governance_mode"] != "SOLO_FUNCTIONAL_SEGREGATION_V1"
            or policy["personal_independence"] != "ABSENT_DECLARED"
        ):
            return self._failure(
                "GOVERNANCE_MODE_UNAUTHORIZED", task, candidate_sha, verification_time
            )
        if len(bindings) != len(SOLO_ROLES) or len(attestations) != len(SOLO_ROLES):
            return self._failure("APPROVAL_MISSING", task, candidate_sha, verification_time)
        if any(self._schemas.code("binding", item) is not None for item in bindings):
            return self._failure("BINDING_INVALID", task, candidate_sha, verification_time)

        binding_by_role: dict[str, dict[str, Any]] = {}
        attestation_by_role: dict[str, dict[str, Any]] = {}
        for role in SOLO_ROLES:
            role_bindings = [item for item in bindings if item.get("role") == role]
            role_attestations = [item for item in attestations if item.get("role") == role]
            if len(role_bindings) != 1 or len(role_attestations) != 1:
                return self._failure(
                    "ROLE_RECORD_AMBIGUOUS", task, candidate_sha, verification_time
                )
            binding_by_role[role] = role_bindings[0]
            attestation_by_role[role] = role_attestations[0]

        ordered = [attestation_by_role[role] for role in SOLO_ROLES]
        for record in ordered:
            code = attestation_code(
                self._schemas,
                record,
                bindings,
                self._trust.profile,
                task["task_id"],
                task_envelope["digest_sha256"],
                candidate_sha,
                checked_at,
            )
            if code is not None:
                return self._failure(code, task, candidate_sha, verification_time)

        principal_pairs = {
            (record["principal"]["issuer"], record["principal"]["subject"])
            for record in ordered
        }
        accountable_subjects = {record["accountable_subject"] for record in ordered}
        if len(principal_pairs) != 1:
            return self._failure("PRINCIPAL_MISMATCH", task, candidate_sha, verification_time)
        if len(accountable_subjects) != 1:
            return self._failure(
                "ACCOUNTABLE_SUBJECT_MISMATCH", task, candidate_sha, verification_time
            )
        if any(
            record["personal_independence"] != "ABSENT_DECLARED" for record in ordered
        ):
            return self._failure(
                "PERSONAL_INDEPENDENCE_INVALID", task, candidate_sha, verification_time
            )

        unique_groups = (
            [record["binding"]["binding_id"] for record in ordered],
            [record["attestation_id"] for record in ordered],
            [record["functional_session"]["session_id"] for record in ordered],
        )
        if any(len(values) != len(set(values)) for values in unique_groups):
            return self._failure("SESSION_REUSE", task, candidate_sha, verification_time)
        key_ids = [record["signature"]["key_id"] for record in ordered]
        if len(key_ids) != len(set(key_ids)):
            return self._failure("KEY_REUSE", task, candidate_sha, verification_time)

        snapshots = {
            record["functional_session"]["input_snapshot_digest_sha256"]
            for record in ordered
        }
        if len(snapshots) != 1:
            return self._failure(
                "SESSION_SNAPSHOT_MISMATCH", task, candidate_sha, verification_time
            )

        previous: dict[str, Any] | None = None
        for sequence, (role, record) in enumerate(zip(SOLO_ROLES, ordered, strict=True), 1):
            session = record["functional_session"]
            if session["role"] != role or session["sequence"] != sequence:
                return self._failure(
                    "SESSION_SEQUENCE_INVALID", task, candidate_sha, verification_time
                )
            started_at = instant(session["started_at"])
            issued_at = instant(record["issued_at"])
            if started_at > issued_at:
                return self._failure(
                    "SESSION_TEMPORAL_INVALID", task, candidate_sha, verification_time
                )
            if previous is None:
                if session["predecessor_attestation_digest_sha256"] is not None:
                    return self._failure(
                        "PREDECESSOR_MISMATCH", task, candidate_sha, verification_time
                    )
            else:
                if started_at <= instant(previous["issued_at"]):
                    return self._failure(
                        "SESSION_TEMPORAL_INVALID", task, candidate_sha, verification_time
                    )
                if session["predecessor_attestation_digest_sha256"] != digest(previous):
                    return self._failure(
                        "PREDECESSOR_MISMATCH", task, candidate_sha, verification_time
                    )
            previous = record

        verifier_input = {
            "task_envelope": task_envelope,
            "candidate_sha": candidate_sha,
            "bindings": [
                {"role": role, "digest_sha256": digest(binding_by_role[role])}
                for role in SOLO_ROLES
            ],
            "attestations": [
                {"role": role, "digest_sha256": digest(attestation_by_role[role])}
                for role in SOLO_ROLES[:-1]
            ],
        }
        for record in ordered[:-1]:
            if record["functional_session"]["verifier_input_set_digest_sha256"] is not None:
                return self._failure(
                    "VERIFIER_INPUT_SET_MISMATCH", task, candidate_sha, verification_time
                )
        owner = attestation_by_role["Project Owner"]
        if owner["functional_session"]["verifier_input_set_digest_sha256"] != digest(
            verifier_input
        ):
            return self._failure(
                "VERIFIER_INPUT_SET_MISMATCH", task, candidate_sha, verification_time
            )

        decisions = {record["role"]: record["decision"] for record in ordered}
        if decisions["Executor"] != "DELIVERED":
            return self._failure("DECISION_INVALID", task, candidate_sha, verification_time)
        if decisions["QA"] not in {"APPROVE", "REJECT"}:
            return self._failure("DECISION_INVALID", task, candidate_sha, verification_time)
        if decisions["Reviewer"] not in {"APPROVE", "REJECT"}:
            return self._failure("DECISION_INVALID", task, candidate_sha, verification_time)
        if decisions["Project Owner"] == "NO_GO":
            return solo_verdict(
                self._schemas,
                "FAIL",
                "OWNER_NO_GO",
                task,
                candidate_sha,
                self._trust.profile,
                verification_time,
                formal_decision="NO_GO",
            )
        if decisions["Project Owner"] != "PASS" or (
            decisions["QA"] != "APPROVE" or decisions["Reviewer"] != "APPROVE"
        ):
            return self._failure("DECISION_INVALID", task, candidate_sha, verification_time)

        return solo_verdict(
            self._schemas,
            "PASS",
            "APPROVAL_AUTHORITY_VERIFIED",
            task,
            candidate_sha,
            self._trust.profile,
            verification_time,
            accountable_subject=next(iter(accountable_subjects)),
            sessions=[record["functional_session"]["session_id"] for record in ordered],
            formal_decision="PASS",
        )
