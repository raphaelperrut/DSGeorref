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


def _candidate_sha() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def test_epic_092_fundacao() -> None:
    candidate_sha = _candidate_sha()
    completed = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(TOOL_PATH),
            "--candidate-sha",
            candidate_sha,
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
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
    execution_evidence = report["execution_evidence"]
    assert execution_evidence["candidate_sha_before"] == candidate_sha
    assert execution_evidence["candidate_sha_after"] == candidate_sha
    assert execution_evidence["tests"] == TOOL.EXPECTED_REQUIRED_TESTS
    assert execution_evidence["command"][-len(TOOL.EXPECTED_REQUIRED_TESTS) :] == (
        TOOL.EXPECTED_REQUIRED_TESTS
    )
    assert execution_evidence["exit_code"] == 0
    assert execution_evidence["status"] == "PASS"
    assert report["requirement_evidence"]["REQ-FRZ-004"] == TOOL.FOUNDATION_CLOSURE_TEST
    assert report["requirement_evidence"]["REQ-GOV-005"] == TOOL.SPRINT_EVIDENCE_TEST

    checkpoint = TOOL.validate_checkpoint(ROOT)
    assert checkpoint["local_command"] == checkpoint["ci_command"]
    assert TOOL.validate_ci_integration(ROOT)["command"] == checkpoint["local_command"]

def test_error_paths_are_fail_closed_without_silent_fallback(tmp_path: Path) -> None:
    contract = TOOL.validate_contract(ROOT)
    TOOL.validate_registry(ROOT, contract=contract)
    assert contract["failure_policy"]["silent_fallback"] is False

    candidate_sha = _candidate_sha()
    passing_test = tmp_path / "test_passing_execution.py"
    passing_test.write_text("def test_passes():\n    assert True\n", encoding="utf-8")
    passing_registry = {
        "required_tests": [str(passing_test)],
        "required_result": "PASS",
    }
    valid = TOOL.capture_test_execution(
        ROOT,
        candidate_sha=candidate_sha,
        registry=passing_registry,
    )
    assert valid["exit_code"] == 0
    assert TOOL.validate_execution_evidence(
        valid,
        candidate_sha=candidate_sha,
        registry=passing_registry,
    )["status"] == "PASS"
    with pytest.raises(TOOL.FoundationValidationError, match="must be an object"):
        TOOL.validate_execution_evidence(
            None,
            candidate_sha=candidate_sha,
            registry=passing_registry,
        )

    failing_test = tmp_path / "test_failing_execution.py"
    failing_test.write_text("def test_fails():\n    assert False\n", encoding="utf-8")
    failing_registry = {
        "required_tests": [str(failing_test)],
        "required_result": "PASS",
    }
    with pytest.raises(TOOL.FoundationValidationError, match="result is unsuccessful"):
        TOOL.execute_registered_tests(
            ROOT,
            candidate_sha=candidate_sha,
            registry=failing_registry,
        )

    stale = copy.deepcopy(valid)
    stale["candidate_sha_after"] = "0" * 40
    with pytest.raises(TOOL.FoundationValidationError, match="execution evidence is stale"):
        TOOL.validate_execution_evidence(
            stale, candidate_sha=candidate_sha, registry=passing_registry
        )

    conflicting = copy.deepcopy(valid)
    conflicting["tests"].append(conflicting["tests"][0])
    with pytest.raises(TOOL.FoundationValidationError, match="evidence is conflicting"):
        TOOL.validate_execution_evidence(
            conflicting, candidate_sha=candidate_sha, registry=passing_registry
        )

    incompatible = copy.deepcopy(valid)
    incompatible["tests"][0] = "unregistered-test"
    with pytest.raises(TOOL.FoundationValidationError, match="evidence is incompatible"):
        TOOL.validate_execution_evidence(
            incompatible, candidate_sha=candidate_sha, registry=passing_registry
        )

    missing = copy.deepcopy(valid)
    missing["tests"].pop()
    with pytest.raises(TOOL.FoundationValidationError, match="evidence is missing"):
        TOOL.validate_execution_evidence(
            missing, candidate_sha=candidate_sha, registry=passing_registry
        )

    stale_candidate = copy.deepcopy(valid)
    stale_candidate["candidate_sha_before"] = "0" * 40
    with pytest.raises(TOOL.FoundationValidationError, match="evidence is stale"):
        TOOL.validate_execution_evidence(
            stale_candidate, candidate_sha=candidate_sha, registry=passing_registry
        )

    execution_command_drift = copy.deepcopy(valid)
    execution_command_drift["command"].append("--collect-only")
    with pytest.raises(TOOL.FoundationValidationError, match="execution command diverges"):
        TOOL.validate_execution_evidence(
            execution_command_drift,
            candidate_sha=candidate_sha,
            registry=passing_registry,
        )

    with pytest.raises(TOOL.FoundationValidationError, match="does not match repository HEAD"):
        TOOL.validate_foundation(
            ROOT,
            candidate_sha="0" * 40,
        )

    checkpoint = TOOL.validate_checkpoint(ROOT, contract=contract)

    command_drift = copy.deepcopy(checkpoint)
    command_drift["ci_command"] = "implicit-ci-fallback"
    with pytest.raises(TOOL.FoundationValidationError, match="commands diverge"):
        TOOL._validate_checkpoint_document(command_drift, contract)

    unsafe_claim = copy.deepcopy(checkpoint)
    unsafe_claim["authorization_claim"] = "AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE"
    with pytest.raises(TOOL.FoundationValidationError, match="unsafe authorization claim"):
        TOOL._validate_checkpoint_document(unsafe_claim, contract)
