from __future__ import annotations

from pathlib import Path


EXPECTED_VERSION = "1.0.0"
CONTRACT_REL = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "governanca-de-decisoes-arquiteturais-e-manutencao-da-b"
)
MANIFEST_REL = CONTRACT_REL / "contract-manifest.yaml"
OWNERSHIP_REL = Path("contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv")
EXPECTED_CONTRACTS = {
    "foundation-boundaries": {
        "schema": CONTRACT_REL / "foundation-boundaries.schema.json",
        "example": CONTRACT_REL / "examples/foundation-boundaries.json",
        "requirement": "REQ-SPRINT-001-004",
        "invariants": {
            "CORE_API_AND_RUNNERS_ARE_DISTINCT_BOUNDARIES",
            "BOUNDARIES_ARE_DECLARATIVE_ONLY_IN_THIS_STORY",
        },
        "failure_modes": {
            "REQUIRED_FIELD_MISSING",
            "BOUNDARY_MISSING",
            "BOUNDARY_COLLAPSED",
            "RUNTIME_MATERIALIZATION_ATTEMPTED",
            "UNKNOWN_PROPERTY",
        },
    },
    "issue-forecast": {
        "schema": CONTRACT_REL / "issue-forecast.schema.json",
        "example": CONTRACT_REL / "examples/issue-forecast.json",
        "requirement": "REQ-ISS-002",
        "invariants": {
            "MINIMUM_LE_MODE_LE_MAXIMUM",
            "CONFIDENCE_IS_EXPLICIT",
            "VARIANCE_REFERENCES_THE_DECLARED_VERSIONED_SNAPSHOT",
        },
        "failure_modes": {
            "REQUIRED_FIELD_MISSING",
            "INVALID_INTERVAL_ORDER",
            "SNAPSHOT_VARIANCE_MISMATCH",
            "UNKNOWN_PROPERTY",
        },
    },
    "portfolio-snapshot": {
        "schema": CONTRACT_REL / "portfolio-snapshot.schema.json",
        "example": CONTRACT_REL / "examples/portfolio-snapshot.json",
        "requirement": "REQ-ISM-004",
        "invariants": {
            "STABLE_ID_IS_INDEPENDENT_FROM_GITHUB_ISSUE_NUMBER",
            "BOTH_REPOSITORY_AND_GITHUB_SIDES_ARE_IDENTIFIED",
            "RECONCILIATION_IS_ONE_TO_ONE_AND_COMPLETE",
        },
        "failure_modes": {
            "REQUIRED_FIELD_MISSING",
            "MISSING_RECONCILIATION_SIDE",
            "INCONSISTENT_RECONCILIATION",
            "UNKNOWN_PROPERTY",
        },
    },
}
