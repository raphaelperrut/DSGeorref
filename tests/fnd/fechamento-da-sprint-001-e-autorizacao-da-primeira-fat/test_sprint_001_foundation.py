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


def _execution_evidence(candidate_sha: str) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "candidate_sha": candidate_sha,
        "results": [
            {"test": test, "candidate_sha": candidate_sha, "result": "PASS"}
            for test in TOOL.EXPECTED_REQUIRED_TESTS
        ],
    }


def test_epic_092_fundacao(tmp_path: Path) -> None:
    candidate_sha = _candidate_sha()
    execution_evidence = _execution_evidence(candidate_sha)
    report = TOOL.validate_foundation(
        ROOT,
        candidate_sha=candidate_sha,
        execution_evidence=execution_evidence,
    )
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
    assert report["execution_evidence"] == {
        "candidate_sha": candidate_sha,
        "result_count": len(TOOL.EXPECTED_REQUIRED_TESTS),
        "status": "PASS",
    }
    assert report["requirement_evidence"]["REQ-FRZ-004"] == TOOL.FOUNDATION_CLOSURE_TEST
    assert report["requirement_evidence"]["REQ-GOV-005"] == TOOL.SPRINT_EVIDENCE_TEST

    checkpoint = TOOL.validate_checkpoint(ROOT)
    assert checkpoint["local_command"] == checkpoint["ci_command"]
    assert TOOL.validate_ci_integration(ROOT)["command"] == checkpoint["local_command"]

    evidence_path = tmp_path / "execution-evidence.json"
    evidence_path.write_text(json.dumps(execution_evidence), encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(TOOL_PATH),
            "--candidate-sha",
            candidate_sha,
            "--evidence",
            str(evidence_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["decision"] == "PASS"


def test_error_paths_are_fail_closed_without_silent_fallback(tmp_path: Path) -> None:
    contract = TOOL.validate_contract(ROOT)
    registry = TOOL.validate_registry(ROOT, contract=contract)
    assert contract["failure_policy"]["silent_fallback"] is False

    candidate_sha = _candidate_sha()
    valid = _execution_evidence(candidate_sha)

    unsuccessful = copy.deepcopy(valid)
    unsuccessful["results"][0]["result"] = "FAIL"
    with pytest.raises(TOOL.FoundationValidationError, match="result is unsuccessful"):
        TOOL.validate_execution_evidence(
            unsuccessful, candidate_sha=candidate_sha, registry=registry
        )
    failed_path = tmp_path / "failed-execution-evidence.json"
    failed_path.write_text(json.dumps(unsuccessful), encoding="utf-8")
    failed_cli = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(TOOL_PATH),
            "--candidate-sha",
            candidate_sha,
            "--evidence",
            str(failed_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert failed_cli.returncode == 1
    assert json.loads(failed_cli.stdout)["decision"] == "FAIL"

    stale = copy.deepcopy(valid)
    stale["results"][0]["candidate_sha"] = "0" * 40
    with pytest.raises(TOOL.FoundationValidationError, match="test evidence is stale"):
        TOOL.validate_execution_evidence(stale, candidate_sha=candidate_sha, registry=registry)

    conflicting = copy.deepcopy(valid)
    conflicting["results"].append(copy.deepcopy(conflicting["results"][0]))
    with pytest.raises(TOOL.FoundationValidationError, match="evidence is conflicting"):
        TOOL.validate_execution_evidence(
            conflicting, candidate_sha=candidate_sha, registry=registry
        )

    incompatible = copy.deepcopy(valid)
    incompatible["results"][0]["test"] = "unregistered-test"
    with pytest.raises(TOOL.FoundationValidationError, match="evidence is incompatible"):
        TOOL.validate_execution_evidence(
            incompatible, candidate_sha=candidate_sha, registry=registry
        )

    missing = copy.deepcopy(valid)
    missing["results"].pop()
    with pytest.raises(TOOL.FoundationValidationError, match="evidence is missing"):
        TOOL.validate_execution_evidence(missing, candidate_sha=candidate_sha, registry=registry)

    stale_candidate = copy.deepcopy(valid)
    stale_candidate["candidate_sha"] = "0" * 40
    with pytest.raises(TOOL.FoundationValidationError, match="evidence is stale"):
        TOOL.validate_execution_evidence(
            stale_candidate, candidate_sha=candidate_sha, registry=registry
        )

    arbitrary_candidate = _execution_evidence("0" * 40)
    with pytest.raises(TOOL.FoundationValidationError, match="does not match repository HEAD"):
        TOOL.validate_foundation(
            ROOT,
            candidate_sha="0" * 40,
            execution_evidence=arbitrary_candidate,
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
