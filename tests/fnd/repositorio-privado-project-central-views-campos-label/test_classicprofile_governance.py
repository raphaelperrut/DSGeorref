from __future__ import annotations

import copy
import sys
from functools import cache
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/repositorio-privado-project-central-views-campos-label/"
    "classicprofile-gov-gov-adr-parte-1"
)
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "classicprofile-gov-gov-adr-parte-1/foundation-policy.json"
)
sys.path.insert(0, str(MODULE_ROOT))

from policy_validation import (  # noqa: E402
    PolicyValidationError,
    load_policy,
    validate_policy,
)


@cache
def _policy() -> dict[str, Any]:
    return load_policy(POLICY_PATH)


def _codes(policy: object) -> set[str]:
    return {finding.code for finding in validate_policy(policy)}


def _replace(path: tuple[str, ...], value: object) -> dict[str, Any]:
    invalid = copy.deepcopy(_policy())
    target: dict[str, Any] = invalid
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value
    return invalid


def test_req_classicprofile_001() -> None:
    control = _policy()["controls"]["classic_matching"]["photometric_preparation"]
    assert control == {"parameters_source": "PROFILE", "implicit_defaults": "REJECT"}
    invalid = _replace(
        ("controls", "classic_matching", "photometric_preparation", "parameters_source"),
        "CALLER_DEFAULT",
    )
    assert "CLASSIC_PROFILE_INVALID" in _codes(invalid)


def test_req_classicprofile_002() -> None:
    control = _policy()["controls"]["classic_matching"]["pyramid_and_tiles"]
    assert control["order"] == "COARSE_TO_FINE"
    assert control["coordinate_lineage"] == control["tile_source_transform"] == "REQUIRED"
    invalid = _replace(
        ("controls", "classic_matching", "pyramid_and_tiles", "coordinate_lineage"),
        "OPTIONAL",
    )
    assert "CLASSIC_PROFILE_INVALID" in _codes(invalid)


def test_req_classicprofile_003() -> None:
    control = _policy()["controls"]["classic_matching"]["spatial_quotas"]
    assert control == {"adaptive": True, "redistribution": "REQUIRED"}
    invalid = _replace(
        ("controls", "classic_matching", "spatial_quotas", "redistribution"),
        "DISABLED",
    )
    assert "CLASSIC_PROFILE_INVALID" in _codes(invalid)


def test_req_classicprofile_005() -> None:
    control = _policy()["controls"]["classic_matching"]["flann_calibration"]
    assert control["ann"] == "FLANN_KD_TREE"
    assert control["oracle"] == "BF_EXACT"
    assert control["recall_floor"] == "BENCHMARK_PROFILE_DERIVED"
    assert control["abstract_owner_threshold"] == "PROHIBITED"
    invalid = _replace(
        ("controls", "classic_matching", "flann_calibration", "recall_floor"),
        "UNSPECIFIED",
    )
    assert "CLASSIC_PROFILE_INVALID" in _codes(invalid)


def test_req_classicprofile_007() -> None:
    control = _policy()["controls"]["classic_matching"]["mask_and_priors"]
    assert control == {"analysis_mask": "REQUIRED", "priors": "SOFT"}
    invalid = _replace(
        ("controls", "classic_matching", "mask_and_priors", "analysis_mask"),
        "OPTIONAL",
    )
    assert "CLASSIC_PROFILE_INVALID" in _codes(invalid)


def test_req_classicprofile_009() -> None:
    control = _policy()["controls"]["classic_matching"]["calibration_gate"]
    assert control["kind"] == "MULTIDIMENSIONAL"
    assert len(control["dimensions"]) == 5
    invalid = _replace(
        ("controls", "classic_matching", "calibration_gate", "dimensions"),
        ["RECALL_FLANN_VS_BF"],
    )
    assert "CLASSIC_PROFILE_INVALID" in _codes(invalid)


def test_single_project_views_fields_and_no_duplicate_backlog() -> None:
    control = _policy()["controls"]["delivery_governance"]["central_project"]
    assert control["count"] == "ONE"
    assert len(control["views"]) == len(set(control["views"])) == 7
    assert control["item_identity"] == "SINGLE"
    assert control["duplicate_items"] == "REJECT"
    invalid = _replace(
        ("controls", "delivery_governance", "central_project", "duplicate_items"),
        "ALLOW",
    )
    assert "DELIVERY_GOVERNANCE_INVALID" in _codes(invalid)


def test_issue_form_required_acceptance_risk_test_rollback_fields() -> None:
    control = _policy()["controls"]["delivery_governance"]["work_items"]
    assert control["epic_semantics"] == "CLOSABLE_OUTCOME"
    assert set(control["implementable_story_required_fields"]) == {
        "ACCEPTANCE_CRITERIA",
        "ADRS",
        "RISKS",
        "TESTS",
        "EVIDENCE",
        "MIGRATION_APPLICABILITY",
        "ROLLBACK",
    }
    invalid = _replace(
        (
            "controls",
            "delivery_governance",
            "work_items",
            "implementable_story_required_fields",
        ),
        ["ACCEPTANCE_CRITERIA"],
    )
    assert "DELIVERY_GOVERNANCE_INVALID" in _codes(invalid)


def test_iteration_wip_limits_and_incomplete_item_history() -> None:
    control = _policy()["controls"]["delivery_governance"]["flow"]
    assert control == {
        "wip": "LIMITED",
        "incomplete_item_history": "PRESERVED",
        "velocity_as_productivity_target": "PROHIBITED",
    }
    invalid = _replace(
        ("controls", "delivery_governance", "flow", "incomplete_item_history"),
        "DISCARDED",
    )
    assert "DELIVERY_GOVERNANCE_INVALID" in _codes(invalid)


def test_adr_governance_overlap() -> None:
    control = _policy()["controls"]["adr_governance"]
    assert control == {
        "independent_boundary": "REQUIRED",
        "durable_impact": "REQUIRED",
        "high_reversal_cost": "REQUIRED",
        "overlap_check": "REQUIRED",
        "validator": "decision_governance.validate_new_adr_eligibility",
    }
    invalid = _replace(
        ("controls", "adr_governance", "high_reversal_cost"), "NOT_DEMONSTRATED"
    )
    assert "ADR_GOVERNANCE_INVALID" in _codes(invalid)


def test_policy_rejects_unknown_fields_and_unreadable_input() -> None:
    invalid = copy.deepcopy(_policy())
    invalid["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(invalid)

    with pytest.raises(PolicyValidationError) as captured:
        load_policy(POLICY_PATH.parent / "missing-policy.json")
    assert captured.value.findings[0].code == "POLICY_UNREADABLE"
