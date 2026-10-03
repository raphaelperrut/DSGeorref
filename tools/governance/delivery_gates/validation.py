"""Planning validation and mandatory immutable consumer-base readiness mode."""

from __future__ import annotations

import argparse
import csv
import io
import sys
from pathlib import Path
from typing import Any

from jsonschema.exceptions import SchemaError, ValidationError

from .model import REGISTRY, SCHEMA, TASK_SCHEMA, GateError, definition_digest, require
from .planning import validate_planning
from .repository import GitRepository, WorkingRepository
from .satisfaction import require_satisfied

ROOT = Path(__file__).resolve().parents[3]


def planning_errors(root: Path) -> list[str]:
    try:
        validate_planning(WorkingRepository(root))
        return []
    except (GateError, ValidationError, SchemaError, ValueError, KeyError, TypeError) as error:
        return [f"delivery gate planning: {error}"]


def bound_current_task(
    root: Path, repository: GitRepository, task_id: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    current = WorkingRepository(root)
    for path in (REGISTRY, SCHEMA, TASK_SCHEMA):
        require(
            repository.json(path) == current.json(path),
            "consumer base does not contain current canonical gate definitions/schemas",
        )
    current_tasks, gates = validate_planning(current)
    base_tasks, _ = validate_planning(repository)
    require(task_id in current_tasks and task_id in base_tasks, "current/base ready task missing")
    task, snapshot = current_tasks[task_id], base_tasks[task_id]
    # Bind the complete validated authorization, including references and write scope.
    # The only normalization is the approved absent gate list == [] default.
    authorizations = [
        {**envelope, "delivery_gate_dependencies": envelope.get("delivery_gate_dependencies", [])}
        for envelope in (task, snapshot)
    ]
    require(
        definition_digest(authorizations[0]) == definition_digest(authorizations[1]),
        f"consumer base differs from current canonical TaskEnvelope authorization: {task_id}",
    )
    return task, gates


def ready_errors(root: Path, task_id: str, consumer_base: str) -> list[str]:
    try:
        repository = GitRepository(root, consumer_base)
        task, gates = bound_current_task(root, repository, task_id)
        statuses = {
            row["story_id"]: row["status"].lower()
            for row in csv.DictReader(
                io.StringIO(repository.read("docs/06-delivery/STORY_INDEX.csv").decode("utf-8-sig"))
            )
        }
        scope = task.get("delivery_gate_scope")
        dependencies = (
            gates[scope["gate_id"]]["stage_story_dependencies"]
            if scope
            else task.get("dependencies", [])
        )
        failures = [
            f"Story dependency not integrated/done at consumer base: {story}"
            for story in dependencies
            if statuses.get(story) != "done"
        ]
        for gate_id in task.get("delivery_gate_dependencies", []):
            try:
                require_satisfied(repository, gates[gate_id])
            except (GateError, ValueError, KeyError, TypeError) as error:
                failures.append(str(error))
        return failures
    except (GateError, ValidationError, SchemaError, ValueError, KeyError, TypeError) as error:
        return [f"READY fail-closed: {error}"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SharedPartialDeliveryGate enforcement")
    parser.add_argument("--ready-task")
    parser.add_argument("--consumer-base")
    args = parser.parse_args(argv)
    if bool(args.ready_task) != bool(args.consumer_base):
        parser.error("--ready-task and --consumer-base must be provided together")
    failures = planning_errors(ROOT)
    if args.ready_task and not failures:
        failures = ready_errors(ROOT, args.ready_task, args.consumer_base)
    for failure in failures:
        print(failure)
    print("DELIVERY GATES FAIL" if failures else "DELIVERY GATES PASS")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
