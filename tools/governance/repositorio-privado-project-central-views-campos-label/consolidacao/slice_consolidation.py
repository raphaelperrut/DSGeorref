from __future__ import annotations

import re
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GOVERNANCE_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_CONSOLIDATION = (
    GOVERNANCE_ROOT
    / "governanca-de-decisoes-arquiteturais-e-manutencao-da-b"
    / "consolidacao"
)
if str(CANONICAL_CONSOLIDATION) not in sys.path:
    sys.path.insert(0, str(CANONICAL_CONSOLIDATION))

from candidate_repository import CandidateView  # noqa: E402
from canonical_completion import validate_governed_completion  # noqa: E402
from candidate_checks import (  # noqa: E402
    Finding,
    coverage_findings,
    integration_findings,
)


PARENT_STORY = "STORY-0007"
PARENT_TASK = "TASK-0007"
TASK_PATH = ".codex/tasks/{task_id}.json"
GRAPH_PATH = "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class ConsolidationResult:
    candidate_revision: str
    dependency_story_ids: tuple[str, ...]
    requirement_ids: tuple[str, ...]
    released_dependents: tuple[str, ...]
    findings: tuple[Finding, ...]

    @property
    def ready(self) -> bool:
        return not self.findings


def validate_slice_consolidation(
    repository_root: Path,
    candidate_revision: str,
    reviewer_record: Mapping[str, Any] | None,
) -> ConsolidationResult:
    if COMMIT_PATTERN.fullmatch(candidate_revision) is None:
        finding = Finding(
            "CANDIDATE_INVALID",
            "candidate_revision",
            "must be one full lowercase Git commit SHA",
        )
        return ConsolidationResult(candidate_revision, (), (), (), (finding,))

    view = CandidateView(repository_root, candidate_revision)
    try:
        parent = view.json(TASK_PATH.format(task_id=PARENT_TASK))
        graph = view.json(GRAPH_PATH)
        dependencies = tuple(parent.get("dependencies", ()))
        tasks = tuple(
            view.json(TASK_PATH.format(task_id=_task_for_story(graph, story_id)))
            for story_id in dependencies
        )
        tracked_paths = view.tracked_paths()
    except (TypeError, ValueError) as error:
        finding = Finding("CANDIDATE_INVALID", "candidate_revision", str(error))
        return ConsolidationResult(candidate_revision, (), (), (), (finding,))

    findings: list[Finding] = []
    findings.extend(_identity_findings(parent, tasks, graph, dependencies))
    scopes = tuple(_owned_scopes(task) for task in tasks)
    findings.extend(_baseline_and_scope_findings(parent, tasks, scopes, tracked_paths))
    try:
        requirements, coverage_issues = coverage_findings(view, tasks)
        findings.extend(coverage_issues)
        findings.extend(integration_findings(view, scopes, tracked_paths))
    except (TypeError, UnicodeDecodeError, ValueError) as error:
        requirements = ()
        findings.append(Finding("CANDIDATE_INVALID", "candidate_revision", str(error)))
    findings.extend(_completion_findings(tasks, reviewer_record, repository_root))
    downstream = _graph_edges(graph, source=PARENT_STORY)
    findings.extend(_review_findings(reviewer_record, candidate_revision, downstream))
    released = downstream if not findings else ()
    return ConsolidationResult(
        candidate_revision,
        tuple(sorted(dependencies)),
        requirements,
        released,
        tuple(sorted(findings)),
    )


def _task_for_story(graph: Mapping[str, Any], story_id: str) -> str:
    nodes = graph.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("dependency graph nodes are absent")
    matches = [
        node
        for node in nodes
        if isinstance(node, Mapping) and node.get("id") == story_id
    ]
    if len(matches) != 1 or not isinstance(matches[0].get("task_id"), str):
        raise ValueError(f"dependency graph has no unique task for {story_id}")
    return str(matches[0]["task_id"])


def _graph_edges(
    graph: Mapping[str, Any], *, source: str | None = None, target: str | None = None
) -> tuple[str, ...]:
    edges = graph.get("edges")
    if not isinstance(edges, list):
        return ()
    values: list[str] = []
    for edge in edges:
        if not isinstance(edge, Mapping) or edge.get("relation") != "blocks":
            continue
        if source is not None and edge.get("from") == source:
            values.append(str(edge.get("to")))
        if target is not None and edge.get("to") == target:
            values.append(str(edge.get("from")))
    return tuple(sorted(values))


