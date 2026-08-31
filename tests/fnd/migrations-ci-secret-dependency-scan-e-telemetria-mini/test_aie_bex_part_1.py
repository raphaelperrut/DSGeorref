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
    / "aie-bex-parte-1/decision_controls.py"
)
TASK_PATH = ROOT / ".codex/tasks/TASK-0708.json"


def _load_controls() -> ModuleType:
    module_name = "aie_bex_decision_controls"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


CONTROLS = _load_controls()
CHECKPOINT_DIGEST = "a" * 64
INPUT_DIGEST = "b" * 64
PROFILE_DIGEST = "c" * 64
MODELPACK_DIGEST = "d" * 64
CORPUS_DIGEST = "e" * 64
CHUNK_PLAN_DIGEST = "f" * 64


def _ai_decision() -> Any:
    return CONTROLS.AIEscalationDecision(
        prerequisites=CONTROLS.ClassicPrerequisites(True, CHECKPOINT_DIGEST, "policy"),
        recommendation=CONTROLS.ModelRecommendation(
            policy_version="1.0.0",
            input_digest=INPUT_DIGEST,
            required_capabilities=frozenset({"matching"}),
            selected_capabilities=frozenset({"matching", "offline"}),
            recommendation_runs=("modelpack@sha256:pack", "modelpack@sha256:pack"),
            selected_modelpack_id="modelpack@sha256:pack",
        ),
        budget=CONTROLS.NeuralBudgetEvidence(
            PROFILE_DIGEST, True, True, True, True, True
        ),
        continuity=CONTROLS.CapabilityContinuity(True, True, True, ""),
        sgv=CONTROLS.SGVEvidence(True, True, True, False, False),
        modelpack=CONTROLS.ModelPackEvidence(
            True, MODELPACK_DIGEST, "license-ref", True, True, False
        ),
        explanation=CONTROLS.ExplanationEvidence(
            "eligible",
            "modelpack@sha256:pack",
            "bounded by profile",
            "candidate only",
            "independent SGV required",
            False,
        ),
        promotion=CONTROLS.PromotionEvidence(
            CORPUS_DIGEST, True, True, True, "rollback-ref"
        ),
    )


def _batch_decision() -> Any:
    return CONTROLS.BatchExecutionDecision(
        execution_order=("PREFLIGHT", "ADAPTIVE_CHUNKING", "ADMISSION"),
        chunk_plan_digest=CHUNK_PLAN_DIGEST,
        scheduler_class="governed-class",
        fairness_policy_version="1.0.0",
        aging_applied=True,
        override_requested=True,
        override_audit_reference="audit-ref",
    )


def _assert_ai_rejected(decision: Any, requirement: str) -> None:
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        CONTROLS.validate_ai_escalation(decision)
    assert requirement in rejected.value.failed_requirements


def _assert_batch_rejected(decision: Any, requirement: str) -> None:
    with pytest.raises(CONTROLS.DecisionRejected) as rejected:
        CONTROLS.validate_batch_execution(decision)
    assert requirement in rejected.value.failed_requirements


def test_ai_escalation_decision_02() -> None:
    decision = _ai_decision()
    CONTROLS.validate_ai_escalation(decision)
    invalid = replace(
        decision,
        prerequisites=replace(decision.prerequisites, checkpoint_digest=""),
    )
    _assert_ai_rejected(invalid, "REQ-AIE-002")


def test_ai_escalation_decision_03() -> None:
    decision = _ai_decision()
    nondeterministic = replace(
        decision.recommendation,
        recommendation_runs=("modelpack-a", "modelpack-b"),
    )
    _assert_ai_rejected(replace(decision, recommendation=nondeterministic), "REQ-AIE-003")
    incapable = replace(
        decision.recommendation,
        selected_capabilities=frozenset({"offline"}),
    )
    _assert_ai_rejected(replace(decision, recommendation=incapable), "REQ-AIE-003")


def test_ai_escalation_decision_04() -> None:
    decision = _ai_decision()
    for field in (
        "attempts_within_limit",
        "time_within_limit",
        "memory_within_limit",
        "device_allowed",
        "priority_allowed",
    ):
        exhausted = replace(decision.budget, **{field: False})
        _assert_ai_rejected(replace(decision, budget=exhausted), "REQ-AIE-004")
    coerced = replace(decision.budget, attempts_within_limit=1)
    _assert_ai_rejected(replace(decision, budget=coerced), "REQ-AIE-004")


