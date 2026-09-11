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


def _valid_automation_report() -> dict[str, object]:
    return {
        "acceptance_evidence": dict.fromkeys(
            integration.EXPECTED_AUTOMATION_AC_IDS,
            "test_epic_086_automacao",
        ),
        "findings": [],
        "flow": list(integration.EXPECTED_FLOW),
        "mode": "DRY_RUN",
        "output_write_performed": False,
        "repository_mutation_performed": False,
        "requirement_evidence": integration.EXPECTED_AUTOMATION_REQUIREMENTS,
        "status": "PASS",
    }


def test_epic_086_integracao() -> None:
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
        "diagnostic_artifact": "AUTOMATION_REPORT_JSON",
        "findings": [],
        "flow": list(integration.EXPECTED_FLOW),
        "issue": "ISSUE-0647",
        "requirement_evidence": dict.fromkeys(
            integration.EXPECTED_REQUIREMENTS, integration.EXPECTED_TEST
        ),
        "schema_version": "1.0.0",
        "status": "PASS",
    }


def test_integration_rejects_failed_consolidation_checkpoint() -> None:
    findings = integration._consolidation_findings("1 failed", 1)
    assert {finding.code for finding in findings} == {
        "CONSOLIDATION_CHECKPOINT_FAILED"
    }


def test_integration_rejects_failed_malformed_or_permissive_automation() -> None:
    failed = _valid_automation_report()
    failed["status"] = "FAIL"
    assert {finding.code for finding in integration._automation_findings(failed, 2)} == {
        "AUTOMATION_VALIDATION_FAILED"
    }
    assert {
        finding.code for finding in integration._automation_findings([], 0)
    } == {"AUTOMATION_VALIDATION_FAILED"}

    permissive = _valid_automation_report()
    permissive["repository_mutation_performed"] = True
    permissive["output_write_performed"] = True
    assert {
        finding.code for finding in integration._automation_findings(permissive, 0)
    } == {"AUTOMATION_VALIDATION_FAILED"}


def test_integration_rejects_task_identity_scope_and_phase_f_drift() -> None:
    task = copy.deepcopy(_task())
    task["issue_id"] = "ISSUE-0646"
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


def test_integration_converts_predecessor_timeout_to_fail_closed_result() -> None:
    timeout = subprocess.TimeoutExpired([sys.executable, "validator.py"], 120)
    with mock.patch.object(integration.subprocess, "run", side_effect=timeout):
        consolidation_output, consolidation_code = integration._run_consolidation(ROOT)
        automation_report, automation_code = integration._run_automation(ROOT)

    assert consolidation_code == automation_code == -1
    assert consolidation_output
    assert isinstance(automation_report, dict)
    assert "execution_error" in automation_report
    assert integration._consolidation_findings(
        consolidation_output, consolidation_code
    )
    assert integration._automation_findings(automation_report, automation_code)


def test_integration_has_no_cross_module_import_or_rule_copy() -> None:
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
    source = SOURCE_PATH.read_text(encoding="utf-8")
    assert "foundation_validation import" not in source
    assert "validator import" not in source
