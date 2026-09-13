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
VALIDATOR_REL = Path(f"tools/governance/{SLUG}/integration_validation.py")
TASK_REL = Path(".codex/tasks/TASK-0568.json")
REGISTRY_REL = Path(
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/"
    "integration-evidence-registry.json"
)
CHECKPOINT_REL = Path(f"tools/governance/{SLUG}/integration-checkpoint.json")
TEST_REL = Path(__file__).relative_to(ROOT)
DEPENDENCY_REL = Path(
    f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py"
)
EVIDENCE_REL = Path("evidence/implementation/epic-092/story-0568/IMPLEMENTATION.md")
SENTINEL_REL = Path("unrelated-sentinel.bin")
SENTINEL_BYTES = b"ISSUE-0678 unrelated sentinel\x00\xff\n"
REQUIREMENT_EVIDENCE = {
    "REQ-DEV-001": "test_host_container_ci_contract_and_no_implicit_downloads",
    "REQ-FRZ-001": "test_foundation_baseline_digest_controlled_change_and_adr_supersession",
    "REQ-FRZ-002": "test_sprint_zero_authorization_and_functional_foundation_gate_blocking",
    "REQ-FRZ-003": "test_issue_adr_decision_package_impact_boundary_and_no_silent_divergence",
    "REQ-FRZ-004": "test_foundation_closure_evidence_set_and_material_reopening_criteria",
    "REQ-GOV-005": "test_sprint_zero_baseline_decision_09",
}


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
            if path.is_file() and "__pycache__" not in path.parts
        )
    )


def _copy_sources(root: Path) -> None:
    for relative in (
        VALIDATOR_REL,
        TASK_REL,
        REGISTRY_REL,
        CHECKPOINT_REL,
        TEST_REL,
        EVIDENCE_REL,
    ):
        source = ROOT / relative
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    (root / SENTINEL_REL).write_bytes(SENTINEL_BYTES)


def _write_dependency_stub(root: Path, *, mode: str = "pass") -> None:
    if mode == "missing":
        return
    path = root / DEPENDENCY_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    if mode == "malformed":
        path.write_text("print('not-json')\n", encoding="utf-8")
        return
    passed = mode == "pass"
    report = {
        "status": "PASS" if passed else "FAIL",
        "issue": "ISSUE-0677",
        "foundation_issue": "ISSUE-0676",
        "candidate_sha": "a" * 40,
        "candidate_state": "READY_FOR_INDEPENDENT_REVIEW" if passed else "BLOCKED",
        "authorization_claim": "NOT_ASSERTED_BY_AUTOMATION",
        "findings": [] if passed else [{"code": "CONTROLLED_FAILURE"}],
        "requirement_evidence": REQUIREMENT_EVIDENCE,
    }
    path.write_text(
        "import json, sys\n"
        f"print(json.dumps({report!r}, sort_keys=True))\n"
        f"sys.exit({0 if passed else 1})\n",
        encoding="utf-8",
    )


def _execute(root: Path, *, candidate_sha: str | None = "a" * 40) -> Execution:
    command = [
        sys.executable,
        "-B",
        str(root / VALIDATOR_REL),
        "--repository-root",
        str(root),
    ]
    if candidate_sha is not None:
        command.extend(["--candidate-sha", candidate_sha])
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
        _snapshot(root),
    )


def _read_json(root: Path, relative: Path) -> dict[str, object]:
    loaded = json.loads((root / relative).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_json(root: Path, relative: Path, value: Mapping[str, object]) -> None:
    (root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _task_drift(root: Path) -> None:
    task = _read_json(root, TASK_REL)
    task["dependencies"] = ["STORY-0566"]
    _write_json(root, TASK_REL, task)


def _registry_drift(root: Path) -> None:
    registry = _read_json(root, REGISTRY_REL)
    registry["authorization_claim"] = "AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE"
    _write_json(root, REGISTRY_REL, registry)


def _checkpoint_drift(root: Path) -> None:
    checkpoint = _read_json(root, CHECKPOINT_REL)
    checkpoint["dependency_validator"] = VALIDATOR_REL.as_posix()
    _write_json(root, CHECKPOINT_REL, checkpoint)


def _missing_test(root: Path) -> None:
    path = root / TEST_REL
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "def test_epic_092_integracao", "def removed_epic_092_integracao"
        ),
        encoding="utf-8",
    )


