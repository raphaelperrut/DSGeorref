from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SLUG = "fechamento-da-sprint-001-e-autorizacao-da-primeira-fat"
VALIDATOR_REL = Path(
    f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py"
)
TASK_REL = Path(".codex/tasks/TASK-0567.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
TEST_REL = Path(__file__).relative_to(ROOT)
EVIDENCE_REL = Path("evidence/operations/epic-092/story-0567/validation.json")
FOUNDATION_REL = Path(f"tools/governance/{SLUG}/foundation_validation.py")
SENTINEL_REL = Path("unrelated-sentinel.bin")
SENTINEL_BYTES = b"ISSUE-0677 unrelated sentinel\x00\xff\n"


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
            if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
        )
    )


def _copy_sources(root: Path) -> None:
    sources = [
        ROOT / VALIDATOR_REL,
        ROOT / TASK_REL,
        ROOT / WORKFLOW_REL,
        ROOT / TEST_REL,
        ROOT / EVIDENCE_REL,
    ]
    for source in sources:
        destination = root / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    (root / SENTINEL_REL).write_bytes(SENTINEL_BYTES)


def _write_foundation_stub(root: Path, *, passing: bool = True) -> None:
    report = {
        "decision": "PASS" if passing else "FAIL",
        "issue_id": "ISSUE-0676",
        "reviewable_state": "READY_FOR_INDEPENDENT_REVIEW",
        "authorization_claim": "NOT_ASSERTED_BY_FOUNDATION",
        "requirement_evidence": {
            "REQ-DEV-001": "test_host_container_ci_contract_and_no_implicit_downloads",
            "REQ-FRZ-001": "test_foundation_baseline_digest_controlled_change_and_adr_supersession",
            "REQ-FRZ-002": "test_sprint_zero_authorization_and_functional_foundation_gate_blocking",
            "REQ-FRZ-003": "test_issue_adr_decision_package_impact_boundary_and_no_silent_divergence",
            "REQ-FRZ-004": "test_foundation_closure_evidence_set_and_material_reopening_criteria",
            "REQ-GOV-005": "test_sprint_zero_baseline_decision_09",
        },
    }
    if not passing:
        report["error"] = "controlled foundation failure"
    path = root / FOUNDATION_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "import json, sys\n"
        f"print(json.dumps({report!r}, sort_keys=True))\n"
        f"sys.exit({0 if passing else 1})\n",
        encoding="utf-8",
    )