def _identity_findings(
    parent: Mapping[str, Any],
    tasks: tuple[Mapping[str, Any], ...],
    graph: Mapping[str, Any],
    dependencies: tuple[str, ...],
) -> list[Finding]:
    findings: list[Finding] = []
    if parent.get("story_id") != PARENT_STORY or parent.get("task_id") != PARENT_TASK:
        findings.append(Finding("PARENT_IDENTITY_MISMATCH", "parent", "TASK-0007 required"))
    if tuple(sorted(dependencies)) != _graph_edges(graph, target=PARENT_STORY):
        findings.append(
            Finding("DEPENDENCY_GRAPH_MISMATCH", "dependencies", "TaskEnvelope and graph differ")
        )
    identity = (parent.get("epic_id"), parent.get("sprint_id"), parent.get("bounded_context"))
    for index, task in enumerate(tasks):
        child = (task.get("epic_id"), task.get("sprint_id"), task.get("bounded_context"))
        if child != identity or task.get("story_id") not in dependencies:
            findings.append(
                Finding(
                    "SLICE_IDENTITY_MISMATCH",
                    f"dependencies[{index}]",
                    "slice ownership differs",
                )
            )
    return findings


def _owned_scopes(task: Mapping[str, Any]) -> tuple[str, ...]:
    allow = task.get("allow_paths")
    if not isinstance(allow, list):
        return ()
    prefixes = ("tools/governance/", "docs/03-engineering/contexts/")
    return tuple(
        sorted(
            path[:-3]
            for path in allow
            if isinstance(path, str) and path.startswith(prefixes) and path.endswith("/**")
        )
    )


def _baseline_and_scope_findings(
    parent: Mapping[str, Any],
    tasks: tuple[Mapping[str, Any], ...],
    scopes: tuple[tuple[str, ...], ...],
    paths: tuple[str, ...],
) -> list[Finding]:
    findings: list[Finding] = []
    baselines = {
        (
            task.get("sprint_review_baseline"),
            task.get("specification_baseline"),
            task.get("cto_review_baseline"),
        )
        for task in (parent, *tasks)
    }
    if len(baselines) != 1:
        findings.append(Finding("BASELINE_MISMATCH", "baseline", "linked slices differ"))
    flat_scopes = [scope for group in scopes for scope in group]
    for group in scopes:
        if len(group) != 2:
            findings.append(
                Finding(
                    "SLICE_SCOPE_INVALID",
                    "allow_paths",
                    "tool and document scopes required",
                )
            )
        for scope in group:
            if not any(path.startswith(f"{scope}/") for path in paths):
                findings.append(
                    Finding(
                        "SLICE_OUTPUT_MISSING",
                        scope,
                        "candidate contains no governed output",
                    )
                )
    for index, left in enumerate(flat_scopes):
        for right in flat_scopes[index + 1 :]:
            if left == right or left.startswith(f"{right}/") or right.startswith(f"{left}/"):
                findings.append(
                    Finding(
                        "SLICE_SCOPE_COLLISION",
                        "allow_paths",
                        f"{left} overlaps {right}",
                    )
                )
    return findings


def _completion_findings(
    tasks: tuple[Mapping[str, Any], ...],
    record: Mapping[str, Any] | None,
    repository_root: Path,
) -> list[Finding]:
    references = record.get("completion_evidence") if record else None
    completed, governed = validate_governed_completion(repository_root, references)
    findings = [Finding(item.code, item.field, item.detail) for item in governed]
    expected = {str(task.get("story_id")) for task in tasks}
    for story_id in sorted(expected - set(completed)):
        findings.append(
            Finding(
                "SLICE_COMPLETION_UNPROVEN",
                story_id,
                "governed completion evidence required",
            )
        )
    if set(completed) - expected:
        findings.append(
            Finding(
                "SLICE_COMPLETION_UNEXPECTED",
                "completion_evidence",
                "unlinked story present",
            )
        )
    return findings


def _review_findings(
    record: Mapping[str, Any] | None,
    candidate_revision: str,
    downstream: tuple[str, ...],
) -> list[Finding]:
    required = {
        "record_type", "authority_role", "reviewed_story_id", "reviewed_candidate_commit",
        "executor_subject", "reviewer_subject", "result", "residual_risks",
        "released_dependents", "completion_evidence",
    }
    if not isinstance(record, Mapping) or set(record) != required:
        return [
            Finding(
                "REVIEW_EVIDENCE_REQUIRED",
                "reviewer_record",
                "complete Reviewer record required",
            )
        ]
    risks = record.get("residual_risks")
    valid_risks = isinstance(risks, list) and all(
        isinstance(item, str) and item.strip() for item in risks
    )
    executor_subject = record.get("executor_subject")
    reviewer_subject = record.get("reviewer_subject")
    valid_subjects = (
        isinstance(executor_subject, str)
        and bool(executor_subject.strip())
        and isinstance(reviewer_subject, str)
        and bool(reviewer_subject.strip())
        and executor_subject.strip() != reviewer_subject.strip()
    )
    valid = (
        record.get("record_type") == "SLICE_CONSOLIDATION_REVIEW"
        and record.get("authority_role") == "Reviewer"
        and record.get("reviewed_story_id") == PARENT_STORY
        and record.get("reviewed_candidate_commit") == candidate_revision
        and valid_subjects
        and record.get("result") == "PASS"
        and valid_risks
        and record.get("released_dependents") == list(downstream)
    )
    return [] if valid else [
        Finding(
            "REVIEW_EVIDENCE_INVALID",
            "reviewer_record",
            "review does not authorize exact candidate and dependents",
        )
    ]
