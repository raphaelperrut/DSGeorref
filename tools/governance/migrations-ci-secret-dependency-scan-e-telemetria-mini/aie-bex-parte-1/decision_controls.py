"""Fail-closed governance controls for AI escalation and batch admission."""

from __future__ import annotations

from dataclasses import dataclass


def _has_text(value: str) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_sha256(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )


def _all_true(values: tuple[bool, ...]) -> bool:
    return all(value is True for value in values)


@dataclass(frozen=True)
class ClassicPrerequisites:
    baseline_succeeded: bool
    checkpoint_digest: str
    controlled_trigger: str

    def is_valid(self) -> bool:
        return bool(
            self.baseline_succeeded is True
            and _is_sha256(self.checkpoint_digest)
            and _has_text(self.controlled_trigger)
        )


@dataclass(frozen=True)
class ModelRecommendation:
    policy_version: str
    input_digest: str
    required_capabilities: frozenset[str]
    selected_capabilities: frozenset[str]
    recommendation_runs: tuple[str, ...]
    selected_modelpack_id: str

    def is_valid(self) -> bool:
        deterministic = len(self.recommendation_runs) >= 2 and all(
            candidate == self.selected_modelpack_id
            for candidate in self.recommendation_runs
        )
        return bool(
            _has_text(self.policy_version)
            and _is_sha256(self.input_digest)
            and _has_text(self.selected_modelpack_id)
            and self.required_capabilities
            and deterministic
            and self.required_capabilities <= self.selected_capabilities
        )


@dataclass(frozen=True)
class NeuralBudgetEvidence:
    profile_digest: str
    attempts_within_limit: bool
    time_within_limit: bool
    memory_within_limit: bool
    device_allowed: bool
    priority_allowed: bool

    def is_valid(self) -> bool:
        return _is_sha256(self.profile_digest) and _all_true(
            (
                self.attempts_within_limit,
                self.time_within_limit,
                self.memory_within_limit,
                self.device_allowed,
                self.priority_allowed,
            )
        )


@dataclass(frozen=True)
class CapabilityContinuity:
    ai_optional: bool
    classic_cpu_operational: bool
    capability_available: bool
    unavailable_reason: str

    def is_valid(self) -> bool:
        booleans_are_strict = all(
            type(value) is bool
            for value in (
                self.ai_optional,
                self.classic_cpu_operational,
                self.capability_available,
            )
        )
        availability_is_consistent = self.capability_available != _has_text(
            self.unavailable_reason
        )
        return (
            booleans_are_strict
            and self.ai_optional
            and self.classic_cpu_operational
            and availability_is_consistent
        )


@dataclass(frozen=True)
class SGVEvidence:
    independent: bool
    consensus_required: bool
    consensus_applied: bool
    review_required: bool
    review_applied: bool

    def is_valid(self) -> bool:
        booleans_are_strict = all(
            type(value) is bool
            for value in (
                self.independent,
                self.consensus_required,
                self.consensus_applied,
                self.review_required,
                self.review_applied,
            )
        )
        return (
            booleans_are_strict
            and self.independent
            and self.consensus_required == self.consensus_applied
            and self.review_required == self.review_applied
        )


@dataclass(frozen=True)
class ModelPackEvidence:
    signed: bool
    pinned_digest: str
    license_id: str
    opt_in: bool
    offline_import_supported: bool
    implicit_download: bool

    def is_valid(self) -> bool:
        return bool(
            self.signed is True
            and _is_sha256(self.pinned_digest)
            and _has_text(self.license_id)
            and self.opt_in is True
            and self.offline_import_supported is True
            and self.implicit_download is False
        )


@dataclass(frozen=True)
class ExplanationEvidence:
    eligibility: str
    model: str
    cost: str
    result: str
    controls: str
    quality_gate_bypass: bool

    def is_valid(self) -> bool:
        return bool(
            _has_text(self.eligibility)
            and _has_text(self.model)
            and _has_text(self.cost)
            and _has_text(self.result)
            and _has_text(self.controls)
            and self.quality_gate_bypass is False
        )


@dataclass(frozen=True)
class PromotionEvidence:
    corpus_digest: str
    shadow_or_dual_run_passed: bool
    canary_passed: bool
    multidimensional_gate_passed: bool
    rollback_reference: str

    def is_valid(self) -> bool:
        return bool(
            _is_sha256(self.corpus_digest)
            and self.shadow_or_dual_run_passed is True
            and self.canary_passed is True
            and self.multidimensional_gate_passed is True
            and _has_text(self.rollback_reference)
        )


@dataclass(frozen=True)
class AIEscalationDecision:
    prerequisites: ClassicPrerequisites
    recommendation: ModelRecommendation
    budget: NeuralBudgetEvidence
    continuity: CapabilityContinuity
    sgv: SGVEvidence
    modelpack: ModelPackEvidence
    explanation: ExplanationEvidence
    promotion: PromotionEvidence

    def failed_requirements(self) -> tuple[str, ...]:
        checks = (
            ("REQ-AIE-002", self.prerequisites.is_valid()),
            ("REQ-AIE-003", self.recommendation.is_valid()),
            ("REQ-AIE-004", self.budget.is_valid()),
            ("REQ-AIE-006", self.continuity.is_valid()),
            ("REQ-AIE-007", self.sgv.is_valid()),
            ("REQ-AIE-008", self.modelpack.is_valid()),
            ("REQ-AIE-009", self.explanation.is_valid()),
            ("REQ-AIE-010", self.promotion.is_valid()),
        )
        return tuple(requirement for requirement, passed in checks if not passed)


@dataclass(frozen=True)
class BatchExecutionDecision:
    execution_order: tuple[str, ...]
    chunk_plan_digest: str
    scheduler_class: str
    fairness_policy_version: str
    aging_applied: bool
    override_requested: bool
    override_audit_reference: str

    def failed_requirements(self) -> tuple[str, ...]:
        required_stages = ("PREFLIGHT", "ADAPTIVE_CHUNKING", "ADMISSION")
        stages_present_once = all(
            self.execution_order.count(stage) == 1 for stage in required_stages
        )
        indices = (
            tuple(self.execution_order.index(stage) for stage in required_stages)
            if stages_present_once
            else ()
        )
        preflight_valid = stages_present_once and indices == tuple(sorted(indices))
        scheduler_valid = bool(
            _has_text(self.scheduler_class)
            and _has_text(self.fairness_policy_version)
            and self.aging_applied is True
            and type(self.override_requested) is bool
            and (
                self.override_requested is False
                or _has_text(self.override_audit_reference)
            )
        )
        checks = (
            ("REQ-BEX-002", preflight_valid and _is_sha256(self.chunk_plan_digest)),
            ("REQ-BEX-004", scheduler_valid),
        )
        return tuple(requirement for requirement, passed in checks if not passed)


class DecisionRejected(ValueError):
    """Raised with requirement IDs when a decision is not conformant."""

    def __init__(self, failed_requirements: list[str]) -> None:
        self.failed_requirements = tuple(failed_requirements)
        super().__init__(", ".join(self.failed_requirements))


def validate_ai_escalation(decision: AIEscalationDecision) -> None:
    """Reject an AI escalation record unless every owned requirement is evidenced."""
    failed = list(decision.failed_requirements())
    if failed:
        raise DecisionRejected(failed)


def validate_batch_execution(decision: BatchExecutionDecision) -> None:
    """Reject batch admission unless ordering and scheduler evidence are complete."""
    failed = list(decision.failed_requirements())
    if failed:
        raise DecisionRejected(failed)
