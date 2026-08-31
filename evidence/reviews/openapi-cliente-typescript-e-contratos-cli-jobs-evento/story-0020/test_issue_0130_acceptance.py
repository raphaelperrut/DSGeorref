"""Executable acceptance evidence for ISSUE-0130.

The public entrypoints delegate to the existing EPIC-004 and delivery-approval
suites. This module does not copy contract rules, mint attestations, or embed a
candidate commit SHA.
"""

from __future__ import annotations

import runpy
import sys
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EPIC_TEST_ROOT = ROOT / (
    "tests/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento"
)
INTEGRATION_SUITE = ROOT / (
    "tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/"
    "test_repository_integration.py"
)
DAA_SUITE = ROOT / (
    "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "test_delivery_approval_authority_contract.py"
)

CONTRACT_SUITE = EPIC_TEST_ROOT / "test_contract_foundation.py"
RUNTIME_SCHEMA_SUITE = EPIC_TEST_ROOT / "test_runtime_schema_contract.py"
AUTOMATION_SUITE = EPIC_TEST_ROOT / "test_automation.py"


@lru_cache(maxsize=None)
def _suite(path: Path) -> dict[str, object]:
    original_path = tuple(sys.path)
    try:
        sys.path.insert(0, str(path.parent))
        return runpy.run_path(str(path))
    finally:
        sys.path[:] = original_path


def _run(path: Path, entrypoint: str) -> None:
    candidate = _suite(path).get(entrypoint)
    assert isinstance(candidate, Callable), f"missing governed entrypoint: {entrypoint}"
    candidate()


def test_epic_004_aceite_happy_path() -> None:
    """Prove the public contracts, generated client controls and integration."""

    _run(CONTRACT_SUITE, "test_generated_client_component_accessibility_e2e")
    _run(CONTRACT_SUITE, "test_req_run_008")
    _run(RUNTIME_SCHEMA_SUITE, "test_fastapi_openapi_contract")
    _run(RUNTIME_SCHEMA_SUITE, "test_cli_api_semantic_contract")
    _run(RUNTIME_SCHEMA_SUITE, "test_no_duplicate_modes_processing_plan_roundtrip")
    _run(INTEGRATION_SUITE, "test_epic_004_integracao")
    _run(DAA_SUITE, "test_delivery_approval_authority_contract")


def test_epic_004_aceite_negative_paths() -> None:
    """Prove applicable deterministic failures without reimplementing them."""

    _run(CONTRACT_SUITE, "test_profile_rejects_missing_or_unknown_control")
    _run(
        RUNTIME_SCHEMA_SUITE,
        (
            "test_versioned_schema_registry_reader_writer_compatibility_window_"
            "and_unknown_major_rejection"
        ),
    )
    _run(
        RUNTIME_SCHEMA_SUITE,
        "test_profile_rejects_missing_unknown_or_permissive_control",
    )
    _run(AUTOMATION_SUITE, "test_epic_004_automacao")
    _run(
        INTEGRATION_SUITE,
        "test_integration_rejects_failed_or_malformed_quality_report",
    )
    _run(DAA_SUITE, "test_delivery_approval_authority_fail_closed")
