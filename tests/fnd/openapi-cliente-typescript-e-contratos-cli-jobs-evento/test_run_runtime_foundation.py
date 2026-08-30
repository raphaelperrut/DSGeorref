from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from functools import cache
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
TOOL_ROOT = ROOT / (
    "tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/"
    "run-runtime-parte-2"
)
CHECKPOINT_PATH = TOOL_ROOT / "runtime-foundation-checkpoint.json"
VALIDATOR_PATH = TOOL_ROOT / "validate_runtime_foundation.py"
TASK_PATH = ROOT / ".codex/tasks/TASK-0704.json"


@cache
def _validator_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_runtime_foundation", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@cache
def _checkpoint() -> dict[str, Any]:
    loaded = json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _assert_valid(checkpoint: dict[str, Any] | None = None) -> None:
    candidate = _checkpoint() if checkpoint is None else checkpoint
    assert _validator_module().validate_checkpoint(candidate, ROOT) == []


def _assert_control_rejected(control: str, field: str, value: object) -> None:
    invalid = copy.deepcopy(_checkpoint())
    invalid["controls"][control][field] = value
    errors = _validator_module().validate_checkpoint(invalid, ROOT)
    assert any(error.startswith(f"controls.{control}") for error in errors)


def test_req_run_002() -> None:
    control = _checkpoint()["controls"]["domain_io_boundary"]
    assert control["domain_core"] == "SYNCHRONOUS"
    assert control["asynchronous_io"] == "BOUNDARIES_ONLY"
    assert control["asynchronous_domain_core"] == "REJECT"
    _assert_control_rejected("domain_io_boundary", "asynchronous_io", "DOMAIN_CORE")


def test_req_run_003() -> None:
    control = _checkpoint()["controls"]["composition"]
    assert control == {
        "composition_roots": "EXPLICIT",
        "dependency_injection": "CONSTRUCTOR",
        "implicit_composition": "REJECT",
    }
    _assert_control_rejected("composition", "dependency_injection", "GLOBAL")


def test_req_run_004() -> None:
    control = _checkpoint()["controls"]["settings"]
    assert control["typing"] == "TYPED"
    assert control["sources"] == "STRATIFIED"
    assert control["required_values"] == "FAIL_CLOSED"
    _assert_control_rejected("settings", "required_values", "BEST_EFFORT")


def test_req_run_005() -> None:
    control = _checkpoint()["controls"]["command_transactions"]
    assert control["unit_of_work"] == "EXPLICIT"
    assert control["transactions"] == "SHORT"
    assert control["implicit_or_long_transaction"] == "REJECT"
    _assert_control_rejected("command_transactions", "transactions", "UNBOUNDED")


def test_req_run_007() -> None:
    control = _checkpoint()["controls"]["repeatable_mutations"]
    assert control == {
        "idempotency": "PERSISTENT",
        "volatile_idempotency": "REJECT",
    }
    _assert_control_rejected("repeatable_mutations", "idempotency", "IN_MEMORY")


def test_req_run_009() -> None:
    control = _checkpoint()["controls"]["logging"]
    assert control["envelope"] == "STRUCTURED"
    assert control["correlation_ids"] == "REQUIRED"
    assert control["redaction"] == "CENTRALIZED"
    _assert_control_rejected("logging", "redaction", "LOCAL_OPTIONAL")


def test_runtime_decision_1() -> None:
    control = _checkpoint()["controls"]["application_boundaries"]
    assert control["namespace"] == "dsgeorref"
    assert control["application_services"] == "SHARED"
    assert control["surfaces"] == {
        "cli": "THIN_ADAPTER",
        "api": "THIN_ADAPTER",
        "worker": "THIN_ADAPTER",
    }
    _assert_control_rejected("application_boundaries", "namespace", "issue_0814")


def test_runtime_decision_2() -> None:
    test_req_run_002()
    _assert_control_rejected("domain_io_boundary", "domain_core", "ASYNC_FRAMEWORK")


def test_runtime_decision_3() -> None:
    test_req_run_003()
    test_req_run_004()
    _assert_control_rejected("composition", "implicit_composition", "ALLOW")
    _assert_control_rejected("settings", "missing_required_value", "DEFAULT_SILENTLY")


def test_runtime_decision_4() -> None:
    state = _checkpoint()["controls"]["state_authority"]
    errors = _checkpoint()["controls"]["domain_errors"]
    assert state["system_of_record"] == "POSTGRESQL_POSTGIS"
    assert state["broker"] == "TRANSPORT_ONLY"
    assert errors["typed"] == "REQUIRED"
    assert errors["unmapped_error"] == "REJECT"
    _assert_control_rejected("state_authority", "broker", "STATE_AUTHORITY")
    _assert_control_rejected("domain_errors", "unmapped_error", "FALLBACK_500")


def test_checkpoint_rejects_missing_or_unknown_control() -> None:
    missing = copy.deepcopy(_checkpoint())
    del missing["controls"]["settings"]
    assert any(
        error.startswith("controls fields:")
        for error in _validator_module().validate_checkpoint(missing, ROOT)
    )
    unknown = copy.deepcopy(_checkpoint())
    unknown["controls"]["silent_fallback"] = {"enabled": True}
    assert any(
        error.startswith("controls fields:")
        for error in _validator_module().validate_checkpoint(unknown, ROOT)
    )


def test_checkpoint_binds_frozen_contracts_and_dependency() -> None:
    invalid_digest = copy.deepcopy(_checkpoint())
    invalid_digest["canonical_contracts"]["foundation_profile"]["sha256"] = "0" * 64
    errors = _validator_module().validate_checkpoint(invalid_digest, ROOT)
    assert any(error.startswith("canonical_contracts:") for error in errors)

    invalid_dependency = copy.deepcopy(_checkpoint())
    invalid_dependency["dependency"]["eligible_story"] = "STORY-UNKNOWN"
    errors = _validator_module().validate_checkpoint(invalid_dependency, ROOT)
    assert any(error.startswith("dependency:") for error in errors)


def test_requirements_and_task_envelope_are_contained() -> None:
    requirement_map = {
        item["id"]: item["test"] for item in _checkpoint()["requirements"]
    }
    assert requirement_map == _validator_module().REQUIREMENT_TESTS
    task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    allow_paths = task["allow_paths"]
    assert ".codex/tasks/TASK-0704.json" not in allow_paths
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in allow_paths
    assert (
        "evidence/implementation/openapi-cliente-typescript-e-contratos-cli-jobs-ev/"
        "run-runtime-parte-2/IMPLEMENTATION_EVIDENCE.yaml"
        in allow_paths
    )
    assert allow_paths == task["phase_f_review"]["files"]["allow_paths"]


def test_checkpoint_cli_reports_pass() -> None:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--repo-root", str(ROOT)],
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout) == {"status": "PASS", "errors": []}


def test_checkpoint_cli_fails_closed_for_unreadable_input() -> None:
    missing = CHECKPOINT_PATH.with_name("missing-checkpoint.json")
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), str(missing), "--repo-root", str(ROOT)],
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    assert completed.returncode == 1
    report = json.loads(completed.stdout)
    assert report["status"] == "FAIL"
    assert report["errors"][0].startswith("checkpoint: unreadable or invalid:")
