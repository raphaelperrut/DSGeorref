from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tomllib
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini"
    / "sgvcal-srg-srp-parte-4/decision_controls.py"
)
TASK_PATH = ROOT / ".codex/tasks/TASK-0711.json"
MAKEFILE_PATH = ROOT / "Makefile"
WORKFLOW_PATH = ROOT / ".github/workflows/ci.yml"
REQUIREMENTS_PATH = ROOT / "requirements-validation.txt"
PYPROJECT_PATH = ROOT / "pyproject.toml"
PACKAGE_PATH = ROOT / "package.json"
FRONTEND_PACKAGE_PATH = ROOT / "src/frontend/package.json"
TSCONFIG_PATH = ROOT / "src/frontend/tsconfig.json"
SGVCAL_PATH = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "migrations-ci-secret-dependency-scan-e-telemetria-mini"
    / "sgvcal-parte-2/examples/sgvcal-conformance.json"
)
DIGESTS = tuple(character * 64 for character in "abcdef")


def _load_controls() -> ModuleType:
    module_name = "sgvcal_srg_srp_decision_controls"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


CONTROLS = _load_controls()


def _sgv_evidence() -> Any:
    controls = json.loads(SGVCAL_PATH.read_text(encoding="utf-8"))["controls"]
    calibration = controls["calibration_governance"]
    gray_zone = controls["gray_zone"]
    promotion = controls["promotion_and_rollback"]
    return CONTROLS.SGVPromotionEvidence(
        calibration=calibration["calibration"],
        holdout=calibration["holdout"],
        false_acceptance_within_budget=True,
        gray_zone_outcome=gray_zone["outcome"],
        failed_hard_gate_outcome=gray_zone["failed_hard_gate"],
        hard_gate_overridden=False,
        promotion_stages=tuple(promotion["stages"]),
        stage_evidence=(("shadow", DIGESTS[0]), ("canary", DIGESTS[1])),
        profile_digest=DIGESTS[2],
        rollback_ready=promotion["rollback"] == "REQUIRED",
        missing_or_invalid="REJECT",
    )


def _selection_evidence() -> Any:
    return CONTROLS.TestSelectionEvidence(
        impact_graph_used=True,
        impact_graph_digest=DIGESTS[0],
        mandatory_tiers=("unit", "contract"),
        selected_tiers=("unit", "contract", "integration"),
        promotion_candidate=False,
        full_matrix_selected=False,
        missing_or_invalid="REJECT",
    )


def _scheduler_evidence() -> Any:
    return CONTROLS.SchedulerReplayEvidence(
        snapshot_id="scheduler-snapshot@1",
        decisions=(
            ("ADMISSION", "ADMIT"),
            ("FAIRNESS", "TENANT_A"),
            ("LEASE", "ACQUIRE"),
            ("BACKPRESSURE", "CONTINUE"),
            ("BREAKER", "CLOSED"),
        ),
        offline=True,
        scientific_workload_executed=False,
        provider_calls=(),
    )


def _release_evidence() -> Any:
    return CONTROLS.ReleaseEvidence(
        lockfiles=(("python.lock", DIGESTS[0]), ("frontend.lock", DIGESTS[1])),
        immutable_pins=True,
        sbom_digest=DIGESTS[2],
        scanning_passed=True,
        checksums=(DIGESTS[3], DIGESTS[4]),
        oci_signature_digest=DIGESTS[5],
        oci_signature_verified=True,
        provenance_digest=DIGESTS[0],
        missing_or_invalid="REJECT",
    )


def _integration_evidence() -> Any:
    return CONTROLS.IntegrationServiceEvidence(
        integration_services=("POSTGIS", "RABBITMQ"),
        integration_services_real=True,
        authoritative_state_store="POSTGRESQL_POSTGIS",
        broker_role="TRANSPORT_ONLY",
    )


def _cutover_evidence() -> Any:
    dimensions = ("INVARIANTS", "HISTORICAL_READERS", "HEALTH", "CANARY")
    return CONTROLS.CutoverEvidence(
        gate_results=tuple(
            (dimension, True, DIGESTS[index])
            for index, dimension in enumerate(dimensions)
        ),
        atomic_writer_cutover=True,
        promotion_requested=True,
        missing_or_invalid="REJECT",
    )


def _assert_rejected(validator: Any, evidence: Any, requirement: str) -> None:
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        validator(evidence)
    assert requirement in rejected.value.failed_requirements


def test_req_sgvcal_008() -> None:
    evidence = _sgv_evidence()
    CONTROLS.validate_sgv_promotion(evidence)
    for changes in (
        {"calibration": "GLOBAL"},
        {"holdout": "DEVELOPMENT"},
        {"false_acceptance_within_budget": False},
        {"false_acceptance_within_budget": 1},
    ):
        _assert_rejected(
            CONTROLS.validate_sgv_promotion,
            replace(evidence, **changes),
            "REQ-SGVCAL-008",
        )