def test_ai_escalation_decision_06() -> None:
    decision = _ai_decision()
    unavailable = replace(
        decision,
        continuity=CONTROLS.CapabilityContinuity(
            ai_optional=True,
            classic_cpu_operational=True,
            capability_available=False,
            unavailable_reason="MODEL_PACK_MISSING",
        ),
    )
    CONTROLS.validate_ai_escalation(unavailable)
    silent = replace(unavailable.continuity, unavailable_reason="")
    _assert_ai_rejected(replace(unavailable, continuity=silent), "REQ-AIE-006")
    broken_classic = replace(unavailable.continuity, classic_cpu_operational=False)
    _assert_ai_rejected(replace(unavailable, continuity=broken_classic), "REQ-AIE-006")


def test_ai_escalation_decision_07() -> None:
    decision = _ai_decision()
    privileged = replace(decision.sgv, independent=False)
    _assert_ai_rejected(replace(decision, sgv=privileged), "REQ-AIE-007")
    unnecessary_review = replace(decision.sgv, review_applied=True)
    _assert_ai_rejected(replace(decision, sgv=unnecessary_review), "REQ-AIE-007")


def test_ai_escalation_decision_08() -> None:
    decision = _ai_decision()
    implicit_download = replace(decision.modelpack, implicit_download=True)
    _assert_ai_rejected(replace(decision, modelpack=implicit_download), "REQ-AIE-008")
    unsigned = replace(decision.modelpack, signed=False)
    _assert_ai_rejected(replace(decision, modelpack=unsigned), "REQ-AIE-008")
    unpinned = replace(decision.modelpack, pinned_digest="floating-tag")
    _assert_ai_rejected(replace(decision, modelpack=unpinned), "REQ-AIE-008")


def test_ai_escalation_decision_09() -> None:
    decision = _ai_decision()
    unexplained = replace(decision.explanation, cost="")
    _assert_ai_rejected(replace(decision, explanation=unexplained), "REQ-AIE-009")
    bypass = replace(decision.explanation, quality_gate_bypass=True)
    _assert_ai_rejected(replace(decision, explanation=bypass), "REQ-AIE-009")


def test_ai_escalation_decision_10() -> None:
    decision = _ai_decision()
    no_canary = replace(decision.promotion, canary_passed=False)
    _assert_ai_rejected(replace(decision, promotion=no_canary), "REQ-AIE-010")
    no_rollback = replace(decision.promotion, rollback_reference="")
    _assert_ai_rejected(replace(decision, promotion=no_rollback), "REQ-AIE-010")


def test_batch_execution_decision_02() -> None:
    decision = _batch_decision()
    CONTROLS.validate_batch_execution(decision)
    out_of_order = replace(
        decision,
        execution_order=("ADMISSION", "PREFLIGHT", "ADAPTIVE_CHUNKING"),
    )
    _assert_batch_rejected(out_of_order, "REQ-BEX-002")
    missing_preflight = replace(
        decision,
        execution_order=("ADAPTIVE_CHUNKING", "ADMISSION"),
    )
    _assert_batch_rejected(missing_preflight, "REQ-BEX-002")
    duplicate_preflight = replace(
        decision,
        execution_order=("PREFLIGHT", "PREFLIGHT", "ADAPTIVE_CHUNKING", "ADMISSION"),
    )
    _assert_batch_rejected(duplicate_preflight, "REQ-BEX-002")
    no_plan = replace(decision, chunk_plan_digest="")
    _assert_batch_rejected(no_plan, "REQ-BEX-002")


def test_batch_execution_decision_04() -> None:
    decision = _batch_decision()
    CONTROLS.validate_batch_execution(decision)
    unaudited = replace(decision, override_audit_reference="")
    _assert_batch_rejected(unaudited, "REQ-BEX-004")
    no_aging = replace(decision, aging_applied=False)
    _assert_batch_rejected(no_aging, "REQ-BEX-004")


def test_task_envelope_is_valid_and_sister_slices_are_not_anticipated() -> None:
    task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(task)
    allowed = set(task["allow_paths"])
    assert ".codex/tasks/TASK-0708.json" in allowed
    assert str(Path(__file__).relative_to(ROOT)).replace("\\", "/") in allowed
    assert any(path.startswith("evidence/implementation/migrations-ci-") for path in allowed)
    assert not any("parte-2" in path or "parte-3" in path or "parte-4" in path for path in allowed)
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "ISSUE-" not in source
    assert "STORY-" not in source
