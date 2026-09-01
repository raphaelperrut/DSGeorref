from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import replace
from pathlib import Path, PureWindowsPath
from types import ModuleType
from typing import Any

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini"
    / "bex-epic-frz-parte-2/decision_controls.py"
)
TASK_PATH = ROOT / ".codex/tasks/TASK-0709.json"
LOCAL_ROOT = str(ROOT / "authorized-inputs")


def _load_controls() -> ModuleType:
    module_name = "bex_epic_frz_decision_controls"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


CONTROLS = _load_controls()
FILE_DIGEST = "a" * 64


def _batch_evidence() -> Any:
    return CONTROLS.BatchExecutionEvidence(
        control_action="PAUSE",
        request_scope="work-unit-7",
        work_unit_scope="work-unit-7",
        persistent_control_token="control-token",
        safe_point_reached=True,
        lease_store="POSTGRESQL",
        lease_generation=3,
        fencing_token=8,
        lease_renewable=True,
        lease_owned=True,
        revision_valid=True,
        resource_budgets_satisfied=True,
        backpressure_applied=True,
        progress_history=(0, 2, 4),
        total_work_units=8,
        progress_persisted=True,
        eta_seconds=12.0,
        eta_confidence=0.75,
        scale_ladder=(1, 10, 100),
        fault_injection_passed=True,
        invariant_results=(True, True, True),
    )


def _external_file(name: str) -> Any:
    return CONTROLS.ExternalFileEvidence(
        file_path=str(Path(LOCAL_ROOT) / name),
        registered_root=LOCAL_ROOT,
        registered_roots=(LOCAL_ROOT,),
        regular_file=True,
        symlink_free=True,
        size_within_limit=True,
        decompression_within_limit=True,
        scanner_available=True,
        scanner_clean=True,
        sha256_digest=FILE_DIGEST,
    )


def _functional_slice() -> Any:
    return CONTROLS.FirstFunctionalSliceEvidence(
        target=_external_file("target.tif"),
        reference=_external_file("reference.tif"),
        originals_preserved=True,
        metadata_complete=True,
        ingest_fail_closed=True,
        classic_pipeline_id="classic-profile@sha256:profile",
        pipeline_runs=(
            "classic-profile@sha256:profile",
            "classic-profile@sha256:profile",
        ),
        pipeline_substitutable=True,
        correspondence_audit_reference="audit-ledger-entry",
        sgv_profile_id="sgv-profile@sha256:profile",
        sgv_applied=True,
        sgv_result="ACCEPTED",
        critical_metrics_complete=True,
        hard_gates_passed=True,
        grey_zone=False,
    )


def _assert_batch_rejected(evidence: Any, requirement: str) -> None:
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        CONTROLS.validate_batch_execution(evidence)
    assert requirement in rejected.value.failed_requirements


def _assert_slice_rejected(evidence: Any, requirement: str) -> None:
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        CONTROLS.validate_first_functional_slice(evidence)
    assert requirement in rejected.value.failed_requirements


def test_batch_execution_decision_07() -> None:
    evidence = _batch_evidence()
    CONTROLS.validate_batch_execution(evidence)
    _assert_batch_rejected(replace(evidence, safe_point_reached=False), "REQ-BEX-007")
    _assert_batch_rejected(replace(evidence, request_scope="other-unit"), "REQ-BEX-007")
    _assert_batch_rejected(replace(evidence, persistent_control_token=""), "REQ-BEX-007")
    _assert_batch_rejected(replace(evidence, safe_point_reached=1), "REQ-BEX-007")


def test_batch_execution_decision_08() -> None:
    evidence = _batch_evidence()
    for changes in (
        {"lease_store": "RABBITMQ"},
        {"lease_renewable": False},
        {"lease_owned": False},
        {"revision_valid": False},
        {"fencing_token": 0},
        {"resource_budgets_satisfied": False},
        {"backpressure_applied": False},
    ):
        _assert_batch_rejected(replace(evidence, **changes), "REQ-BEX-008")


def test_batch_execution_decision_09() -> None:
    evidence = _batch_evidence()
    CONTROLS.validate_batch_execution(replace(evidence, eta_seconds=None, eta_confidence=None))
    for changes in (
        {"progress_history": (0, 4, 3)},
        {"progress_history": (0, 9)},
        {"progress_persisted": False},
        {"eta_confidence": None},
        {"eta_confidence": 1.1},
        {"eta_seconds": float("inf")},
        {"total_work_units": True},
    ):
        _assert_batch_rejected(replace(evidence, **changes), "REQ-BEX-009")


def test_batch_execution_decision_10() -> None:
    evidence = _batch_evidence()
    for changes in (
        {"scale_ladder": (1,)},
        {"scale_ladder": (1, 10, 10)},
        {"fault_injection_passed": False},
        {"invariant_results": (True,)},
        {"invariant_results": (True, False)},
    ):
        _assert_batch_rejected(replace(evidence, **changes), "REQ-BEX-010")