def test_req_sgvcal_009() -> None:
    evidence = _sgv_evidence()
    CONTROLS.validate_sgv_promotion(evidence)
    for changes in (
        {"gray_zone_outcome": "ACCEPTED"},
        {"failed_hard_gate_outcome": "REVIEWABLE"},
        {"hard_gate_overridden": True},
    ):
        _assert_rejected(
            CONTROLS.validate_sgv_promotion,
            replace(evidence, **changes),
            "REQ-SGVCAL-009",
        )


def test_req_sgvcal_0010() -> None:
    evidence = _sgv_evidence()
    CONTROLS.validate_sgv_promotion(evidence)
    for changes in (
        {"promotion_stages": ("canary",)},
        {"stage_evidence": (("shadow", DIGESTS[0]),)},
        {"profile_digest": "floating-profile"},
        {"rollback_ready": False},
    ):
        _assert_rejected(
            CONTROLS.validate_sgv_promotion,
            replace(evidence, **changes),
            "REQ-SGVCAL-010",
        )


def test_change_impact_graph_mandatory_tiers_and_full_promotion_matrix() -> None:
    evidence = _selection_evidence()
    CONTROLS.validate_test_selection(evidence)
    CONTROLS.validate_test_selection(
        replace(evidence, promotion_candidate=True, full_matrix_selected=True)
    )
    for changes in (
        {"impact_graph_used": False},
        {"impact_graph_used": 1},
        {"impact_graph_digest": "floating-graph"},
        {"selected_tiers": ("unit",)},
        {"mandatory_tiers": ("unit", "unit")},
        {"promotion_candidate": True, "full_matrix_selected": False},
    ):
        _assert_rejected(
            CONTROLS.validate_test_selection,
            replace(evidence, **changes),
            "REQ-SRG-002",
        )


def test_offline_scheduler_decision_replay_without_scientific_workload_or_providers() -> None:
    evidence = _scheduler_evidence()
    first = CONTROLS.replay_scheduler_decisions(evidence)
    assert first == CONTROLS.replay_scheduler_decisions(evidence)
    for changes in (
        {"decisions": evidence.decisions[:-1]},
        {"offline": False},
        {"offline": 1},
        {"scientific_workload_executed": True},
        {"provider_calls": ("external-provider",)},
    ):
        _assert_rejected(
            CONTROLS.replay_scheduler_decisions,
            replace(evidence, **changes),
            "REQ-SRP-002",
        )


def test_release_sbom_signature_provenance_immutable_pins() -> None:
    evidence = _release_evidence()
    CONTROLS.validate_release(evidence)
    for changes in (
        {"lockfiles": (("python.lock", "floating"),)},
        {"immutable_pins": False},
        {"immutable_pins": 1},
        {"sbom_digest": "missing"},
        {"scanning_passed": False},
        {"checksums": ()},
        {"oci_signature_verified": False},
        {"provenance_digest": "missing"},
    ):
        _assert_rejected(
            CONTROLS.validate_release,
            replace(evidence, **changes),
            "REQ-SUP-001",
        )


def test_ruff_mypy_gate() -> None:
    requirements = REQUIREMENTS_PATH.read_text(encoding="utf-8").splitlines()
    pyproject = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
    makefile = MAKEFILE_PATH.read_text(encoding="utf-8")
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "ruff==0.16.5" in requirements
    assert "mypy==2.3.1" in requirements
    assert pyproject["tool"]["ruff"]["target-version"] == "py312"
    assert pyproject["tool"]["mypy"]["python_version"] == "3.12"
    assert pyproject["tool"]["mypy"]["strict"] is True
    assert "verify: python-quality frontend-quality" in makefile
    assert "$(PYTHON) -m ruff check $(RUFF_PATHS)" in makefile
    assert "$(PYTHON) -m mypy $(MYPY_PATHS)" in makefile
    assert "-r requirements-validation.txt" in workflow
    assert "run: make verify" in workflow

    gate = subprocess.run(
        ["make", "python-quality", f"PYTHON={sys.executable}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    assert gate.returncode == 0, gate.stdout + gate.stderr

    ruff_failure = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--stdin-filename", "broken.py", "-"],
        input="import os\n",
        capture_output=True,
        check=False,
        text=True,
    )
    assert ruff_failure.returncode != 0
    mypy_failure = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "-c", "def f() -> int:\n return 'x'"],
        capture_output=True,
        check=False,
        text=True,
    )
    assert mypy_failure.returncode != 0


