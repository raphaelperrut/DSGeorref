from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from unittest.mock import patch

import slice_consolidation as consolidation
from candidate_repository import CandidateView


ROOT = Path(__file__).resolve().parents[4]
SLICE_MERGES = {
    "STORY-0688": "2cf9f446e50d5c08ad4e694cb0edeb7c745c7048",
    "STORY-0689": "98ba69341310b369147e512b75415458f938f939",
}
SLICE_EVIDENCE = {
    "STORY-0688": (
        "TASK-0688",
        "evidence/implementation/governanca-de-decisoes-arquiteturais-e-manutencao/"
        "frz-gov-adr-gov-dec-parte-1/implementation-report.md",
    ),
    "STORY-0689": (
        "TASK-0689",
        "evidence/implementation/governanca-de-decisoes-arquiteturais-e-manutencao/"
        "sprint-001-tool-parte-2/validator-behavior-evidence.json",
    ),
}


def _candidate() -> str:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        encoding="ascii",
    )
    return completed.stdout.strip()


def _completion_reference(story_id: str) -> dict[str, object]:
    revision = SLICE_MERGES[story_id]
    _task_id, evidence_path = SLICE_EVIDENCE[story_id]
    content = CandidateView(ROOT, revision).blob(evidence_path)
    return {
        "source_revision": revision,
        "path": evidence_path,
        "sha256": hashlib.sha256(content).hexdigest(),
    }


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
        "completion_evidence": [
            _completion_reference("STORY-0688"),
            _completion_reference("STORY-0689"),
        ],
    }


def _canonical_completion(
    story_ids: tuple[str, ...] = ("STORY-0688", "STORY-0689"),
    findings: tuple[consolidation.Finding, ...] = (),
):
    return patch.object(
        consolidation,
        "validate_governed_completion",
        return_value=(list(story_ids), list(findings)),
    )


def _story_states(states: dict[str, str | None]):
    original_blob = CandidateView.blob
    markers = {
        "STORY-0688": "STORY-0688-ISSUE-0798",
        "STORY-0689": "STORY-0689-ISSUE-0799",
    }

    def replaced(view: CandidateView, path: str) -> bytes:
        content = original_blob(view, path)
        for story_id, state in states.items():
            if markers[story_id] in path:
                replacement = b"" if state is None else f"- **Estado:** `{state}`".encode()
                return re.sub(
                    rb"^- \*\*Estado:\*\* `[^`]*`\r?\n?",
                    replacement + (b"\n" if replacement else b""),
                    content,
                    count=1,
                    flags=re.MULTILINE,
                )
        return content

    return patch.object(CandidateView, "blob", replaced)


def _story_state(story_id: str, state: str | None):
    return _story_states({story_id: state})


def test_story_0002_slice_consolidation() -> None:
    candidate = _candidate()
    with _canonical_completion():
        result = consolidation.validate_slice_consolidation(
            ROOT,
            candidate,
            _review(candidate),
        )

    assert result.ready, result.findings
    assert result.dependency_story_ids == ("STORY-0688", "STORY-0689")
    assert len(result.requirement_ids) == 20
    assert result.released_dependents == ("STORY-0004",)


def test_done_slice_without_canonical_proof_is_rejected() -> None:
    candidate = _candidate()
    review = _review(candidate)

    with _story_state("STORY-0688", "Done"), _canonical_completion(("STORY-0689",)):
        result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert "SLICE_COMPLETION_UNPROVEN" in {
        finding.code for finding in result.findings
    }
    assert result.released_dependents == ()


def test_all_done_with_zero_canonical_references_fails_closed() -> None:
    candidate = _candidate()
    review = _review(candidate)
    review["completion_evidence"] = []

    with _story_states({"STORY-0688": "Done", "STORY-0689": "Done"}):
        result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert {
        finding.field
        for finding in result.findings
        if finding.code == "SLICE_COMPLETION_UNPROVEN"
    } == {"STORY-0688", "STORY-0689"}
    assert result.released_dependents == ()


