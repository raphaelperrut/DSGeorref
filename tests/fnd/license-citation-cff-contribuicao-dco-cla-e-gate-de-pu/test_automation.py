from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SLUG = "license-citation-cff-contribuicao-dco-cla-e-gate-de-pu"
QUALITY_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}")
VALIDATOR_REL = QUALITY_REL / "validator.py"
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
TASK_REL = Path(".codex/tasks/TASK-0033.json")
TASK_SCHEMA_REL = Path(".codex/tasks/TASK_ENVELOPE.schema.json")
CONTRACT_ROOT_REL = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
CONTRACT_EXAMPLE_REL = CONTRACT_ROOT_REL / "examples/license-publication-governance.json"
FOUNDATION_ROOT_REL = Path(f"tools/governance/{SLUG}")
CHECKPOINT_REL = FOUNDATION_ROOT_REL / "foundation-checkpoint.json"
DOC_ROOT_REL = Path(f"docs/03-engineering/contexts/engineering_governance/{SLUG}")
SENTINEL_REL = Path(f"tests/fnd/{SLUG}/unrelated-sentinel.txt")
SENTINEL_BYTES = b"ISSUE-0143 unrelated sentinel\n"

SOURCE_FILES = (
    TASK_REL,
    TASK_SCHEMA_REL,
    WORKFLOW_REL,
    CONTRACT_ROOT_REL / "license-publication-governance.schema.json",
    CONTRACT_EXAMPLE_REL,
    FOUNDATION_ROOT_REL / "foundation_validation.py",
    CHECKPOINT_REL,
    DOC_ROOT_REL / "license-inventory.json",
    DOC_ROOT_REL / "dependency-inventory.json",
    Path(".reuse/dep5"),
    Path("CITATION.cff"),
    Path("CONTRIBUTING.md"),
    Path("LICENSE"),
    Path("LICENSES/AGPL-3.0-or-later.txt"),
    Path("LICENSES/Apache-2.0.txt"),
    Path("LICENSES/CC-BY-4.0.txt"),
    Path("Makefile"),
    Path("NOTICE"),
    Path("THIRD_PARTY_NOTICES.md"),
    Path("pnpm-lock.yaml"),
    Path("pyproject.toml"),
    Path("requirements-validation.txt"),
    Path("src/frontend/package.json"),
    Path(__file__).relative_to(ROOT),
)


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
            and ".git" not in path.parts
            and "__pycache__" not in path.parts
        )
    )


def _git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


def _copy_sources(root: Path) -> None:
    quality_sources = [path.relative_to(ROOT) for path in (ROOT / QUALITY_REL).glob("*.py")]
    sources = [*SOURCE_FILES, *quality_sources]
    for relative in sources:
        source = ROOT / relative
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    sentinel = root / SENTINEL_REL
    sentinel.parent.mkdir(parents=True, exist_ok=True)
    sentinel.write_bytes(SENTINEL_BYTES)
    _git(root, "init", "-q")
    _git(root, "add", "--all")
    _git(
        root,
        "-c",
        "user.name=Sentinel QA",
        "-c",
        "user.email=sentinel@example.com",
        "commit",
        "-q",
        "-m",
        "test: baseline\n\nSigned-off-by: Sentinel QA <sentinel@example.com>",
    )


def _execute(
    root: Path,
    *,
    dry_run: bool = False,
    external_commit_range: str | None = None,
) -> Execution:
    command = [
        sys.executable,
        "-B",
        "-X",
        "utf8",
        str(root / VALIDATOR_REL),
        "--repository-root",
        str(root),
    ]
    if dry_run:
        command.append("--dry-run")
    if external_commit_range is not None:
        command.extend(["--external-commit-range", external_commit_range])
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        command,
        cwd=root,
        check=False,
        capture_output=True,
        env=environment,
        timeout=180,
    )
    return Execution(completed.returncode, completed.stdout, completed.stderr, _snapshot(root))