def test_pytest_real_services() -> None:
    evidence = _integration_evidence()
    CONTROLS.validate_real_services(evidence)
    for changes in (
        {"integration_services": ("POSTGIS",)},
        {"integration_services_real": False},
        {"integration_services_real": 1},
        {"authoritative_state_store": "RABBITMQ"},
        {"broker_role": "STATE_STORE"},
    ):
        _assert_rejected(
            CONTROLS.validate_real_services,
            replace(evidence, **changes),
            "REQ-TOOL-007",
        )


def test_frontend_strict_and_browser(tmp_path: Path) -> None:
    package = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
    frontend = json.loads(FRONTEND_PACKAGE_PATH.read_text(encoding="utf-8"))
    tsconfig = json.loads(TSCONFIG_PATH.read_text(encoding="utf-8"))
    makefile = MAKEFILE_PATH.read_text(encoding="utf-8")
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert package["packageManager"] == "pnpm@10.26.1"
    assert package["engines"]["node"] == "24.20.0"
    assert tsconfig["compilerOptions"]["strict"] is True
    assert tsconfig["compilerOptions"]["noEmit"] is True
    assert set(frontend["devDependencies"]) >= {
        "typescript",
        "vitest",
        "@testing-library/dom",
        "@playwright/test",
    }
    assert frontend["scripts"] == {
        "typecheck": "tsc --noEmit",
        "test:unit": (
            "vitest run tests/tooling/testing-library.unit.test.ts --environment jsdom"
        ),
        "test:browser": (
            "playwright test tests/tooling/playwright.browser.spec.ts --browser=chromium"
        ),
    }
    assert "$(PNPM) run frontend:verify" in makefile
    assert "node-version: '24.20.0'" in workflow
    assert "pnpm install --frozen-lockfile" in workflow
    assert "playwright install --with-deps chromium" in workflow

    pnpm = shutil.which("pnpm")
    assert pnpm is not None
    gate = subprocess.run(
        [pnpm, "run", "frontend:verify"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    assert gate.returncode == 0, gate.stdout + gate.stderr

    invalid_typescript = tmp_path / "invalid.ts"
    invalid_typescript.write_text("const value: number = 'invalid';\n", encoding="utf-8")
    strict_failure = subprocess.run(
        [
            pnpm,
            "--dir",
            "src/frontend",
            "exec",
            "tsc",
            "--noEmit",
            "--strict",
            str(invalid_typescript),
        ],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    assert strict_failure.returncode != 0


def test_post_migration_multidimensional_evidence_gate_canary_and_atomic_cutover() -> None:
    evidence = _cutover_evidence()
    CONTROLS.validate_cutover(evidence)
    failed_canary = (*evidence.gate_results[:-1], ("CANARY", False, DIGESTS[3]))
    for changes in (
        {"gate_results": evidence.gate_results[:-1]},
        {"gate_results": failed_canary},
        {"atomic_writer_cutover": False},
        {"atomic_writer_cutover": 1},
        {"promotion_requested": False},
    ):
        _assert_rejected(
            CONTROLS.validate_cutover,
            replace(evidence, **changes),
            "REQ-UPG-003",
        )


def test_missing_malformed_or_permissive_evidence_is_rejected_without_fallback() -> None:
    validators = (
        (
            CONTROLS.validate_sgv_promotion,
            ("REQ-SGVCAL-008", "REQ-SGVCAL-009", "REQ-SGVCAL-010"),
        ),
        (CONTROLS.validate_test_selection, ("REQ-SRG-002",)),
        (CONTROLS.replay_scheduler_decisions, ("REQ-SRP-002",)),
        (CONTROLS.validate_release, ("REQ-SUP-001",)),
        (
            CONTROLS.validate_real_services,
            ("REQ-TOOL-007",),
        ),
        (CONTROLS.validate_cutover, ("REQ-UPG-003",)),
    )
    for validator, requirements in validators:
        with pytest.raises(CONTROLS.DecisionRejected) as rejected:
            validator(None)
        assert rejected.value.failed_requirements == requirements

    permissive = replace(_sgv_evidence(), missing_or_invalid="WARN")
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        CONTROLS.validate_sgv_promotion(permissive)
    assert rejected.value.failed_requirements == (
        "REQ-SGVCAL-008",
        "REQ-SGVCAL-009",
        "REQ-SGVCAL-010",
    )


def test_task_envelope_contains_only_the_final_slice_paths() -> None:
    task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(task)
    allowed = set(task["allow_paths"])
    assert ".codex/tasks/TASK-0711.json" in allowed
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in allowed
    assert any(path.startswith("evidence/implementation/migrations-ci-") for path in allowed)
    assert "Makefile" in allowed
    assert ".github/workflows/ci.yml" in allowed
    assert "pnpm-lock.yaml" in allowed
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "ISSUE-" not in source
    assert "STORY-" not in source
