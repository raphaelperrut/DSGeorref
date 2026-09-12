from __future__ import annotations

import copy
import csv
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "issue-forms-templates-e-taxonomia-de-tipos-com-validac"
)
SCHEMA_PATH = CONTRACT_ROOT / "issue-form-governance.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/issue-form-governance.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0555.json"
DESIGN_REVIEW_PATH = (
    ROOT
    / "docs/02-architecture/design-reviews"
    / "issue-forms-templates-e-taxonomia-de-tipos-com-validac/DESIGN-REVIEW.md"
)


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _validator() -> Draft202012Validator:
    schema = _load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_epic_090_contrato() -> None:
    contract = _load_json(EXAMPLE_PATH)
    manifest = _load_yaml(MANIFEST_PATH)
    task = _load_json(TASK_PATH)

    _validator().validate(contract)
    assert manifest["identity"] == {
        "epic_id": "EPIC-090",
        "story_id": "STORY-0555",
        "issue_id": "ISSUE-0665",
        "task_id": "TASK-0555",
    }
    assert manifest["requirements"] == [
        {
            "id": "REQ-GOV-002",
            "source": contract["requirement_evidence"]["source"],
            "canonical_test": (
                contract["requirement_evidence"]["canonical_test"]
            ),
        }
    ]
    assert manifest["acceptance_criteria"] == task["acceptance_criterion_ids"]
    assert manifest["proof"]["required_tests"] == task["tests"]
    assert manifest["review"]["self_approval"] == "PROHIBITED"

    required_allow_paths = {
        ".codex/tasks/TASK-0555.json",
        "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv",
        "tests/fnd/issue-forms-templates-e-taxonomia-de-tipos-com-validac/test_contract.py",
        "evidence/implementation/epic-090/story-0555/**",
    }
    assert required_allow_paths <= set(task["allow_paths"])
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]

    expected_contracts = {
        path.relative_to(ROOT).as_posix()
        for path in (MANIFEST_PATH, SCHEMA_PATH, EXAMPLE_PATH)
    }
    with OWNERSHIP_PATH.open(encoding="utf-8", newline="") as ownership_file:
        registered = {
            row["contract"]
            for row in csv.DictReader(ownership_file)
            if row["owner_context"] == "BC-001" and row["status"] == "VERSIONED"
        }
    assert expected_contracts <= registered

    design_review = DESIGN_REVIEW_PATH.read_text(encoding="utf-8")
    for criterion_id in task["acceptance_criterion_ids"]:
        assert criterion_id in design_review


def test_issue_taxonomy_and_required_fields_are_complete() -> None:
    contract = _load_json(EXAMPLE_PATH)
    types = {
        item["type"]: item for item in contract["issue_taxonomy"]["types"]
    }
    assert set(types) == {"BUG", "SPIKE", "STORY", "TASK"}
    assert set(types["STORY"]["required_fields"]) >= {
        "ACCEPTANCE_CRITERIA",
        "ADRS",
        "RISKS",
        "TESTS",
        "EVIDENCE",
        "MIGRATION_APPLICABILITY",
        "ROLLBACK",
    }
    assert contract["template_contract"] == {
        "format": "GITHUB_ISSUE_FORM_YAML",
        "source_root": ".github/ISSUE_TEMPLATE",
        "blank_issues_enabled": False,
        "required_field_encoding": "validations.required=true",
        "security_reporting": {
            "route": "PRIVATE_SECURITY_ADVISORY",
            "public_issue": "REJECT",
        },
        "runtime_materialization": "DOWNSTREAM_STORIES_ONLY",
    }


def test_contract_rejects_missing_field_unknown_type_and_bypasses() -> None:
    invalid = copy.deepcopy(_load_json(EXAMPLE_PATH))
    invalid["issue_taxonomy"]["types"][2]["required_fields"].remove("ROLLBACK")
    invalid["issue_taxonomy"]["types"][3]["type"] = "CHORE"
    invalid["template_contract"]["blank_issues_enabled"] = True
    invalid["template_contract"]["required_field_encoding"] = "best-effort"
    invalid["template_contract"]["security_reporting"]["public_issue"] = "ALLOW"
    invalid["failure_policy"]["silent_fallback"] = True
    invalid["unexpected"] = "implicit-contract-extension"

    errors = list(_validator().iter_errors(invalid))
    assert {error.validator for error in errors} == {"additionalProperties", "const"}
    assert len(errors) == 7


def test_contract_rejects_absent_required_sections() -> None:
    invalid = copy.deepcopy(_load_json(EXAMPLE_PATH))
    del invalid["authority"]
    del invalid["failure_policy"]["missing_required_field"]

    errors = list(_validator().iter_errors(invalid))
    assert {error.validator for error in errors} == {"required"}
    assert len(errors) == 2
