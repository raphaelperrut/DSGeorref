from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = ROOT / (
    "tools/quality/contexts/engineering_governance/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/validator.py"
)
PROFILE_REL = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "examples/walking-skeleton.json"
)
WORKFLOW_REL = Path(
    ".github/workflows/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw.yaml"
)
BASE_COPY_PATHS = (
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
        "contract-manifest.yaml"
    ),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
        "walking-skeleton.schema.json"
    ),
    PROFILE_REL,
    Path(".codex/tasks/TASK-0536.json"),
    Path(
        "tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
        "test_automation.py"
    ),
    WORKFLOW_REL,
)


def _load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("walking_skeleton_gate", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


gate = _load_validator()


def _copy(source_root: Path, target_root: Path, relative: Path) -> None:
    target = target_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_root / relative, target)


def _isolated_repository(tmp_path: Path) -> Path:
    for relative in BASE_COPY_PATHS:
        _copy(ROOT, tmp_path, relative)
    profile = json.loads((ROOT / PROFILE_REL).read_text(encoding="utf-8"))
    sources = profile["contract_sources"]
    for key, value in sources.items():
        if key != "operations":
            _copy(ROOT, tmp_path, Path(value))
    manifest = yaml.safe_load((ROOT / BASE_COPY_PATHS[0]).read_text(encoding="utf-8"))
    for item in manifest["traceability"]["requirements"]:
        evidence = item["evidence"]
        evidence_source = next(
            path
            for path in (ROOT / "tests").rglob("test_*.py")
            if f"def {evidence}(" in path.read_text(encoding="utf-8")
        )
        _copy(ROOT, tmp_path, evidence_source.relative_to(ROOT))
    return tmp_path


def _run_cli(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR_PATH),
            "--repository-root",
            str(root),
            *arguments,
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def test_epic_086_automacao() -> None:
    report = gate.build_report(ROOT, dry_run=False)

    assert report["status"] == "PASS"
    assert report["repository_mutation_performed"] is False
    assert report["flow"] == [
        "FRONTEND",
        "API",
        "POSTGRESQL",
        "RABBITMQ_CELERY",
        "WORKER",
        "DIAGNOSTIC_ARTIFACT",
    ]
    assert report["requirement_evidence"] == {
        "REQ-EPIC-001": "test_executable_foundation_gate_clean_room_end_to_end",
        "REQ-SPRINT-001-004": "test_sprint_zero_baseline_decision_04",
    }
    assert report["acceptance_evidence"] == {
        f"AC-ISSUE-0646-{index:02d}": "test_epic_086_automacao"
        for index in range(1, 5)
    }
    assert len(report["input_sha256"]) == 6
    assert report["findings"] == []


def test_gate_accepts_authorized_upload_artifact_v7(tmp_path: Path) -> None:
    repository = _isolated_repository(tmp_path)
    workflow = (repository / WORKFLOW_REL).read_text(encoding="utf-8")

    assert "actions/upload-artifact@v7" in workflow
    assert gate.build_report(repository, dry_run=True)["findings"] == []


@pytest.mark.parametrize(
    "upload_action",
    (None, "actions/upload-artifact@v8"),
    ids=("missing", "unauthorized-version"),
)
def test_gate_rejects_missing_or_unauthorized_upload_artifact_action(
    tmp_path: Path, upload_action: str | None
) -> None:
    repository = _isolated_repository(tmp_path)
    workflow_path = repository / WORKFLOW_REL
    workflow = workflow_path.read_text(encoding="utf-8")
    replacement = upload_action or ""
    workflow_path.write_text(
        workflow.replace("actions/upload-artifact@v7", replacement),
        encoding="utf-8",
    )

    report = gate.build_report(repository, dry_run=True)

    assert report["status"] == "FAIL"
    assert "WORKFLOW_CONTROL_MISSING" in {
        finding["code"] for finding in report["findings"]
    }


def test_gate_rejects_silent_fallback_without_substitution(tmp_path: Path) -> None:
    repository = _isolated_repository(tmp_path)
    profile_path = repository / PROFILE_REL
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile["failure_policy"]["silent_fallback"] = True
    profile_path.write_text(json.dumps(profile), encoding="utf-8")

    report = gate.build_report(repository, dry_run=True)

    assert report["status"] == "FAIL"
    assert {finding["code"] for finding in report["findings"]} == {
        "PROFILE_SCHEMA_INVALID"
    }
    assert "approved, versioned contract revision" in report["findings"][0]["remediation"]


@pytest.mark.parametrize(
    "relative",
    (BASE_COPY_PATHS[0], BASE_COPY_PATHS[1], PROFILE_REL),
    ids=("manifest", "schema", "profile"),
)
def test_gate_rejects_non_mapping_contract_input(
    tmp_path: Path, relative: Path
) -> None:
    repository = _isolated_repository(tmp_path)
    (repository / relative).write_text("[]", encoding="utf-8")

    report = gate.build_report(repository, dry_run=True)

    assert report["status"] == "FAIL"
    finding = next(
        item for item in report["findings"]
        if item["code"] == "INPUT_STRUCTURE_INVALID" and item["path"] == relative.as_posix()
    )
    assert "object/mapping" in finding["message"]
    assert "versioned object/mapping" in finding["remediation"]


def test_gate_rejects_missing_contract_source_with_actionable_diagnostic(
    tmp_path: Path,
) -> None:
    repository = _isolated_repository(tmp_path)
    missing = repository / "contracts/domain/failure-diagnostic.schema.json"
    missing.unlink()

    report = gate.build_report(repository, dry_run=True)

    finding = next(
        item for item in report["findings"] if item["code"] == "CONTRACT_SOURCE_MISSING"
    )
    assert report["status"] == "FAIL"
    assert finding["path"] == "contracts/domain/failure-diagnostic.schema.json"
    assert "never substitutes a fallback" in finding["remediation"]


def test_cli_is_idempotent_and_dry_run_does_not_write(tmp_path: Path) -> None:
    first = _run_cli(ROOT, "--dry-run")
    second = _run_cli(ROOT, "--dry-run")
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert json.loads(first.stdout)["mode"] == "DRY_RUN"

    output = tmp_path / "diagnostics/gate.json"
    assert _run_cli(ROOT, "--output", str(output)).returncode == 0
    first_digest = output.read_bytes()
    assert _run_cli(ROOT, "--output", str(output)).returncode == 0
    assert output.read_bytes() == first_digest

    dry_run_output = tmp_path / "diagnostics/dry-run.json"
    dry_run = _run_cli(ROOT, "--dry-run", "--output", str(dry_run_output))
    assert dry_run.returncode == 0
    assert json.loads(dry_run.stdout)["output_write_performed"] is False
    assert not dry_run_output.exists()


def test_cli_fails_closed_for_malformed_input(tmp_path: Path) -> None:
    repository = _isolated_repository(tmp_path)
    (repository / PROFILE_REL).write_text("{not-json", encoding="utf-8")

    result = _run_cli(repository, "--dry-run")
    report = json.loads(result.stdout)

    assert result.returncode == 2
    assert report["status"] == "FAIL"
    assert report["findings"]
    assert all(finding["remediation"] for finding in report["findings"])
    assert "INPUT_UNREADABLE" in {finding["code"] for finding in report["findings"]}
