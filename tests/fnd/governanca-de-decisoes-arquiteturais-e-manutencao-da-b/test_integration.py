from __future__ import annotations

import json
import shutil
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b"
)
sys.path.insert(0, str(MODULE_ROOT))

from repository_integration import (  # noqa: E402
    GRAPH_PATH,
    REQUIRED_SURFACES,
    STORY_PATH,
    TASK_PATH,
    TOOL_ROOT,
    WORKFLOW_PATH,
    Finding,
    validate_repository_integration,
)


Mutation = Callable[[Path], None]


def _copy_file(destination: Path, relative: Path) -> None:
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, target)


def _fixture(destination: Path) -> Path:
    for relative in (TASK_PATH, STORY_PATH, GRAPH_PATH, WORKFLOW_PATH, *REQUIRED_SURFACES):
        _copy_file(destination, relative)
    shutil.copytree(ROOT / TOOL_ROOT, destination / TOOL_ROOT, dirs_exist_ok=True)
    return destination


def _mutate_json(root: Path, relative: Path, change: Callable[[dict[str, Any]], None]) -> None:
    path = root / relative
    value = json.loads(path.read_text(encoding="utf-8"))
    change(value)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _codes(findings: tuple[Finding, ...]) -> set[str]:
    return {finding.code for finding in findings}


def _assert_failure(root: Path, expected: str) -> None:
    first = validate_repository_integration(root)
    second = validate_repository_integration(root)
    assert first == second
    assert expected in _codes(first)


def _remove_integration_scope(root: Path) -> None:
    def change(task: dict[str, Any]) -> None:
        path = (
            "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
            "test_integration.py"
        )
        task["allow_paths"].remove(path)

    _mutate_json(root, TASK_PATH, change)


def _remove_dependency(root: Path) -> None:
    def change(graph: dict[str, Any]) -> None:
        graph["edges"] = [
            edge
            for edge in graph["edges"]
            if not (edge.get("from") == "STORY-0759" and edge.get("to") == "STORY-0004")
        ]

    _mutate_json(root, GRAPH_PATH, change)


def _disconnect_control_plane(root: Path) -> None:
    path = root / WORKFLOW_PATH
    text = path.read_text(encoding="utf-8")
    disconnected = text.replace(
        "test_epic_001_integracao", "integration_test_removed"
    )
    path.write_text(disconnected, encoding="utf-8")


def _create_import_cycle(root: Path) -> None:
    cycle_root = root / TOOL_ROOT / "integration-cycle"
    cycle_root.mkdir(parents=True)
    (cycle_root / "cycle_a.py").write_text("from cycle_b import VALUE\n", encoding="utf-8")
    (cycle_root / "cycle_b.py").write_text("from cycle_a import VALUE\n", encoding="utf-8")


def test_epic_001_integracao() -> None:
    first = validate_repository_integration(ROOT)
    assert first == ()
    assert validate_repository_integration(ROOT) == first

    with tempfile.TemporaryDirectory(
        prefix=".issue-0114-integration-", dir=ROOT
    ) as temporary:
        cases: tuple[tuple[str, Mutation, str], ...] = (
            ("scope", _remove_integration_scope, "TASK_SCOPE_INVALID"),
            ("dependency", _remove_dependency, "DEPENDENCY_GRAPH_MISMATCH"),
            ("control-plane", _disconnect_control_plane, "CONTROL_PLANE_INVALID"),
            ("import-cycle", _create_import_cycle, "PYTHON_IMPORT_CYCLE"),
        )
        for name, mutate, expected in cases:
            root = _fixture(Path(temporary) / name)
            mutate(root)
            _assert_failure(root, expected)