def _read_json(root: Path, relative: Path) -> dict[str, object]:
    value = json.loads((root / relative).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _write_json(root: Path, relative: Path, value: dict[str, object]) -> None:
    (root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _missing_contract(root: Path) -> None:
    (root / CONTRACT_EXAMPLE_REL).unlink()


def _invalid_citation(root: Path) -> None:
    path = root / "CITATION.cff"
    path.write_text(
        path.read_text(encoding="utf-8").replace("AGPL-3.0-or-later", "MIT"),
        encoding="utf-8",
    )


def _invalid_task(root: Path) -> None:
    task = _read_json(root, TASK_REL)
    task["tests"] = ["untracked_test"]
    _write_json(root, TASK_REL, task)


def _invalid_workflow(root: Path) -> None:
    path = root / WORKFLOW_REL
    changed = path.read_text(encoding="utf-8").replace("--dry-run", "--write")
    path.write_text(changed, encoding="utf-8")


def _publication_state_drift(root: Path) -> None:
    checkpoint = _read_json(root, CHECKPOINT_REL)
    publication = checkpoint["publication_gate"]
    assert isinstance(publication, dict)
    evidence = publication["candidate_evidence"]
    assert isinstance(evidence, dict)
    evidence.update(dict.fromkeys(evidence, "PASS"))
    _write_json(root, CHECKPOINT_REL, checkpoint)


def _assert_failure(execution: Execution, code: str) -> None:
    report = json.loads(execution.stdout)
    assert execution.returncode == 1
    assert execution.stderr == b""
    assert report["status"] == "FAIL"
    assert report["destructive_actions"] == 0
    assert report["publication_gate"]["decision"] == "UNVERIFIED"
    assert code in {finding["code"] for finding in report["findings"]}


def _commit_marker(root: Path, message: str, marker: bytes) -> tuple[str, str]:
    base = _git(root, "rev-parse", "HEAD")
    (root / SENTINEL_REL).write_bytes(marker)
    _git(root, "add", SENTINEL_REL.as_posix())
    _git(
        root,
        "-c",
        "user.name=External Contributor",
        "-c",
        "user.email=external@example.com",
        "commit",
        "-q",
        "-m",
        message,
    )
    return base, _git(root, "rev-parse", "HEAD")


def test_epic_007_automacao() -> None:
    with tempfile.TemporaryDirectory(prefix="issue-0143-valid-") as temporary:
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
        assert report["status"] == "PASS"
        assert report["mode"] == "READ_ONLY"
        assert json.loads(dry_first.stdout)["mode"] == "DRY_RUN"
        assert set(report["requirement_evidence"]) == {
            "REQ-CIT-001",
            "REQ-EPIC-042",
            "REQ-OSS-001",
            "REQ-PUB-002",
        }
        assert set(report["acceptance_evidence"]) == {
            "AC-ISSUE-0143-01",
            "AC-ISSUE-0143-02",
            "AC-ISSUE-0143-03",
            "AC-ISSUE-0143-04",
        }
        assert report["publication_gate"]["failure_mode"] == "FAIL_CLOSED"
        assert dict(first.snapshot)[SENTINEL_REL.as_posix()] == _sha256(SENTINEL_BYTES)

    cases: tuple[tuple[str, str, Mutation], ...] = (
        ("missing-contract", "CONTRACT_UNREADABLE", _missing_contract),
        ("invalid-citation", "FOUNDATION_VALIDATION_FAILED", _invalid_citation),
        ("invalid-task", "TASK_CONTROL_INVALID", _invalid_task),
        ("invalid-workflow", "WORKFLOW_INVALID", _invalid_workflow),
        ("publication-drift", "PUBLICATION_GATE_INVALID", _publication_state_drift),
    )
    for name, code, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0143-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            mutate(sandbox)
            before = _snapshot(sandbox)
            first = _execute(sandbox, dry_run=True)
            second = _execute(sandbox, dry_run=True)
            _assert_failure(first, code)
            assert first == second
            assert before == first.snapshot

    with tempfile.TemporaryDirectory(prefix="issue-0143-dco-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        signed_base, signed_head = _commit_marker(
            sandbox,
            "test: signed external change\n\n"
            "Signed-off-by: External Contributor <external@example.com>",
            b"signed external change\n",
        )
        signed = _execute(
            sandbox,
            dry_run=True,
            external_commit_range=f"{signed_base}..{signed_head}",
        )
        assert signed.returncode == 0, signed.stdout.decode()

        unsigned_base, unsigned_head = _commit_marker(
            sandbox,
            "test: unsigned external change",
            b"unsigned external change\n",
        )
        unsigned = _execute(
            sandbox,
            dry_run=True,
            external_commit_range=f"{unsigned_base}..{unsigned_head}",
        )
        _assert_failure(unsigned, "DCO_VALIDATION_FAILED")
        unsafe = _execute(sandbox, dry_run=True, external_commit_range="main;echo unsafe..HEAD")
        _assert_failure(unsafe, "DCO_VALIDATION_FAILED")
        empty = _execute(sandbox, dry_run=True, external_commit_range="")
        _assert_failure(empty, "DCO_VALIDATION_FAILED")
