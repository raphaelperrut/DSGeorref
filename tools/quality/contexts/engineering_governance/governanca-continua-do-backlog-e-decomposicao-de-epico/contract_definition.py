from __future__ import annotations

from pathlib import Path

CONTRACT_REL = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico"
)
MANIFEST_REL = CONTRACT_REL / "contract-manifest.yaml"
SCHEMA_REL = CONTRACT_REL / "backlog-governance-profile.schema.json"
EXAMPLE_REL = CONTRACT_REL / "examples/backlog-governance-profile.json"

EXPECTED_IDENTITY = {
    "epic_id": "EPIC-110",
    "story_id": "STORY-0683",
    "issue_id": "ISSUE-0793",
    "github_issue": 68,
    "task_id": "TASK-0683",
}
EXPECTED_REQUIREMENTS = {
    "REQ-ISM-004": {
        "control": "/controls/portfolio_catalog",
        "test": "test_versioned_issue_portfolio_catalog_github_reconciliation",
    },
    "REQ-ISS-002": {
        "control": "/controls/forecast",
        "test": "test_issue_forecast_min_mode_max_confidence_and_snapshot_variance",
    },
    "REQ-PLN-009": {
        "control": "/controls/integration_checkpoint",
        "test": "test_cross_domain_contract_checkpoint_and_walking_skeleton_integration",
    },
    "REQ-PRJ-004": {
        "control": "/controls/workflow",
        "test": "test_canonical_workflow_transitions",
    },
    "REQ-SPRINT-001-004": {
        "control": "/controls/foundation_boundaries",
        "test": "test_epic_110_contrato",
    },
}
