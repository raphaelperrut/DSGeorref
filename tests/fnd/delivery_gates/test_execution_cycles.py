from __future__ import annotations

import copy
from pathlib import Path

import pytest
from tools.governance.delivery_gates.model import GRAPH, REGISTRY, definition_digest
from tools.governance.delivery_gates.repository import WorkingRepository
from tools.governance.delivery_gates.validation import planning_errors

from .fixture import GATE_ID, planning_fixture, write

OTHER_GATE = "DG-TASK-0185-A"


def registry_owned_gates(root: Path, *, cycle: bool, scopes: bool) -> Path:
    planning_fixture(root)
    reader = WorkingRepository(root)
    graph = reader.json(GRAPH)
    graph["edges"] = []
    write(root, GRAPH, graph)
    tasks = {}
    for node in graph["nodes"]:
        task = reader.json(f".codex/tasks/{node['task_id']}.json")
        task["dependencies"] = []
        task.pop("delivery_gate_scope", None)
        tasks[task["task_id"]] = task
    registry = reader.json(REGISTRY)
    other = copy.deepcopy(registry["gates"][0])
    other.update(gate_id=OTHER_GATE, owner_task_id="TASK-0185", owner_story_id="STORY-0185")
    other["required_outputs"] = [
        {
            "output_id": "synthetic-owner-output",
            "path": tasks["TASK-0185"]["allow_paths"][0].removesuffix("/**") + "/stage-a.json",
        }
    ]
    registry["gates"].append(other)
    tasks["TASK-0738"]["delivery_gate_dependencies"] = [OTHER_GATE]
    if cycle:
        tasks["TASK-0185"]["delivery_gate_dependencies"] = [GATE_ID]
    if scopes:
        for gate in registry["gates"]:
            tasks[gate["owner_task_id"]]["delivery_gate_scope"] = {
                "gate_id": gate["gate_id"],
                "definition_sha256": definition_digest(gate),
            }
    for task_id, task in tasks.items():
        write(root, f".codex/tasks/{task_id}.json", task)
    write(root, REGISTRY, registry)
    return root


@pytest.mark.parametrize("scopes", [False, True])
def test_reciprocal_gate_owners_are_rejected_with_or_without_scope(
    tmp_path: Path, scopes: bool
) -> None:
    root = registry_owned_gates(tmp_path / "repository", cycle=True, scopes=scopes)
    assert "execution dependency cycle" in ";".join(planning_errors(root))


@pytest.mark.parametrize("scopes", [False, True])
def test_acyclic_chain_resolves_gate_owners_from_registry(tmp_path: Path, scopes: bool) -> None:
    root = registry_owned_gates(tmp_path / "repository", cycle=False, scopes=scopes)
    assert planning_errors(root) == []
    if not scopes:
        reader = WorkingRepository(root)
        assert "delivery_gate_scope" not in reader.json(".codex/tasks/TASK-0738.json")
        assert "delivery_gate_scope" not in reader.json(".codex/tasks/TASK-0185.json")


def test_registry_owner_must_exist_without_scope(tmp_path: Path) -> None:
    root = registry_owned_gates(tmp_path / "repository", cycle=False, scopes=False)
    registry = WorkingRepository(root).json(REGISTRY)
    registry["gates"][1]["owner_task_id"] = "TASK-9999"
    write(root, REGISTRY, registry)
    assert "owner Task missing" in ";".join(planning_errors(root))


def test_registry_owner_cannot_consume_own_gate_without_scope(tmp_path: Path) -> None:
    root = registry_owned_gates(tmp_path / "repository", cycle=False, scopes=False)
    task = WorkingRepository(root).json(".codex/tasks/TASK-0738.json")
    task["delivery_gate_dependencies"] = [GATE_ID, OTHER_GATE]
    write(root, ".codex/tasks/TASK-0738.json", task)
    assert "autoconsumption" in ";".join(planning_errors(root))
