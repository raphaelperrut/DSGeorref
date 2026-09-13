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
    / "ruleset-de-main-checks-unicos-codeowners-politica-de-b"
)
SCHEMA_PATH = CONTRACT_ROOT / "main-ruleset-governance.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/main-ruleset-governance.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0560.json"
DESIGN_REVIEW_PATH = (
    ROOT
    / "docs/02-architecture/design-reviews"
    / "ruleset-de-main-checks-unicos-codeowners-politica-de-b/DESIGN-REVIEW.md"
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


def test_epic_091_contrato() -> None:
    contract = _load_json(EXAMPLE_PATH)
    manifest = _load_yaml(MANIFEST_PATH)
    task = _load_json(TASK_PATH)

    _validator().validate(contract)
    assert manifest["identity"] == {
        "epic_id": "EPIC-091",
        "story_id": "STORY-0560",
        "issue_id": "ISSUE-0670",
        "task_id": "TASK-0560",
    }
    assert manifest["requirements"] == [
        {
            "id": item["requirement_id"],
            "source": item["source"],
            "canonical_test": item["canonical_test"],
        }
        for item in contract["requirement_evidence"]
    ]
    for item in contract["requirement_evidence"]:
        assert (ROOT / item["source"]).is_file()
        assert item["candidate_evidence"] == "test_epic_091_contrato"

    assert manifest["acceptance_criteria"] == task["acceptance_criterion_ids"]
    assert manifest["proof"]["required_tests"] == task["tests"]
    assert manifest["review"]["self_approval"] == "PROHIBITED"
    assert "ADR-058" in task["governing_adrs"]

    required_allow_paths = {
        ".codex/tasks/TASK-0560.json",
        "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv",
        "tests/fnd/ruleset-de-main-checks-unicos-codeowners-politica-de-b/test_contract.py",
        "evidence/implementation/epic-091/story-0560/**",
    }
    assert required_allow_paths <= set(task["allow_paths"])
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]

    expected_contracts = {
        path.relative_to(ROOT).as_posix() for path in (MANIFEST_PATH, SCHEMA_PATH, EXAMPLE_PATH)
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


def test_main_ruleset_invariants_and_authorities_are_frozen() -> None:
    contract = _load_json(EXAMPLE_PATH)

    assert contract["branch_policy"] == {
        "protected_branch": "main",
        "entry_issue_state": "READY",
        "execution_issue_state": "IN_PROGRESS",
        "branch_lifecycle": "SHORT_LIVED",
        "change_path": "PULL_REQUEST_ONLY",
        "direct_push": "REJECT",
        "automerge": "REJECT",
        "sensitive_gate_decision": "AUTHORIZED_HUMAN_ONLY",
    }
    assert contract["required_check_policy"]["uniqueness_key"] == "CHECK_CONTEXT"
    assert contract["codeowners_policy"]["review_semantics"] == ("REVIEW_ROUTING_ONLY")
    assert contract["codeowners_policy"]["delivery_approval_substitute"] is False
    assert contract["authority"]["delivery_approval"] == ("ADR-058_DELIVERY_APPROVAL_AUTHORITY")
    assert contract["authority"]["github_approval_signal"] == ("SUPPORTING_SIGNAL_ONLY")
    assert contract["authority"]["product_runtime_state"] == "NOT_APPLICABLE"


def test_contract_rejects_unsafe_branch_check_owner_and_bypass_policies() -> None:
    invalid = copy.deepcopy(_load_json(EXAMPLE_PATH))
    invalid["branch_policy"]["direct_push"] = "ALLOW"
    invalid["branch_policy"]["automerge"] = "ALLOW"
    invalid["required_check_policy"]["duplicate_context"] = "ALLOW"
    invalid["codeowners_policy"]["unresolved_owner"] = "ALLOW"
    invalid["codeowners_policy"]["delivery_approval_substitute"] = True
    invalid["bypass_policy"]["missing_or_invalid_evidence"] = "ALLOW"
    invalid["bypass_policy"]["candidate_sha_binding"] = "LATEST"
    invalid["failure_policy"]["silent_fallback"] = True
    invalid["unexpected"] = "implicit-contract-extension"

    errors = list(_validator().iter_errors(invalid))
    assert {error.validator for error in errors} == {
        "additionalProperties",
        "const",
    }
    assert len(errors) == 9


def test_contract_rejects_missing_ruleset_or_incomplete_bypass_proof() -> None:
    invalid = copy.deepcopy(_load_json(EXAMPLE_PATH))
    del invalid["required_check_policy"]
    invalid["bypass_policy"]["record_fields"].remove("candidate_sha")
    del invalid["failure_policy"]["unverified_bypass"]

    errors = list(_validator().iter_errors(invalid))
    assert {error.validator for error in errors} == {"const", "required"}
    assert len(errors) == 3
