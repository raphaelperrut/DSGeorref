from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from pathlib import PurePosixPath
from typing import Any

from candidate_repository import CandidateView


COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
TERMINAL_COMPLETED_STATE = "Done"
PROOF_FIELDS = frozenset(
    {
        "record_type",
        "story_id",
        "task_id",
        "state",
        "candidate_revision",
        "evidence_path",
        "sha256",
    }
)
FindingTuple = tuple[str, str, str]


def index_completion_proofs(
    value: object,
) -> tuple[dict[str, Mapping[str, Any]], list[FindingTuple]]:
    if value is None:
        return {}, []
    if not isinstance(value, list):
        return {}, [_finding("slice_completion must be an array")]
    indexed: dict[str, Mapping[str, Any]] = {}
    findings: list[FindingTuple] = []
    for item in value:
        story_id = item.get("story_id") if isinstance(item, Mapping) else None
        if not isinstance(story_id, str) or story_id in indexed:
            findings.append(_finding("completion proofs must have unique story IDs"))
            continue
        indexed[story_id] = item
    return indexed, findings


def completion_findings(
    view: CandidateView,
    task: Mapping[str, Any],
    story_content: str,
    proof: Mapping[str, Any] | None,
) -> list[FindingTuple]:
    story_id = str(task.get("story_id"))
    state = re.search(
        r"^- \*\*Estado:\*\* `([^`]+)`",
        story_content,
        re.MULTILINE,
    )
    if state is not None and state.group(1) == TERMINAL_COMPLETED_STATE:
        return []
    if proof is None:
        return [_finding(f"{story_id} lacks positive completion proof", story_id)]
    detail = _proof_error(view, task, proof)
    return [] if detail is None else [_finding(detail, story_id)]


def _proof_error(
    view: CandidateView,
    task: Mapping[str, Any],
    proof: Mapping[str, Any],
) -> str | None:
    if set(proof) != PROOF_FIELDS:
        return "completion evidence fields are incomplete or unknown"
    if (
        proof.get("record_type") != "STORY_COMPLETION_EVIDENCE"
        or proof.get("story_id") != task.get("story_id")
        or proof.get("task_id") != task.get("task_id")
        or proof.get("state") != "COMPLETED"
    ):
        return "completion evidence identity or terminal state is invalid"
    revision = proof.get("candidate_revision")
    evidence_path = proof.get("evidence_path")
    digest = proof.get("sha256")
    if not all(isinstance(item, str) for item in (revision, evidence_path, digest)):
        return "completion evidence revision, path and digest are required"
    assert isinstance(revision, str)
    assert isinstance(evidence_path, str)
    assert isinstance(digest, str)
    if COMMIT_PATTERN.fullmatch(revision) is None or not view.is_ancestor(revision):
        return "completion candidate must be an immutable ancestor"
    child = CandidateView(view.repository_root, revision)
    if child.parent_count() < 2:
        return "completion candidate must be an integrated merge commit"
    if not _authorized_evidence_path(task, evidence_path):
        return "completion artifact is not recognized by the TaskEnvelope"
    try:
        content = child.blob(evidence_path)
        paths = child.tracked_paths()
    except ValueError as error:
        return str(error)
    if hashlib.sha256(content).hexdigest() != digest:
        return "completion artifact digest does not match the merge candidate"
    if not _outputs_present(task, paths):
        return "completion merge does not contain every governed slice output"
    return None


def _authorized_evidence_path(task: Mapping[str, Any], path: str) -> bool:
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts or "\\" in path:
        return False
    evidence = task.get("evidence")
    roots = (
        item
        for item in evidence or []
        if isinstance(item, str) and item.endswith("/")
    )
    return any(path.startswith(root) and path != root for root in roots)


def _outputs_present(task: Mapping[str, Any], paths: tuple[str, ...]) -> bool:
    allow = task.get("allow_paths")
    if not isinstance(allow, list):
        return False
    prefixes = ("tools/governance/", "docs/03-engineering/contexts/")
    roots = [
        item[:-3]
        for item in allow
        if isinstance(item, str)
        and item.startswith(prefixes)
        and item.endswith("/**")
    ]
    return bool(roots) and all(
        any(path.startswith(f"{root}/") for path in paths) for root in roots
    )


def _finding(detail: str, field: str = "slice_completion") -> FindingTuple:
    return ("SLICE_COMPLETION_UNPROVEN", field, detail)
