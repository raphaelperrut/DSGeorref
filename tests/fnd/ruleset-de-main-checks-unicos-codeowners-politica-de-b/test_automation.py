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
SLUG = "ruleset-de-main-checks-unicos-codeowners-politica-de-b"
VALIDATOR_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py")
FOUNDATION_ROOT_REL = Path(f"tools/governance/{SLUG}")
CONTRACT_ROOT_REL = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
CONTROL_ROOT_REL = Path(f"docs/03-engineering/contexts/engineering_governance/{SLUG}")
TASK_REL = Path(".codex/tasks/TASK-0562.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
TEST_REL = Path(__file__).relative_to(ROOT)
EVIDENCE_REL = Path("evidence/operations/epic-091/story-0562/validation.json")
SENTINEL_REL = Path("unrelated-sentinel.bin")
SENTINEL_BYTES = b"ISSUE-0672 unrelated sentinel\x00\xff\n"


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
        ROOT / FOUNDATION_ROOT_REL / "foundation_validation.py",
        ROOT / FOUNDATION_ROOT_REL / "main_ruleset_policy_validation.py",
        ROOT / FOUNDATION_ROOT_REL / "foundation-checkpoint.json",
        ROOT / CONTRACT_ROOT_REL / "main-ruleset-governance.schema.json",
        ROOT / CONTRACT_ROOT_REL / "examples/main-ruleset-governance.json",
        ROOT / CONTROL_ROOT_REL / "main-ruleset.json",
        ROOT / CONTROL_ROOT_REL / "required-check-registry.json",
        ROOT / ".github/CODEOWNERS",
        ROOT / ".github/workflows/ci.yml",
        ROOT / WORKFLOW_REL,
        ROOT / ".codex/tasks/TASK-0561.json",
        ROOT / TASK_REL,
        ROOT / "Makefile",
        ROOT / TEST_REL,
        ROOT / EVIDENCE_REL,
    ]
    for source in sources:
        destination = root / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    (root / SENTINEL_REL).write_bytes(SENTINEL_BYTES)


def _execute(
    root: Path,
    *,
    dry_run: bool = False,
    bypass_record: Path | None = None,
    candidate_sha: str | None = None,
    verdict_ref: str | None = None,
) -> Execution:
    command = [
        sys.executable,
        "-B",
        str(root / VALIDATOR_REL),
        "--repository-root",
        str(root),
    ]
    if dry_run:
        command.append("--dry-run")
    if bypass_record is not None:
        command.extend(["--bypass-record", str(bypass_record)])
    if candidate_sha is not None:
        command.extend(["--candidate-sha", candidate_sha])
    if verdict_ref is not None:
        command.extend(["--delivery-approval-verdict-ref", verdict_ref])
    environment = os.environ.copy()
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"})
    completed = subprocess.run(command, cwd=root, env=environment, check=False, capture_output=True)
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


def _duplicate_required_check(root: Path) -> None:
    relative = CONTROL_ROOT_REL / "required-check-registry.json"
    registry = _read_json(root, relative)
    checks = registry["required_checks"]
    assert isinstance(checks, list)
    checks.append(checks[0])
    _write_json(root, relative, registry)


def _unsafe_branch_policy(root: Path) -> None:
    relative = CONTROL_ROOT_REL / "main-ruleset.json"
    ruleset = _read_json(root, relative)
    branch = ruleset["branch_policy"]
    assert isinstance(branch, dict)
    branch["direct_push"] = "ALLOW"
    _write_json(root, relative, ruleset)


def _ambiguous_check_producer(root: Path) -> None:
    path = root / WORKFLOW_REL
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "validate-main-ruleset-controls:", "verify-foundation:"
        ),
        encoding="utf-8",
    )


def _missing_codeowner(root: Path) -> None:
    (root / ".github/CODEOWNERS").write_text("/src/ @raphaelperrut\n", encoding="utf-8")


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


def _missing_test(root: Path) -> None:
    path = root / TEST_REL
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "def test_epic_091_automacao", "def removed_epic_091_automacao"
        ),
        encoding="utf-8",
    )


def _evidence_drift(root: Path) -> None:
    evidence = _read_json(root, EVIDENCE_REL)
    evidence["status"] = "UNKNOWN"
    _write_json(root, EVIDENCE_REL, evidence)


def _bypass_record(candidate_sha: str) -> dict[str, str]:
    return {
        "event_id": "bypass-event-001",
        "ruleset_id": "DSGEOREF-MAIN",
        "protected_branch": "main",
        "candidate_sha": candidate_sha,
        "actor_subject": "authorized-maintainer",
        "reason": "documented emergency recovery",
        "occurred_at": "2026-09-13T12:00:00Z",
        "delivery_approval_verdict_ref": "delivery-verdict-001",
    }


