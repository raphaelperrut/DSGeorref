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


def _json(path: Path) -> dict[str, object]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def test_epic_006_integracao() -> None:
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
            integration.EXPECTED_AC_IDS, "test_epic_006_integracao"
        ),
        "control_plane": "SUBPROCESS_READ_ONLY",
        "dependencies": list(integration.EXPECTED_DEPENDENCIES),
        "findings": [],
        "issue": "ISSUE-0139",
        "requirement_evidence": dict.fromkeys(
            integration.EXPECTED_REQUIREMENTS, "test_epic_006_integracao"
        ),
        "status": "PASS",
    }


def test_integration_rejects_predecessor_failure_and_malformed_report() -> None:
    failed_foundation = {"status": "FAIL", "findings": [{"code": "CORPUS_HASH_MISMATCH"}]}
    assert {
        finding.code
        for finding in integration._foundation_report_findings(failed_foundation, 2)
    } == {"FOUNDATION_VALIDATION_FAILED"}
    assert {
        finding.code for finding in integration._foundation_report_findings([], 0)
    } == {"FOUNDATION_VALIDATION_FAILED"}

    permissive_automation = {
        "automation": "EPIC-006_CAPABILITY_CATALOG_CONTROLS",
        "destructive_actions": 1,
        "findings": [],
        "mode": "DRY_RUN",
        "requirement_evidence": dict.fromkeys(integration.EXPECTED_REQUIREMENTS, "test"),
        "status": "PASS",
    }
    assert {
        finding.code
        for finding in integration._automation_report_findings(permissive_automation, 0)
    } == {"AUTOMATION_VALIDATION_FAILED"}
    assert {
        finding.code for finding in integration._automation_report_findings([], 0)
    } == {"AUTOMATION_VALIDATION_FAILED"}


def test_integration_rejects_scope_or_requirement_evidence_drift() -> None:
    task = copy.deepcopy(_json(ROOT / integration.TASK_PATH))
    task["dependencies"] = ["STORY-0027"]
    assert {finding.code for finding in integration._task_findings(task)} == {
        "TASK_SCOPE_INVALID"
    }

    task["phase_f_review"] = {"files": {"allow_paths": None}}
    assert {finding.code for finding in integration._task_findings(task)} == {
        "TASK_SCOPE_INVALID"
    }

    catalog = copy.deepcopy(_json(ROOT / integration.CATALOG_PATH))
    catalog["requirement_evidence"] = {"REQ-AI-007": "test_only_one_requirement"}
    assert {finding.code for finding in integration._requirement_findings(catalog)} == {
        "REQUIREMENT_EVIDENCE_INVALID"
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
