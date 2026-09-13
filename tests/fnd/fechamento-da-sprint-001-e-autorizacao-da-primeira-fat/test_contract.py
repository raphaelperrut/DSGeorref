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
    / "fechamento-da-sprint-001-e-autorizacao-da-primeira-fat"
)
SCHEMA_PATH = CONTRACT_ROOT / "sprint-001-closure-authorization.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/sprint-001-closure-authorization.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0565.json"
DESIGN_REVIEW_PATH = (
    ROOT
    / "docs/02-architecture/design-reviews"
    / "fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/DESIGN-REVIEW.md"
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


def test_epic_092_contrato() -> None:
    contract = _load_json(EXAMPLE_PATH)
    manifest = _load_yaml(MANIFEST_PATH)
    task = _load_json(TASK_PATH)

    _validator().validate(contract)
    assert manifest["identity"] == {
        "epic_id": "EPIC-092",
        "story_id": "STORY-0565",
        "issue_id": "ISSUE-0675",
        "task_id": "TASK-0565",
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
        assert item["candidate_evidence"] == "test_epic_092_contrato"

    assert manifest["acceptance_criteria"] == task["acceptance_criterion_ids"]
    assert manifest["proof"]["required_tests"] == task["tests"]
    assert manifest["review"]["self_approval"] == "PROHIBITED"

    required_allow_paths = {
        ".codex/tasks/TASK-0565.json",
        "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv",
        "tests/fnd/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/test_contract.py",
        "evidence/implementation/epic-092/story-0565/**",
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

    for source in contract["contract_sources"].values():
        assert (ROOT / source).is_file()
    assert manifest["upstream"]["manifest"] == contract["contract_sources"][
        "foundation_manifest"
    ]

    design_review = DESIGN_REVIEW_PATH.read_text(encoding="utf-8")
    for criterion_id in task["acceptance_criterion_ids"]:
        assert criterion_id in design_review


def test_sprint_exit_states_authorities_and_compatibility_are_frozen() -> None:
    contract = _load_json(EXAMPLE_PATH)

    assert contract["foundation_evidence"]["canonical_test"] == (
        "test_executable_foundation_gate_clean_room_end_to_end"
    )
    assert contract["foundation_evidence"]["required_result"] == "PASS"
    assert contract["sprint_exit_conditions"] == {
        "adr_019_022_evidence": "ATTACHED",
        "contracts": "FROZEN",
        "story_requirement_limit": 10,
        "story_requirement_limit_violation": "BLOCK",
        "transient_write_scope": "PROHIBITED",
        "write_scope_overlap": "BLOCK",
        "runtime_resolution": "RESOLVED",
        "runtime_signature": "REQUIRED",
    }
    assert contract["state_model"]["authorized_state"] == (
        "AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE"
    )
    assert contract["data_authority"]["foundation_runtime_state"] == (
        "POSTGRESQL_POSTGIS"
    )
    assert contract["data_authority"]["broker"] == "TRANSPORT_ONLY"
    assert contract["data_authority"]["telemetry"] == (
        "DERIVED_NON_AUTHORITATIVE"
    )
    assert contract["compatibility"]["policy"] == "SEMVER"
    assert contract["review_gate"]["same_candidate_commit"] is True


def test_contract_rejects_unsafe_or_ambiguous_authorization() -> None:
    invalid = copy.deepcopy(_load_json(EXAMPLE_PATH))
    invalid["foundation_evidence"]["required_result"] = "UNKNOWN"
    invalid["sprint_exit_conditions"]["contracts"] = "MUTABLE"
    invalid["sprint_exit_conditions"]["transient_write_scope"] = "ALLOW"
    invalid["state_model"]["unknown_or_unmapped_state"] = "MAP_TO_PENDING"
    invalid["data_authority"]["broker"] = "STATE_AUTHORITY"
    invalid["evidence_policy"]["candidate_sha_binding"] = "LATEST"
    invalid["failure_policy"]["silent_fallback"] = True
    invalid["review_gate"]["self_approval"] = "ALLOWED"
    invalid["unexpected"] = "implicit-contract-extension"

    errors = list(_validator().iter_errors(invalid))
    assert {error.validator for error in errors} == {
        "additionalProperties",
        "const",
    }
    assert len(errors) == 8


def test_contract_rejects_missing_proof_exit_condition_or_review_gate() -> None:
    invalid = copy.deepcopy(_load_json(EXAMPLE_PATH))
    del invalid["foundation_evidence"]
    del invalid["sprint_exit_conditions"]
    del invalid["review_gate"]

    errors = list(_validator().iter_errors(invalid))
    assert {error.validator for error in errors} == {"required"}
    assert len(errors) == 3
