from __future__ import annotations

import copy
import importlib.util
import sys
from functools import cache
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[4]
MODULE_ROOT = Path(__file__).resolve().parent
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico/"
    "prj-prm-parte-3/foundation-policy.json"
)
_SPEC = importlib.util.spec_from_file_location(
    "backlog_project_governance_policy_validation",
    MODULE_ROOT / "policy_validation.py",
)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError("cannot load backlog project governance policy validator")
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


def test_issue_type_forms() -> None:
    control = _policy()["controls"]["issue_types"]
    assert control == {
        "taxonomy": "VERSIONED_CANONICAL",
        "form_per_registered_type": "REQUIRED",
        "unknown_type": "REJECT",
    }
    assert "ISSUE_TYPES_INVALID" in _codes(
        _replace("issue_types", "unknown_type", "GENERIC_FORM")
    )


def test_mandatory_core_type_fields() -> None:
    control = _policy()["controls"]["mandatory_fields"]
    assert control == {
        "core": "REQUIRED",
        "per_type_extensions": "REQUIRED",
        "missing_applicable_field": "REJECT",
    }
    assert "MANDATORY_FIELDS_INVALID" in _codes(
        _replace("mandatory_fields", "per_type_extensions", "OPTIONAL")
    )


def test_single_parent_limited_hierarchy() -> None:
    control = _policy()["controls"]["hierarchy"]
    assert control == {
        "primary_parent": "EXACTLY_ONE",
        "operational_hierarchy": "LIMITED",
        "multiple_primary_parents": "REJECT",
    }
    assert "HIERARCHY_INVALID" in _codes(
        _replace("hierarchy", "multiple_primary_parents", "ALLOW")
    )


def test_definition_of_ready_gate() -> None:
    control = _policy()["controls"]["ready_gate"]
    assert control["definition"] == "docs/00-governance/DEFINITION_OF_READY.md"
    assert control["applicability"] == "PROPORTIONAL"
    assert control["unsatisfied"] == "REJECT"
    assert "READY_GATE_INVALID" in _codes(
        _replace("ready_gate", "unsatisfied", "READY")
    )


def test_evidence_based_definition_of_done() -> None:
    control = _policy()["controls"]["done_gate"]
    assert control["definition"] == "docs/00-governance/DEFINITION_OF_DONE.md"
    assert control["evidence"] == "REQUIRED"
    assert control["applicable_checks"] == "REQUIRED"
    assert control["unsatisfied"] == "REJECT"
    assert "DONE_GATE_INVALID" in _codes(
        _replace("done_gate", "evidence", "OPTIONAL")
    )


def test_typed_dependency_cycle_detection() -> None:
    control = _policy()["controls"]["typed_dependencies"]
    assert control["edge_type"] == "REQUIRED"
    assert control["material_cycle_detection"] == "REQUIRED"
    assert control["material_cycle"] == "REJECT"
    assert "DEPENDENCY_GRAPH_INVALID" in _codes(
        _replace("typed_dependencies", "material_cycle", "ALLOW")
    )


def test_derived_priority_dimensions() -> None:
    control = _policy()["controls"]["priority"]
    assert control["dimensions"] == ["IMPACT", "URGENCY", "RISK", "GATE"]
    assert control["derivation"] == "EXPLICIT"
    assert control["collapsed_dimension"] == "REJECT"
    assert "PRIORITY_INVALID" in _codes(
        _replace("priority", "dimensions", ["PRIORITY"])
    )


def test_relative_size_uncertainty_split() -> None:
    control = _policy()["controls"]["relative_size"]
    assert control["estimate"] == "RELATIVE_BAND"
    assert control["confidence"] == "REQUIRED"
    assert control["split_rule"] == "REQUIRED"
    assert control["uncertain_without_split_rule"] == "REJECT"
    assert "RELATIVE_SIZE_INVALID" in _codes(
        _replace("relative_size", "confidence", "OPTIONAL")
    )


def test_guarded_project_automation() -> None:
    control = _policy()["controls"]["guarded_automation"]
    assert control["integrity_preservation"] == "REQUIRED"
    assert control["material_decision_approval"] == "PROHIBITED"
    assert control["material_decision_gate"] == "HUMAN_REQUIRED"
    assert control["silent_approval"] == "REJECT"
    assert "AUTOMATION_GUARD_INVALID" in _codes(
        _replace("guarded_automation", "material_decision_approval", "ALLOW")
    )


def test_portfolio_materialization_decision_01() -> None:
    control = _policy()["controls"]["staging_materialization"]
    assert control["first_target"] == "REPRESENTATIVE_STAGING"
    assert control["operational_project_after_staging"] == "REQUIRED"
    assert control["direct_first_operational_materialization"] == "REJECT"
    assert "STAGING_MATERIALIZATION_INVALID" in _codes(
        _replace(
            "staging_materialization",
            "direct_first_operational_materialization",
            "ALLOW",
        )
    )


def test_policy_input_is_strict_and_fail_closed(tmp_path: Path) -> None:
    unknown = copy.deepcopy(_policy())
    unknown["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _codes(unknown)

    missing = copy.deepcopy(_policy())
    del missing["controls"]["ready_gate"]["unsatisfied"]
    assert "READY_GATE_INVALID" in _codes(missing)

    missing_evidence = copy.deepcopy(_policy())
    del missing_evidence["requirement_evidence"]["REQ-PRJ-001"]
    assert "REQUIREMENT_EVIDENCE_INVALID" in _codes(missing_evidence)

    assert "POLICY_STRUCTURE_INVALID" in _codes([])

    duplicate = tmp_path / "duplicate-policy.json"
    duplicate.write_text('{"schema_version":"1.0.0","schema_version":"1.0.0"}')
    with pytest.raises(PolicyValidationError) as duplicate_error:
        load_policy(duplicate)
    assert duplicate_error.value.findings[0].code == "POLICY_DUPLICATE_KEY"

    with pytest.raises(PolicyValidationError) as missing_file_error:
        load_policy(tmp_path / "missing-policy.json")
    assert missing_file_error.value.findings[0].code == "POLICY_UNREADABLE"
