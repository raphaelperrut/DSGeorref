from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[3]
SLUG = "fechamento-da-sprint-001-e-autorizacao-da-primeira-fat"
TOOL_PATH = ROOT / "tools/governance" / SLUG / "foundation_validation.py"


def _load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "sprint_001_foundation_validation", TOOL_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TOOL = _load_tool()


def test_epic_092_fundacao() -> None:
    report = TOOL.validate_foundation(ROOT)
    assert report["decision"] == "PASS"
    assert report["reviewable_state"] == "READY_FOR_INDEPENDENT_REVIEW"
    assert report["authorization_claim"] == "NOT_ASSERTED_BY_FOUNDATION"
    assert set(report["requirement_evidence"]) == {
        "REQ-DEV-001",
        "REQ-FRZ-001",
        "REQ-FRZ-002",
        "REQ-FRZ-003",
        "REQ-FRZ-004",
        "REQ-GOV-005",
    }
    assert report["acceptance_evidence"] == TOOL.EXPECTED_AC_EVIDENCE

    checkpoint = TOOL.validate_checkpoint(ROOT)
    assert checkpoint["local_command"] == checkpoint["ci_command"]
    assert TOOL.validate_ci_integration(ROOT)["command"] == checkpoint["local_command"]

    completed = subprocess.run(
        [sys.executable, "-X", "utf8", str(TOOL_PATH)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["decision"] == "PASS"


def test_error_paths_are_fail_closed_without_silent_fallback() -> None:
    contract = TOOL.validate_contract(ROOT)
    registry = TOOL.validate_registry(ROOT, contract=contract)
    assert contract["failure_policy"]["silent_fallback"] is False

    missing = copy.deepcopy(registry)
    del missing["requirement_evidence"]["REQ-FRZ-004"]
    with pytest.raises(TOOL.FoundationValidationError, match="requirement evidence diverges"):
        TOOL._validate_registry_document(missing, contract)

    stale = copy.deepcopy(registry)
    stale["evidence_policy"]["candidate_sha_binding"] = "LATEST"
    with pytest.raises(TOOL.FoundationValidationError, match="evidence policy diverges"):
        TOOL._validate_registry_document(stale, contract)

    conflicting = copy.deepcopy(registry)
    conflicting["required_tests"] = list(reversed(conflicting["required_tests"]))
    with pytest.raises(TOOL.FoundationValidationError, match="required test registry diverges"):
        TOOL._validate_registry_document(conflicting, contract)

    checkpoint = TOOL.validate_checkpoint(ROOT, contract=contract)

    command_drift = copy.deepcopy(checkpoint)
    command_drift["ci_command"] = "implicit-ci-fallback"
    with pytest.raises(TOOL.FoundationValidationError, match="commands diverge"):
        TOOL._validate_checkpoint_document(command_drift, contract)

    unsafe_claim = copy.deepcopy(checkpoint)
    unsafe_claim["authorization_claim"] = "AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE"
    with pytest.raises(TOOL.FoundationValidationError, match="unsafe authorization claim"):
        TOOL._validate_checkpoint_document(unsafe_claim, contract)