def _assert_failure(execution: Execution, code: str) -> None:
    report = json.loads(execution.stdout)
    assert execution.returncode == 1
    assert execution.stderr == b""
    assert report["status"] == "FAIL"
    assert report["destructive_actions"] == 0
    matching = [finding for finding in report["findings"] if finding["code"] == code]
    assert matching, report["findings"]
    assert all(finding["detail"] and finding["remediation"] for finding in matching)


def test_epic_091_automacao() -> None:
    with tempfile.TemporaryDirectory(prefix="issue-0672-valid-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        before = _snapshot(sandbox)
        first = _execute(sandbox)
        second = _execute(sandbox)
        dry_first = _execute(sandbox, dry_run=True)
        dry_second = _execute(sandbox, dry_run=True)
        assert {first.returncode, second.returncode, dry_first.returncode} == {0}
        assert first == second
        assert dry_first == dry_second
        assert before == first.snapshot == dry_first.snapshot
        report = json.loads(first.stdout)
        dry_report = json.loads(dry_first.stdout)
        assert report["status"] == "PASS"
        assert report["mode"] == "READ_ONLY"
        assert dry_report["mode"] == "DRY_RUN"
        assert report["destructive_actions"] == 0
        assert report["live_ruleset_enforcement"] == "NOT_ASSERTED_BY_AUTOMATION"
        assert set(report["requirement_evidence"]) == {
            "REQ-FRZ-003",
            "REQ-GOV-004",
            "REQ-ISS-003",
            "REQ-ISS-006",
            "REQ-PUB-002",
        }
        assert set(report["acceptance_evidence"]) == {
            "AC-ISSUE-0672-01",
            "AC-ISSUE-0672-02",
            "AC-ISSUE-0672-03",
            "AC-ISSUE-0672-04",
        }
        assert dict(first.snapshot)[SENTINEL_REL.as_posix()] == _sha256(SENTINEL_BYTES)

        candidate_sha = "a" * 40
        record_path = sandbox / "bypass-record.json"
        _write_json(sandbox, record_path.relative_to(sandbox), _bypass_record(candidate_sha))
        bypass_before = _snapshot(sandbox)
        bypass_first = _execute(
            sandbox,
            dry_run=True,
            bypass_record=record_path,
            candidate_sha=candidate_sha,
            verdict_ref="delivery-verdict-001",
        )
        bypass_second = _execute(
            sandbox,
            dry_run=True,
            bypass_record=record_path,
            candidate_sha=candidate_sha,
            verdict_ref="delivery-verdict-001",
        )
        assert bypass_first == bypass_second
        assert bypass_first.returncode == 0
        assert bypass_before == bypass_first.snapshot
        assert json.loads(bypass_first.stdout)["bypass_evidence"] == "VALIDATED"

    cases: tuple[tuple[str, str, Mutation], ...] = (
        ("duplicate-check", "FOUNDATION_VALIDATION_FAILED", _duplicate_required_check),
        ("ambiguous-check", "FOUNDATION_VALIDATION_FAILED", _ambiguous_check_producer),
        ("unsafe-branch", "FOUNDATION_VALIDATION_FAILED", _unsafe_branch_policy),
        ("missing-owner", "FOUNDATION_VALIDATION_FAILED", _missing_codeowner),
        ("task-drift", "TASK_CONTROL_INVALID", _task_drift),
        ("workflow-drift", "WORKFLOW_INVALID", _workflow_drift),
        ("missing-test", "REQUIRED_TEST_MISSING", _missing_test),
        ("evidence-drift", "EVIDENCE_INVALID", _evidence_drift),
    )
    for name, code, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0672-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            mutate(sandbox)
            before = _snapshot(sandbox)
            first = _execute(sandbox, dry_run=True)
            second = _execute(sandbox, dry_run=True)
            _assert_failure(first, code)
            assert first == second
            assert before == first.snapshot

    with tempfile.TemporaryDirectory(prefix="issue-0672-bypass-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        record_path = sandbox / "bypass-record.json"
        _write_json(sandbox, record_path.relative_to(sandbox), _bypass_record("a" * 40))
        before = _snapshot(sandbox)
        stale = _execute(
            sandbox,
            dry_run=True,
            bypass_record=record_path,
            candidate_sha="b" * 40,
            verdict_ref="delivery-verdict-001",
        )
        incomplete = _execute(sandbox, dry_run=True, candidate_sha="a" * 40)
        _assert_failure(stale, "BYPASS_VALIDATION_FAILED")
        _assert_failure(incomplete, "BYPASS_EVIDENCE_INCOMPLETE")
        assert before == stale.snapshot == incomplete.snapshot
