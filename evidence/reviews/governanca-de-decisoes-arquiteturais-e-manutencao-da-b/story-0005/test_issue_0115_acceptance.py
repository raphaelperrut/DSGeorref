"""Executable acceptance evidence for ISSUE-0115.

The two public entrypoints deliberately delegate to the frozen EPIC-001 suites.
This module does not mint delivery attestations or embed a candidate commit SHA.
The Delivery Approval Authority receives the expected candidate SHA from its
calling gate and verifies it against the signed evidence at verification time.
"""

from __future__ import annotations

import runpy
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EPIC_TEST_ROOT = (
    ROOT
    / "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b"
)

CONTRACT_SUITE = EPIC_TEST_ROOT / "test_contract.py"
AUTOMATION_SUITE = EPIC_TEST_ROOT / "test_automation.py"
INTEGRATION_SUITE = EPIC_TEST_ROOT / "test_integration.py"
DAA_SUITE = EPIC_TEST_ROOT / "test_delivery_approval_authority_contract.py"


@lru_cache(maxsize=None)
def _suite(path: Path) -> dict[str, object]:
    return runpy.run_path(str(path))


def _run(path: Path, entrypoint: str) -> None:
    candidate = _suite(path).get(entrypoint)
    assert isinstance(candidate, Callable), f"missing governed entrypoint: {entrypoint}"
    candidate()


def test_epic_001_aceite_happy_path() -> None:
    """Prove the frozen contract, automation, integration and DAA golden path."""

    _run(CONTRACT_SUITE, "test_epic_001_contrato")
    _run(AUTOMATION_SUITE, "test_epic_001_automacao")
    _run(INTEGRATION_SUITE, "test_epic_001_integracao")
    _run(DAA_SUITE, "test_delivery_approval_authority_contract")


def test_epic_001_aceite_negative_paths() -> None:
    """Prove deterministic fail-closed behavior without reimplementing it."""

    _run(CONTRACT_SUITE, "test_epic_001_contrato")
    _run(AUTOMATION_SUITE, "test_epic_001_automacao")
    _run(INTEGRATION_SUITE, "test_epic_001_integracao")
    _run(DAA_SUITE, "test_delivery_approval_authority_fail_closed")
