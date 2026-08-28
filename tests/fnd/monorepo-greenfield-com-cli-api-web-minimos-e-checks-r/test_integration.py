from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r"
)
sys.path.insert(0, str(MODULE_ROOT))

from repository_integration import (  # noqa: E402
    EVIDENCE_PATH,
    GRAPH_PATH,
    QUALITY_VALIDATOR,
    STORY_PATH,
    TASK_PATH,
    TEST_PATH,
    TOOL_ROOT,
    WORKFLOW_PATH,
    Finding,
    validate_repository_integration,
)


Mutation = Callable[[Path], None]
QUALITY_ROOT = QUALITY_VALIDATOR.parent
FOUNDATION_DOC_ROOT = Path(
    "docs/03-engineering/contexts/engineering_governance/"
    "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r"
)
CONTRACT_ROOT = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r"
)
TEST_ROOT = TEST_PATH.parent
TASK_0013 = Path(".codex/tasks/TASK-0013.json")
TASK_SCHEMA = Path(".codex/tasks/TASK_ENVELOPE.schema.json")


def _copy_file(destination: Path, relative: Path) -> None:
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, target)


def _fixture(destination: Path) -> Path:
    for relative in (
        TASK_PATH,
        TASK_0013,
        TASK_SCHEMA,
        STORY_PATH,
        GRAPH_PATH,
        WORKFLOW_PATH,
        EVIDENCE_PATH,
    ):
        _copy_file(destination, relative)
    for relative in (TOOL_ROOT, QUALITY_ROOT, FOUNDATION_DOC_ROOT, CONTRACT_ROOT, TEST_ROOT):
        shutil.copytree(ROOT / relative, destination / relative, dirs_exist_ok=True)
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
        task["allow_paths"].remove(TEST_PATH.as_posix())

    _mutate_json(root, TASK_PATH, change)


def _remove_dependency(root: Path) -> None:
    def change(graph: dict[str, Any]) -> None:
        graph["edges"] = [
            edge
            for edge in graph["edges"]
            if not (edge.get("from") == "STORY-0013" and edge.get("to") == "STORY-0014")
        ]

    _mutate_json(root, GRAPH_PATH, change)


def _disconnect_control_plane(root: Path) -> None:
    path = root / WORKFLOW_PATH
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("test_epic_003_integracao", "integration_removed"),
        encoding="utf-8",
    )


def _remove_test_surface(root: Path) -> None:
    path = root / TEST_PATH
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("def test_epic_003_integracao", "def removed_integration_test"),
        encoding="utf-8",
    )


def _enable_silent_fallback(root: Path) -> None:
    def change(plan: dict[str, Any]) -> None:
        plan["failure_policy"]["mode"] = "BEST_EFFORT"
        plan["failure_policy"]["silent_fallback"] = True

    _mutate_json(root, FOUNDATION_DOC_ROOT / "foundation-plan.json", change)


def _create_import_cycle(root: Path) -> None:
    tool_root = root / TOOL_ROOT
    (tool_root / "cycle_a.py").write_text("from cycle_b import VALUE\n", encoding="utf-8")
    (tool_root / "cycle_b.py").write_text("from cycle_a import VALUE\n", encoding="utf-8")


def _duplicate_rule(root: Path) -> None:
    shutil.copy2(root / TOOL_ROOT / "foundation_contract.py", root / TOOL_ROOT / "duplicate.py")


def test_epic_003_integracao() -> None:
    first = validate_repository_integration(ROOT)
    assert first == ()
    assert validate_repository_integration(ROOT) == first

    command = [sys.executable, "-B", str(MODULE_ROOT / "repository_integration.py")]
    environment = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "PYTHONUTF8": "1",
    }
    first_cli = subprocess.run(
        command, check=False, capture_output=True, text=True, env=environment
    )
    second_cli = subprocess.run(
        command, check=False, capture_output=True, text=True, env=environment
    )
    assert (
        first_cli.returncode,
        first_cli.stdout,
        first_cli.stderr,
    ) == (
        second_cli.returncode,
        second_cli.stdout,
        second_cli.stderr,
    )
    assert first_cli.returncode == 0
    report = json.loads(first_cli.stdout)
    assert report["status"] == "PASS"
    assert report["requirements"] == ["REQ-DEL-001", "REQ-DEV-001", "REQ-TOP-001"]
    assert report["acceptance_criteria"] == [
        "AC-ISSUE-0124-01",
        "AC-ISSUE-0124-02",
        "AC-ISSUE-0124-03",
        "AC-ISSUE-0124-04",
    ]

    with tempfile.TemporaryDirectory(prefix=".issue-0124-integration-", dir=ROOT) as temporary:
        cases: tuple[tuple[str, Mutation, str], ...] = (
            ("scope", _remove_integration_scope, "TASK_SCOPE_INVALID"),
            ("dependency", _remove_dependency, "DEPENDENCY_GRAPH_MISMATCH"),
            ("control-plane", _disconnect_control_plane, "CONTROL_PLANE_INVALID"),
            ("test-surface", _remove_test_surface, "TEST_SURFACE_INVALID"),
            ("silent-fallback", _enable_silent_fallback, "FAILURE_POLICY_INVALID"),
            ("import-cycle", _create_import_cycle, "PYTHON_IMPORT_CYCLE"),
            ("duplicate-rule", _duplicate_rule, "RULE_DUPLICATED"),
        )
        for name, mutate, expected in cases:
            root = _fixture(Path(temporary) / name)
            mutate(root)
            _assert_failure(root, expected)
