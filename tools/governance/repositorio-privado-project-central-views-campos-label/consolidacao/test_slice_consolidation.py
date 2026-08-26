from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import slice_consolidation as consolidation


ROOT = Path(__file__).resolve().parents[4]
SLICE_STORIES = tuple(f"STORY-{number:04d}" for number in range(692, 701))


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
        "reviewed_story_id": "STORY-0007",
        "reviewed_candidate_commit": candidate,
        "executor_subject": "executor-fixture",
        "reviewer_subject": "reviewer-fixture",
        "result": "PASS",
        "residual_risks": [],
        "released_dependents": ["STORY-0009"],
        "completion_evidence": [],
    }


def _completion(
    story_ids: tuple[str, ...] = SLICE_STORIES,
    findings: tuple[consolidation.Finding, ...] = (),
):
    return patch.object(
        consolidation,
        "validate_governed_completion",
        return_value=(list(story_ids), list(findings)),
    )


def test_story_0007_slice_consolidation() -> None:
    candidate = _candidate()
    with _completion():
        result = consolidation.validate_slice_consolidation(ROOT, candidate, _review(candidate))

    assert result.ready, result.findings
    assert result.dependency_story_ids == SLICE_STORIES
    assert len(result.requirement_ids) == 82
    assert result.released_dependents == ("STORY-0009",)


def test_consolidation_rejects_invalid_candidate_revision() -> None:
    result = consolidation.validate_slice_consolidation(ROOT, "HEAD", None)

    assert not result.ready
    assert {finding.code for finding in result.findings} == {"CANDIDATE_INVALID"}


def test_consolidation_requires_all_governed_slice_completions() -> None:
    candidate = _candidate()
    with _completion(SLICE_STORIES[:-1]):
        result = consolidation.validate_slice_consolidation(ROOT, candidate, _review(candidate))

    assert not result.ready
    assert "SLICE_COMPLETION_UNPROVEN" in {finding.code for finding in result.findings}
    assert result.released_dependents == ()


def test_consolidation_preserves_canonical_completion_failures() -> None:
    candidate = _candidate()
    canonical = consolidation.Finding(
        "DELIVERY_APPROVAL_INVALID",
        "$.completion_evidence[0]",
        "trusted DAA approval is required",
    )
    with _completion(SLICE_STORIES, (canonical,)):
        result = consolidation.validate_slice_consolidation(ROOT, candidate, _review(candidate))

    assert canonical in result.findings
    assert result.released_dependents == ()


def test_consolidation_requires_independent_reviewer() -> None:
    candidate = _candidate()
    review = _review(candidate)
    review["reviewer_subject"] = review["executor_subject"]
    with _completion():
        result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert "REVIEW_EVIDENCE_INVALID" in {finding.code for finding in result.findings}
    assert result.released_dependents == ()


def _assert_invalid_identity(identity: str) -> None:
    candidate = _candidate()
    for field in ("executor_subject", "reviewer_subject"):
        review = _review(candidate)
        review[field] = identity
        with _completion():
            result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

        assert not result.ready, field
        assert "REVIEW_EVIDENCE_INVALID" in {
            finding.code for finding in result.findings
        }
        assert result.released_dependents == (), field


def test_consolidation_rejects_empty_identity() -> None:
    _assert_invalid_identity("")


def test_consolidation_rejects_whitespace_identity() -> None:
    _assert_invalid_identity(" \t\r\n")


def test_consolidation_rejects_same_normalized_identity() -> None:
    candidate = _candidate()
    review = _review(candidate)
    review["reviewer_subject"] = "  executor-fixture\t"
    with _completion():
        result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert "REVIEW_EVIDENCE_INVALID" in {finding.code for finding in result.findings}
    assert result.released_dependents == ()


def test_consolidation_rejects_review_for_another_candidate() -> None:
    candidate = _candidate()
    review = _review(candidate)
    review["reviewed_candidate_commit"] = "0" * 40
    with _completion():
        result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert "REVIEW_EVIDENCE_INVALID" in {finding.code for finding in result.findings}
    assert result.released_dependents == ()


def test_consolidation_does_not_self_release_without_review() -> None:
    candidate = _candidate()
    with _completion():
        result = consolidation.validate_slice_consolidation(ROOT, candidate, None)

    assert not result.ready
    assert "REVIEW_EVIDENCE_REQUIRED" in {finding.code for finding in result.findings}
    assert result.released_dependents == ()
