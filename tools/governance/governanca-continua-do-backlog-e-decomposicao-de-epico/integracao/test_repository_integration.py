from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[4]
TASK_PATH = Path(".codex/tasks/TASK-0686.json")
CONSOLIDATION_TEST_PATH = Path(
    "tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/"
    "consolidacao/test_slice_consolidation.py"
)
VALIDATOR_PATH = Path(
    "tools/quality/contexts/engineering_governance/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico/validator.py"
)
EVIDENCE_SCOPE = "evidence/implementation/epic-110/story-0686/**"
DEPENDENCY_COMMITS = {
    "STORY-0684": "a409ef45232d04283ac4cf5a7d71c6f4606342e5",
    "STORY-0685": "c1f46422db4ab430adcac7faaf870f6f18af76e6",
}


def _load_module(name: str, path: Path) -> ModuleType:
    module_path = ROOT / path
    module_directory = str(module_path.parent)
    if module_directory not in sys.path:
        sys.path.insert(0, module_directory)
    spec = importlib.util.spec_from_file_location(name, module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _assert_ancestor(commit: str) -> None:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, (
        f"dependency commit {commit} is not in candidate HEAD: {completed.stderr}"
    )


def test_epic_110_integracao(tmp_path: Path) -> None:
    task = json.loads((ROOT / TASK_PATH).read_text(encoding="utf-8"))
    assert task["dependencies"] == list(DEPENDENCY_COMMITS)
    assert EVIDENCE_SCOPE in task["allow_paths"]
    assert EVIDENCE_SCOPE in task["phase_f_review"]["files"]["allow_paths"]
    for commit in DEPENDENCY_COMMITS.values():
        _assert_ancestor(commit)

    consolidation = _load_module("epic_110_slice_consolidation", CONSOLIDATION_TEST_PATH)
    consolidation.test_story_0684_slice_consolidation()

    validator = _load_module("epic_110_integration_validator", VALIDATOR_PATH)
    report = validator.build_report(ROOT)
    assert report["status"] == "PASS"
    assert report["failure_policy"] == "FAIL_CLOSED"
    assert report["execution_mode"] == "READ_ONLY"
    assert report["destructive_actions"] is False
    assert report["findings"] == []

    first_failure = validator.build_report(tmp_path)
    second_failure = validator.build_report(tmp_path)
    assert first_failure == second_failure
    assert first_failure["status"] == "FAIL"
    assert first_failure["failure_policy"] == "FAIL_CLOSED"
    assert first_failure["findings"]
    assert tuple(tmp_path.iterdir()) == ()
