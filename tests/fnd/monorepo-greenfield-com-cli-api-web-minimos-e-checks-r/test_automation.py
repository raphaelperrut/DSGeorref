from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SLUG = "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r"
VALIDATOR_REL = Path(
    f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py"
)
QUALITY_DIR_REL = VALIDATOR_REL.parent
FOUNDATION_TOOL_DIR_REL = Path(f"tools/governance/{SLUG}")
FOUNDATION_REL = Path(
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/foundation-plan.json"
)
CONTRACT_ROOT_REL = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
TASK_REL = Path(".codex/tasks/TASK-0013.json")
TASK_SCHEMA_REL = Path(".codex/tasks/TASK_ENVELOPE.schema.json")
TEST_DIR_REL = Path(f"tests/fnd/{SLUG}")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
SENTINEL_REL = Path("unrelated-sentinel.bin")
SENTINEL_BYTES = b"ISSUE-0123 unrelated sentinel\x00\xff\n"


@dataclass(frozen=True)
class Execution:
    returncode: int
    stdout: bytes
    stderr: bytes
    snapshot: tuple[tuple[str, str], ...]


Mutation = Callable[[Path], None]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _snapshot(root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            (path.relative_to(root).as_posix(), _sha256(path.read_bytes()))
            for path in root.rglob("*")
            if path.is_file()
        )
    )


def _copy_sources(root: Path) -> None:
    sources = [
        *(ROOT / QUALITY_DIR_REL).glob("*.py"),
        *(ROOT / FOUNDATION_TOOL_DIR_REL).glob("*.py"),
        *(ROOT / CONTRACT_ROOT_REL).rglob("*"),
        *(ROOT / TEST_DIR_REL).glob("test_foundation*.py"),
        ROOT / FOUNDATION_REL,
        ROOT / TASK_REL,
        ROOT / TASK_SCHEMA_REL,
        ROOT / WORKFLOW_REL,
    ]
    for source in sources:
        if not source.is_file():
            continue
        destination = root / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    (root / SENTINEL_REL).write_bytes(SENTINEL_BYTES)


def _execute(root: Path, *, dry_run: bool = False) -> Execution:
    command = [
        sys.executable,
        "-B",
        str(root / VALIDATOR_REL),
        "--repository-root",
        str(root),
    ]
    if dry_run:
        command.append("--dry-run")
    environment = os.environ.copy()
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"})
    completed = subprocess.run(
        command,
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
    )
    return Execution(completed.returncode, completed.stdout, completed.stderr, _snapshot(root))


def _read_json(root: Path, relative: Path) -> dict[str, object]:
    loaded = json.loads((root / relative).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_json(root: Path, relative: Path, value: dict[str, object]) -> None:
    (root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _missing_foundation(root: Path) -> None:
    (root / FOUNDATION_REL).unlink()


def _silent_fallback(root: Path) -> None:
    plan = _read_json(root, FOUNDATION_REL)
    policy = plan["failure_policy"]
    assert isinstance(policy, dict)
    policy["mode"] = "BEST_EFFORT"
    policy["silent_fallback"] = True
    _write_json(root, FOUNDATION_REL, plan)


def _missing_requirement_test(root: Path) -> None:
    path = root / TEST_DIR_REL / "test_foundation_contract.py"
    source = path.read_text(encoding="utf-8")
    path.write_text(
        source.replace("def test_cli_api_semantic_contract", "def removed_contract_test"),
        encoding="utf-8",
    )


def _invalid_task(root: Path) -> None:
    task = _read_json(root, TASK_REL)
    task["tests"] = ["untracked_test"]
    _write_json(root, TASK_REL, task)


def _invalid_workflow(root: Path) -> None:
    path = root / WORKFLOW_REL
    path.write_text(path.read_text(encoding="utf-8").replace(" --dry-run", ""), encoding="utf-8")


def _assert_failure(execution: Execution, code: str) -> None:
    report = json.loads(execution.stdout)
    assert execution.returncode != 0
    assert execution.stderr == b""
    assert report["status"] == "FAIL"
    assert report["destructive_actions"] == 0
    assert code in {finding["code"] for finding in report["findings"]}


def test_epic_003_automacao() -> None:
    with tempfile.TemporaryDirectory(prefix="issue-0123-valid-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        before = _snapshot(sandbox)
        first = _execute(sandbox)
        second = _execute(sandbox)
        dry_first = _execute(sandbox, dry_run=True)
        dry_second = _execute(sandbox, dry_run=True)
        assert {
            first.returncode,
            second.returncode,
            dry_first.returncode,
            dry_second.returncode,
        } == {0}
        assert first == second
        assert dry_first == dry_second
        assert before == first.snapshot == dry_first.snapshot
        report = json.loads(first.stdout)
        assert report["status"] == "PASS"
        assert report["mode"] == "READ_ONLY"
        assert json.loads(dry_first.stdout)["mode"] == "DRY_RUN"
        assert report["requirements"] == ["REQ-DEL-001", "REQ-DEV-001", "REQ-TOP-001"]
        assert report["acceptance_criteria"] == [
            "AC-ISSUE-0123-01",
            "AC-ISSUE-0123-02",
            "AC-ISSUE-0123-03",
            "AC-ISSUE-0123-04",
        ]
        assert dict(first.snapshot)[SENTINEL_REL.as_posix()] == _sha256(SENTINEL_BYTES)

    cases: tuple[tuple[str, str, Mutation], ...] = (
        ("missing_foundation", "FOUNDATION_UNREADABLE", _missing_foundation),
        ("silent_fallback", "FAILURE_POLICY_INVALID", _silent_fallback),
        ("missing_requirement_test", "REQUIREMENT_TEST_MISSING", _missing_requirement_test),
        ("invalid_task", "TASK_CONTROL_INVALID", _invalid_task),
        ("invalid_workflow", "WORKFLOW_INVALID", _invalid_workflow),
    )
    for name, code, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0123-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            mutate(sandbox)
            before = _snapshot(sandbox)
            first = _execute(sandbox, dry_run=True)
            second = _execute(sandbox, dry_run=True)
            _assert_failure(first, code)
            assert first == second
            assert before == first.snapshot
