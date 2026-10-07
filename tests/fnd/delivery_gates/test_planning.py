from __future__ import annotations

import copy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from tools.governance.delivery_gates.model import (
    GRAPH,
    REGISTRY,
    SCHEMA,
    TASK_SCHEMA,
    GateError,
    definition_digest,
    parse,
    validate_schema,
)
from tools.governance.delivery_gates.planning import validate_planning
from tools.governance.delivery_gates.repository import WorkingRepository
from tools.governance.delivery_gates.validation import planning_errors, ready_errors

from .fixture import GATE_ID, ROOT, planning_fixture, write


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    return planning_fixture(tmp_path / "repository")


def test_canonical_registry_schema_and_all_envelopes() -> None:
    tasks, gates = validate_planning(WorkingRepository(ROOT))
    assert len(tasks) == 765
    assert set(gates) == {GATE_ID}
    assert tasks["TASK-0038"]["dependencies"] == ["STORY-0036"]
    assert tasks["TASK-0738"]["dependencies"] == ["STORY-0185"]
    assert tasks["TASK-0038"]["delivery_gate_dependencies"] == [GATE_ID]
    assert len(tasks["TASK-0038"]["allow_paths"]) == 1
    Draft202012Validator.check_schema(WorkingRepository(ROOT).json(SCHEMA))


@pytest.mark.parametrize(
    "mutation, expected",
    [
        ("duplicate", "duplicate gate_id"),
        ("owner", "owner"),
        ("consumer", "unknown gate"),
        ("self", "autoconsumption"),
        ("orphan", "orphan gate"),
        ("digest", "digest mismatch"),
        ("cycle", "execution dependency cycle"),
        ("scope", "not owned"),
        ("dependencies", "Story predecessors"),
    ],
)
def test_planning_rejects_invalid_bindings(repository: Path, mutation: str, expected: str) -> None:
    registry = WorkingRepository(repository).json(REGISTRY)
    owner_path, consumer_path = ".codex/tasks/TASK-0738.json", ".codex/tasks/TASK-0038.json"
    owner = WorkingRepository(repository).json(owner_path)
    consumer = WorkingRepository(repository).json(consumer_path)
    gate = registry["gates"][0]
    if mutation == "duplicate":
        other = copy.deepcopy(gate)
        other["stage"] = "B"
        registry["gates"].append(other)
    elif mutation == "owner":
        gate["owner_story_id"] = "STORY-9999"
    elif mutation == "consumer":
        consumer["delivery_gate_dependencies"] = ["DG-TASK-9999-A"]
    elif mutation == "self":
        owner["delivery_gate_dependencies"] = [GATE_ID]
    elif mutation == "orphan":
        del consumer["delivery_gate_dependencies"]
    elif mutation == "digest":
        owner["delivery_gate_scope"]["definition_sha256"] = "0" * 64
    elif mutation == "cycle":
        gate["stage_story_dependencies"] = ["STORY-0038"]
        owner["delivery_gate_scope"]["definition_sha256"] = definition_digest(gate)
    elif mutation == "scope":
        consumer["delivery_gate_scope"] = owner["delivery_gate_scope"].copy()
    elif mutation == "dependencies":
        consumer["dependencies"] = ["STORY-0738"]
    write(repository, REGISTRY, registry)
    write(repository, owner_path, owner)
    write(repository, consumer_path, consumer)
    assert expected in ";".join(planning_errors(repository))


def test_envelope_without_gates_and_pending_planning_are_valid(repository: Path) -> None:
    assert planning_errors(repository) == []
    from .fixture import git

    base = git(repository, "rev-parse", "HEAD")
    failures = ready_errors(repository, "TASK-0038", base)
    assert any("PENDING" in failure for failure in failures)
    assert ready_errors(repository, "TASK-0738", base) == []
    ordinary = WorkingRepository(repository).json(".codex/tasks/TASK-0036.json")
    assert "delivery_gate_dependencies" not in ordinary
    Draft202012Validator(WorkingRepository(repository).json(TASK_SCHEMA)).validate(ordinary)


@pytest.mark.parametrize(
    "path", ["/absolute", "../escape", "C:/host", "a/**", "a\\b", "a/../b", "a//b", "./a"]
)
def test_registry_paths_fail_closed(repository: Path, path: str) -> None:
    registry = WorkingRepository(repository).json(REGISTRY)
    registry["gates"][0]["required_outputs"][0]["path"] = path
    with pytest.raises(GateError):
        validate_schema(registry, WorkingRepository(repository).json(SCHEMA))


def test_digest_deterministic_and_duplicate_json_keys_fail_closed() -> None:
    gate = WorkingRepository(ROOT).json(REGISTRY)["gates"][0]
    reordered = dict(reversed(list(gate.items())))
    assert definition_digest(gate) == definition_digest(reordered)
    with pytest.raises(GateError, match="duplicate JSON key"):
        parse(b'{"gates":[],"gates":[]}')


def test_unknown_properties_duplicates_and_authoral_satisfaction_rejected(repository: Path) -> None:
    reader = WorkingRepository(repository)
    schema, registry = reader.json(SCHEMA), reader.json(REGISTRY)
    registry["gates"][0]["satisfied"] = True
    with pytest.raises(GateError, match="schema invalid"):
        validate_schema(registry, schema)
    task = reader.json(".codex/tasks/TASK-0038.json")
    task["delivery_gate_dependencies"] = [GATE_ID, GATE_ID]
    write(repository, ".codex/tasks/TASK-0038.json", task)
    assert planning_errors(repository)


def test_current_definition_must_exist_in_consumer_base(repository: Path) -> None:
    from .fixture import git

    base = git(repository, "rev-parse", "HEAD")
    registry = WorkingRepository(repository).json(REGISTRY)
    registry["gates"][0]["stage_story_dependencies"] = ["STORY-0036"]
    write(repository, REGISTRY, registry)
    assert "current canonical" in ";".join(ready_errors(repository, "TASK-0038", base))


def test_story_graph_is_not_modified_by_planning_validation(repository: Path) -> None:
    before = (repository / GRAPH).read_bytes()
    validate_planning(WorkingRepository(repository))
    assert (repository / GRAPH).read_bytes() == before


def test_stage_b_without_scope_preserves_gate_and_full_story_dependency(repository: Path) -> None:
    from .fixture import commit

    owner = WorkingRepository(repository).json(".codex/tasks/TASK-0738.json")
    del owner["delivery_gate_scope"]
    write(repository, ".codex/tasks/TASK-0738.json", owner)
    assert planning_errors(repository) == []
    base = commit(repository, "test: resume functional Stage B")
    failures = ready_errors(repository, "TASK-0738", base)
    assert failures == ["Story dependency not integrated/done at consumer base: STORY-0185"]
