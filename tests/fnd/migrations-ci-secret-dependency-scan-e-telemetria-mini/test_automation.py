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

import yaml

ROOT = Path(__file__).resolve().parents[3]
SLUG = "migrations-ci-secret-dependency-scan-e-telemetria-mini"
VALIDATOR_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py")
QUALITY_DIR_REL = VALIDATOR_REL.parent
CONTRACT_ROOT_REL = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
TEST_DIR_REL = Path(f"tests/fnd/{SLUG}")
TASK_REL = Path(".codex/tasks/TASK-0023.json")
TASK_SCHEMA_REL = Path(".codex/tasks/TASK_ENVELOPE.schema.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
CONSOLIDATION_REL = Path(
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/consolidacao/CONSOLIDATION.json"
)
VERSION_MATRIX_REL = Path("contracts/operations/version-and-rollback-matrix.yaml")
SLO_CATALOG_REL = Path("contracts/operations/slo-sli-catalog.yaml")
FOUNDATION_EXAMPLE_REL = CONTRACT_ROOT_REL / (
    "aie-bex-epic-parte-1/examples/contract-foundation.json"
)
FOUNDATION_SCHEMA_REL = CONTRACT_ROOT_REL / ("aie-bex-epic-parte-1/contract-foundation.schema.json")
FOUNDATION_TEST_REL = TEST_DIR_REL / "test_contract_foundation.py"
EVIDENCE_ROOT_REL = Path(
    "evidence/implementation/migrations-ci-secret-dependency-scan-e-telemetria"
)
IMPLEMENTATION_EVIDENCE_RELS = (
    EVIDENCE_ROOT_REL / "aie-bex-parte-1/IMPLEMENTATION_EVIDENCE.yaml",
    EVIDENCE_ROOT_REL / "bex-epic-frz-parte-2/IMPLEMENTATION_EVIDENCE.yaml",
    EVIDENCE_ROOT_REL / "fs1-gov-sgvcal-parte-3/IMPLEMENTATION_EVIDENCE.yaml",
    EVIDENCE_ROOT_REL / "sgvcal-srg-srp-parte-4/IMPLEMENTATION_EVIDENCE.yaml",
)
SENTINEL_REL = Path("unrelated-sentinel.bin")
SENTINEL_BYTES = b"ISSUE-0133 unrelated sentinel\x00\xff\n"


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


def _implementation_artifacts() -> list[Path]:
    artifacts: list[Path] = []
    for relative in IMPLEMENTATION_EVIDENCE_RELS:
        evidence_path = ROOT / relative
        document = yaml.safe_load(evidence_path.read_text(encoding="utf-8"))
        artifacts.extend(Path(value) for value in document["implementation_artifacts"])
    return artifacts


def _copy_sources(root: Path) -> None:
    sources = [
        *(ROOT / QUALITY_DIR_REL).glob("*.py"),
        *(ROOT / CONTRACT_ROOT_REL).rglob("*"),
        *(ROOT / relative for relative in IMPLEMENTATION_EVIDENCE_RELS),
        *(ROOT / TEST_DIR_REL).glob("test_*.py"),
        *(ROOT / relative for relative in _implementation_artifacts()),
        ROOT / TASK_REL,
        ROOT / TASK_SCHEMA_REL,
        ROOT / WORKFLOW_REL,
        ROOT / CONSOLIDATION_REL,
        ROOT / VERSION_MATRIX_REL,
        ROOT / SLO_CATALOG_REL,
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


def _missing_contract(root: Path) -> None:
    (root / FOUNDATION_SCHEMA_REL).unlink()


def _silent_fallback(root: Path) -> None:
    profile = _read_json(root, FOUNDATION_EXAMPLE_REL)
    controls = profile["controls"]
    assert isinstance(controls, dict)
    telemetry = controls["telemetry"]
    assert isinstance(telemetry, dict)
    telemetry["missing_correlation"] = "WARN"
    _write_json(root, FOUNDATION_EXAMPLE_REL, profile)


def _missing_requirement_test(root: Path) -> None:
    path = root / FOUNDATION_TEST_REL
    source = path.read_text(encoding="utf-8")
    path.write_text(
        source.replace("def migration_upgrade_rollback", "def removed_migration_proof"),
        encoding="utf-8",
    )


def _missing_implementation_artifact(root: Path) -> None:
    (
        root
        / Path(
            "tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/aie-bex-parte-1/decision_controls.py"
        )
    ).unlink()


def _invalid_migration_policy(root: Path) -> None:
    matrix = yaml.safe_load((root / VERSION_MATRIX_REL).read_text(encoding="utf-8"))
    matrix["migration_rules"] = matrix["migration_rules"][:-1]
    (root / VERSION_MATRIX_REL).write_text(
        yaml.safe_dump(matrix, sort_keys=False), encoding="utf-8"
    )


def _invalid_telemetry_policy(root: Path) -> None:
    catalog = yaml.safe_load((root / SLO_CATALOG_REL).read_text(encoding="utf-8"))
    catalog["scientific"]["no_unbenchmarked_claims"] = False
    (root / SLO_CATALOG_REL).write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")


def _invalid_task(root: Path) -> None:
    task = _read_json(root, TASK_REL)
    task["tests"] = ["untracked_test"]
    _write_json(root, TASK_REL, task)


def _invalid_workflow(root: Path) -> None:
    path = root / WORKFLOW_REL
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e", "unversioned"
        ),
        encoding="utf-8",
    )