@pytest.mark.parametrize(
    "changes",
    (
        {"file_path": str(Path(LOCAL_ROOT).parent / "escaped.tif")},
        {"file_path": str(Path(LOCAL_ROOT) / ".." / "escaped.tif")},
        {"registered_roots": (str(Path(LOCAL_ROOT).parent),)},
        {"symlink_free": False},
        {"size_within_limit": False},
        {"decompression_within_limit": False},
        {"scanner_available": False},
        {"scanner_clean": False},
        {"sha256_digest": "not-a-digest"},
    ),
)
def test_malicious_file_suite(changes: dict[str, object]) -> None:
    evidence = replace(_external_file("target.tif"), **changes)
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        CONTROLS.validate_external_file(evidence)
    assert rejected.value.failed_requirements == ("REQ-EPIC-041",)


def test_sprint_zero_authorization_and_functional_foundation_gate_blocking() -> None:
    planning_only = CONTROLS.SprintFoundationAuthorization(
        ("SPRINT-001",), True, True, False, False
    )
    CONTROLS.validate_sprint_authorization(planning_only)
    functional = replace(
        planning_only, foundation_gate_passed=True, functional_implementation_requested=True
    )
    CONTROLS.validate_sprint_authorization(functional)
    for invalid in (
        replace(planning_only, authorized_sprints=("SPRINT-001", "SPRINT-002")),
        replace(planning_only, foundation_gate_executable=False),
        replace(planning_only, functional_implementation_requested=True),
        replace(planning_only, final_approval=1),
    ):
        with pytest.raises(CONTROLS.DecisionRejected) as rejected:
            CONTROLS.validate_sprint_authorization(invalid)
        assert rejected.value.failed_requirements == ("REQ-FRZ-002",)


def test_first_functional_slice_decision_02(monkeypatch: pytest.MonkeyPatch) -> None:
    evidence = _functional_slice()
    CONTROLS.validate_first_functional_slice(evidence)
    traversal = replace(
        evidence.target, file_path=str(Path(LOCAL_ROOT) / ".." / "escaped.tif")
    )
    _assert_slice_rejected(replace(evidence, target=traversal), "REQ-FS1-002")
    unregistered = replace(
        evidence.reference, registered_roots=(str(Path(LOCAL_ROOT).parent),)
    )
    _assert_slice_rejected(replace(evidence, reference=unregistered), "REQ-FS1-002")
    symlink = replace(evidence.target, symlink_free=False)
    _assert_slice_rejected(replace(evidence, target=symlink), "REQ-FS1-002")

    unc_root = r"\\server\share\registered"
    remote_target = replace(
        evidence.target,
        file_path=rf"{unc_root}\target.tif",
        registered_root=unc_root,
        registered_roots=(unc_root,),
    )
    remote_reference = replace(
        evidence.reference,
        file_path=rf"{unc_root}\reference.tif",
        registered_root=unc_root,
        registered_roots=(unc_root,),
    )
    local_path_factory = CONTROLS.Path
    monkeypatch.setattr(CONTROLS, "Path", PureWindowsPath)
    assert remote_target.path_is_authorized() is False
    assert remote_reference.path_is_authorized() is False
    monkeypatch.setattr(CONTROLS, "Path", local_path_factory)
    _assert_slice_rejected(replace(evidence, target=remote_target), "REQ-FS1-002")
    _assert_slice_rejected(replace(evidence, reference=remote_reference), "REQ-FS1-002")


def test_first_functional_slice_decision_03() -> None:
    evidence = _functional_slice()
    for changes in (
        {"originals_preserved": False},
        {"metadata_complete": False},
        {"ingest_fail_closed": False},
    ):
        _assert_slice_rejected(replace(evidence, **changes), "REQ-FS1-003")
    unscanned = replace(evidence.target, scanner_available=False)
    _assert_slice_rejected(replace(evidence, target=unscanned), "REQ-FS1-003")


def test_first_functional_slice_decision_05() -> None:
    evidence = _functional_slice()
    for changes in (
        {"pipeline_runs": ("classic-a", "classic-b")},
        {"pipeline_substitutable": False},
        {"correspondence_audit_reference": ""},
    ):
        _assert_slice_rejected(replace(evidence, **changes), "REQ-FS1-005")


def test_first_functional_slice_decision_07() -> None:
    evidence = _functional_slice()
    reviewable = replace(evidence, sgv_result="REVIEWABLE", grey_zone=True)
    CONTROLS.validate_first_functional_slice(reviewable)
    rejected = replace(
        evidence,
        sgv_result="REJECTED",
        critical_metrics_complete=False,
        hard_gates_passed=False,
    )
    CONTROLS.validate_first_functional_slice(rejected)
    for changes in (
        {"sgv_applied": False},
        {"sgv_result": "UNKNOWN"},
        {"sgv_result": []},
        {"sgv_result": "ACCEPTED", "critical_metrics_complete": False},
        {"sgv_result": "ACCEPTED", "grey_zone": True},
        {"sgv_result": "REVIEWABLE", "hard_gates_passed": False},
    ):
        _assert_slice_rejected(replace(evidence, **changes), "REQ-FS1-007")


def test_task_envelope_is_valid_and_sister_slices_are_not_anticipated() -> None:
    task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(task)
    allowed = set(task["allow_paths"])
    assert task["phase_f_review"]["files"]["allow_paths"] == task["allow_paths"]
    assert ".codex/tasks/TASK-0709.json" in allowed
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in allowed
    assert any(path.startswith("evidence/implementation/migrations-ci-") for path in allowed)
    assert not any("parte-3" in path or "parte-4" in path for path in allowed)
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "ISSUE-" not in source
    assert "STORY-" not in source
