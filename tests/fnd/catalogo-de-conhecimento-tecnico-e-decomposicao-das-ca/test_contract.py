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
    / "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca"
)
SCHEMA_PATH = CONTRACT_ROOT / "capability-catalog-foundation.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/capability-catalog-foundation.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0026.json"
INTERFACE_PATH = ROOT / "contracts/http/operations/get_capabilities.md"
DESIGN_REVIEW_PATH = (
    ROOT
    / "docs/02-architecture/design-reviews"
    / "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/DESIGN-REVIEW.md"
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


def test_epic_006_contrato() -> None:
    contract = _load_json(EXAMPLE_PATH)
    manifest = _load_yaml(MANIFEST_PATH)
    task = _load_json(TASK_PATH)

    _validator().validate(contract)
    assert manifest["identity"] == {
        "epic_id": "EPIC-006",
        "story_id": "STORY-0026",
        "issue_id": "ISSUE-0136",
        "task_id": "TASK-0026",
    }
    assert manifest["requirements"] == contract["requirement_ids"] == [
        "REQ-AI-007",
        "REQ-TST-001",
    ]
    assert manifest["acceptance_criteria"] == task["acceptance_criterion_ids"]
    assert manifest["proof"]["required_tests"] == task["tests"]
    assert manifest["review"]["self_approval"] == "PROHIBITED"

    required_allow_paths = {
        ".codex/tasks/TASK-0026.json",
        "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv",
        "tests/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_contract.py",
        "evidence/implementation/epic-006/story-0026/**",
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

    interface = INTERFACE_PATH.read_text(encoding="utf-8")
    assert "GET /capabilities" in interface
    assert "Estado do contrato:** `FROZEN`" in interface

    design_review = DESIGN_REVIEW_PATH.read_text(encoding="utf-8")
    for criterion_id in task["acceptance_criterion_ids"]:
        assert criterion_id in design_review


def test_capability_and_corpus_contract_is_complete() -> None:
    contract = _load_json(EXAMPLE_PATH)
    assert contract["catalog_contract"]["descriptor_required_fields"] == [
        "stable_name",
        "stage",
        "inputs",
        "outputs",
        "hardware_requirements",
        "budget",
        "determinism_level",
        "limitations",
        "operator_explanation",
        "owner",
        "contract",
    ]
    assert contract["catalog_contract"]["runtime_materialization"] == (
        "DOWNSTREAM_STORIES_ONLY"
    )
    assert contract["knowledge_boundary"] == {
        "prior_system_use": "REQUIREMENTS_AND_ATTRIBUTED_CORPUS_ONLY",
        "code_import": "PROHIBITED",
        "plugin_import": "PROHIBITED",
        "runtime_import": "PROHIBITED",
        "provenance": "REQUIRED",
    }
    assert contract["corpus_contract"] == {
        "splits": ["DEVELOPMENT", "VALIDATION_PROTECTED", "HOLDOUT_BLIND"],
        "origin": "REQUIRED",
        "license": "REQUIRED",
        "sha256": "REQUIRED",
        "access_integrity": "FAIL_CLOSED",
        "split_overlap": "REJECT",
    }


def test_contract_rejects_silent_fallback_legacy_runtime_and_missing_evidence() -> None:
    invalid = copy.deepcopy(_load_json(EXAMPLE_PATH))
    invalid["failure_policy"]["silent_fallback"] = True
    invalid["knowledge_boundary"]["runtime_import"] = "ALLOW"
    invalid["corpus_contract"]["license"] = "OPTIONAL"
    invalid["unexpected"] = "implicit-contract-extension"

    errors = list(_validator().iter_errors(invalid))
    assert {error.validator for error in errors} == {"additionalProperties", "const"}
    assert len(errors) == 4
