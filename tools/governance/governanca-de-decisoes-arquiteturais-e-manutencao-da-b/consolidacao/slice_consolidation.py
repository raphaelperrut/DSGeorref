from __future__ import annotations

import ast
import csv
import hashlib
import io
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from candidate_repository import CandidateView
from completion_evidence import completion_findings, index_completion_proofs


PARENT_STORY = "STORY-0002"
PARENT_TASK = "TASK-0002"
TASK_PATH = ".codex/tasks/{task_id}.json"
GRAPH_PATH = "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
REVIEW_PATH = "docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv"
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


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
        paths = view.tracked_paths()
    except (TypeError, ValueError) as error:
        finding = Finding("CANDIDATE_INVALID", "candidate_revision", str(error))
        return ConsolidationResult(candidate_revision, (), (), (), (finding,))

    findings: list[Finding] = []
    findings.extend(_identity_findings(parent, tasks, graph, dependencies))
    scopes = tuple(_production_scopes(task) for task in tasks)
    findings.extend(_baseline_findings(parent, tasks, scopes, paths))
    proof_value = reviewer_record.get("slice_completion") if reviewer_record else None
    proofs, proof_findings = index_completion_proofs(proof_value)
    findings.extend(Finding(*finding) for finding in proof_findings)
    requirements, coverage_findings = _coverage(view, tasks, proofs)
    findings.extend(coverage_findings)
    findings.extend(_integration_findings(view, scopes, paths))
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
    matches = [node for node in nodes if isinstance(node, Mapping) and node.get("id") == story_id]
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
        findings.append(
            Finding("PARENT_IDENTITY_MISMATCH", "parent", "TASK-0002 identity required")
        )
    if tuple(sorted(dependencies)) != _graph_edges(graph, target=PARENT_STORY):
        findings.append(
            Finding(
                "DEPENDENCY_GRAPH_MISMATCH",
                "dependencies",
                "TaskEnvelope and graph differ",
            )
        )
    identity = (parent.get("epic_id"), parent.get("sprint_id"), parent.get("bounded_context"))
    for index, task in enumerate(tasks):
        child_identity = (task.get("epic_id"), task.get("sprint_id"), task.get("bounded_context"))
        if child_identity != identity or task.get("story_id") not in dependencies:
            findings.append(
                Finding(
                    "SLICE_IDENTITY_MISMATCH",
                    f"dependencies[{index}]",
                    "slice ownership differs",
                )
            )
    return findings


def _production_scopes(task: Mapping[str, Any]) -> tuple[str, ...]:
    allow = task.get("allow_paths")
    if not isinstance(allow, list):
        return ()
    prefixes = ("tools/governance/", "docs/03-engineering/contexts/")
    scopes = (
        path[:-3]
        for path in allow
        if isinstance(path, str) and path.startswith(prefixes) and path.endswith("/**")
    )
    return tuple(sorted(scopes))


def _baseline_findings(
    parent: Mapping[str, Any],
    tasks: tuple[Mapping[str, Any], ...],
    scopes: tuple[tuple[str, ...], ...],
    paths: tuple[str, ...],
) -> list[Finding]:
    findings: list[Finding] = []
    baselines = {
        (task.get("sprint_review_baseline"), task.get("specification_baseline"))
        for task in (parent, *tasks)
    }
    if len(baselines) != 1:
        findings.append(
            Finding(
                "BASELINE_MISMATCH",
                "baseline",
                "linked slices do not share frozen baselines",
            )
        )
    flat_scopes = [scope for group in scopes for scope in group]
    for scope in flat_scopes:
        if not any(path.startswith(f"{scope}/") for path in paths):
            findings.append(
                Finding(
                    "SLICE_OUTPUT_MISSING",
                    scope,
                    "candidate contains no output in governed scope",
                )
            )
    for index, left in enumerate(flat_scopes):
        for right in flat_scopes[index + 1 :]:
            if left.startswith(f"{right}/") or right.startswith(f"{left}/") or left == right:
                findings.append(
                    Finding(
                        "SLICE_SCOPE_COLLISION",
                        "allow_paths",
                        f"{left} overlaps {right}",
                    )
                )
    return findings