def test_non_terminal_states_are_rejected_without_completion_evidence() -> None:
    candidate = _candidate()
    states = (
        "Ready",
        "Ready-after-authorization",
        "Planned",
        "In Progress",
        "Blocked",
        "Unknown",
    )
    for state in states:
        review = _review(candidate)
        with _story_state("STORY-0688", state), _canonical_completion(("STORY-0689",)):
            result = consolidation.validate_slice_consolidation(ROOT, candidate, review)
        assert not result.ready, state
        assert "SLICE_COMPLETION_UNPROVEN" in {
            finding.code for finding in result.findings
        }
        assert result.released_dependents == ()


def test_missing_canonical_state_and_completion_evidence_is_rejected() -> None:
    candidate = _candidate()
    review = _review(candidate)

    with _story_state("STORY-0688", None), _canonical_completion(("STORY-0689",)):
        result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert "SLICE_COMPLETION_UNPROVEN" in {
        finding.code for finding in result.findings
    }
    assert result.released_dependents == ()


def test_local_path_hash_completion_authority_is_rejected() -> None:
    candidate = _candidate()
    review = _review(candidate)
    review["completion_evidence"] = [
        {
            "record_type": "STORY_COMPLETION_EVIDENCE",
            "story_id": "STORY-0688",
            "task_id": "TASK-0688",
            "state": "COMPLETED",
            "candidate_revision": SLICE_MERGES["STORY-0688"],
            "evidence_path": SLICE_EVIDENCE["STORY-0688"][1],
            "sha256": "0" * 64,
        }
    ]

    result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert "SLICE_COMPLETION_UNPROVEN" in {
        finding.code for finding in result.findings
    }
    assert result.released_dependents == ()


def test_missing_slice_completion_proof_rejects_blocked_slice() -> None:
    candidate = _candidate()
    review = _review(candidate)

    with _story_state("STORY-0689", "Blocked"), _canonical_completion(("STORY-0688",)):
        result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert "SLICE_COMPLETION_UNPROVEN" in {
        finding.code for finding in result.findings
    }
    assert result.released_dependents == ()


def test_no_dependent_release_when_any_other_finding_remains() -> None:
    candidate = _candidate()
    forced = consolidation.Finding("FORCED_BLOCKER", "baseline", "incomplete")

    with (
        patch.object(consolidation, "_baseline_findings", return_value=[forced]),
        _canonical_completion(),
    ):
        result = consolidation.validate_slice_consolidation(
            ROOT,
            candidate,
            _review(candidate),
        )

    assert not result.ready
    assert forced in result.findings
    assert result.released_dependents == ()


def test_slice_consolidation_requires_independent_review() -> None:
    result = consolidation.validate_slice_consolidation(ROOT, _candidate(), None)

    assert not result.ready
    assert "REVIEW_EVIDENCE_REQUIRED" in {
        finding.code for finding in result.findings
    }
    assert result.released_dependents == ()


def test_slice_consolidation_rejects_review_for_another_candidate() -> None:
    candidate = _candidate()
    review = _review(candidate)
    review["reviewed_candidate_commit"] = "0" * 40

    with _canonical_completion():
        result = consolidation.validate_slice_consolidation(ROOT, candidate, review)

    assert not result.ready
    assert "REVIEW_EVIDENCE_INVALID" in {
        finding.code for finding in result.findings
    }
    assert result.released_dependents == ()


def _assert_canonical_rejection(code: str, detail: str) -> None:
    candidate = _candidate()
    canonical = consolidation.Finding(code, "$.completion_evidence[0]", detail)
    with _canonical_completion(("STORY-0689",), (canonical,)):
        result = consolidation.validate_slice_consolidation(
            ROOT, candidate, _review(candidate)
        )
    assert not result.ready
    assert canonical in result.findings
    assert result.released_dependents == ()


def test_missing_qa_assurance_is_rejected() -> None:
    _assert_canonical_rejection(
        "COMPLETION_EVIDENCE_INVALID", "QA and Reviewer evidence required"
    )


def test_missing_reviewer_assurance_is_rejected() -> None:
    _assert_canonical_rejection(
        "EVIDENCE_AUTHORITY_INVALID", "Reviewer assurance proof mismatch"
    )


def test_missing_daa_is_rejected() -> None:
    _assert_canonical_rejection(
        "DELIVERY_APPROVAL_INVALID", "trusted DAA approval is required"
    )


def test_mismatched_or_stale_governed_reference_is_rejected() -> None:
    _assert_canonical_rejection(
        "COMPLETION_EVIDENCE_INVALID", "assurance proof mismatch"
    )
