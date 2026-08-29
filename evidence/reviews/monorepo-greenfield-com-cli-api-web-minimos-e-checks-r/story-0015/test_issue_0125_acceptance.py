"""Executable acceptance evidence for ISSUE-0125.

The public entrypoints delegate to the frozen EPIC-003 and delivery-approval
suites. This module does not mint attestations or embed a candidate commit SHA.
"""

from __future__ import annotations

import runpy
import sys
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EPIC_TEST_ROOT = ROOT / (
    "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r"
)
DAA_SUITE = ROOT / (
    "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "test_delivery_approval_authority_contract.py"
)

CONTRACT_SUITE = EPIC_TEST_ROOT / "test_foundation_contract.py"
FOUNDATION_SUITE = EPIC_TEST_ROOT / "test_foundation.py"
AUTOMATION_SUITE = EPIC_TEST_ROOT / "test_automation.py"
INTEGRATION_SUITE = EPIC_TEST_ROOT / "test_integration.py"


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


def test_epic_003_aceite_happy_path() -> None:
    """Prove the frozen contract, foundation, automation and integration."""

    _run(CONTRACT_SUITE, "test_epic_003_contrato")
    _run(FOUNDATION_SUITE, "test_epic_003_fundacao")
    _run(AUTOMATION_SUITE, "test_epic_003_automacao")
    _run(INTEGRATION_SUITE, "test_epic_003_integracao")
    _run(DAA_SUITE, "test_delivery_approval_authority_contract")


def test_epic_003_aceite_negative_paths() -> None:
    """Prove applicable deterministic failures without reimplementing them."""

    _run(
        CONTRACT_SUITE,
        "test_foundation_contract_rejects_silent_fallback_and_duplicate_authority",
    )
    _run(FOUNDATION_SUITE, "test_foundation_rejects_contract_drift_and_silent_fallback")
    _run(FOUNDATION_SUITE, "test_validator_cli_is_deterministic_and_fails_closed")
    _run(AUTOMATION_SUITE, "test_epic_003_automacao")
    _run(INTEGRATION_SUITE, "test_epic_003_integracao")
    _run(DAA_SUITE, "test_delivery_approval_authority_fail_closed")
