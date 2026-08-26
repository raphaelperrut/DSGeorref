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
    "tools/governance/repositorio-privado-project-central-views-campos-label"
)
sys.path.insert(0, str(MODULE_ROOT))

from repository_integration import (  # noqa: E402
    CONTRACT_ROOT,
    GRAPH_PATH,
    QUALITY_ROOT,
    REQUIREMENT_PATHS,
    STORY_PATH,
    TASK_PATH,
    TEST_PATH,
    TOOL_ROOT,
    TRACE_PATH,
    WORKFLOW_PATH,
    Finding,
    validate_repository_integration,
    validate_requirement_traceability,
)


Mutation = Callable[[Path], None]
OWNERSHIP_PATH = Path("contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv")
EXTERNAL_CONTRACTS = (
    Path(".codex/tasks/TASK_ENVELOPE.schema.json"),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "foundation-boundaries.schema.json"
    ),
)
AUTOMATION_TEST = Path(
    "tests/fnd/repositorio-privado-project-central-views-campos-label/"
    "test_automation.py"
)


def _copy_file(destination: Path, relative: Path) -> None:
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, target)


def _fixture(destination: Path) -> Path:
    for directory in (TOOL_ROOT, QUALITY_ROOT, CONTRACT_ROOT):
        shutil.copytree(ROOT / directory, destination / directory, dirs_exist_ok=True)
    files = (
        TASK_PATH,
        STORY_PATH,
        GRAPH_PATH,
        TRACE_PATH,
        WORKFLOW_PATH,
        TEST_PATH,
        AUTOMATION_TEST,
        OWNERSHIP_PATH,
        *EXTERNAL_CONTRACTS,
        *REQUIREMENT_PATHS.values(),
    )
    for relative in files:
        _copy_file(destination, relative)
    return destination


def _mutate_json(
    root: Path, relative: Path, change: Callable[[dict[str, Any]], None]
) -> None:
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


def _remove_requirement(root: Path) -> None:
    (root / REQUIREMENT_PATHS["REQ-NATIVE-004"]).unlink()


def _remove_dependency(root: Path) -> None:
    def change(graph: dict[str, Any]) -> None:
        graph["edges"] = [
            edge
            for edge in graph["edges"]
            if not (edge.get("from") == "STORY-0008" and edge.get("to") == "STORY-0009")
        ]

    _mutate_json(root, GRAPH_PATH, change)


def _drift_requirement(root: Path) -> None:
    path = root / TRACE_PATH
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("test_req_classicprofile_006", "test_requirement_drifted", 1),
        encoding="utf-8",
    )


def _duplicate_requirement(root: Path) -> None:
    def change(task: dict[str, Any]) -> None:
        task["references"].append(REQUIREMENT_PATHS["REQ-NATIVE-001"].as_posix())

    _mutate_json(root, TASK_PATH, change)


def _disconnect_workflow(root: Path) -> None:
    path = root / WORKFLOW_PATH
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace(TEST_PATH.as_posix(), "integration-test-removed"),
        encoding="utf-8",
    )


def _duplicate_rule(root: Path) -> None:
    source = root / TOOL_ROOT / "repository_structure.py"
    shutil.copy2(source, source.with_name("duplicated_structure.py"))


def _create_import_cycle(root: Path) -> None:
    cycle_root = root / TOOL_ROOT / "integration-cycle"
    cycle_root.mkdir(parents=True)
    (cycle_root / "cycle_a.py").write_text("from cycle_b import VALUE\n", encoding="utf-8")
    (cycle_root / "cycle_b.py").write_text("from cycle_a import VALUE\n", encoding="utf-8")


def _create_dependency_cycle(root: Path) -> None:
    def change(graph: dict[str, Any]) -> None:
        graph["edges"].append(
            {"from": "STORY-0009", "to": "STORY-0007", "relation": "blocks"}
        )

    _mutate_json(root, GRAPH_PATH, change)


def _assert_requirement(requirement_id: str) -> None:
    assert validate_requirement_traceability(ROOT, requirement_id) == ()


def test_req_classicprofile_006() -> None:
    _assert_requirement("REQ-CLASSICPROFILE-006")


def test_req_classicprofile_008() -> None:
    _assert_requirement("REQ-CLASSICPROFILE-008")


def test_req_classicprofile_0010() -> None:
    _assert_requirement("REQ-CLASSICPROFILE-010")


def test_req_native_001() -> None:
    _assert_requirement("REQ-NATIVE-001")


def test_req_native_004() -> None:
    _assert_requirement("REQ-NATIVE-004")


def test_epic_002_integracao() -> None:
    first = validate_repository_integration(ROOT)
    assert first == ()
    assert validate_repository_integration(ROOT) == first

    cases: tuple[tuple[str, Mutation, str], ...] = (
        ("missing-requirement", _remove_requirement, "REQUIREMENT_DOCUMENT_INVALID"),
        ("missing-dependency", _remove_dependency, "DEPENDENCY_GRAPH_MISMATCH"),
        ("requirement-drift", _drift_requirement, "REQUIREMENT_TRACE_DRIFT"),
        ("requirement-duplicate", _duplicate_requirement, "REQUIREMENT_TRACE_DUPLICATED"),
        ("control-plane", _disconnect_workflow, "CONTROL_PLANE_INVALID"),
        ("rule-duplicate", _duplicate_rule, "RULE_DUPLICATED"),
        ("import-cycle", _create_import_cycle, "PYTHON_IMPORT_CYCLE"),
        ("dependency-cycle", _create_dependency_cycle, "DEPENDENCY_CYCLE"),
    )
    with tempfile.TemporaryDirectory(prefix=".issue-0119-integration-", dir=ROOT) as temporary:
        temporary_root = Path(temporary)
        for name, mutate, expected in cases:
            root = _fixture(temporary_root / name)
            mutate(root)
            _assert_failure(root, expected)
