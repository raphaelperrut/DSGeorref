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
    "gov-adr-ism-iss-parte-2"
)
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "gov-adr-ism-iss-parte-2/foundation-policy.json"
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


def _replace(control: str, field: str, value: object) -> dict[str, Any]:
    invalid = copy.deepcopy(_policy())
    invalid["controls"][control][field] = value
    return invalid


def test_adr_governance_overlap() -> None:
    control = _policy()["controls"]["adr_governance"]
    assert control["local_kinds"] == [
        "REFINEMENT",
        "PROFILE",
        "BENCHMARK",
        "LOCAL_DETAIL",
    ]
    assert control["local_promotion"] == "REJECT"
    assert control["overlap_check"] == "REQUIRED"
    assert control["normative_owner"] == "REQUIRED"
    assert control["owner_decision_gate"] == "REQUIRED"
    assert control["eligibility_validator"].endswith("validate_new_adr_eligibility")
    assert control["change_validator"].endswith("validate_adr_change_governance")
    invalid = _replace("adr_governance", "owner_decision_gate", "OPTIONAL")
    assert "ADR_GOVERNANCE_INVALID" in _codes(invalid)


def test_canonical_domain_taxonomy_primary_and_affected_domains() -> None:
    control = _policy()["controls"]["domain_taxonomy"]
    assert control == {
        "source": "CANONICAL_REGISTRY",
        "primary_domain_count": 1,
        "affected_domains": "ZERO_OR_MORE_UNIQUE",
        "primary_in_affected": "REJECT",
        "unknown_domain": "REJECT",
    }
    invalid = _replace("domain_taxonomy", "unknown_domain", "ACCEPT")
    assert "DOMAIN_TAXONOMY_INVALID" in _codes(invalid)


def test_req_ism_006() -> None:
    control = _policy()["controls"]["issue_sync"]
    assert control["default_mode"] == "DRY_RUN"
    assert control["dry_run_writes"] == "PROHIBITED"
    assert control["managed_field_registry"] == "REQUIRED"
    invalid = _replace("issue_sync", "default_mode", "APPLY")
    assert "ISSUE_SYNC_INVALID" in _codes(invalid)


def test_single_primary_cross_domain_issue_contracts() -> None:
    control = _policy()["controls"]["cross_domain_work"]
    assert control == {
        "issue_identity": "SINGLE",
        "primary_domain_count": 1,
        "affected_domains": "REQUIRED_WHEN_CROSS_DOMAIN",
        "duplicate_issue": "REJECT",
    }
    invalid = _replace("cross_domain_work", "duplicate_issue", "ALLOW")
    assert "CROSS_DOMAIN_WORK_INVALID" in _codes(invalid)


def test_all_work_packages_have_parent_issue_and_slice_skeleton() -> None:
    control = _policy()["controls"]["portfolio"]
    assert control["epic_issue"] == "REQUIRED"
    assert control["implementable_slice_skeleton"] == "REQUIRED"
    assert control["traceability"] == "REQUIRED"
    invalid = _replace("portfolio", "epic_issue", "OPTIONAL")
    assert "PORTFOLIO_INVALID" in _codes(invalid)


def test_complete_portfolio_skeleton_and_progressive_detailing_rules() -> None:
    control = _policy()["controls"]["portfolio"]
    assert control["complete_skeleton"] == "REQUIRED"
    assert control["future_detailing"] == "PROGRESSIVE"
    invalid = _replace("portfolio", "future_detailing", "FULL_UPFRONT")
    assert "PORTFOLIO_INVALID" in _codes(invalid)


def test_idempotent_dry_run_managed_field_issue_sync() -> None:
    control = _policy()["controls"]["issue_sync"]
    assert control["dry_run_writes"] == "PROHIBITED"
    assert control["unmanaged_field_mutation"] == "REJECT"
    assert control["repeat_convergence"] == "NO_CHANGES"
    invalid = _replace("issue_sync", "unmanaged_field_mutation", "ALLOW")
    assert "ISSUE_SYNC_INVALID" in _codes(invalid)


def test_bounded_research_spike_exit_decision() -> None:
    control = _policy()["controls"]["research_spike"]
    assert control == {
        "budget": "REQUIRED",
        "verifiable_question": "REQUIRED",
        "decision_output": "REQUIRED",
        "objective_exit_criterion": "REQUIRED",
    }
    invalid = _replace("research_spike", "objective_exit_criterion", "OPTIONAL")
    assert "RESEARCH_SPIKE_INVALID" in _codes(invalid)


def test_req_native_003() -> None:
    control = _policy()["controls"]["geometry_boundary"]
    assert control == {
        "domain_library": "SHAPELY",
        "io_adapters": "EXPLICIT",
        "domain_parsing": "PROHIBITED",
        "domain_serialization": "PROHIBITED",
    }
    invalid = _replace("geometry_boundary", "io_adapters", "IMPLICIT")
    assert "GEOMETRY_BOUNDARY_INVALID" in _codes(invalid)


def test_policy_rejects_unknown_fields_and_unreadable_input() -> None:
    invalid = copy.deepcopy(_policy())
    invalid["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(invalid)

    with pytest.raises(PolicyValidationError) as captured:
        load_policy(POLICY_PATH.parent / "missing-policy.json")
    assert captured.value.findings[0].code == "POLICY_UNREADABLE"
