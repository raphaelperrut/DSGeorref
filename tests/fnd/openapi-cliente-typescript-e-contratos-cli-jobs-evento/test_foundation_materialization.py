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
TOOL_ROOT = (
    ROOT
    / "tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento"
    / "artlayout-dbschema-fs1-parte-1"
)
CHECKPOINT_PATH = TOOL_ROOT / "foundation-checkpoint.json"
VALIDATOR_PATH = TOOL_ROOT / "validate_foundation.py"
TASK_PATH = ROOT / ".codex/tasks/TASK-0703.json"


@cache
def _validator_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("foundation_materialization", VALIDATOR_PATH)
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
    assert any(error.startswith(f"controls.{control}:") for error in errors)


def test_req_artlayout_0010() -> None:
    control = _checkpoint()["controls"]["artifact_serving"]
    assert control == {
        "authorization": "REQUIRED",
        "locator_resolution": "SAFE_REGISTERED_ROOT_ONLY",
        "unauthorized_or_unsafe": "REJECT",
    }
    _assert_valid()
    _assert_control_rejected("artifact_serving", "authorization", "OPTIONAL")
    _assert_control_rejected("artifact_serving", "unauthorized_or_unsafe", "WARN")


def test_req_dbschema_002() -> None:
    control = _checkpoint()["controls"]["identity"]
    assert control["logical_id"] == "UUIDV7_APPLICATION_GENERATED"
    assert control["stable"] is True
    assert control["ordered_when_required"] is True
    assert control["invalid_id"] == "REJECT"
    _assert_control_rejected("identity", "logical_id", "RANDOM_STRING")


def test_req_dbschema_004() -> None:
    control = _checkpoint()["controls"]["time_and_concurrency"]
    assert control == {
        "timestamp": "TIMESTAMPTZ",
        "locking": "OPTIMISTIC_REVISION_OR_EXPLICIT_LOCK",
        "concurrency_policy": "EXPLICIT",
        "implicit_last_write_wins": "REJECT",
    }
    _assert_control_rejected(
        "time_and_concurrency", "implicit_last_write_wins", "ACCEPT"
    )


def test_first_functional_slice_decision_02() -> None:
    control = _checkpoint()["controls"]["local_inputs"]
    assert control["source"] == "LOCAL_AUTHORIZED_REGISTERED_ROOT"
    assert control["locator"] == "RELATIVE_OPAQUE"
    assert control["root_escape"] == "REJECT"
    _assert_control_rejected("local_inputs", "source", "ARBITRARY_HOST_PATH")


def test_first_functional_slice_decision_03() -> None:
    control = _checkpoint()["controls"]["ingestion"]
    assert control == {
        "originals": "IMMUTABLE",
        "sha256": "REQUIRED",
        "source_identity": "REQUIRED",
        "metadata": "REQUIRED",
        "invalid_or_incomplete": "REJECT",
    }
    _assert_control_rejected("ingestion", "sha256", "OPTIONAL")
    _assert_control_rejected("ingestion", "invalid_or_incomplete", "BEST_EFFORT")


def test_first_functional_slice_decision_05() -> None:
    control = _checkpoint()["controls"]["classic_pipeline"]
    assert control["execution_order"] == "CLASSIC_BEFORE_OPTIONAL_AI"
    assert control["deterministic"] is True
    assert control["replaceable"] is True
    assert control["correspondence_audit"] == "REQUIRED"
    _assert_control_rejected("classic_pipeline", "deterministic", False)
    _assert_control_rejected("classic_pipeline", "untracked_correspondence", "ACCEPT")


def test_first_functional_slice_decision_07() -> None:
    control = _checkpoint()["controls"]["sgv"]
    assert control["mandatory"] is True
    assert control["verdicts"] == ["accepted", "reviewable", "rejected"]
    assert control["hard_gate_override"] == "PROHIBITED"
    _assert_control_rejected("sgv", "mandatory", False)
    _assert_control_rejected("sgv", "hard_gate_override", "ALLOWED")


def test_first_functional_slice_decision_08() -> None:
    control = _checkpoint()["controls"]["artifact_set"]
    assert control["immutable"] is True
    assert control["required_kinds"] == [
        "COG_RASTER",
        "PROVENANCE_MANIFEST",
        "QUALITY_REPORT",
    ]
    assert control["publication"] == "ATOMIC_AFTER_SGV_ACCEPTED"
    assert control["partial_or_nonaccepted"] == "REJECT"
    _assert_control_rejected("artifact_set", "immutable", False)
    _assert_control_rejected("artifact_set", "partial_or_nonaccepted", "PUBLISH")


def test_first_functional_slice_decision_09() -> None:
    control = _checkpoint()["controls"]["shared_core"]
    assert control["application_services"] == "SHARED"
    assert control["surfaces"] == ["REST", "CLI", "DIRECT_RUNNER", "CELERY"]
    assert control["semantic_equivalence"] == "REQUIRED"
    _assert_control_rejected("shared_core", "surfaces", ["REST", "CLI"])
    _assert_control_rejected("shared_core", "surface_specific_rule", "ACCEPT")


def test_first_functional_slice_decision_10() -> None:
    control = _checkpoint()["controls"]["promotion"]
    assert control["corpus"] == "VERSIONED_STRATIFIED_INITIAL_CORPUS"
    assert control["dimensions"] == [
        "FALSE_ACCEPTANCE",
        "QUALITY",
        "RUNTIME",
        "SECURITY",
    ]
    assert control["evidence"] == "REQUIRED"
    _assert_control_rejected("promotion", "dimensions", ["QUALITY"])
    _assert_control_rejected("promotion", "failed_or_missing_dimension", "WARN")


def test_checkpoint_rejects_missing_or_unknown_control() -> None:
    missing = copy.deepcopy(_checkpoint())
    del missing["controls"]["sgv"]
    errors = _validator_module().validate_checkpoint(missing, ROOT)
    assert any(error.startswith("controls fields:") for error in errors)

    unknown = copy.deepcopy(_checkpoint())
    unknown["controls"]["silent_fallback"] = {"enabled": True}
    errors = _validator_module().validate_checkpoint(unknown, ROOT)
    assert any(error.startswith("controls fields:") for error in errors)


def test_checkpoint_requirements_and_task_envelope_are_contained() -> None:
    expected = _validator_module().REQUIREMENT_TESTS
    requirement_map = {
        item["id"]: item["test"] for item in _checkpoint()["requirements"]
    }
    assert requirement_map == expected

    task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    allow_paths = set(task["allow_paths"])
    assert ".codex/tasks/TASK-0703.json" not in allow_paths
    assert any(path.startswith("tools/governance/openapi-") for path in allow_paths)
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in allow_paths
    assert (
        "evidence/implementation/openapi-cliente-typescript-e-contratos-cli-jobs-ev/"
        "artlayout-dbschema-fs1-parte-1/IMPLEMENTATION_EVIDENCE.yaml"
        in allow_paths
    )
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]


def test_checkpoint_cli_reports_pass() -> None:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), str(CHECKPOINT_PATH), "--repo-root", str(ROOT)],
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout) == {"status": "PASS", "errors": []}
