"""Planning validation and mandatory immutable consumer-base readiness mode."""

from __future__ import annotations

import argparse
import csv
import io
import sys
from pathlib import Path

from jsonschema.exceptions import SchemaError, ValidationError

from .model import REGISTRY, SCHEMA, TASK_SCHEMA, GateError, require
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


def ready_errors(root: Path, task_id: str, consumer_base: str) -> list[str]:
    try:
        repository = GitRepository(root, consumer_base)
        tasks, gates = validate_planning(repository)
        require(
            repository.json(REGISTRY) == WorkingRepository(root).json(REGISTRY),
            "consumer base does not contain current canonical gate definitions",
        )
        for path in (SCHEMA, TASK_SCHEMA):
            require(
                repository.json(path) == WorkingRepository(root).json(path),
                "consumer base does not contain current canonical schemas",
            )
        task = tasks.get(task_id)
        if task is None:
            raise GateError("unknown ready task")
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
