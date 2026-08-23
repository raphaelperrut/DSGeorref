from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[4]
MODULE_ROOT = ROOT / (
    "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "consolidacao"
)
sys.path.insert(0, str(MODULE_ROOT))

import slice_consolidation as consolidation  # noqa: E402
from candidate_repository import CandidateView  # noqa: E402


validate_slice_consolidation = consolidation.validate_slice_consolidation


def _candidate() -> str:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        encoding="ascii",
    )
    return completed.stdout.strip()


def _review(candidate: str) -> dict[str, object]:
    return {
        "record_type": "SLICE_CONSOLIDATION_REVIEW",
        "authority_role": "Reviewer",
        "reviewed_story_id": "STORY-0002",
        "reviewed_candidate_commit": candidate,
        "executor_subject": "executor-fixture",
        "reviewer_subject": "reviewer-fixture",
        "result": "PASS",
        "residual_risks": [],
        "released_dependents": ["STORY-0004"],
    }


def test_story_0002_slice_consolidation() -> None:
    candidate = _candidate()
    result = validate_slice_consolidation(ROOT, candidate, _review(candidate))

    assert result.ready, result.findings
    assert result.dependency_story_ids == ("STORY-0688", "STORY-0689")
    assert len(result.requirement_ids) == 20
    assert result.released_dependents == ("STORY-0004",)


def test_slice_consolidation_requires_independent_review() -> None:
    result = validate_slice_consolidation(ROOT, _candidate(), None)

    assert not result.ready
    assert [finding.code for finding in result.findings] == ["REVIEW_EVIDENCE_REQUIRED"]
    assert result.released_dependents == ()


def test_slice_consolidation_rejects_review_for_another_candidate() -> None:
    candidate = _candidate()
    review = _review(candidate)
    review["reviewed_candidate_commit"] = "0" * 40

    result = validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert [finding.code for finding in result.findings] == ["REVIEW_EVIDENCE_INVALID"]
    assert result.released_dependents == ()


def test_ac01_rejects_canonically_blocked_slice() -> None:
    candidate = _candidate()
    original_blob = CandidateView.blob

    def blocked_story(view: CandidateView, path: str) -> bytes:
        content = original_blob(view, path)
        if "STORY-0689-ISSUE-0799" in path:
            return content.replace(b"**Estado:** `Done`", b"**Estado:** `Blocked`")
        return content

    with patch.object(CandidateView, "blob", blocked_story):
        result = validate_slice_consolidation(ROOT, candidate, _review(candidate))

    assert not result.ready
    assert "SLICE_COMPLETION_STATE_INVALID" in {
        finding.code for finding in result.findings
    }
    assert result.released_dependents == ()


def test_ac04_never_releases_when_any_finding_remains() -> None:
    candidate = _candidate()
    forced = consolidation.Finding("FORCED_BLOCKER", "baseline", "incomplete")

    with patch.object(consolidation, "_baseline_findings", return_value=[forced]):
        result = validate_slice_consolidation(ROOT, candidate, _review(candidate))

    assert not result.ready
    assert forced in result.findings
    assert result.released_dependents == ()