def _assert_failure(execution: Execution, code: str) -> None:
    report = json.loads(execution.stdout)
    assert execution.returncode == 1
    assert execution.stderr == b""
    assert report["status"] == "FAIL"
    assert report["candidate_state"] == "BLOCKED"
    matching = [finding for finding in report["findings"] if finding["code"] == code]
    assert matching, report["findings"]
    assert all(finding["detail"] and finding["remediation"] for finding in matching)


def test_epic_092_integracao() -> None:
    with tempfile.TemporaryDirectory(prefix="issue-0678-valid-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        _write_dependency_stub(sandbox)
        before = _snapshot(sandbox)
        first = _execute(sandbox)
        second = _execute(sandbox)
        assert first.returncode == second.returncode == 0
        assert first.stdout == second.stdout
        assert first.stderr == second.stderr == b""
        assert before == first.snapshot == second.snapshot

        report = json.loads(first.stdout)
        assert report["status"] == "PASS"
        assert report["issue"] == "ISSUE-0678"
        assert report["story"] == "STORY-0568"
        assert report["candidate_sha"] == "a" * 40
        assert report["candidate_state"] == "READY_FOR_INDEPENDENT_REVIEW"
        assert report["dependency_issues"] == ["ISSUE-0676", "ISSUE-0677"]
        assert report["authorization_claim"] == "NOT_ASSERTED_BY_INTEGRATION"
        assert report["migration"] == "NOT_APPLICABLE"
        assert report["rollback"] == "REVERT_COMMIT"
        assert report["requirement_evidence"] == REQUIREMENT_EVIDENCE
        assert set(report["acceptance_evidence"]) == {
            "AC-ISSUE-0678-01",
            "AC-ISSUE-0678-02",
            "AC-ISSUE-0678-03",
            "AC-ISSUE-0678-04",
        }

    cases: tuple[tuple[str, str, Mutation], ...] = (
        ("task-drift", "TASK_CONTROL_INVALID", _task_drift),
        ("registry-drift", "REGISTRY_INVALID", _registry_drift),
        ("checkpoint-drift", "CHECKPOINT_INVALID", _checkpoint_drift),
        ("missing-test", "REQUIRED_TEST_MISSING", _missing_test),
    )
    for name, code, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0678-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            _write_dependency_stub(sandbox)
            mutate(sandbox)
            before = _snapshot(sandbox)
            first = _execute(sandbox)
            second = _execute(sandbox)
            _assert_failure(first, code)
            assert first == second
            assert before == first.snapshot
            assert dict(first.snapshot)[SENTINEL_REL.as_posix()] == _sha256(SENTINEL_BYTES)

    dependency_cases = (
        ("missing", "DEPENDENCY_REPORT_INVALID"),
        ("malformed", "DEPENDENCY_REPORT_INVALID"),
        ("fail", "DEPENDENCY_VALIDATION_FAILED"),
    )
    for mode, code in dependency_cases:
        with tempfile.TemporaryDirectory(
            prefix=f"issue-0678-dependency-{mode}-"
        ) as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            _write_dependency_stub(sandbox, mode=mode)
            before = _snapshot(sandbox)
            execution = _execute(sandbox)
            _assert_failure(execution, code)
            assert before == execution.snapshot

    with tempfile.TemporaryDirectory(prefix="issue-0678-no-sha-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        _write_dependency_stub(sandbox)
        before = _snapshot(sandbox)
        execution = _execute(sandbox, candidate_sha=None)
        _assert_failure(execution, "CANDIDATE_SHA_REQUIRED")
        assert before == execution.snapshot
