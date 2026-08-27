"""Executable acceptance evidence for ISSUE-0120.

The public entrypoints delegate to the frozen EPIC-002 and delivery-approval
suites. This module does not mint attestations or embed a candidate commit SHA.
"""

from __future__ import annotations

import runpy
import sys
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EPIC_TEST_ROOT = (
    ROOT / "tests/fnd/repositorio-privado-project-central-views-campos-label"
)
CONSOLIDATION_ROOT = ROOT / (
    "tools/governance/repositorio-privado-project-central-views-campos-label/"
    "consolidacao"
)
DAA_SUITE = ROOT / (
    "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "test_delivery_approval_authority_contract.py"
)

CONTRACT_SUITE = EPIC_TEST_ROOT / "test_slice_consolidation.py"
CONSOLIDATION_SUITE = CONSOLIDATION_ROOT / "test_slice_consolidation.py"
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


def test_epic_002_aceite_happy_path() -> None:
    """Prove the frozen contract, consolidation, automation and integration."""

    _run(CONTRACT_SUITE, "test_story_0006_slice_consolidation")
    _run(CONSOLIDATION_SUITE, "test_story_0007_slice_consolidation")
    _run(AUTOMATION_SUITE, "test_epic_002_automacao")
    _run(INTEGRATION_SUITE, "test_epic_002_integracao")
    _run(DAA_SUITE, "test_delivery_approval_authority_contract")


def test_epic_002_aceite_negative_paths() -> None:
    """Prove applicable deterministic failures without reimplementing them."""

    _run(CONTRACT_SUITE, "test_consolidation_rejects_implicit_or_self_release")
    for entrypoint in (
        "test_consolidation_rejects_invalid_candidate_revision",
        "test_consolidation_requires_all_governed_slice_completions",
        "test_consolidation_preserves_canonical_completion_failures",
        "test_consolidation_requires_independent_reviewer",
        "test_consolidation_rejects_empty_identity",
        "test_consolidation_rejects_whitespace_identity",
        "test_consolidation_rejects_same_normalized_identity",
        "test_consolidation_rejects_review_for_another_candidate",
        "test_consolidation_does_not_self_release_without_review",
    ):
        _run(CONSOLIDATION_SUITE, entrypoint)
    _run(AUTOMATION_SUITE, "test_epic_002_automacao")
    _run(INTEGRATION_SUITE, "test_epic_002_integracao")
    _run(DAA_SUITE, "test_delivery_approval_authority_fail_closed")
