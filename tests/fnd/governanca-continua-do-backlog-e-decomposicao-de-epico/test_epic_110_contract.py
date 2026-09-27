from __future__ import annotations

import copy
import csv
import json
from functools import cache
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "governanca-continua-do-backlog-e-decomposicao-de-epico"
)
SCHEMA_PATH = CONTRACT_ROOT / "backlog-governance-profile.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/backlog-governance-profile.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"

REQUIREMENT_TESTS = {
    "REQ-ISM-004": "test_versioned_issue_portfolio_catalog_github_reconciliation",
    "REQ-ISS-002": "test_issue_forecast_min_mode_max_confidence_and_snapshot_variance",
    "REQ-PLN-009": (
        "test_cross_domain_contract_checkpoint_and_walking_skeleton_integration"
    ),
    "REQ-PRJ-004": "test_canonical_workflow_transitions",
    "REQ-SPRINT-001-004": "test_epic_110_contrato",
}
OWN_CONTRACTS = {
    path.relative_to(ROOT).as_posix()
    for path in (MANIFEST_PATH, SCHEMA_PATH, EXAMPLE_PATH)
}


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


@cache
def _load_manifest() -> dict[str, Any]:
    loaded = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


@cache
def _validator() -> Draft202012Validator:
    schema = _load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _profile() -> dict[str, Any]:
    profile = _load_json(EXAMPLE_PATH)
    _validator().validate(profile)
    return profile


def _assert_rejected(candidate: dict[str, Any]) -> None:
    assert list(_validator().iter_errors(candidate)), "fail-open profile was accepted"


def _referenced_contracts(profile: dict[str, Any]) -> set[str]:
    controls = profile["controls"]
    return {
        controls["portfolio_catalog"]["schema"],
        controls["portfolio_catalog"]["example"],
        controls["forecast"]["schema"],
        controls["forecast"]["example"],
        controls["integration_checkpoint"]["profile_schema"],
        controls["integration_checkpoint"]["profile_example"],
        controls["foundation_boundaries"]["schema"],
        controls["foundation_boundaries"]["example"],
    }


def _validate_referenced_pairs(profile: dict[str, Any]) -> None:
    controls = profile["controls"]
    pairs = (
        (controls["portfolio_catalog"]["schema"], controls["portfolio_catalog"]["example"]),
        (controls["forecast"]["schema"], controls["forecast"]["example"]),
        (
            controls["integration_checkpoint"]["profile_schema"],
            controls["integration_checkpoint"]["profile_example"],
        ),
        (
            controls["foundation_boundaries"]["schema"],
            controls["foundation_boundaries"]["example"],
        ),
    )
    for schema_ref, example_ref in pairs:
        schema = _load_json(ROOT / schema_ref)
        example = _load_json(ROOT / example_ref)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(example)


def test_epic_110_contrato() -> None:
    manifest = _load_manifest()
    profile = _profile()
    assert manifest["schema_version"] == manifest["contract_version"] == "1.0.0"
    assert profile["schema_version"] == profile["profile_version"] == "1.0.0"
    assert manifest["owner"] == profile["owner"] == "BC-001"
    assert manifest["status"] == profile["status"] == "FROZEN"
    assert manifest["identity"] == {
        "epic_id": "EPIC-110",
        "story_id": "STORY-0683",
        "issue_id": "ISSUE-0793",
        "github_issue": 68,
        "task_id": "TASK-0683",
    }
    assert manifest["compatibility"] == {
        "policy": "SEMVER",
        "compatible_change": "OPTIONAL_ADDITION_WITHIN_CURRENT_MAJOR",
        "breaking_change": "NEW_MAJOR_AND_ARCHITECT_REVIEW",
        "unknown_properties": "REJECT",
    }
    assert manifest["authority"]["contract_source"] == "VERSIONED_REPOSITORY"
    assert manifest["authority"]["runtime_state"] == "NOT_APPLICABLE"
    assert manifest["boundary"]["prohibited"] == [
        "entity",
        "repository",
        "orm_model",
        "state_machine",
    ]

    requirements = {entry["id"]: entry for entry in manifest["requirements"]}
    assert set(requirements) == set(REQUIREMENT_TESTS)
    for requirement, test_name in REQUIREMENT_TESTS.items():
        assert requirements[requirement]["test"] == test_name
        assert requirements[requirement]["failure_modes"]
    assert set(manifest["proof"]["required_tests"]) == set(REQUIREMENT_TESTS.values())

    controls = profile["controls"]
    assert controls["forecast"]["components"] == [
        "MINIMUM",
        "MODE",
        "MAXIMUM",
        "CONFIDENCE",
        "VERSIONED_SNAPSHOT",
        "VARIANCE",
    ]
    assert controls["workflow"]["state_catalog"] == "VERSIONED_CANONICAL"
    assert controls["workflow"]["transition_policy"] == "REGISTERED_ONLY"
    assert controls["foundation_boundaries"]["required"] == ["CORE", "API", "RUNNERS"]
    _validate_referenced_pairs(profile)

    with OWNERSHIP_PATH.open(encoding="utf-8", newline="") as ownership_file:
        registered = {
            row["contract"]
            for row in csv.DictReader(ownership_file)
            if row["owner_context"] == "BC-001" and row["status"] == "VERSIONED"
        }
    assert OWN_CONTRACTS | _referenced_contracts(profile) <= registered


@pytest.mark.parametrize(
    ("control", "field", "fail_open_value"),
    [
        ("portfolio_catalog", "missing_or_mismatch", "ACCEPT"),
        ("forecast", "interval_policy", "UNORDERED"),
        ("forecast", "snapshot_variance", "BEST_EFFORT"),
        ("integration_checkpoint", "producer_contract", "OPTIONAL"),
        ("integration_checkpoint", "missing_or_incompatible", "CONTINUE"),
        ("workflow", "unknown_state", "ACCEPT"),
        ("workflow", "invalid_transition", "ACCEPT"),
        ("foundation_boundaries", "separation", "OPTIONAL"),
        ("foundation_boundaries", "runtime_materialization", "IMPLEMENTED"),
    ],
)
def test_epic_110_contract_rejects_fail_open_paths(
    control: str, field: str, fail_open_value: str
) -> None:
    candidate = copy.deepcopy(_profile())
    candidate["controls"][control][field] = fail_open_value
    _assert_rejected(candidate)


def test_epic_110_contract_rejects_missing_unknown_or_wrong_authority() -> None:
    missing_control = copy.deepcopy(_profile())
    missing_control["controls"].pop("workflow")
    _assert_rejected(missing_control)

    unknown_property = copy.deepcopy(_profile())
    unknown_property["fallback"] = "accept"
    _assert_rejected(unknown_property)

    wrong_owner = copy.deepcopy(_profile())
    wrong_owner["owner"] = "BC-013"
    _assert_rejected(wrong_owner)
