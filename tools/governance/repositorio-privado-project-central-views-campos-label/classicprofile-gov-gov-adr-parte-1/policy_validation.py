from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


class PolicyValidationError(ValueError):
    def __init__(self, findings: list[Finding] | tuple[Finding, ...]) -> None:
        self.findings = tuple(sorted(findings))
        message = "; ".join(
            f"{finding.code} at {finding.field}: {finding.detail}"
            for finding in self.findings
        )
        super().__init__(message)


EXPECTED_POLICY: dict[str, Any] = {
    "schema_version": "1.0.0",
    "policy_id": "ENGINEERING-FOUNDATION-CLASSICPROFILE-GOVERNANCE",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "controls": {
        "classic_matching": {
            "photometric_preparation": {
                "parameters_source": "PROFILE",
                "implicit_defaults": "REJECT",
            },
            "pyramid_and_tiles": {
                "order": "COARSE_TO_FINE",
                "coordinate_lineage": "REQUIRED",
                "tile_source_transform": "REQUIRED",
            },
            "spatial_quotas": {
                "adaptive": True,
                "redistribution": "REQUIRED",
            },
            "flann_calibration": {
                "ann": "FLANN_KD_TREE",
                "oracle": "BF_EXACT",
                "recall_floor": "BENCHMARK_PROFILE_DERIVED",
                "abstract_owner_threshold": "PROHIBITED",
            },
            "mask_and_priors": {
                "analysis_mask": "REQUIRED",
                "priors": "SOFT",
            },
            "calibration_gate": {
                "kind": "MULTIDIMENSIONAL",
                "dimensions": [
                    "RECALL_FLANN_VS_BF",
                    "FALSE_ACCEPT_AND_REJECT",
                    "COVERAGE_AND_CONDITIONING",
                    "TIME_RAM_AND_DISK",
                    "ENVIRONMENT_STABILITY",
                ],
            },
        },
        "delivery_governance": {
            "central_project": {
                "count": "ONE",
                "views": [
                    "ROADMAP",
                    "BACKLOG",
                    "SPRINT",
                    "RISKS",
                    "ADRS",
                    "RELEASES",
                    "GEO_AND_AI",
                ],
                "item_identity": "SINGLE",
                "duplicate_items": "REJECT",
            },
            "work_items": {
                "epic_semantics": "CLOSABLE_OUTCOME",
                "implementable_story_required_fields": [
                    "ACCEPTANCE_CRITERIA",
                    "ADRS",
                    "RISKS",
                    "TESTS",
                    "EVIDENCE",
                    "MIGRATION_APPLICABILITY",
                    "ROLLBACK",
                ],
            },
            "flow": {
                "wip": "LIMITED",
                "incomplete_item_history": "PRESERVED",
                "velocity_as_productivity_target": "PROHIBITED",
            },
        },
        "adr_governance": {
            "independent_boundary": "REQUIRED",
            "durable_impact": "REQUIRED",
            "high_reversal_cost": "REQUIRED",
            "overlap_check": "REQUIRED",
            "validator": "decision_governance.validate_new_adr_eligibility",
        },
    },
    "requirement_evidence": {
        "REQ-CLASSICPROFILE-001": "test_req_classicprofile_001",
        "REQ-CLASSICPROFILE-002": "test_req_classicprofile_002",
        "REQ-CLASSICPROFILE-003": "test_req_classicprofile_003",
        "REQ-CLASSICPROFILE-005": "test_req_classicprofile_005",
        "REQ-CLASSICPROFILE-007": "test_req_classicprofile_007",
        "REQ-CLASSICPROFILE-009": "test_req_classicprofile_009",
        "REQ-GOV-001": "test_single_project_views_fields_and_no_duplicate_backlog",
        "REQ-GOV-002": "test_issue_form_required_acceptance_risk_test_rollback_fields",
        "REQ-GOV-003": "test_iteration_wip_limits_and_incomplete_item_history",
        "REQ-GOV-ADR-002": "test_adr_governance_overlap",
    },
}


def _finding_code(field: str) -> str:
    if field.startswith("$.controls.classic_matching"):
        return "CLASSIC_PROFILE_INVALID"
    if field.startswith("$.controls.delivery_governance"):
        return "DELIVERY_GOVERNANCE_INVALID"
    if field.startswith("$.controls.adr_governance"):
        return "ADR_GOVERNANCE_INVALID"
    if field.startswith("$.requirement_evidence"):
        return "EVIDENCE_MAPPING_INVALID"
    return "POLICY_STRUCTURE_INVALID"


def _compare(actual: object, expected: object, field: str) -> list[Finding]:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [Finding(_finding_code(field), field, "object is required")]
        findings: list[Finding] = []
        for key in sorted(set(expected) - set(actual)):
            child = f"{field}.{key}"
            findings.append(Finding(_finding_code(child), child, "field is required"))
        for key in sorted(set(actual) - set(expected)):
            child = f"{field}.{key}"
            findings.append(Finding(_finding_code(child), child, "unknown field"))
        for key in sorted(set(actual) & set(expected)):
            findings.extend(_compare(actual[key], expected[key], f"{field}.{key}"))
        return findings
    if type(actual) is not type(expected) or actual != expected:
        return [Finding(_finding_code(field), field, f"expected {expected!r}")]
    return []


def validate_policy(policy: object) -> list[Finding]:
    return sorted(_compare(policy, EXPECTED_POLICY, "$"))


def require_valid(policy: object) -> None:
    findings = validate_policy(policy)
    if findings:
        raise PolicyValidationError(findings)


def load_policy(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PolicyValidationError(
            [Finding("POLICY_UNREADABLE", "$", str(error))]
        ) from error
    require_valid(loaded)
    return loaded
