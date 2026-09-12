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
SLUG = "issue-forms-templates-e-taxonomia-de-tipos-com-validac"
VALIDATOR_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py")
FOUNDATION_VALIDATOR_REL = Path(f"tools/governance/{SLUG}/validate_issue_forms.py")
CONTRACT_REL = Path(
    f"contracts/contexts/engineering_governance/fnd/{SLUG}/examples/issue-form-governance.json"
)
REGISTRY_REL = Path(
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/issue-form-registry.json"
)
TASK_REL = Path(".codex/tasks/TASK-0557.json")
FOUNDATION_TASK_REL = Path(".codex/tasks/TASK-0556.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
FOUNDATION_WORKFLOW_REL = Path(".github/workflows/issue-form-governance.yaml")
TEST_REL = Path(__file__).relative_to(ROOT)
EVIDENCE_REL = Path("evidence/operations/epic-090/story-0557/validation.json")
SENTINEL_REL = Path("unrelated-sentinel.bin")
SENTINEL_BYTES = b"ISSUE-0667 unrelated sentinel\x00\xff\n"


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
        ROOT / VALIDATOR_REL,
        ROOT / FOUNDATION_VALIDATOR_REL,
        ROOT / CONTRACT_REL,
        ROOT / REGISTRY_REL,
        ROOT / TASK_REL,
        ROOT / FOUNDATION_TASK_REL,
        ROOT / WORKFLOW_REL,
        ROOT / FOUNDATION_WORKFLOW_REL,
        ROOT / TEST_REL,
        ROOT / EVIDENCE_REL,
        *(ROOT / ".github/ISSUE_TEMPLATE").glob("*.yml"),
    ]
    for source in sources:
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
    return Execution(
        completed.returncode,
        completed.stdout,
        completed.stderr,
        _snapshot(root),
    )


def _read_json(root: Path, relative: Path) -> dict[str, object]:
    loaded = json.loads((root / relative).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_json(root: Path, relative: Path, value: dict[str, object]) -> None:
    (root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _unregistered_type(root: Path) -> None:
    registry = _read_json(root, REGISTRY_REL)
    forms = registry["forms"]
    assert isinstance(forms, list) and isinstance(forms[-1], dict)
    forms[-1]["type"] = "CHORE"
    _write_json(root, REGISTRY_REL, registry)


def _invalid_task(root: Path) -> None:
    task = _read_json(root, TASK_REL)
    task["tests"] = ["untracked_test"]
    _write_json(root, TASK_REL, task)


def _invalid_workflow(root: Path) -> None:
    path = root / WORKFLOW_REL
    path.write_text(
        path.read_text(encoding="utf-8").replace("--dry-run", "--write"),
        encoding="utf-8",
    )


def _missing_test(root: Path) -> None:
    path = root / TEST_REL
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "def test_epic_090_automacao", "def removed_epic_090_automacao"
        ),
        encoding="utf-8",
    )


def _invalid_evidence(root: Path) -> None:
    evidence = _read_json(root, EVIDENCE_REL)
    evidence["status"] = "UNKNOWN"
    _write_json(root, EVIDENCE_REL, evidence)


def _assert_failure(execution: Execution, code: str) -> None:
    report = json.loads(execution.stdout)
    assert execution.returncode == 1
    assert execution.stderr == b""
    assert report["status"] == "FAIL"
    assert report["destructive_actions"] == 0
    matching = [finding for finding in report["findings"] if finding["code"] == code]
    assert matching, report["findings"]
    assert all(finding["detail"] and finding["remediation"] for finding in matching)


def test_epic_090_automacao() -> None:
    with tempfile.TemporaryDirectory(prefix="issue-0667-valid-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        before = _snapshot(sandbox)
        first = _execute(sandbox)
        second = _execute(sandbox)
        dry_first = _execute(sandbox, dry_run=True)
        dry_second = _execute(sandbox, dry_run=True)

        returncodes = {
            first.returncode,
            second.returncode,
            dry_first.returncode,
            dry_second.returncode,
        }
        assert returncodes == {0}
        assert first == second
        assert dry_first == dry_second
        assert before == first.snapshot == dry_first.snapshot
        report = json.loads(first.stdout)
        dry_report = json.loads(dry_first.stdout)
        assert report["status"] == "PASS"
        assert report["mode"] == "READ_ONLY"
        assert dry_report["mode"] == "DRY_RUN"
        assert report["destructive_actions"] == 0
        assert report["requirement_evidence"] == {"REQ-GOV-002": "test_epic_090_automacao"}
        assert set(report["acceptance_evidence"]) == {
            "AC-ISSUE-0667-01",
            "AC-ISSUE-0667-02",
            "AC-ISSUE-0667-03",
            "AC-ISSUE-0667-04",
        }
        assert dict(first.snapshot)[SENTINEL_REL.as_posix()] == _sha256(SENTINEL_BYTES)

    cases: tuple[tuple[str, str, Mutation], ...] = (
        ("unregistered_type", "ISSUE_TYPE_INVALID", _unregistered_type),
        ("task_drift", "TASK_CONTROL_INVALID", _invalid_task),
        ("workflow_drift", "WORKFLOW_INVALID", _invalid_workflow),
        ("missing_test", "REQUIRED_TEST_MISSING", _missing_test),
        ("evidence_drift", "EVIDENCE_INVALID", _invalid_evidence),
    )
    for name, code, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0667-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            mutate(sandbox)
            before = _snapshot(sandbox)
            first = _execute(sandbox, dry_run=True)
            second = _execute(sandbox, dry_run=True)
            _assert_failure(first, code)
            assert first == second
            assert before == first.snapshot
