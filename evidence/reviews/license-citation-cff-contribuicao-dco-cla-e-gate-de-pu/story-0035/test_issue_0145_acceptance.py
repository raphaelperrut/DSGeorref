"""Executable acceptance evidence for ISSUE-0145.

The public entrypoints reuse the governed EPIC-007 suites and bind the review
to the immutable ISSUE-0144 candidate. They do not copy publication rules or
mint an independent QA approval.
"""

from __future__ import annotations

import copy
import hashlib
import json
import runpy
import subprocess
import sys
from collections.abc import Callable, Mapping
from functools import cache
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[4]
SLUG = "license-citation-cff-contribuicao-dco-cla-e-gate-de-pu"
REVIEW_EVIDENCE = Path(__file__).with_name("REVIEW_EVIDENCE.json")
FOUNDATION_SUITE = ROOT / f"tests/fnd/{SLUG}/test_foundation.py"
CONTRACT_SUITE = ROOT / f"tests/fnd/{SLUG}/test_contract.py"
AUTOMATION_SUITE = ROOT / f"tests/fnd/{SLUG}/test_automation.py"
INTEGRATION_SUITE = ROOT / f"tools/governance/{SLUG}/test_repository_integration.py"
EXPECTED_CANDIDATE = "8cd5884ec495b6e23a57d22eccba25e30a7d6d53"
EXPECTED_REQUIREMENTS = {"REQ-CIT-001", "REQ-EPIC-042", "REQ-OSS-001", "REQ-PUB-002"}
EXPECTED_AC_IDS = [f"AC-ISSUE-0145-{index:02d}" for index in range(1, 5)]
EXPECTED_TESTS = [
    "test_epic_007_aceite_happy_path",
    "test_epic_007_aceite_negative_paths",
]


@cache
def _suite(path: Path) -> dict[str, object]:
    suite_directory = str(path.parent)
    sys.path.insert(0, suite_directory)
    try:
        return runpy.run_path(str(path))
    finally:
        sys.path.remove(suite_directory)


def _run(path: Path, entrypoint: str) -> None:
    candidate = _suite(path).get(entrypoint)
    assert isinstance(candidate, Callable), f"missing governed entrypoint: {entrypoint}"
    candidate()


def _load_evidence() -> dict[str, Any]:
    loaded = json.loads(REVIEW_EVIDENCE.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_text(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def _candidate_blob(path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{EXPECTED_CANDIDATE}:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stderr.decode(errors="replace")
    return completed.stdout


def _assert_review_evidence(evidence: Mapping[str, Any]) -> None:
    assert evidence.get("issue_id") == "ISSUE-0145"
    assert evidence.get("reviewed_issue_id") == "ISSUE-0144"
    assert evidence.get("candidate_sha") == EXPECTED_CANDIDATE
    assert evidence.get("acceptance_criteria") == EXPECTED_AC_IDS
    assert evidence.get("acceptance_tests") == EXPECTED_TESTS
    assert evidence.get("requirements_evidence") == dict.fromkeys(
        sorted(EXPECTED_REQUIREMENTS), "test_epic_007_aceite_happy_path"
    )
    assert evidence.get("implicit_approval") is False
    assert evidence.get("contract_impact") == "NONE"
    assert evidence.get("migration_required") is False
    assert evidence.get("publication") == {
        "decision": "BLOCKED",
        "failure_mode": "FAIL_CLOSED",
        "distribution_readiness_claimed": False,
    }

    hosted = evidence.get("hosted_validation")
    assert isinstance(hosted, Mapping)
    assert hosted.get("head_sha") == EXPECTED_CANDIDATE
    assert hosted.get("required_checks") == "PASS"

    artifacts = evidence.get("candidate_artifacts")
    assert isinstance(artifacts, list) and artifacts
    for artifact in artifacts:
        assert isinstance(artifact, Mapping)
        path = artifact.get("path")
        digest = artifact.get("sha256")
        assert isinstance(path, str) and path
        assert isinstance(digest, str) and len(digest) == 64
        assert _sha256(_canonical_text(ROOT / path)) == digest
        assert _sha256(_candidate_blob(path)) == digest

    coordination = evidence.get("coordination")
    assert isinstance(coordination, list) and len(coordination) == 2
    by_role = {
        item.get("role"): item for item in coordination if isinstance(item, Mapping)
    }
    assert set(by_role) == {"QA", "Reviewer"}
    reviewer = by_role["Reviewer"]
    qa = by_role["QA"]
    assert reviewer.get("decision") == "PASS"
    assert qa.get("decision") == "PENDING"
    assert reviewer.get("candidate_sha") == qa.get("candidate_sha") == EXPECTED_CANDIDATE
    assert reviewer.get("evidence_paths") == qa.get("evidence_paths")
    assert reviewer.get("residual_risk_ids") == qa.get("residual_risk_ids")

    risks = evidence.get("residual_risks")
    assert isinstance(risks, list) and risks
    risk_ids = {risk.get("id") for risk in risks if isinstance(risk, Mapping)}
    assert risk_ids == set(reviewer.get("residual_risk_ids", []))


def test_epic_007_aceite_happy_path() -> None:
    """Prove the candidate artifacts and governed contract-to-integration path."""

    _assert_review_evidence(_load_evidence())
    _run(CONTRACT_SUITE, "test_epic_007_contrato")
    _run(FOUNDATION_SUITE, "test_epic_007_fundacao")
    _run(INTEGRATION_SUITE, "test_epic_007_integracao")


def test_epic_007_aceite_negative_paths() -> None:
    """Prove fail-closed controls and reject ambiguous review coordination."""

    _run(CONTRACT_SUITE, "test_contract_rejects_silent_fallback_and_invalid_governance")
    _run(AUTOMATION_SUITE, "test_epic_007_automacao")
    for entrypoint in (
        "test_integration_rejects_failed_or_malformed_foundation_report",
        "test_integration_rejects_failed_or_permissive_automation_report",
        "test_integration_converts_predecessor_timeout_to_fail_closed_report",
        "test_integration_rejects_task_identity_scope_and_phase_f_drift",
        "test_integration_control_plane_has_no_cross_module_import_or_rule_copy",
    ):
        _run(INTEGRATION_SUITE, entrypoint)

    sha_mismatch = copy.deepcopy(_load_evidence())
    sha_mismatch["coordination"][1]["candidate_sha"] = "0" * 40
    with pytest.raises(AssertionError):
        _assert_review_evidence(sha_mismatch)

    digest_mismatch = copy.deepcopy(_load_evidence())
    digest_mismatch["candidate_artifacts"][0]["sha256"] = "0" * 64
    with pytest.raises(AssertionError):
        _assert_review_evidence(digest_mismatch)

    implicit_approval = copy.deepcopy(_load_evidence())
    implicit_approval["implicit_approval"] = True
    with pytest.raises(AssertionError):
        _assert_review_evidence(implicit_approval)

    invented_qa_approval = copy.deepcopy(_load_evidence())
    invented_qa_approval["coordination"][1]["decision"] = "PASS"
    with pytest.raises(AssertionError):
        _assert_review_evidence(invented_qa_approval)
