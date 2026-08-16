from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
import re
from typing import Any

from canonical_json import CanonicalizationError, load_json_bytes
from foundation_validation_types import Finding


GRAPH_PATH = Path("docs/06-delivery/STORY_DEPENDENCY_GRAPH.json")
PROFILE_PATH = Path("docs/03-engineering/application-profiles/AP-008-sprint-001-execution-profile.md")
BACKLOG_PATH = Path("docs/06-delivery/sprint-backlogs/SPRINT-001-BACKLOG.md")
MINIMUM_SCOPE_PREFIX = "O escopo mínimo inclui "
SPRINT_HEADING_PATTERN = re.compile(r"^# AP-008 — (SPRINT-[0-9]{3}) execution profile$")
BACKLOG_STORY_PATTERN = re.compile(r"^\| `(STORY-[0-9]{4})` \|", re.MULTILINE)


def minimum_sprint_scope(repository_root: Path) -> tuple[str, ...]:
    try:
        text = (repository_root / PROFILE_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError(f"AP-008 is unavailable or invalid: {error}") from error
    start = text.find(MINIMUM_SCOPE_PREFIX)
    if start < 0:
        raise ValueError("AP-008 does not declare the minimum scope")
    start += len(MINIMUM_SCOPE_PREFIX)
    end = text.find(".", start)
    if end < 0:
        raise ValueError("AP-008 minimum scope is incomplete")
    declaration = text[start:end].replace("`", "")
    head, separator, tail = declaration.rpartition(" e ")
    if not separator:
        raise ValueError("AP-008 minimum scope has no closed final item")
    items = tuple(part.strip() for part in head.split(",")) + (tail.strip(),)
    if any(not item for item in items) or len(items) != len(set(items)):
        raise ValueError("AP-008 minimum scope is empty or ambiguous")
    return items


def validate_minimum_sprint_scope(
    repository_root: Path, selected_capabilities: Iterable[str]
) -> list[Finding]:
    selected = tuple(selected_capabilities)
    try:
        expected = minimum_sprint_scope(repository_root)
    except ValueError as error:
        return [Finding("SPRINT_PROFILE_INVALID", str(PROFILE_PATH), str(error))]
    if selected == expected:
        return []
    return [
        Finding(
            "SPRINT_MINIMUM_SCOPE_MISMATCH",
            "selected_capabilities",
            "selection must exactly match AP-008 minimum scope and canonical order",
        )
    ]


def _load_graph(repository_root: Path) -> dict[str, Any]:
    try:
        graph = load_json_bytes((repository_root / GRAPH_PATH).read_bytes())
    except (OSError, CanonicalizationError) as error:
        raise ValueError(f"canonical story graph is invalid: {error}") from error
    if not isinstance(graph, dict) or graph.get("semantics") != (
        "Only hard blockers; edge from prerequisite to dependent."
    ):
        raise ValueError("canonical story graph has unknown semantics")
    nodes, edges = graph.get("nodes"), graph.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("canonical story graph has invalid structure")
    return graph


def _graph_parts(
    graph: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]], list[tuple[str, str]]]:
    nodes: dict[str, dict[str, Any]] = {}
    predecessors: dict[str, set[str]] = defaultdict(set)
    edges: list[tuple[str, str]] = []
    for node in graph["nodes"]:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str):
            raise ValueError("story graph contains an invalid node")
        story_id = node["id"]
        if story_id in nodes:
            raise ValueError(f"story graph contains duplicate node: {story_id}")
        nodes[story_id] = node
    for edge in graph["edges"]:
        if not isinstance(edge, dict) or edge.get("relation") != "blocks":
            raise ValueError("story graph contains an invalid edge")
        source, target = edge.get("from"), edge.get("to")
        if source not in nodes or target not in nodes:
            raise ValueError("story graph edge references an unknown node")
        predecessors[target].add(source)
        edges.append((source, target))
    return nodes, predecessors, edges


def _derive_story_selection(
    graph: dict[str, Any], requested_story_ids: Iterable[str]
) -> tuple[str, ...]:
    nodes, predecessors, edges = _graph_parts(graph)
    requested = tuple(requested_story_ids)
    if not requested or len(requested) != len(set(requested)):
        raise ValueError("requested story set must be non-empty and unique")
    unknown = sorted(set(requested) - set(nodes))
    if unknown:
        raise ValueError(f"unknown requested stories: {', '.join(unknown)}")
    selected = _predecessor_closure(requested, predecessors)
    return _topological_order(selected, edges)


def _predecessor_closure(
    requested: tuple[str, ...], predecessors: dict[str, set[str]]
) -> set[str]:
    selected = set(requested)
    pending = list(requested)
    while pending:
        story_id = pending.pop()
        for predecessor in sorted(predecessors.get(story_id, set())):
            if predecessor not in selected:
                selected.add(predecessor)
                pending.append(predecessor)
    return selected


