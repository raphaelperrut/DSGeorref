from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini"
    / "fs1-gov-sgvcal-parte-3/decision_controls.py"
)
TASK_PATH = ROOT / ".codex/tasks/TASK-0710.json"
FOUNDATION_PATH = (
    ROOT
    / "tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento"
    / "artlayout-dbschema-fs1-parte-1/foundation-checkpoint.json"
)
SGVCAL_PATH = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "migrations-ci-secret-dependency-scan-e-telemetria-mini"
    / "sgvcal-parte-2/examples/sgvcal-conformance.json"
)
DIGESTS = tuple(character * 64 for character in "abcdef")


def _load_controls() -> ModuleType:
    module_name = "fs1_gov_sgvcal_decision_controls"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


CONTROLS = _load_controls()


def _functional_evidence() -> Any:
    checkpoint = json.loads(FOUNDATION_PATH.read_text(encoding="utf-8"))["controls"]
    artifact = checkpoint["artifact_set"]
    shared_core = checkpoint["shared_core"]
    promotion = checkpoint["promotion"]
    return CONTROLS.FunctionalSliceEvidence(
        artifact_set_immutable=artifact["immutable"],
        artifact_kinds=tuple(artifact["required_kinds"]),
        artifact_digests=DIGESTS[:3],
        publication_atomic=artifact["publication"] == "ATOMIC_AFTER_SGV_ACCEPTED",
        sgv_verdict="ACCEPTED",
        shared_application_service="georeference-application-service",
        surface_runs=tuple(
            (surface, "georeference-application-service", DIGESTS[3])
            for surface in shared_core["surfaces"]
        ),
        corpus_version="initial-corpus@1.0.0",
        corpus_digest=DIGESTS[4],
        corpus_stratified=promotion["corpus"] == "VERSIONED_STRATIFIED_INITIAL_CORPUS",
        promotion_gates=tuple(
            (dimension, True, DIGESTS[5]) for dimension in promotion["dimensions"]
        ),
        promotion_requested=True,
    )


def _sgv_evidence() -> Any:
    controls = json.loads(SGVCAL_PATH.read_text(encoding="utf-8"))["controls"]
    return CONTROLS.SGVCalibrationEvidence(
        stratum_id="sensor-family:aerial-film",
        profile_id="sgv-profile@1.0.0",
        profile_digest=DIGESTS[0],
        hard_invariants_immutable=(
            controls["profile_immutability"]["hard_invariants"] == "IMMUTABLE"
        ),
        profile_immutable=(
            controls["profile_immutability"]["sgv_profile"] == "IMMUTABLE_VERSIONED"
        ),
        metric_declarations=(
            ("symmetric-transfer-error", "image", "pixel", "lower-is-better", "none"),
        ),
        transfer_error=controls["robust_error_distribution"]["transfer_error"],
        error_distribution=controls["robust_error_distribution"]["distribution"],
        coverage_dimensions=tuple(
            controls["multidimensional_coverage"]["required_dimensions"]
        ),
        stability_checks=tuple(controls["stability_gates"]["required_checks"]),
        local_deformation_measure=controls["local_deformation"]["measurement"],
        missing_or_invalid="REJECT",
    )


def _governance_evidence() -> Any:
    return CONTROLS.DeliveryGovernanceEvidence(
        authorized_task="TASK-0710",
        issue_ready=True,
        dedicated_branch=True,
        short_lived_worktree=True,
        pull_request_required=True,
        direct_main_prohibited=True,
        automerge_prohibited=True,
        sensitive_gate_decision_by_codex=False,
    )


def _assert_functional_rejected(evidence: Any, requirement: str) -> None:
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        CONTROLS.validate_functional_slice(evidence)
    assert requirement in rejected.value.failed_requirements


def _assert_sgv_rejected(evidence: Any, requirement: str) -> None:
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        CONTROLS.validate_sgv_calibration(evidence)
    assert requirement in rejected.value.failed_requirements


def test_first_functional_slice_decision_08() -> None:
    evidence = _functional_evidence()
    CONTROLS.validate_functional_slice(evidence)
    for changes in (
        {"artifact_set_immutable": False},
        {"artifact_kinds": ("COG_RASTER", "QUALITY_REPORT")},
        {"artifact_digests": ("not-a-digest",) * 3},
        {"publication_atomic": False},
        {"sgv_verdict": "REVIEWABLE"},
    ):
        _assert_functional_rejected(replace(evidence, **changes), "REQ-FS1-008")


def test_first_functional_slice_decision_09() -> None:
    evidence = _functional_evidence()
    for surface_runs in (
        evidence.surface_runs[:-1],
        (("REST", "alternate-service", DIGESTS[3]),) + evidence.surface_runs[1:],
        evidence.surface_runs[:-1]
        + (("CELERY", evidence.shared_application_service, DIGESTS[4]),),
        (("REST", evidence.shared_application_service, []),) + evidence.surface_runs[1:],
        (None,) + evidence.surface_runs[1:],
    ):
        _assert_functional_rejected(
            replace(evidence, surface_runs=surface_runs), "REQ-FS1-009"
        )


