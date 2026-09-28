from __future__ import annotations

import copy
import importlib.util
import sys
from functools import cache
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[4]
MODULE_ROOT = Path(__file__).resolve().parent
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico/"
    "sprint-001-parte-5/foundation-policy.json"
)
_SPEC = importlib.util.spec_from_file_location(
    "sprint_foundation_slice_policy_validation",
    MODULE_ROOT / "policy_validation.py",
)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError("cannot load sprint foundation policy validator")
_VALIDATOR = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _VALIDATOR
_SPEC.loader.exec_module(_VALIDATOR)

PolicyValidationError = _VALIDATOR.PolicyValidationError
load_policy = _VALIDATOR.load_policy
validate_policy = _VALIDATOR.validate_policy


@cache
def _policy() -> dict[str, Any]:
    return load_policy(POLICY_PATH)


def _codes(policy: object) -> set[str]:
    return {finding.code for finding in validate_policy(policy)}


def _replace(control: str, field: str, value: object) -> dict[str, Any]:
    invalid = copy.deepcopy(_policy())
    invalid["controls"][control][field] = value
    return invalid


def test_sprint_foundation_policy_decision_02() -> None:
    control = _policy()["controls"]["graph_selection"]
    assert control["closure"] == "DETERMINISTIC_HARD_PREDECESSORS"
    assert control["gates"] == ["DEPENDENCIES", "REQUIREMENTS", "RISK"]
    assert control["caller_selected_issues"] == "REJECT"
    assert "GRAPH_SELECTION_INVALID" in _codes(
        _replace("graph_selection", "caller_selected_issues", "ALLOW")
    )


def test_sprint_foundation_policy_decision_03() -> None:
    control = _policy()["controls"]["vertical_waves"]
    assert control["selection"] == "GRAPH_DERIVED"
    assert control["size"] == "PROPER_SUBSET"
    assert control["direct_blockers"] == "COMPLETED_WITH_EVIDENCE"
    assert control["evidence_oriented"] == "REQUIRED"
    assert "VERTICAL_WAVES_INVALID" in _codes(
        _replace("vertical_waves", "unbounded_wave", "ALLOW")
    )


def test_sprint_foundation_policy_decision_05() -> None:
    control = _policy()["controls"]["essential_contracts"]
    assert control["scope"] == "EXACT_ESSENTIAL_SET"
    assert control["versioned"] == "REQUIRED"
    assert control["exercise_evidence"] == "REQUIRED"
    assert "ESSENTIAL_CONTRACTS_INVALID" in _codes(
        _replace("essential_contracts", "missing_or_extra_contract", "ALLOW")
    )


def test_sprint_foundation_policy_decision_06() -> None:
    control = _policy()["controls"]["synthetic_diagnostic"]
    assert control["synthetic"] == "REQUIRED"
    assert control["end_to_end"] == "REQUIRED"
    assert control["functional_georeferencing_claim"] == "REJECT"
    assert "SYNTHETIC_DIAGNOSTIC_INVALID" in _codes(
        _replace("synthetic_diagnostic", "passing_execution_evidence", "OPTIONAL")
    )


def test_sprint_foundation_policy_decision_07() -> None:
    control = _policy()["controls"]["progressive_ci"]
    assert control["capability_source"] == "REPOSITORY_REVISION"
    assert control["test_per_present_capability"] == "REQUIRED"
    assert control["make_verify_parity"] == "REQUIRED"
    assert control["caller_capability_assertion"] == "IGNORED"
    assert "PROGRESSIVE_CI_INVALID" in _codes(
        _replace("progressive_ci", "untested_present_capability", "ALLOW")
    )


def test_sprint_foundation_policy_decision_08() -> None:
    control = _policy()["controls"]["sprint_evidence_set"]
    assert control["record_type"] == "SPRINT_EVIDENCE_SET"
    assert control["machine_readable"] == "REQUIRED"
    assert control["immutable_digest"] == "SHA-256"
    assert control["human_summary"] == "REQUIRED"
    assert "SPRINT_EVIDENCE_SET_INVALID" in _codes(
        _replace("sprint_evidence_set", "incomplete_or_mutated_evidence", "ALLOW")
    )


def test_sprint_foundation_policy_decision_09() -> None:
    control = _policy()["controls"]["sprint_closure"]
    assert control["basis"] == "EVIDENCE"
    assert control["calendar_closure"] == "REJECT"
    assert control["extension_authority"] == "PRODUCT_OWNER"
    assert control["extension_basis"] == "DIRECT_GRAPH_BLOCKER"
    assert "SPRINT_CLOSURE_INVALID" in _codes(
        _replace("sprint_closure", "self_declared_extension", "ALLOW")
    )


def test_sprint_foundation_policy_decision_10() -> None:
    control = _policy()["controls"]["first_slice_cutover"]
    assert control["mode"] == "EXPLICIT"
    assert control["foundation_gate"] == "G1_APPROVED"
    assert control["first_slice_authorization"] == "REQUIRED"
    assert control["candidate_lineage"] == "REQUIRED"
    assert "FIRST_SLICE_CUTOVER_INVALID" in _codes(
        _replace("first_slice_cutover", "silent_or_unapproved_cutover", "ALLOW")
    )


def test_sprint_foundation_policy_is_strict_and_fail_closed() -> None:
    unknown = copy.deepcopy(_policy())
    unknown["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(unknown)

    missing = copy.deepcopy(_policy())
    del missing["controls"]["first_slice_cutover"]["foundation_gate"]
    assert "FIRST_SLICE_CUTOVER_INVALID" in _codes(missing)

    missing_evidence = copy.deepcopy(_policy())
    del missing_evidence["requirement_evidence"]["REQ-SPRINT-001-008"]
    assert "REQUIREMENT_EVIDENCE_INVALID" in _codes(missing_evidence)
    assert "POLICY_STRUCTURE_INVALID" in _codes([])

    duplicate_text = '{"schema_version":"1.0.0","schema_version":"1.0.0"}'
    with (
        patch.object(Path, "read_text", return_value=duplicate_text),
        pytest.raises(PolicyValidationError) as duplicate_error,
    ):
        load_policy(POLICY_PATH)
    assert duplicate_error.value.findings[0].code == "POLICY_DUPLICATE_KEY"

    with pytest.raises(PolicyValidationError) as missing_file_error:
        load_policy(POLICY_PATH.with_name("missing-policy.json"))
    assert missing_file_error.value.findings[0].code == "POLICY_UNREADABLE"