def _topological_order(
    selected: set[str], edges: list[tuple[str, str]]
) -> tuple[str, ...]:
    indegree = {story_id: 0 for story_id in selected}
    successors: dict[str, set[str]] = defaultdict(set)
    for source, target in edges:
        if source in selected and target in selected:
            indegree[target] += 1
            successors[source].add(target)
    ready = sorted(story_id for story_id, count in indegree.items() if count == 0)
    ordered: list[str] = []
    while ready:
        story_id = ready.pop(0)
        ordered.append(story_id)
        for successor in sorted(successors.get(story_id, set())):
            indegree[successor] -= 1
            if indegree[successor] == 0:
                ready.append(successor)
                ready.sort()
    if len(ordered) != len(selected):
        raise ValueError("canonical story graph contains a dependency cycle")
    return tuple(ordered)


def _canonical_sprint_id(repository_root: Path) -> str:
    try:
        first_line = (repository_root / PROFILE_PATH).read_text(encoding="utf-8").splitlines()[0]
    except (IndexError, OSError, UnicodeDecodeError) as error:
        raise ValueError(f"AP-008 sprint identity is unavailable: {error}") from error
    match = SPRINT_HEADING_PATTERN.fullmatch(first_line)
    if match is None:
        raise ValueError("AP-008 sprint identity is invalid")
    return match.group(1)


def _canonical_backlog_story_ids(repository_root: Path, sprint_id: str) -> tuple[str, ...]:
    try:
        text = (repository_root / BACKLOG_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError(f"canonical sprint backlog is unavailable: {error}") from error
    if f"- **Sprint:** `{sprint_id}`" not in text:
        raise ValueError("canonical sprint backlog has wrong sprint identity")
    story_ids = tuple(BACKLOG_STORY_PATTERN.findall(text))
    if not story_ids or len(story_ids) != len(set(story_ids)):
        raise ValueError("canonical sprint backlog story inventory is empty or duplicated")
    return story_ids


def derive_canonical_sprint_selection(repository_root: Path) -> tuple[str, ...]:
    graph = _load_graph(repository_root)
    nodes, _predecessors, _edges = _graph_parts(graph)
    sprint_id = _canonical_sprint_id(repository_root)
    backlog_story_ids = _canonical_backlog_story_ids(repository_root, sprint_id)
    unknown = sorted(set(backlog_story_ids) - set(nodes))
    if unknown:
        raise ValueError(f"canonical sprint backlog references unknown stories: {', '.join(unknown)}")
    for story_id in backlog_story_ids:
        node = nodes[story_id]
        task_path = Path(".codex/tasks") / f"{node.get('task_id')}.json"
        try:
            task = load_json_bytes((repository_root / task_path).read_bytes())
        except (OSError, CanonicalizationError) as error:
            raise ValueError(f"canonical task is invalid for {story_id}: {error}") from error
        if not isinstance(task, dict) or task.get("story_id") != story_id or task.get("sprint_id") != sprint_id:
            raise ValueError(f"backlog/task sprint authority mismatch for {story_id}")
    return _derive_story_selection(graph, backlog_story_ids)


def _selected_task_findings(
    repository_root: Path, selected: tuple[str, ...], nodes: dict[str, dict[str, Any]]
) -> list[Finding]:
    findings: list[Finding] = []
    for story_id in selected:
        node = nodes[story_id]
        task_id = node.get("task_id")
        task_path = Path(".codex/tasks") / f"{task_id}.json"
        try:
            task = load_json_bytes((repository_root / task_path).read_bytes())
        except (OSError, CanonicalizationError) as error:
            findings.append(Finding("TASK_ENVELOPE_INVALID", story_id, str(error)))
            continue
        gates_pass = (
            isinstance(task, dict)
            and task.get("story_id") == story_id
            and task.get("sprint_id") == "SPRINT-001"
            and task.get("requirements_review_status") == "PASS"
            and task.get("phase_f_review", {}).get("dependencies", {}).get("status") == "PASS"
            and task.get("phase_g_review", {}).get("status") == "PASS"
        )
        if not gates_pass:
            findings.append(
                Finding(
                    "STORY_GATE_INVALID",
                    story_id,
                    "selected story lacks canonical sprint, dependency, requirement or risk gate",
                )
            )
    return findings


def validate_graph_derived_selection(
    repository_root: Path,
    selected_story_ids: Iterable[str],
) -> list[Finding]:
    selected = tuple(selected_story_ids)
    try:
        expected = derive_canonical_sprint_selection(repository_root)
        nodes, _predecessors, _edges = _graph_parts(_load_graph(repository_root))
    except ValueError as error:
        return [Finding("STORY_GRAPH_INVALID", str(GRAPH_PATH), str(error))]
    findings = _selected_task_findings(repository_root, expected, nodes)
    if selected != expected:
        findings.append(
            Finding(
                "SPRINT_SELECTION_NON_CANONICAL",
                "selected_story_ids",
                "selection differs from deterministic hard-predecessor closure",
            )
        )
    return sorted(findings)
