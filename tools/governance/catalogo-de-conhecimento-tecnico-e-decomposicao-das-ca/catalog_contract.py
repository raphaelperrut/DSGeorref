from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOC_ROOT = (
    ROOT
    / "docs/03-engineering/contexts/engineering_governance"
    / "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca"
)
CHECKPOINT_PATH = Path(__file__).with_name("foundation-checkpoint.json")
CATALOG_PATH = DOC_ROOT / "capability-catalog.json"
CATALOG_SCHEMA_PATH = DOC_ROOT / "capability-catalog.schema.json"
CORPUS_PATH = DOC_ROOT / "test-corpus-manifest.json"
CORPUS_SCHEMA_PATH = DOC_ROOT / "test-corpus-manifest.schema.json"
CONTRACT_PATH = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/contract-manifest.yaml"
)
COMMAND = (
    "python tools/governance/"
    "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/validate_catalog.py"
)
EXPECTED_OWNERS = {
    "dsgeorref.processing.geospatial_pipeline": {
        "module": "MOD-005",
        "bounded_contexts": ["BC-005", "BC-006", "BC-008"],
    },
    "dsgeorref.processing.strong_geometric_verifier": {
        "module": "MOD-006",
        "bounded_contexts": ["BC-007"],
    },
    "dsgeorref.processing.governed_ai_recovery": {
        "module": "MOD-007",
        "bounded_contexts": ["BC-009"],
    },
}
EXPECTED_LAYER_POLICY = {
    "UNIT_FIXTURE": ("DEVELOPMENT", "DEVELOPMENT"),
    "EXTERNAL_INTEGRATION": ("DEVELOPMENT", "DEVELOPMENT"),
    "PROTECTED_VALIDATION": ("VALIDATION_PROTECTED", "QA_PROTECTED"),
    "BLIND_HOLDOUT": ("HOLDOUT_BLIND", "INDEPENDENT_QA_BLIND"),
}
EXPECTED_SOURCES = {
    "contract": (
        "contracts/contexts/engineering_governance/fnd/"
        "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/contract-manifest.yaml"
    ),
    "catalog": (
        "docs/03-engineering/contexts/engineering_governance/"
        "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/capability-catalog.json"
    ),
    "catalog_schema": (
        "docs/03-engineering/contexts/engineering_governance/"
        "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/capability-catalog.schema.json"
    ),
    "corpus": (
        "docs/03-engineering/contexts/engineering_governance/"
        "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test-corpus-manifest.json"
    ),
    "corpus_schema": (
        "docs/03-engineering/contexts/engineering_governance/"
        "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/"
        "test-corpus-manifest.schema.json"
    ),
}
EXPECTED_FAILURE_POLICY = {
    "mode": "FAIL_CLOSED",
    "silent_fallback": False,
    "invalid_descriptor": "REJECT",
    "missing_corpus_evidence": "REJECT",
    "legacy_runtime_detected": "REJECT",
}
EXPECTED_CHECKPOINT_IDENTITY = {
    "checkpoint_id": "EPIC-006-CAPABILITY-CATALOG-FOUNDATION",
    "story_id": "STORY-0027",
    "issue_id": "ISSUE-0137",
    "task_id": "TASK-0027",
    "contract_version": "1.0.0",
}
EXPECTED_TESTS = {
    "test_reference_capability_inventory_no_code_import",
    "test_corpus_license_hash_split_and_access_integrity",
    "test_epic_006_fundacao",
}
EXPECTED_CRITERIA = {f"AC-ISSUE-0137-0{index}" for index in range(1, 5)}
