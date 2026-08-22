from __future__ import annotations

import copy
import hashlib
import importlib.util
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

from slice_one import Finding, canonical_json_bytes


VERIFIER_PATH = (
    "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "test_delivery_approval_authority_contract.py"
)
REQUIRED_ROLES = frozenset({"Executor", "QA", "Reviewer"})


@dataclass(frozen=True)
class VerifiedDeliveryApproval:
    candidate_sha: str
    task_id: str
    accountable_subjects: Mapping[str, tuple[str, ...]]


class DeliveryApprovalGate:
    """Trusted adapter to the verifier published by ISSUE-0870.

    Trust anchors and the profile are gate configuration, never evidence fields.
    Records passed to ``verify`` remain untrusted until the canonical verifier
    returns its complete fail-closed verdict.
    """

    def __init__(
        self,
        authority_repository: Path,
        *,
        trust_anchors: Mapping[str, Any],
        trust_profile: Mapping[str, Any],
        verification_time: str,
    ) -> None:
        self._module = _load_contract_verifier(authority_repository)
        self._trust_anchors = copy.deepcopy(dict(trust_anchors))
        self._trust_profile = copy.deepcopy(dict(trust_profile))
        self._verification_time = verification_time
        self._cache: dict[
            str, tuple[VerifiedDeliveryApproval | None, tuple[Finding, ...]]
        ] = {}

    def verify(
        self,
        *,
        evidence: Mapping[str, Any],
        task_envelope: Mapping[str, Any],
        candidate_sha: str,
    ) -> tuple[VerifiedDeliveryApproval | None, list[Finding]]:
        cache_key = hashlib.sha256(
            canonical_json_bytes(
                {
                    "candidate_sha": candidate_sha,
                    "evidence": evidence,
                    "task_envelope": task_envelope,
                }
            )
        ).hexdigest()
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached[0], list(cached[1])
        verifier = getattr(self._module, "_verify", None)
        if not callable(verifier):
            return None, [_finding("canonical DAA verifier is unavailable")]
        try:
            verdict = verifier(
                copy.deepcopy(dict(evidence)),
                copy.deepcopy(self._trust_anchors),
                copy.deepcopy(self._trust_profile),
                copy.deepcopy(dict(task_envelope)),
                candidate_sha,
                self._verification_time,
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


def _load_contract_verifier(authority_repository: Path) -> ModuleType:
    path = authority_repository / VERIFIER_PATH
    if not path.is_file():
        raise ValueError("ISSUE-0870 DAA verifier is absent")
    spec = importlib.util.spec_from_file_location("dsgeorref_daa_verifier", path)
    if spec is None or spec.loader is None:
        raise ValueError("ISSUE-0870 DAA verifier cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