def _coverage(
    view: CandidateView,
    tasks: tuple[Mapping[str, Any], ...],
    proofs: Mapping[str, Mapping[str, Any]],
) -> tuple[tuple[str, ...], list[Finding]]:
    text = view.blob(REVIEW_PATH).decode("utf-8")
    rows = {row["issue_id"]: row for row in csv.DictReader(io.StringIO(text))}
    findings: list[Finding] = []
    seen: set[str] = set()
    for task in tasks:
        issue_id = task.get("issue_id")
        references = task.get("references")
        story_paths = [
            item for item in references or []
            if isinstance(item, str) and "/stories/STORY-" in item
        ]
        if not isinstance(issue_id, str) or len(story_paths) != 1:
            findings.append(
                Finding(
                    "REQUIREMENT_COVERAGE_INVALID",
                    "requirements",
                    "slice mapping is absent",
                )
            )
            continue
        story = view.blob(story_paths[0]).decode("utf-8")
        story_id = str(task.get("story_id"))
        findings.extend(
            Finding(*finding)
            for finding in completion_findings(view, task, story, proofs.get(story_id))
        )
        section = re.search(r"## Requisitos\s+(.*?)\s+## ADRs", story, re.DOTALL)
        section_text = section.group(1) if section else ""
        declared = tuple(sorted(set(re.findall(r"REQ-[A-Z0-9-]+", section_text))))
        row = rows.get(issue_id)
        reviewed = tuple(sorted(row["requirements"].split("/"))) if row else ()
        if row is None or row.get("status") != "PASS" or declared != reviewed:
            findings.append(
                Finding(
                    "REQUIREMENT_COVERAGE_INVALID",
                    issue_id,
                    "story and review matrix differ",
                )
            )
        duplicates = seen.intersection(declared)
        if duplicates:
            findings.append(
                Finding(
                    "REQUIREMENT_DUPLICATED",
                    issue_id,
                    ", ".join(sorted(duplicates)),
                )
            )
        seen.update(declared)
    return tuple(sorted(seen)), findings


def _integration_findings(
    view: CandidateView,
    scopes: tuple[tuple[str, ...], ...],
    paths: tuple[str, ...],
) -> list[Finding]:
    findings: list[Finding] = []
    digests: dict[str, str] = {}
    second_slice_sources: list[bytes] = []
    for slice_index, group in enumerate(scopes):
        for path in paths:
            if not path.endswith(".py") or not any(path.startswith(f"{scope}/") for scope in group):
                continue
            content = view.blob(path)
            try:
                ast.parse(content, filename=path)
            except SyntaxError as error:
                findings.append(Finding("SLICE_OUTPUT_INVALID", path, str(error)))
            digest = hashlib.sha256(content).hexdigest()
            if digest in digests:
                findings.append(
                    Finding(
                        "REDUNDANT_IMPLEMENTATION",
                        path,
                        f"duplicates {digests[digest]}",
                    )
                )
            digests[digest] = path
            if slice_index == 1:
                second_slice_sources.append(content)
    reuses_slice_one = any(
        b"from slice_one import" in source for source in second_slice_sources
    )
    if len(scopes) == 2 and not reuses_slice_one:
        findings.append(
            Finding(
                "SLICE_INTEGRATION_MISSING",
                "outputs",
                "slice 2 does not reuse slice 1 boundary",
            )
        )
    return findings


def _review_findings(
    record: Mapping[str, Any] | None,
    candidate_revision: str,
    downstream: tuple[str, ...],
) -> list[Finding]:
    required = {
        "record_type",
        "authority_role",
        "reviewed_story_id",
        "reviewed_candidate_commit",
        "executor_subject",
        "reviewer_subject",
        "result",
        "residual_risks",
        "released_dependents",
        "slice_completion",
    }
    if not isinstance(record, Mapping) or set(record) != required:
        return [
            Finding(
                "REVIEW_EVIDENCE_REQUIRED",
                "reviewer_record",
                "complete reviewer record required",
            )
        ]
    valid_risks = isinstance(record.get("residual_risks"), list) and all(
        isinstance(item, str) and item.strip() for item in record["residual_risks"]
    )
    valid = (
        record.get("record_type") == "SLICE_CONSOLIDATION_REVIEW"
        and record.get("authority_role") == "Reviewer"
        and record.get("reviewed_story_id") == PARENT_STORY
        and record.get("reviewed_candidate_commit") == candidate_revision
        and isinstance(record.get("executor_subject"), str)
        and isinstance(record.get("reviewer_subject"), str)
        and record.get("executor_subject") != record.get("reviewer_subject")
        and record.get("result") == "PASS"
        and valid_risks
        and isinstance(record.get("slice_completion"), list)
        and record.get("released_dependents") == list(downstream)
    )
    if valid:
        return []
    return [
        Finding(
            "REVIEW_EVIDENCE_INVALID",
            "reviewer_record",
            "review does not authorize exact candidate and dependents",
        )
    ]