def test_first_functional_slice_decision_10() -> None:
    evidence = _functional_evidence()
    failed_gate = evidence.promotion_gates[:-1] + (("SECURITY", False, DIGESTS[5]),)
    for changes in (
        {"corpus_version": ""},
        {"corpus_stratified": False},
        {"promotion_gates": failed_gate},
        {"promotion_gates": evidence.promotion_gates[:-1]},
        {"promotion_gates": (None,) + evidence.promotion_gates[1:]},
        {"promotion_requested": False},
    ):
        _assert_functional_rejected(replace(evidence, **changes), "REQ-FS1-010")


def test_codex_issue_scope_required_pr_no_direct_main_or_automerge() -> None:
    evidence = _governance_evidence()
    CONTROLS.validate_delivery_governance(evidence)
    for changes in (
        {"authorized_task": ""},
        {"issue_ready": False},
        {"dedicated_branch": False},
        {"short_lived_worktree": False},
        {"pull_request_required": False},
        {"direct_main_prohibited": False},
        {"automerge_prohibited": False},
        {"sensitive_gate_decision_by_codex": True},
        {"issue_ready": 1},
    ):
        with pytest.raises(CONTROLS.DecisionRejected) as rejected:
            CONTROLS.validate_delivery_governance(replace(evidence, **changes))
        assert rejected.value.failed_requirements == ("REQ-GOV-004",)


def test_req_sgvcal_001() -> None:
    evidence = _sgv_evidence()
    CONTROLS.validate_sgv_calibration(evidence)
    for changes in (
        {"stratum_id": ""},
        {"profile_digest": "floating-profile"},
        {"hard_invariants_immutable": False},
        {"profile_immutable": 1},
    ):
        _assert_sgv_rejected(replace(evidence, **changes), "REQ-SGVCAL-001")


def test_req_sgvcal_002() -> None:
    evidence = _sgv_evidence()
    for declarations in (
        (),
        (("metric", "image", "pixel", "", "none"),),
        (("metric", "image", "pixel", "lower-is-better"),),
        (([], "image", "pixel", "lower-is-better", "none"),),
        (
            ("metric", "image", "pixel", "lower-is-better", "none"),
            ("metric", "map", "metre", "lower-is-better", "scale"),
        ),
    ):
        _assert_sgv_rejected(
            replace(evidence, metric_declarations=declarations), "REQ-SGVCAL-002"
        )


def test_req_sgvcal_003() -> None:
    evidence = _sgv_evidence()
    _assert_sgv_rejected(
        replace(evidence, transfer_error="FORWARD_ONLY"), "REQ-SGVCAL-003"
    )
    _assert_sgv_rejected(
        replace(evidence, error_distribution="MEAN_ONLY"), "REQ-SGVCAL-003"
    )


def test_req_sgvcal_004() -> None:
    evidence = _sgv_evidence()
    _assert_sgv_rejected(
        replace(evidence, coverage_dimensions=("leverage",)), "REQ-SGVCAL-004"
    )


def test_req_sgvcal_005() -> None:
    evidence = _sgv_evidence()
    _assert_sgv_rejected(
        replace(evidence, stability_checks=("conditioning", "degeneracy")),
        "REQ-SGVCAL-005",
    )


def test_req_sgvcal_006() -> None:
    evidence = _sgv_evidence()
    _assert_sgv_rejected(
        replace(evidence, local_deformation_measure="GLOBAL_ONLY"),
        "REQ-SGVCAL-006",
    )


def test_missing_or_malformed_evidence_is_rejected_without_fallback() -> None:
    validators = (
        (CONTROLS.validate_functional_slice, ("REQ-FS1-008", "REQ-FS1-009", "REQ-FS1-010")),
        (
            CONTROLS.validate_sgv_calibration,
            tuple(f"REQ-SGVCAL-{index:03d}" for index in range(1, 7)),
        ),
        (CONTROLS.validate_delivery_governance, ("REQ-GOV-004",)),
    )
    for validator, requirements in validators:
        with pytest.raises(CONTROLS.DecisionRejected) as rejected:
            validator(None)
        assert rejected.value.failed_requirements == requirements

    incomplete = replace(_sgv_evidence(), missing_or_invalid="WARN")
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        CONTROLS.validate_sgv_calibration(incomplete)
    assert rejected.value.failed_requirements == tuple(
        f"REQ-SGVCAL-{index:03d}" for index in range(1, 7)
    )


def test_task_envelope_is_valid_and_sister_slice_is_not_anticipated() -> None:
    task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(task)
    allowed = set(task["allow_paths"])
    assert ".codex/tasks/TASK-0710.json" in allowed
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in allowed
    assert any(path.startswith("evidence/implementation/migrations-ci-") for path in allowed)
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    assert not any("parte-4" in path for path in allowed)
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "ISSUE-" not in source
    assert "STORY-" not in source
