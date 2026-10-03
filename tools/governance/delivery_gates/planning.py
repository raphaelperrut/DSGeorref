"""Validate additive planning gates without changing Story predecessors."""

from __future__ import annotations

import re
import subprocess
from fnmatch import fnmatchcase
from typing import Any

from jsonschema import Draft202012Validator

from .model import (
    GRAPH,
    REGISTRY,
    SCHEMA,
    TASK_SCHEMA,
    GateError,
    definition_digest,
    relative_path,
    require,
)
from .repository import GitRepository, WorkingRepository

Reader = GitRepository | WorkingRepository


def validate_reference(reader: Reader, reference: str) -> None:
    path, _, anchor = reference.partition("#")
    content = reader.read(relative_path(path)).decode("utf-8")
    if anchor:
        require(f'<a id="{anchor}"></a>' in content, f"reference anchor missing: {reference}")


def unique_ids(records: list[dict[str, Any]], key: str) -> None:
    ids = [item[key] for item in records]
    require(len(ids) == len(set(ids)), f"duplicate {key}")


def authorized_output(path: str, task: dict[str, Any]) -> bool:
    def matches(pattern: str) -> bool:
        if pattern.endswith("/**"):
            return path.startswith(pattern[:-2])
        return fnmatchcase(path, pattern)

    return any(matches(pattern) for pattern in task["allow_paths"]) and not any(
        matches(pattern) for pattern in task["deny_paths"]
    )


def validate_tasks(reader: Reader, graph: dict[str, Any]) -> dict[str, Any]:
    nodes = {node["id"]: node for node in graph["nodes"]}
    require(len(nodes) == len(graph["nodes"]), "duplicate Story ID")
    predecessors: dict[str, set[str]] = {story: set() for story in nodes}
    for edge in graph["edges"]:
        require(edge["from"] in nodes and edge["to"] in nodes, "unknown Story edge")
        predecessors[edge["to"]].add(edge["from"])
    schema = reader.json(TASK_SCHEMA)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    tasks = {}
    for path in reader.paths(".codex/tasks"):
        if re.fullmatch(r"\.codex/tasks/TASK-[0-9]{4}\.json", path) is None:
            continue
        task = reader.json(path)
        validator.validate(task)
        require(task["task_id"] not in tasks, "duplicate Task ID")
        node = nodes.get(task["story_id"])
        require(
            node is not None
            and node["task_id"] == task["task_id"]
            and node["issue_id"] == task["issue_id"],
            "Task/Story owner mismatch",
        )
        dependencies = task.get("dependencies", [])
        require(len(dependencies) == len(set(dependencies)), "duplicate Story dependency")
        require(
            set(dependencies) == predecessors[task["story_id"]],
            f"{task['task_id']}: dependencies differ from Story predecessors",
        )
        tasks[task["task_id"]] = task
    require({task["story_id"] for task in tasks.values()} == set(nodes), "orphan Story")
    return tasks


def validate_gate(reader: Reader, gate: dict[str, Any], tasks: dict[str, Any]) -> None:
    owner = tasks.get(gate["owner_task_id"])
    if owner is None:
        raise GateError("gate owner Task missing")
    require(
        owner is not None and owner["story_id"] == gate["owner_story_id"],
        "gate owner Task/Story missing or incoherent",
    )
    scope = owner.get("delivery_gate_scope")
    require(
        gate["gate_id"] == f"DG-{gate['owner_task_id']}-{gate['stage']}",
        "gate ID/owner/stage mismatch",
    )
    if scope:
        require(scope.get("gate_id") == gate["gate_id"], "gate owner scope mismatch")
        require(
            scope.get("definition_sha256") == definition_digest(gate),
            "gate definition digest mismatch",
        )
    require(
        re.fullmatch(r"refs/heads/(?!.*\.\.|.*//)[A-Za-z0-9_./-]+", gate["required_baseline_ref"])
        is not None,
        "invalid required_baseline_ref",
    )
    require(
        subprocess.run(
            ["git", "check-ref-format", gate["required_baseline_ref"]],
            capture_output=True,
            check=False,
        ).returncode
        == 0,
        "invalid required_baseline_ref",
    )
    validate_reference(reader, gate["authorization_ref"])
    unique_ids(gate["required_outputs"], "output_id")
    unique_ids(gate["acceptance_checks"], "check_id")
    paths = [relative_path(output["path"]) for output in gate["required_outputs"]]
    require(len(paths) == len(set(paths)), "duplicate output path")
    require(
        all(authorized_output(path, owner) for path in paths),
        "required output outside owner write scope",
    )
    for check in gate["acceptance_checks"]:
        validate_reference(reader, check["reference"])
    stories = {task["story_id"] for task in tasks.values()}
    require(set(gate["stage_story_dependencies"]) <= stories, "unknown stage Story dependency")


def validate_bindings(tasks: dict[str, Any], gates: dict[str, Any]) -> None:
    consumers: set[str] = set()
    for task in tasks.values():
        scope = task.get("delivery_gate_scope")
        if scope:
            require(scope["gate_id"] in gates, "scope references unknown gate")
            gate = gates[scope["gate_id"]]
            require(
                (gate["owner_task_id"], gate["owner_story_id"])
                == (task["task_id"], task["story_id"]),
                "scope owner is not owned by task",
            )
        for gate_id in task.get("delivery_gate_dependencies", []):
            require(gate_id in gates, "consumer references unknown gate")
            require(gates[gate_id]["owner_task_id"] != task["task_id"], "gate autoconsumption")
            consumers.add(gate_id)
    require(consumers == set(gates), "orphan gate: no consumer")


def validate_execution_cycles(
    graph: dict[str, Any], tasks: dict[str, Any], gates: dict[str, Any]
) -> None:
    adjacency: dict[str, set[str]] = {node["id"]: set() for node in graph["nodes"]}
    adjacency.update({gate_id: set() for gate_id in gates})
    for edge in graph["edges"]:
        adjacency[edge["from"]].add(edge["to"])
    for gate_id, gate in gates.items():
        adjacency[gate_id].add(gate["owner_story_id"])
        for story in gate["stage_story_dependencies"]:
            adjacency[story].add(gate_id)
    for task in tasks.values():
        for gate_id in task.get("delivery_gate_dependencies", []):
            adjacency[gate_id].add(task["story_id"])
            if scope := task.get("delivery_gate_scope"):
                adjacency[gate_id].add(scope["gate_id"])
    incoming = dict.fromkeys(adjacency, 0)
    for targets in adjacency.values():
        for target in targets:
            incoming[target] += 1
    queue = sorted(node for node, count in incoming.items() if count == 0)
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for target in sorted(adjacency[node]):
            incoming[target] -= 1
            if incoming[target] == 0:
                queue.append(target)
    require(visited == len(adjacency), "execution dependency cycle via Story/delivery gate")


def validate_planning(reader: Reader) -> tuple[dict[str, Any], dict[str, Any]]:
    from .model import validate_schema

    registry, schema = reader.json(REGISTRY), reader.json(SCHEMA)
    validate_schema(registry, schema)
    unique_ids(registry["gates"], "gate_id")
    graph = reader.json(GRAPH)
    tasks = validate_tasks(reader, graph)
    gates = {gate["gate_id"]: gate for gate in registry["gates"]}
    validate_bindings(tasks, gates)
    for gate in gates.values():
        validate_gate(reader, gate, tasks)
    validate_execution_cycles(graph, tasks, gates)
    return tasks, gates
