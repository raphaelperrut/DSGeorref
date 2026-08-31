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


def test_first_functional_slice_decision_06() -> None:
    assert integration.validate_requirement_evidence(ROOT) == ()

    task = _load_json(ROOT / integration.TASK_PATH)
    runtime = _load_json(ROOT / integration.RUNTIME_PROFILE_PATH)
    requirement = (ROOT / integration.REQUIREMENT_PATH).read_text(encoding="utf-8")

    permissive = copy.deepcopy(runtime)
    controls = permissive["controls"]
    assert isinstance(controls, dict)
    composition = controls["processing_plan_composition"]
    assert isinstance(composition, dict)
    gate_bypass = composition["gate_bypass"]
    assert isinstance(gate_bypass, dict)
    gate_bypass["scientific_gate"] = True
    findings = integration._requirement_binding_findings(task, requirement, permissive)
    assert {finding.code for finding in findings} == {"REQ_FS1_006_FAIL_CLOSED_INVALID"}


def test_epic_004_integracao() -> None:
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
        "contracts": list(integration.EXPECTED_CONTRACTS),
        "findings": [],
        "issue": "ISSUE-0129",
        "requirement": "REQ-FS1-006",
        "status": "PASS",
    }


def test_integration_rejects_failed_or_malformed_quality_report() -> None:
    failed = {"status": "FAIL", "findings": [{"code": "OPENAPI_INVALID"}]}
    assert {finding.code for finding in integration._quality_report_findings(failed, 1)} == {
        "QUALITY_VALIDATION_FAILED"
    }
    assert {
        finding.code for finding in integration._quality_report_findings([], 0)
    } == {"QUALITY_VALIDATOR_INVALID"}
    malformed = {"status": "PASS", "findings": [], "contracts": None}
    assert {
        finding.code for finding in integration._quality_report_findings(malformed, 0)
    } == {"QUALITY_VALIDATION_FAILED"}


def test_integration_boundary_has_no_repository_import_cycle() -> None:
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
