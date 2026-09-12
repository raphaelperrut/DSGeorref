from __future__ import annotations

import ast
import copy
import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

import repository_integration as integration

ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = Path(__file__).with_name("repository_integration.py")


def _task() -> dict[str, object]:
    loaded = json.loads((ROOT / integration.TASK_PATH).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def test_epic_090_integracao() -> None:
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
        "acceptance_evidence": dict.fromkeys(
            integration.EXPECTED_AC_IDS, integration.EXPECTED_TEST
        ),
        "control_plane": "SUBPROCESS_READ_ONLY",
        "dependencies": list(integration.EXPECTED_DEPENDENCIES),
        "findings": [],
        "issue": "ISSUE-0668",
        "requirement_evidence": dict.fromkeys(
            integration.EXPECTED_REQUIREMENTS, integration.EXPECTED_TEST
        ),
        "status": "PASS",
    }


def test_integration_rejects_failed_or_malformed_foundation_report() -> None:
    failed = {
        "acceptance_evidence": dict.fromkeys(
            integration.FOUNDATION_AC_IDS, "test_epic_090_fundacao"
        ),
        "failure_policy": "FAIL_CLOSED",
        "findings": [],
        "issue": "ISSUE-0666",
        "requirement_evidence": {
            "REQ-GOV-002": "test_issue_form_required_acceptance_risk_test_rollback_fields"
        },
        "status": "FAIL",
    }
    assert {finding.code for finding in integration._foundation_findings(failed, 1)} == {
        "FOUNDATION_VALIDATION_FAILED"
    }
    assert {finding.code for finding in integration._foundation_findings([], 0)} == {
        "FOUNDATION_VALIDATION_FAILED"
    }


def test_integration_rejects_failed_or_permissive_automation_report() -> None:
    permissive = {
        "acceptance_evidence": dict.fromkeys(
            integration.AUTOMATION_AC_IDS, "test_epic_090_automacao"
        ),
        "automation": "EPIC-090_ISSUE_FORM_CONTROLS",
        "destructive_actions": 1,
        "findings": [],
        "issue": "ISSUE-0667",
        "mode": "READ_WRITE",
        "requirement_evidence": {"REQ-GOV-002": "test_epic_090_automacao"},
        "status": "PASS",
    }
    assert {finding.code for finding in integration._automation_findings(permissive, 0)} == {
        "AUTOMATION_VALIDATION_FAILED"
    }
    assert {finding.code for finding in integration._automation_findings({}, 0)} == {
        "AUTOMATION_VALIDATION_FAILED"
    }


def test_integration_converts_predecessor_timeout_to_fail_closed_report() -> None:
    timeout = subprocess.TimeoutExpired([sys.executable, "validator.py"], 120)
    with mock.patch.object(integration.subprocess, "run", side_effect=timeout):
        report, returncode = integration._run_report(ROOT, integration.FOUNDATION_PATH, ())
    assert returncode == -1
    assert isinstance(report, dict)
    assert "execution_error" in report
    assert {finding.code for finding in integration._foundation_findings(report, returncode)} == {
        "FOUNDATION_VALIDATION_FAILED"
    }


def test_integration_rejects_task_identity_scope_and_phase_f_drift() -> None:
    task = copy.deepcopy(_task())
    task["issue_id"] = "ISSUE-0667"
    assert {finding.code for finding in integration._task_findings(task)} == {
        "TASK_IDENTITY_INVALID"
    }

    task = copy.deepcopy(_task())
    task["allow_paths"] = list(integration.EXPECTED_ALLOW_PATHS[:-1])
    phase_f = task["phase_f_review"]
    assert isinstance(phase_f, dict)
    files = phase_f["files"]
    assert isinstance(files, dict)
    files["allow_paths"] = None
    assert {finding.code for finding in integration._task_findings(task)} == {
        "TASK_SCOPE_INVALID"
    }


def test_integration_control_plane_has_no_cross_module_import_or_rule_copy() -> None:
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
    text = SOURCE_PATH.read_text(encoding="utf-8")
    assert "validate_issue_forms import" not in text
    assert "validator import" not in text
