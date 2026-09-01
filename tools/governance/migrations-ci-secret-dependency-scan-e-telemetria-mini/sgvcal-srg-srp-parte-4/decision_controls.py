"""Fail-closed controls for calibration, delivery gates, replay, and cutover."""

from __future__ import annotations

from dataclasses import dataclass


def _has_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_sha256(value: object) -> bool:
    hexadecimal = "0123456789abcdef"
    return isinstance(value, str) and len(value) == 64 and all(c in hexadecimal for c in value)


def _unique_text_tuple(values: object) -> bool:
    return bool(
        type(values) is tuple
        and values
        and all(_has_text(value) for value in values)
        and len(values) == len(set(values))
    )


def _has_exact_names(values: object, required: tuple[str, ...]) -> bool:
    return _unique_text_tuple(values) and set(values) == set(required)


def _digested_items_are_valid(items: object) -> bool:
    return bool(
        type(items) is tuple
        and items
        and all(
            type(item) is tuple
            and len(item) == 2
            and _has_text(item[0])
            and _is_sha256(item[1])
            for item in items
        )
        and len(items) == len({item[0] for item in items})
    )


def _strict_true(values: tuple[object, ...]) -> bool:
    return bool(values) and all(type(value) is bool and value for value in values)


@dataclass(frozen=True)
class SGVPromotionEvidence:
    calibration: str
    holdout: str
    false_acceptance_within_budget: bool
    gray_zone_outcome: str
    failed_hard_gate_outcome: str
    hard_gate_overridden: bool
    promotion_stages: tuple[str, ...]
    stage_evidence: tuple[tuple[str, str], ...]
    profile_digest: str
    rollback_ready: bool
    missing_or_invalid: str

    def failed_requirements(self) -> tuple[str, ...]:
        checks = (
            ("REQ-SGVCAL-008", self._calibration_is_valid()),
            ("REQ-SGVCAL-009", self._gray_zone_is_valid()),
            ("REQ-SGVCAL-010", self._promotion_is_valid()),
        )
        return tuple(requirement for requirement, passed in checks if not passed)

    def _calibration_is_valid(self) -> bool:
        return bool(
            self.calibration == "STRATIFIED"
            and self.holdout == "BLIND_SEPARATE"
            and self.false_acceptance_within_budget is True
            and self.missing_or_invalid == "REJECT"
        )

    def _gray_zone_is_valid(self) -> bool:
        return bool(
            self.gray_zone_outcome == "REVIEWABLE"
            and self.failed_hard_gate_outcome == "REJECTED"
            and self.hard_gate_overridden is False
            and self.missing_or_invalid == "REJECT"
        )

    def _promotion_is_valid(self) -> bool:
        expected_stages = ("shadow", "canary")
        return bool(
            type(self.promotion_stages) is tuple
            and self.promotion_stages == expected_stages
            and _digested_items_are_valid(self.stage_evidence)
            and tuple(item[0] for item in self.stage_evidence) == expected_stages
            and _is_sha256(self.profile_digest)
            and self.rollback_ready is True
            and self.missing_or_invalid == "REJECT"
        )


@dataclass(frozen=True)
class TestSelectionEvidence:
    impact_graph_used: bool
    impact_graph_digest: str
    mandatory_tiers: tuple[str, ...]
    selected_tiers: tuple[str, ...]
    promotion_candidate: bool
    full_matrix_selected: bool
    missing_or_invalid: str

    def is_valid(self) -> bool:
        tiers_valid = _unique_text_tuple(self.mandatory_tiers) and _unique_text_tuple(
            self.selected_tiers
        )
        return bool(
            self.impact_graph_used is True
            and _is_sha256(self.impact_graph_digest)
            and tiers_valid
            and set(self.mandatory_tiers).issubset(self.selected_tiers)
            and type(self.promotion_candidate) is bool
            and type(self.full_matrix_selected) is bool
            and (not self.promotion_candidate or self.full_matrix_selected)
            and self.missing_or_invalid == "REJECT"
        )


@dataclass(frozen=True)
class SchedulerReplayEvidence:
    snapshot_id: str
    decisions: tuple[tuple[str, str], ...]
    offline: bool
    scientific_workload_executed: bool
    provider_calls: tuple[str, ...]

    def is_valid(self) -> bool:
        expected = ("ADMISSION", "FAIRNESS", "LEASE", "BACKPRESSURE", "BREAKER")
        return bool(
            _has_text(self.snapshot_id)
            and type(self.decisions) is tuple
            and len(self.decisions) == len(expected)
            and all(
                type(decision) is tuple
                and len(decision) == 2
                and _has_text(decision[0])
                and _has_text(decision[1])
                for decision in self.decisions
            )
            and _has_exact_names(tuple(decision[0] for decision in self.decisions), expected)
            and self.offline is True
            and self.scientific_workload_executed is False
            and type(self.provider_calls) is tuple
            and not self.provider_calls
        )


@dataclass(frozen=True)
class ReleaseEvidence:
    lockfiles: tuple[tuple[str, str], ...]
    immutable_pins: bool
    sbom_digest: str
    scanning_passed: bool
    checksums: tuple[str, ...]
    oci_signature_digest: str
    oci_signature_verified: bool
    provenance_digest: str
    missing_or_invalid: str

    def is_valid(self) -> bool:
        return bool(
            _digested_items_are_valid(self.lockfiles)
            and self.immutable_pins is True
            and _is_sha256(self.sbom_digest)
            and self.scanning_passed is True
            and type(self.checksums) is tuple
            and self.checksums
            and all(_is_sha256(checksum) for checksum in self.checksums)
            and _is_sha256(self.oci_signature_digest)
            and self.oci_signature_verified is True
            and _is_sha256(self.provenance_digest)
            and self.missing_or_invalid == "REJECT"
        )


