from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[3]
SLUG = "ruleset-de-main-checks-unicos-codeowners-politica-de-b"
TOOL_ROOT = ROOT / "tools/governance" / SLUG
TOOL_PATH = TOOL_ROOT / "integration_validation.py"


def _load_tool() -> ModuleType:
    sys.path.insert(0, str(TOOL_ROOT))
    spec = importlib.util.spec_from_file_location("main_ruleset_integration_validation", TOOL_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TOOL = _load_tool()


def _read_json(root: Path, relative: Path) -> dict[str, Any]:
    value = json.loads((root / relative).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _write_json(root: Path, relative: Path, value: dict[str, Any]) -> None:
    (root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _copy_sources(destination: Path) -> None:
    files = [
        Path(".codex/tasks/TASK-0561.json"),
        TOOL.TASK_PATH,
        Path(".github/CODEOWNERS"),
        Path(".github/workflows/ci.yml"),
        TOOL.WORKFLOW_PATH,
        Path("Makefile"),
        Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}/main-ruleset-governance.schema.json"),
        Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}/examples/main-ruleset-governance.json"),
        Path(f"tools/governance/{SLUG}/foundation_validation.py"),
        Path(f"tools/governance/{SLUG}/foundation-checkpoint.json"),
        Path(f"tools/governance/{SLUG}/main_ruleset_policy_validation.py"),
        TOOL.VALIDATOR_PATH,
        TOOL.CONTROL_ROOT / "main-ruleset.json",
        TOOL.CONTROL_ROOT / "required-check-registry.json",
        TOOL.CHECKPOINT_PATH,
        TOOL.EVIDENCE_PATH,
        TOOL.TEST_PATH,
    ]
    for relative in files:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)


def _missing_integration_check(root: Path) -> None:
    registry = _read_json(root, TOOL.CONTROL_ROOT / "required-check-registry.json")
    ruleset = _read_json(root, TOOL.CONTROL_ROOT / "main-ruleset.json")
    registry["required_checks"] = registry["required_checks"][:1]
    ruleset["required_check_policy"]["required_contexts"] = ["verify-foundation"]
    _write_json(root, TOOL.CONTROL_ROOT / "required-check-registry.json", registry)
    _write_json(root, TOOL.CONTROL_ROOT / "main-ruleset.json", ruleset)


def _ignored_workflow_failure(root: Path) -> None:
    path = root / TOOL.WORKFLOW_PATH
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "    timeout-minutes: 10", "    timeout-minutes: 10\n    continue-on-error: true"
        ),
        encoding="utf-8",
    )


def _evidence_drift(root: Path) -> None:
    evidence = _read_json(root, TOOL.EVIDENCE_PATH)
    evidence["status"] = "UNKNOWN"
    _write_json(root, TOOL.EVIDENCE_PATH, evidence)


def _dependency_cycle(root: Path) -> None:
    path = root / f"tools/governance/{SLUG}/main_ruleset_policy_validation.py"
    path.write_text(
        path.read_text(encoding="utf-8") + "\nimport integration_validation\n",
        encoding="utf-8",
    )


def _missing_required_test(root: Path) -> None:
    path = root / TOOL.TEST_PATH
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "def test_epic_091_integracao", "def removed_epic_091_integracao"
        ),
        encoding="utf-8",
    )


def test_epic_091_integracao() -> None:
    report = TOOL.validate_integration(ROOT)
    assert report == {
        "acceptance_evidence": TOOL.ACCEPTANCE_EVIDENCE,
        "decision": "PASS",
        "issue_id": "ISSUE-0673",
        "live_ruleset_enforcement": "NOT_ASSERTED_BY_INTEGRATION",
        "required_checks": ["verify-foundation", "validate-main-ruleset-controls"],
        "requirement_evidence": TOOL.REQUIREMENT_EVIDENCE,
    }

    checkpoint = _read_json(ROOT, TOOL.CHECKPOINT_PATH)
    assert checkpoint["architecture_evidence"] == {
        "integration_reuses": "foundation_validation.validate_foundation",
        "local_policy_reimplementation": "NONE",
        "dependency_direction": (
            "integration_validation -> foundation_validation -> main_ruleset_policy_validation"
        ),
    }
    assert TOOL.main(["--repository-root", str(ROOT)]) == 0

    cases: tuple[tuple[str, str, Callable[[Path], None]], ...] = (
        ("missing-check", "required checks are not integrated", _missing_integration_check),
        ("ignored-failure", "may not ignore failures", _ignored_workflow_failure),
        ("evidence-drift", "candidate evidence diverges", _evidence_drift),
        ("dependency-cycle", "dependency cycle", _dependency_cycle),
        ("missing-test", "required integration test missing", _missing_required_test),
    )
    for name, message, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0673-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            mutate(sandbox)
            with pytest.raises(TOOL.IntegrationValidationError, match=message):
                TOOL.validate_integration(sandbox)

    with tempfile.TemporaryDirectory(prefix="issue-0673-invalid-root-") as temporary:
        assert TOOL.main(["--repository-root", temporary]) == 1
