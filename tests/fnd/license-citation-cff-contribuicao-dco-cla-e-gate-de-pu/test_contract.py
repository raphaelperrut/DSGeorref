from __future__ import annotations

import copy
import csv
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
SLUG = "license-citation-cff-contribuicao-dco-cla-e-gate-de-pu"
CONTRACT_ROOT = ROOT / "contracts/contexts/engineering_governance/fnd" / SLUG
SCHEMA_PATH = CONTRACT_ROOT / "license-publication-governance.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/license-publication-governance.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0031.json"
LICENSING_PATH = ROOT / "LICENSING.md"
CONTRIBUTING_PATH = ROOT / "CONTRIBUTING.md"
DESIGN_REVIEW_PATH = ROOT / "docs/02-architecture/design-reviews" / SLUG / "DESIGN-REVIEW.md"


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


def test_epic_007_contrato() -> None:
    contract = _load_json(EXAMPLE_PATH)
    manifest = _load_yaml(MANIFEST_PATH)
    task = _load_json(TASK_PATH)

    _validator().validate(contract)
    assert manifest["identity"] == {
        "epic_id": "EPIC-007",
        "story_id": "STORY-0031",
        "issue_id": "ISSUE-0141",
        "task_id": "TASK-0031",
    }
    assert manifest["requirements"] == contract["requirement_ids"] == [
        "REQ-CIT-001",
        "REQ-EPIC-042",
        "REQ-OSS-001",
        "REQ-PUB-002",
    ]
    assert manifest["acceptance_criteria"] == task["acceptance_criterion_ids"]
    assert manifest["proof"]["required_tests"] == task["tests"]
    assert manifest["review"]["self_approval"] == "PROHIBITED"

    required_allow_paths = {
        ".codex/tasks/TASK-0031.json",
        "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv",
        f"tests/fnd/{SLUG}/test_contract.py",
        "evidence/implementation/epic-007/story-0031/**",
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


def test_license_citation_contribution_and_publication_policies_are_complete() -> None:
    contract = _load_json(EXAMPLE_PATH)

    assert contract["license_policy"] == {
        "application_code": "AGPL-3.0-or-later",
        "reusable_sdks_schemas_examples": "Apache-2.0",
        "original_documentation": "CC-BY-4.0",
        "datasets_fixtures_corpora_models_assets": "EXPLICIT_PER_ASSET",
        "spdx": "REQUIRED",
        "reuse_inventory": "REQUIRED",
        "notice": "REQUIRED_WHEN_APPLICABLE",
        "dependency_inventory": "REQUIRED",
    }
    assert contract["citation_policy"]["artifact"] == "CITATION.cff"
    assert contract["contribution_policy"] == {
        "external_contribution_gate": "CLOSED_UNTIL_PUBLICATION_GATE",
        "origin_certification": "DCO-1.1",
        "signoff": "REQUIRED_FOR_EXTERNAL_CONTRIBUTIONS",
        "inbound_outbound": "INBOUND_EQUALS_OUTBOUND",
        "automated_verification": "REQUIRED",
        "cla": "NOT_REQUIRED_INITIAL_BASELINE",
        "cla_introduction": "LEGAL_DECISION_REQUIRED",
    }
    assert contract["publication_gate"]["required_gates"] == ["G0", "G6"]
    assert contract["scope"]["publication_readiness_claim"] == "PROHIBITED"

    licensing = LICENSING_PATH.read_text(encoding="utf-8")
    for license_id in ("AGPL-3.0-or-later", "Apache-2.0", "CC-BY-4.0"):
        assert license_id in licensing
    contributing = CONTRIBUTING_PATH.read_text(encoding="utf-8")
    assert "DCO 1.1" in contributing
    assert "inbound=outbound" in contributing


def test_contract_rejects_silent_fallback_and_invalid_governance() -> None:
    invalid = copy.deepcopy(_load_json(EXAMPLE_PATH))
    invalid["failure_policy"]["silent_fallback"] = True
    invalid["license_policy"]["application_code"] = "MIT"
    invalid["citation_policy"]["public_release"] = "OPTIONAL"
    invalid["contribution_policy"]["origin_certification"] = "CLA"
    invalid["publication_gate"]["decision"] = "ALLOW"
    invalid["authority"]["broker"] = "AUTHORITATIVE"
    invalid["unexpected"] = "implicit-contract-extension"

    errors = list(_validator().iter_errors(invalid))
    assert {error.validator for error in errors} == {"additionalProperties", "const"}
    assert len(errors) == 7
