from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
SLUG = "issue-forms-templates-e-taxonomia-de-tipos-com-validac"
MODULE_ROOT = ROOT / f"tools/governance/{SLUG}"
SOURCE_PATH = MODULE_ROOT / "validate_issue_forms.py"
REGISTRY_PATH = ROOT / (
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/issue-form-registry.json"
)
sys.path.insert(0, str(MODULE_ROOT))

import validate_issue_forms as validation  # noqa: E402


def _json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def test_issue_form_required_acceptance_risk_test_rollback_fields() -> None:
    assert validation.validate_repository(ROOT) == ()
    registry = _json(REGISTRY_PATH)
    story = next(item for item in registry["forms"] if item["type"] == "STORY")
    assert set(story["required_fields"]) == {
        "STABLE_ID",
        "PARENT_EPIC",
        "EXPECTED_VALUE",
        "SCOPE_LIMITS",
        "ACCEPTANCE_CRITERIA",
        "ADRS",
        "RISKS",
        "TESTS",
        "EVIDENCE",
        "MIGRATION_APPLICABILITY",
        "ROLLBACK",
    }
    document = _yaml(ROOT / validation.TEMPLATE_ROOT / story["template"])
    assert validation.form_document_findings(
        story["template"], document, story["required_fields"]
    ) == []


def test_epic_090_fundacao() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(SOURCE_PATH),
            "--repository-root",
            str(ROOT),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)
    assert completed.returncode == 0, report
    assert report == {
        "acceptance_evidence": dict.fromkeys(
            validation.EXPECTED_AC_IDS, "test_epic_090_fundacao"
        ),
        "failure_policy": "FAIL_CLOSED",
        "findings": [],
        "issue": "ISSUE-0666",
        "requirement_evidence": {
            "REQ-GOV-002": "test_issue_form_required_acceptance_risk_test_rollback_fields"
        },
        "status": "PASS",
        "templates": ["BUG", "SPIKE", "STORY", "TASK"],
    }


def test_required_field_and_unknown_type_fail_closed() -> None:
    registry = _json(REGISTRY_PATH)
    story = next(item for item in registry["forms"] if item["type"] == "STORY")
    document = copy.deepcopy(
        _yaml(ROOT / validation.TEMPLATE_ROOT / story["template"])
    )
    risks = next(item for item in document["body"] if item.get("id") == "risks")
    risks["validations"]["required"] = False
    risks["fallback"] = "allow"
    assert {
        finding.code
        for finding in validation.form_document_findings(
            story["template"], document, story["required_fields"]
        )
    } == {"FORM_STRUCTURE_INVALID", "REQUIRED_MARKER_INVALID"}

    unknown_registry = copy.deepcopy(registry)
    unknown_registry["forms"][3]["type"] = "CHORE"
    contract = _json(ROOT / validation.CONTRACT_PATH)
    _, findings = validation._registry_findings(contract, unknown_registry)
    assert {finding.code for finding in findings} == {"ISSUE_TYPE_INVALID"}
