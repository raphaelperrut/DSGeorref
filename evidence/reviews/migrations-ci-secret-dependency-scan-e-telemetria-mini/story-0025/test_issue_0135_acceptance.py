"""Executable acceptance evidence for ISSUE-0135.

The public entrypoints delegate to the governed EPIC-005 suites and validate
the immutable review target. They do not duplicate implementation rules or
mint a QA approval.
"""

from __future__ import annotations

import copy
import hashlib
import json
import runpy
import sys
from collections.abc import Callable, Mapping
from functools import cache
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[4]
SLUG = "migrations-ci-secret-dependency-scan-e-telemetria-mini"
REVIEW_EVIDENCE = Path(__file__).with_name("REVIEW_EVIDENCE.json")
AUTOMATION_SUITE = ROOT / f"tests/fnd/{SLUG}/test_automation.py"
INTEGRATION_SUITE = ROOT / f"tools/governance/{SLUG}/test_repository_integration.py"
EXPECTED_CANDIDATE = "780f45410d237f43b2658254fbe9742df96b9c28"
EXPECTED_AC_IDS = [f"AC-ISSUE-0135-{index:02d}" for index in range(1, 5)]
EXPECTED_TESTS = [
    "test_epic_005_aceite_happy_path",
    "test_epic_005_aceite_negative_paths",
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


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_review_evidence(evidence: Mapping[str, Any]) -> None:
    assert evidence.get("issue_id") == "ISSUE-0135"
    assert evidence.get("reviewed_issue_id") == "ISSUE-0134"
    assert evidence.get("candidate_sha") == EXPECTED_CANDIDATE
    assert evidence.get("acceptance_criteria") == EXPECTED_AC_IDS
    assert evidence.get("acceptance_tests") == EXPECTED_TESTS
    assert evidence.get("implicit_approval") is False
    assert evidence.get("contract_impact") == "NONE"
    assert evidence.get("migration_required") is False

    artifacts = evidence.get("candidate_artifacts")
    assert isinstance(artifacts, list) and artifacts
    for artifact in artifacts:
        assert isinstance(artifact, Mapping)
        path = artifact.get("path")
        digest = artifact.get("sha256")
        assert isinstance(path, str) and path
        assert isinstance(digest, str) and len(digest) == 64
        assert _sha256(ROOT / path) == digest

    coordination = evidence.get("coordination")
    assert isinstance(coordination, list) and len(coordination) == 2
    by_role = {
        item.get("role"): item
        for item in coordination
        if isinstance(item, Mapping)
    }
    assert set(by_role) == {"QA", "Reviewer"}
    reviewer = by_role["Reviewer"]
    qa = by_role["QA"]
    assert reviewer.get("decision") == "PASS"
    assert qa.get("decision") == "PENDING"
    assert reviewer.get("candidate_sha") == qa.get("candidate_sha")
    assert reviewer.get("candidate_sha") == EXPECTED_CANDIDATE
    assert reviewer.get("evidence_paths") == qa.get("evidence_paths")
    assert reviewer.get("residual_risk_ids") == qa.get("residual_risk_ids")

    risks = evidence.get("residual_risks")
    assert isinstance(risks, list) and risks
    risk_ids = {
        risk.get("id") for risk in risks if isinstance(risk, Mapping)
    }
    assert risk_ids == set(reviewer.get("residual_risk_ids", []))


def test_epic_005_aceite_happy_path() -> None:
    """Prove the candidate artifacts and their governed integration path."""

    _assert_review_evidence(_load_evidence())
    _run(INTEGRATION_SUITE, "test_batch_execution_decision_01")
    _run(INTEGRATION_SUITE, "test_batch_execution_decision_06")
    _run(INTEGRATION_SUITE, "test_first_functional_slice_decision_06")
    _run(INTEGRATION_SUITE, "test_epic_005_integracao")


def test_epic_005_aceite_negative_paths() -> None:
    """Prove fail-closed controls and reject ambiguous review coordination."""

    _run(AUTOMATION_SUITE, "test_epic_005_automacao")
    _run(
        INTEGRATION_SUITE,
        "test_integration_rejects_failed_or_malformed_quality_report",
    )
    _run(
        INTEGRATION_SUITE,
        "test_integration_rejects_unknown_requirement_and_import_cycles",
    )

    sha_mismatch = copy.deepcopy(_load_evidence())
    sha_mismatch["coordination"][1]["candidate_sha"] = "0" * 40
    with pytest.raises(AssertionError):
        _assert_review_evidence(sha_mismatch)

    implicit_approval = copy.deepcopy(_load_evidence())
    implicit_approval["implicit_approval"] = True
    with pytest.raises(AssertionError):
        _assert_review_evidence(implicit_approval)