def _execute(
    root: Path, *, candidate_sha: str | None = None, dry_run: bool = False
) -> Execution:
    command = [
        sys.executable,
        "-B",
        str(root / VALIDATOR_REL),
        "--repository-root",
        str(root),
    ]
    if candidate_sha is not None:
        command.extend(["--candidate-sha", candidate_sha])
    if dry_run:
        command.append("--dry-run")
    environment = os.environ.copy()
    environment.update(
        {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"}
    )
    completed = subprocess.run(
        command, cwd=root, env=environment, check=False, capture_output=True
    )
    return Execution(
        completed.returncode,
        completed.stdout,
        completed.stderr,
        () if root.resolve() == ROOT.resolve() else _snapshot(root),
    )


def _read_json(root: Path, relative: Path) -> dict[str, object]:
    loaded = json.loads((root / relative).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_json(root: Path, relative: Path, value: Mapping[str, object]) -> None:
    (root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _task_drift(root: Path) -> None:
    task = _read_json(root, TASK_REL)
    task["tests"] = ["untracked_test"]
    _write_json(root, TASK_REL, task)


def _workflow_drift(root: Path) -> None:
    path = root / WORKFLOW_REL
    path.write_text(
        path.read_text(encoding="utf-8").replace("--dry-run", "--write"),
        encoding="utf-8",
    )


def _evidence_drift(root: Path) -> None:
    evidence = _read_json(root, EVIDENCE_REL)
    evidence["authorization_claim"] = "AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE"
    _write_json(root, EVIDENCE_REL, evidence)


def _missing_test(root: Path) -> None:
    path = root / TEST_REL
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "def test_epic_092_automacao", "def removed_epic_092_automacao"
        ),
        encoding="utf-8",
    )


def _assert_failure(execution: Execution, code: str) -> None:
    report = json.loads(execution.stdout)
    assert execution.returncode == 1
    assert execution.stderr == b""
    assert report["status"] == "FAIL"
    assert report["candidate_state"] == "BLOCKED"
    assert report["destructive_actions"] == 0
    matching = [finding for finding in report["findings"] if finding["code"] == code]
    assert matching, report["findings"]
    assert all(finding["detail"] and finding["remediation"] for finding in matching)


def test_epic_092_automacao() -> None:
    candidate_sha = "a" * 40
    with tempfile.TemporaryDirectory(prefix="issue-0677-valid-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        _write_foundation_stub(sandbox)
        before = _snapshot(sandbox)
        normal = _execute(sandbox, candidate_sha=candidate_sha)
        dry_first = _execute(sandbox, candidate_sha=candidate_sha, dry_run=True)
        dry_second = _execute(sandbox, candidate_sha=candidate_sha, dry_run=True)
        executions = (normal, dry_first, dry_second)
        assert all(execution.returncode == 0 for execution in executions), [
            json.loads(execution.stdout) for execution in executions
        ]
        assert dry_first == dry_second
        assert before == normal.snapshot == dry_first.snapshot

        report = json.loads(normal.stdout)
        dry_report = json.loads(dry_first.stdout)
        assert report["status"] == "PASS"
        assert report["mode"] == "READ_ONLY"
        assert dry_report["mode"] == "DRY_RUN"
        assert report["candidate_sha"] == candidate_sha
        assert report["candidate_state"] == "READY_FOR_INDEPENDENT_REVIEW"
        assert report["authorization_claim"] == "NOT_ASSERTED_BY_AUTOMATION"
        assert report["destructive_actions"] == 0
        assert set(report["requirement_evidence"]) == {
            "REQ-DEV-001",
            "REQ-FRZ-001",
            "REQ-FRZ-002",
            "REQ-FRZ-003",
            "REQ-FRZ-004",
            "REQ-GOV-005",
        }
        assert set(report["acceptance_evidence"]) == {
            "AC-ISSUE-0677-01",
            "AC-ISSUE-0677-02",
            "AC-ISSUE-0677-03",
            "AC-ISSUE-0677-04",
        }

    cases: tuple[tuple[str, str, Mutation], ...] = (
        ("task-drift", "TASK_CONTROL_INVALID", _task_drift),
        ("workflow-drift", "WORKFLOW_INVALID", _workflow_drift),
        ("unsafe-evidence", "EVIDENCE_INVALID", _evidence_drift),
        ("missing-test", "REQUIRED_TEST_MISSING", _missing_test),
    )
    for name, code, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0677-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            mutate(sandbox)
            before = _snapshot(sandbox)
            first = _execute(sandbox, candidate_sha="a" * 40, dry_run=True)
            second = _execute(sandbox, candidate_sha="a" * 40, dry_run=True)
            _assert_failure(first, code)
            assert first == second
            assert before == first.snapshot
            assert dict(first.snapshot)[SENTINEL_REL.as_posix()] == _sha256(SENTINEL_BYTES)

    with tempfile.TemporaryDirectory(prefix="issue-0677-foundation-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        before = _snapshot(sandbox)
        missing_foundation = _execute(sandbox, candidate_sha="a" * 40, dry_run=True)
        _assert_failure(missing_foundation, "FOUNDATION_REPORT_INVALID")
        assert before == missing_foundation.snapshot

    with tempfile.TemporaryDirectory(prefix="issue-0677-fail-closed-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        _write_foundation_stub(sandbox, passing=False)
        before = _snapshot(sandbox)
        missing_sha = _execute(sandbox, dry_run=True)
        failed_foundation = _execute(sandbox, candidate_sha=candidate_sha, dry_run=True)
        _assert_failure(missing_sha, "CANDIDATE_SHA_REQUIRED")
        _assert_failure(failed_foundation, "FOUNDATION_VALIDATION_FAILED")
        assert before == missing_sha.snapshot == failed_foundation.snapshot