def _assert_failure(execution: Execution, code: str) -> None:
    report = json.loads(execution.stdout)
    assert execution.returncode != 0
    assert execution.stderr == b""
    assert report["status"] == "FAIL"
    assert report["destructive_actions"] == 0
    assert code in {finding["code"] for finding in report["findings"]}


def test_epic_005_automacao() -> None:
    with tempfile.TemporaryDirectory(prefix="issue-0133-valid-") as temporary:
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
        assert len(report["requirements"]) == 51
        assert report["acceptance_criteria"] == [
            "AC-ISSUE-0133-01",
            "AC-ISSUE-0133-02",
            "AC-ISSUE-0133-03",
            "AC-ISSUE-0133-04",
        ]
        assert dict(first.snapshot)[SENTINEL_REL.as_posix()] == _sha256(SENTINEL_BYTES)

    cases: tuple[tuple[str, str, Mutation], ...] = (
        ("missing_contract", "CONTRACT_UNREADABLE", _missing_contract),
        ("silent_fallback", "CONTRACT_SCHEMA_INVALID", _silent_fallback),
        ("missing_requirement_test", "REQUIREMENT_TEST_MISSING", _missing_requirement_test),
        ("missing_artifact", "IMPLEMENTATION_ARTIFACT_MISSING", _missing_implementation_artifact),
        ("invalid_migration", "MIGRATION_CONTROL_INVALID", _invalid_migration_policy),
        ("invalid_telemetry", "TELEMETRY_CONTROL_INVALID", _invalid_telemetry_policy),
        ("invalid_task", "TASK_CONTROL_INVALID", _invalid_task),
        ("invalid_workflow", "WORKFLOW_INVALID", _invalid_workflow),
    )
    for name, code, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0133-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            mutate(sandbox)
            before = _snapshot(sandbox)
            first = _execute(sandbox, dry_run=True)
            second = _execute(sandbox, dry_run=True)
            _assert_failure(first, code)
            assert first == second
            assert before == first.snapshot


def test_pnpm_setup_pin_is_fail_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="issue-0133-pnpm-approved-") as temporary:
        approved_sandbox = Path(temporary)
        _copy_sources(approved_sandbox)
        approved = _execute(approved_sandbox, dry_run=True)
        assert approved.returncode == 0
        assert json.loads(approved.stdout)["status"] == "PASS"

    mutations = {
        "missing": ("replace", "name: pnpm setup intentionally absent"),
        "unapproved": ("replace", f"uses: pnpm/action-setup@{'0' * 40}"),
        "approved-plus-unapproved": ("append", f"uses: pnpm/action-setup@{'0' * 40}"),
        "approved-plus-floating": ("append", "uses: pnpm/action-setup@v6"),
    }
    for name, (operation, replacement) in mutations.items():
        with tempfile.TemporaryDirectory(prefix=f"issue-0133-pnpm-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            path = sandbox / WORKFLOW_REL
            source = path.read_text(encoding="utf-8")
            lines = [
                line for line in source.splitlines() if "uses: pnpm/action-setup@" in line
            ]
            assert len(lines) == 1
            line = lines[0]
            indent = line[: len(line) - len(line.lstrip())]
            mutation = f"{indent}- {replacement}"
            if operation == "append":
                mutation = f"{line}\n{mutation}"
            path.write_text(
                source.replace(line, mutation, 1), encoding="utf-8"
            )
            execution = _execute(sandbox, dry_run=True)
            _assert_failure(execution, "WORKFLOW_INVALID")
            report = json.loads(execution.stdout)
            assert "missing pinned pnpm setup" in {
                finding["detail"] for finding in report["findings"]
            }