@dataclass(frozen=True)
class ToolingEvidence:
    local_python_gates: tuple[str, ...]
    ci_python_gates: tuple[str, ...]
    configurations_versioned: bool
    violations_block_candidate: bool
    integration_services: tuple[str, ...]
    integration_services_real: bool
    authoritative_state_store: str
    broker_role: str
    frontend_typescript_strict: bool
    frontend_test_tools: tuple[str, ...]
    frontend_failures_block_candidate: bool

    def failed_requirements(self) -> tuple[str, ...]:
        checks = (
            ("REQ-TOOL-006", self._python_gates_are_valid()),
            ("REQ-TOOL-007", self._integration_services_are_valid()),
            ("REQ-TOOL-009", self._frontend_gate_is_valid()),
        )
        return tuple(requirement for requirement, passed in checks if not passed)

    def _python_gates_are_valid(self) -> bool:
        expected = ("ruff", "mypy")
        return bool(
            _has_exact_names(self.local_python_gates, expected)
            and _has_exact_names(self.ci_python_gates, expected)
            and _strict_true((self.configurations_versioned, self.violations_block_candidate))
        )

    def _integration_services_are_valid(self) -> bool:
        return bool(
            _has_exact_names(self.integration_services, ("POSTGIS", "RABBITMQ"))
            and self.integration_services_real is True
            and self.authoritative_state_store == "POSTGRESQL_POSTGIS"
            and self.broker_role == "TRANSPORT_ONLY"
        )

    def _frontend_gate_is_valid(self) -> bool:
        return bool(
            self.frontend_typescript_strict is True
            and _has_exact_names(
                self.frontend_test_tools, ("VITEST", "TESTING_LIBRARY", "PLAYWRIGHT")
            )
            and self.frontend_failures_block_candidate is True
        )


@dataclass(frozen=True)
class CutoverEvidence:
    gate_results: tuple[tuple[str, bool, str], ...]
    atomic_writer_cutover: bool
    promotion_requested: bool
    missing_or_invalid: str

    def is_valid(self) -> bool:
        expected = ("INVARIANTS", "HISTORICAL_READERS", "HEALTH", "CANARY")
        return bool(
            type(self.gate_results) is tuple
            and len(self.gate_results) == len(expected)
            and all(
                type(result) is tuple
                and len(result) == 3
                and _has_text(result[0])
                and type(result[1]) is bool
                and _is_sha256(result[2])
                for result in self.gate_results
            )
            and _has_exact_names(tuple(result[0] for result in self.gate_results), expected)
            and _strict_true(tuple(result[1] for result in self.gate_results))
            and _strict_true((self.atomic_writer_cutover, self.promotion_requested))
            and self.missing_or_invalid == "REJECT"
        )


class DecisionRejected(ValueError):
    """Raised with requirement IDs when evidence cannot authorize a decision."""

    def __init__(self, failed_requirements: tuple[str, ...]) -> None:
        self.failed_requirements = failed_requirements
        super().__init__(", ".join(failed_requirements))


def _reject_if_failed(failed_requirements: tuple[str, ...]) -> None:
    if failed_requirements:
        raise DecisionRejected(failed_requirements)


def validate_sgv_promotion(evidence: SGVPromotionEvidence) -> None:
    """Require SGVCAL-008 through SGVCAL-010 evidence."""
    failed = (
        evidence.failed_requirements()
        if isinstance(evidence, SGVPromotionEvidence)
        else ("REQ-SGVCAL-008", "REQ-SGVCAL-009", "REQ-SGVCAL-010")
    )
    _reject_if_failed(failed)


def validate_test_selection(evidence: TestSelectionEvidence) -> None:
    """Require impact selection, mandatory tiers, and promotion matrix coverage."""
    if not isinstance(evidence, TestSelectionEvidence) or not evidence.is_valid():
        raise DecisionRejected(("REQ-SRG-002",))


def replay_scheduler_decisions(
    evidence: SchedulerReplayEvidence,
) -> tuple[tuple[str, str], ...]:
    """Replay a complete scheduler decision snapshot without external execution."""
    if not isinstance(evidence, SchedulerReplayEvidence) or not evidence.is_valid():
        raise DecisionRejected(("REQ-SRP-002",))
    return evidence.decisions


def validate_release(evidence: ReleaseEvidence) -> None:
    """Require immutable release supply-chain evidence."""
    if not isinstance(evidence, ReleaseEvidence) or not evidence.is_valid():
        raise DecisionRejected(("REQ-SUP-001",))


def validate_tooling(evidence: ToolingEvidence) -> None:
    """Require Python, real-service, and frontend integration gates."""
    failed = (
        evidence.failed_requirements()
        if isinstance(evidence, ToolingEvidence)
        else ("REQ-TOOL-006", "REQ-TOOL-007", "REQ-TOOL-009")
    )
    _reject_if_failed(failed)


def validate_cutover(evidence: CutoverEvidence) -> None:
    """Require multidimensional evidence before atomic writer cutover."""
    if not isinstance(evidence, CutoverEvidence) or not evidence.is_valid():
        raise DecisionRejected(("REQ-UPG-003",))
