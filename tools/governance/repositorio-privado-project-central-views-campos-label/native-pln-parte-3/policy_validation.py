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
    "policy_id": "ENGINEERING-FOUNDATION-NATIVE-PLANNING",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "controls": {
        "classic_descriptor": {
            "descriptor": "ROOTSIFT",
            "numeric_representation": "FLOAT32",
            "promotion": "CANONICAL",
        },
        "classic_matcher": {
            "ann": "FLANN_KD_TREE",
            "ann_status": "REQUIRED",
            "calibration_oracle": "BF_EXACT",
            "oracle_mode": "CONTROLLED",
        },
        "robust_estimator": {
            "library": "OPENCV",
            "estimator": "USAC_MAGSAC",
            "versioning": "OCI_DIGEST_PINNED",
            "boundary": "ENCAPSULATED",
            "silent_fallback": "PROHIBITED",
        },
        "cog": {
            "writer": "GDAL_NATIVE_STACK",
            "validation_path": "INDEPENDENT",
            "validation_dimensions": ["STRUCTURAL", "SPATIAL", "CONTENT"],
            "invalid_output": "REJECT",
        },
        "native_stack": {
            "promotion_unit": "OCI_ABI",
            "members": ["GDAL", "PROJ", "GEOS", "OPENCV", "GRIDS", "BINDINGS"],
            "pin": "NATIVE_OCI_STACK_DIGEST",
            "abi_smoke": "REQUIRED",
        },
        "native_io": {
            "drivers": "ALLOWLIST",
            "vsi": "ALLOWLIST",
            "network_vsi": "DISABLED_BY_DEFAULT",
            "external_files": "HOSTILE",
            "dataset_handles": "WORK_UNIT_LOCAL",
            "process_isolation": "REQUIRED",
        },
        "roadmap": {
            "structure": ["HORIZON", "OUTCOME", "GATE"],
            "dates": "EXCEPTION_ONLY",
            "date_justification": "REAL_COMMITMENT_REQUIRED",
            "unjustified_date": "REJECT",
        },
        "milestones": {
            "outcome_gate": "SEPARATE_LAYER",
            "release": "SEPARATE_LAYER",
            "iteration": "SEPARATE_LAYER",
            "mapping": "EXPLICIT_REQUIRED",
        },
        "sequencing": {
            "order_by": [
                "BLOCKER",
                "GATE",
                "DEPENDENCY",
                "EXPLAINABLE_PRIORITY",
            ],
            "priority_override": "AUDIT_REQUIRED",
            "unaudited_override": "REJECT",
        },
        "critical_dependencies": {
            "classifications": [
                "ENABLER",
                "HIGH_FAN_OUT",
                "SINGLE_POINT_OF_FAILURE",
                "UNCERTAIN_DEPENDENCY",
            ],
            "uncertain_dependency": "RISK_BUFFER_REQUIRED",
            "unclassified_critical_dependency": "REJECT",
        },
    },
    "requirement_evidence": {
        "REQ-NATIVE-005": "test_req_native_005",
        "REQ-NATIVE-006": "test_req_native_006",
        "REQ-NATIVE-007": "test_req_native_007",
        "REQ-NATIVE-008": "test_req_native_008",
        "REQ-NATIVE-009": "test_req_native_009",
        "REQ-NATIVE-010": "test_req_native_0010",
        "REQ-PLN-001": "test_roadmap_horizons_outcomes_gates_and_date_exception",
        "REQ-PLN-002": "test_layered_milestones_gate_release_mapping",
        "REQ-PLN-003": "test_sequence_gates_dependencies_priority_override_audit",
        "REQ-PLN-004": (
            "test_critical_enablers_uncertain_dependencies_and_risk_buffers"
        ),
    },
}


def _finding_code(field: str) -> str:
    mappings = {
        "classic_descriptor": "CLASSIC_DESCRIPTOR_INVALID",
        "classic_matcher": "CLASSIC_MATCHER_INVALID",
        "robust_estimator": "ROBUST_ESTIMATOR_INVALID",
        "cog": "COG_INVALID",
        "native_stack": "NATIVE_STACK_INVALID",
        "native_io": "NATIVE_IO_INVALID",
        "roadmap": "ROADMAP_INVALID",
        "milestones": "MILESTONES_INVALID",
        "sequencing": "SEQUENCING_INVALID",
        "critical_dependencies": "CRITICAL_DEPENDENCIES_INVALID",
    }
    for control, code in mappings.items():
        if field.startswith(f"$.controls.{control}"):
            return code
    if field.startswith("$.requirement_evidence"):
        return "REQUIREMENT_EVIDENCE_INVALID"
    return "POLICY_STRUCTURE_INVALID"


def _compare(actual: object, expected: object, field: str) -> list[Finding]:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [Finding(_finding_code(field), field, "expected object")]
        findings: list[Finding] = []
        for key in sorted(actual.keys() - expected.keys()):
            findings.append(
                Finding("POLICY_STRUCTURE_INVALID", f"{field}.{key}", "unknown field")
            )
        for key in sorted(expected.keys() - actual.keys()):
            target = f"{field}.{key}"
            findings.append(Finding(_finding_code(target), target, "missing field"))
        for key in sorted(actual.keys() & expected.keys()):
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
