from __future__ import annotations

import copy
import importlib.util
import json
from functools import cache
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
TOOL_ROOT = ROOT / (
    "tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/"
    "runtime-tool-upg-parte-3"
)
CHECKPOINT_PATH = TOOL_ROOT / "runtime-tool-upgrade-foundation-checkpoint.json"
VALIDATOR_PATH = TOOL_ROOT / "validate_runtime_tool_upgrade_foundation.py"
TASK_PATH = ROOT / ".codex/tasks/TASK-0705.json"


@cache
def _validator_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "runtime_tool_upgrade_foundation", VALIDATOR_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@cache
def _checkpoint() -> dict[str, Any]:
    loaded = json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _assert_valid() -> None:
    assert _validator_module().validate_checkpoint(_checkpoint(), ROOT) == []


def _assert_control_rejected(control: str, field: str, value: object) -> None:
    invalid = copy.deepcopy(_checkpoint())
    invalid["controls"][control][field] = value
    errors = _validator_module().validate_checkpoint(invalid, ROOT)
    assert any(error.startswith(f"controls.{control}:") for error in errors)


def _assert_scope_is_exact() -> None:
    task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    test_path = str(Path(__file__).relative_to(ROOT)).replace("\\", "/")
    evidence_path = (
        "evidence/implementation/openapi-cliente-typescript-e-contratos-cli-jobs-ev/"
        "runtime-tool-upg-parte-3/IMPLEMENTATION_EVIDENCE.yaml"
    )
    assert test_path in task["allow_paths"]
    assert evidence_path in task["allow_paths"]
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    assert ".codex/tasks/TASK-0705.json" not in task["allow_paths"]


def test_runtime_decision_6() -> None:
    _assert_valid()
    _assert_scope_is_exact()
    control = _checkpoint()["controls"]["browser_boundary"]
    assert control["surface"] == "PUBLISHED_HTTP_CONTRACT_ONLY"
    assert control["host_paths"] == "PROHIBITED"
    assert control["broker_payloads"] == "PROHIBITED"
    assert control["direct_persistence"] == "PROHIBITED"
    assert control["violation"] == "REJECT"
    _assert_control_rejected("browser_boundary", "host_paths", "EXPOSE")
    _assert_control_rejected("browser_boundary", "broker_payloads", "FORWARD_RAW")
    _assert_control_rejected("browser_boundary", "direct_persistence", "ALLOW")
    invalid = copy.deepcopy(_checkpoint())
    invalid["canonical_bindings"]["http_api"]["sha256"] = "0" * 64
    errors = _validator_module().validate_checkpoint(invalid, ROOT)
    assert any(error.startswith("canonical_bindings:") for error in errors)


def test_runtime_decision_7() -> None:
    _assert_valid()
    control = _checkpoint()["controls"]["authorized_selection"]
    assert control["roots"] == "AUTHORIZED_REGISTERED_ONLY"
    assert control["root_identifier"] == "OPAQUE_UUID"
    assert control["entry_identifier"] == "OPAQUE_STRING"
    assert control["absolute_host_path"] == "REJECT"
    assert control["unknown_root_or_entry"] == "REJECT"
    _assert_control_rejected("authorized_selection", "roots", "ARBITRARY")
    _assert_control_rejected("authorized_selection", "root_identifier", "HOST_PATH")
    _assert_control_rejected("authorized_selection", "absolute_host_path", "ACCEPT")


def test_model_boundary_architecture() -> None:
    _assert_valid()
    control = _checkpoint()["controls"]["model_boundaries"]
    assert control["domain_models"] == "SEPARATE"
    assert control["transport_models"] == "SEPARATE_HTTP_ADAPTER_ONLY"
    assert control["persistence_models"] == "SEPARATE_ADAPTER_ONLY"
    assert control["mapping"] == "EXPLICIT_TRANSPORT_DOMAIN_PERSISTENCE"
    assert control["shared_boundary_model"] == "REJECT"
    _assert_control_rejected("model_boundaries", "mapping", "IMPLICIT")
    _assert_control_rejected("model_boundaries", "shared_boundary_model", "ALLOW")
    missing = copy.deepcopy(_checkpoint())
    del missing["controls"]["model_boundaries"]
    errors = _validator_module().validate_checkpoint(missing, ROOT)
    assert any(error.startswith("controls fields:") for error in errors)


def test_phased_rollout_limited_mixed_version_window_drain_and_long_job_pinning(
) -> None:
    _assert_valid()
    control = _checkpoint()["controls"]["upgrade_rollout"]
    assert control["mixed_version_window"] == "ONE_UPGRADE_OPERATION"
    assert control["writers"] == "SINGLE_VERSION"
    assert control["writer_drain"] == "EXPLICIT_REQUIRED_BEFORE_CUTOVER"
    assert control["long_jobs"] == "PINNED_TO_COMPATIBLE_VERSION_UNTIL_COMPLETION"
    assert control["incompatible_or_unpinned"] == "REJECT"
    _assert_control_rejected("upgrade_rollout", "mixed_version_window", "UNBOUNDED")
    _assert_control_rejected("upgrade_rollout", "writer_drain", "IMPLICIT")
    _assert_control_rejected("upgrade_rollout", "long_jobs", "MIGRATE_IN_PLACE")
    invalid = copy.deepcopy(_checkpoint())
    invalid["dependency"]["eligible_story"] = "STORY-UNKNOWN"
    errors = _validator_module().validate_checkpoint(invalid, ROOT)
    assert any(error.startswith("dependency:") for error in errors)
