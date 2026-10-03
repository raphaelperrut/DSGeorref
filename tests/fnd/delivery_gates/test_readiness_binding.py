from __future__ import annotations

import copy
from pathlib import Path

import pytest
from tools.governance.delivery_gates.model import GRAPH
from tools.governance.delivery_gates.repository import GitRepository, WorkingRepository
from tools.governance.delivery_gates.validation import planning_errors, ready_errors

from .fixture import GATE_ID, commit, delivery_fixture, git, planning_fixture, write
from .signed_approval import install_test_verifier


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    return planning_fixture(tmp_path / "repository")


def divergent_base(root: Path, mutation: str) -> tuple[str, str]:
    reader = WorkingRepository(root)
    paths = [f".codex/tasks/TASK-{number}.json" for number in ("0038", "0185", "0738")]
    original = {path: reader.json(path) for path in paths}
    tasks = copy.deepcopy(original)
    graph = reader.json(GRAPH)
    changed_graph = copy.deepcopy(graph)
    consumer, other, owner = (tasks[path] for path in paths)
    task_id = "TASK-0038"
    if mutation in {"removed_gate", "moved_gate", "old_envelope"}:
        # Keep the registry non-orphaned: this is the Reviewer's READY bypass.
        other["delivery_gate_dependencies"] = [GATE_ID]
        if mutation == "removed_gate":
            consumer["delivery_gate_dependencies"] = []
        else:
            del consumer["delivery_gate_dependencies"]
    elif mutation == "dependencies":
        consumer["dependencies"] = []
        changed_graph["edges"] = [edge for edge in graph["edges"] if edge["to"] != "STORY-0038"]
    elif mutation == "owner_scope":
        del owner["delivery_gate_scope"]
        task_id = "TASK-0738"
    elif mutation == "allow_paths":
        consumer["allow_paths"].append("src/frontend/shared/**")
    elif mutation == "deny_paths":
        consumer["deny_paths"] = []
    elif mutation == "references":
        consumer["references"].remove("docs/06-delivery/DELIVERY_GATES.json")
    elif mutation == "owner":
        consumer["bounded_context"] = "BC-016"
    for path, task in tasks.items():
        write(root, path, task)
    write(root, GRAPH, changed_graph)
    assert planning_errors(root) == []
    base = commit(root, f"test: divergent base {mutation}")
    for path, task in original.items():
        write(root, path, task)
    write(root, GRAPH, graph)
    return task_id, base


def test_canonical_base_with_pending_gate_is_not_ready(repository: Path) -> None:
    failures = ready_errors(repository, "TASK-0038", git(repository, "rev-parse", "HEAD"))
    assert any("PENDING" in failure for failure in failures)


@pytest.mark.parametrize(
    "mutation",
    [
        "removed_gate",
        "moved_gate",
        "old_envelope",
        "dependencies",
        "owner_scope",
        "allow_paths",
        "deny_paths",
        "references",
        "owner",
    ],
)
def test_divergent_base_cannot_weaken_current_authorization(
    repository: Path, mutation: str
) -> None:
    task_id, base = divergent_base(repository, mutation)
    assert planning_errors(repository) == []
    failures = ready_errors(repository, task_id, base)
    assert failures and "current canonical TaskEnvelope" in ";".join(failures)
    assert GitRepository(repository, base).paths("evidence/delivery-gates") == []


def test_base_missing_current_task_fails_closed(repository: Path) -> None:
    path = ".codex/tasks/TASK-0038.json"
    current = WorkingRepository(repository).json(path)
    (repository / path).unlink()
    base = commit(repository, "test: missing consumer envelope")
    write(repository, path, current)
    assert ready_errors(repository, "TASK-0038", base)


def test_equivalent_base_with_signed_integrated_gate_is_ready(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, _, _, _ = delivery_fixture(tmp_path / "repository")
    install_test_verifier(monkeypatch, root)
    assert ready_errors(root, "TASK-0038", git(root, "rev-parse", "HEAD")) == []


def test_current_envelope_without_gates_remains_backward_compatible(repository: Path) -> None:
    base = git(repository, "rev-parse", "HEAD")
    task = WorkingRepository(repository).json(".codex/tasks/TASK-0036.json")
    assert "delivery_gate_dependencies" not in task
    assert ready_errors(repository, "TASK-0036", base) == []
    task["delivery_gate_dependencies"] = []
    write(repository, ".codex/tasks/TASK-0036.json", task)
    assert ready_errors(repository, "TASK-0036", base) == []
