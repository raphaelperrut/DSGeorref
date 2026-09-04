from __future__ import annotations

import ast
import copy
import json
import subprocess
import sys
from pathlib import Path

import repository_integration as integration

ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = Path(__file__).with_name("repository_integration.py")


def _load_json(path: Path) -> dict[str, object]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def test_batch_execution_decision_01() -> None:
    assert integration.validate_requirement_evidence(ROOT, "REQ-BEX-001") == ()

    foundation = _load_json(ROOT / integration.FOUNDATION_PATH)
    invalid = copy.deepcopy(foundation)
    invalid["controls"]["batch_execution"]["image_verdicts"] = "AGGREGATE_ONLY"
    findings = integration._batch_hierarchy_findings(
        invalid,
        _load_json(ROOT / integration.JOB_PATH),
        _load_json(ROOT / integration.ATTEMPT_PATH),
        _load_json(ROOT / integration.TASK_ENVELOPE_PATH),
        (ROOT / integration.BATCH_REPORTING_PATH).read_text(encoding="utf-8"),
    )
    assert {finding.code for finding in findings} == {
        "REQ_BEX_001_HIERARCHY_INVALID"
    }


def test_batch_execution_decision_06() -> None:
    assert integration.validate_requirement_evidence(ROOT, "REQ-BEX-006") == ()

    foundation = _load_json(ROOT / integration.FOUNDATION_PATH)
    invalid = copy.deepcopy(foundation)
    invalid["controls"]["canonical_reuse"]["checkpoints"] = "BEST_EFFORT"
    findings = integration._checkpoint_findings(
        invalid,
        (ROOT / integration.DATABASE_MIGRATIONS_PATH).read_text(encoding="utf-8"),
        (ROOT / integration.ROLLBACK_MATRIX_PATH).read_text(encoding="utf-8"),
    )
    assert {finding.code for finding in findings} == {
        "REQ_BEX_006_CHECKPOINT_INVALID"
    }


def test_first_functional_slice_decision_06() -> None:
    assert integration.validate_requirement_evidence(ROOT, "REQ-FS1-006") == ()

    policy = _load_json(ROOT / integration.NATIVE_POLICY_PATH)
    invalid = copy.deepcopy(policy)
    invalid["controls"]["robust_estimator"]["estimator"] = "RANSAC"
    findings = integration._scientific_control_findings(
        invalid,
        (ROOT / integration.TECHNOLOGY_BASELINE_PATH).read_text(encoding="utf-8"),
    )
    assert {finding.code for finding in findings} == {
        "REQ_FS1_006_FAIL_CLOSED_INVALID"
    }


def test_epic_005_integracao() -> None:
    assert integration.validate_repository_integration(ROOT) == ()
    completed = subprocess.run(
        [sys.executable, "-B", str(SOURCE_PATH), "--repository-root", str(ROOT)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)
    assert completed.returncode == 0, report
    assert report == {
        "acceptance_criteria": list(integration.EXPECTED_AC_IDS),
        "control_plane": "SUBPROCESS_READ_ONLY",
        "findings": [],
        "issue": "ISSUE-0134",
        "migration_policy": "EXPAND_MIGRATE_CONTRACT_WITH_ROLLBACK",
        "requirements": list(integration.REQUIREMENTS),
        "status": "PASS",
    }


def test_integration_rejects_failed_or_malformed_quality_report() -> None:
    failed = {
        "status": "FAIL",
        "mode": "DRY_RUN",
        "destructive_actions": 0,
        "findings": [{"code": "WORKFLOW_INVALID"}],
    }
    assert {finding.code for finding in integration._quality_report_findings(failed, 1)} == {
        "QUALITY_VALIDATION_FAILED"
    }
    assert {
        finding.code for finding in integration._quality_report_findings([], 0)
    } == {"QUALITY_VALIDATOR_INVALID"}
    permissive = {
        "status": "PASS",
        "mode": "DRY_RUN",
        "destructive_actions": 0,
        "findings": [],
        "automation": "EPIC-005_MIGRATIONS_CI_SCANS_TELEMETRY_CONTROLS",
        "acceptance_criteria": list(integration.EXPECTED_QUALITY_AC_IDS),
        "requirements": ["REQ-AIE-001"],
    }
    assert {
        finding.code
        for finding in integration._quality_report_findings(permissive, 0)
    } == {"QUALITY_VALIDATION_FAILED"}


def test_integration_rejects_unknown_requirement_and_import_cycles() -> None:
    findings = integration.validate_requirement_evidence(ROOT, "REQ-UNKNOWN-001")
    assert {finding.code for finding in findings} == {"REQUIREMENT_UNKNOWN"}

    tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"), SOURCE_PATH.as_posix())
    imports = {
        alias.name.split(".", maxsplit=1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        (node.module or "").split(".", maxsplit=1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    assert imports <= {
        "__future__",
        "argparse",
        "collections",
        "dataclasses",
        "json",
        "os",
        "pathlib",
        "subprocess",
        "sys",
        "typing",
    }
