"""Fail-closed evidence controls for first-slice, SGVCAL, and delivery governance."""

from __future__ import annotations

from dataclasses import dataclass


def _has_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_sha256(value: object) -> bool:
    hexadecimal = "0123456789abcdef"
    return isinstance(value, str) and len(value) == 64 and all(c in hexadecimal for c in value)


def _strict_true(values: tuple[object, ...]) -> bool:
    return bool(values) and all(type(value) is bool and value for value in values)


@dataclass(frozen=True)
class FunctionalSliceEvidence:
    artifact_set_immutable: bool
    artifact_kinds: tuple[str, ...]
    artifact_digests: tuple[str, ...]
    publication_atomic: bool
    sgv_verdict: str
    shared_application_service: str
    surface_runs: tuple[tuple[str, str, str], ...]
    corpus_version: str
    corpus_digest: str
    corpus_stratified: bool
    promotion_gates: tuple[tuple[str, bool, str], ...]
    promotion_requested: bool

    def failed_requirements(self) -> tuple[str, ...]:
        checks = (
            ("REQ-FS1-008", self._artifact_set_is_valid()),
            ("REQ-FS1-009", self._shared_core_is_valid()),
            ("REQ-FS1-010", self._promotion_is_valid()),
        )
        return tuple(requirement for requirement, passed in checks if not passed)

    def _artifact_set_is_valid(self) -> bool:
        required_kinds = ("COG_RASTER", "PROVENANCE_MANIFEST", "QUALITY_REPORT")
        return bool(
            self.artifact_set_immutable is True
            and type(self.artifact_kinds) is tuple
            and self.artifact_kinds == required_kinds
            and type(self.artifact_digests) is tuple
            and len(self.artifact_digests) == len(required_kinds)
            and all(_is_sha256(digest) for digest in self.artifact_digests)
            and self.publication_atomic is True
            and self.sgv_verdict == "ACCEPTED"
        )

    def _shared_core_is_valid(self) -> bool:
        expected_surfaces = ("REST", "CLI", "DIRECT_RUNNER", "CELERY")
        if not _has_text(self.shared_application_service) or type(self.surface_runs) is not tuple:
            return False
        if len(self.surface_runs) != len(expected_surfaces) or any(
            type(run) is not tuple or len(run) != 3 for run in self.surface_runs
        ):
            return False
        surfaces = tuple(run[0] for run in self.surface_runs)
        services = tuple(run[1] for run in self.surface_runs)
        digests = tuple(run[2] for run in self.surface_runs)
        return bool(
            surfaces == expected_surfaces
            and all(service == self.shared_application_service for service in services)
            and all(_is_sha256(digest) for digest in digests)
            and len(set(digests)) == 1
        )

    def _promotion_is_valid(self) -> bool:
        expected_dimensions = ("FALSE_ACCEPTANCE", "QUALITY", "RUNTIME", "SECURITY")
        if type(self.promotion_gates) is not tuple or len(self.promotion_gates) != 4 or any(
            type(gate) is not tuple or len(gate) != 3 for gate in self.promotion_gates
        ):
            return False
        dimensions = tuple(gate[0] for gate in self.promotion_gates)
        results = tuple(gate[1] for gate in self.promotion_gates)
        digests = tuple(gate[2] for gate in self.promotion_gates)
        return bool(
            _has_text(self.corpus_version)
            and _is_sha256(self.corpus_digest)
            and self.corpus_stratified is True
            and dimensions == expected_dimensions
            and _strict_true(results)
            and all(_is_sha256(digest) for digest in digests)
            and self.promotion_requested is True
        )


@dataclass(frozen=True)
class SGVCalibrationEvidence:
    stratum_id: str
    profile_id: str
    profile_digest: str
    hard_invariants_immutable: bool
    profile_immutable: bool
    metric_declarations: tuple[tuple[str, str, str, str, str], ...]
    transfer_error: str
    error_distribution: str
    coverage_dimensions: tuple[str, ...]
    stability_checks: tuple[str, ...]
    local_deformation_measure: str
    missing_or_invalid: str

    def failed_requirements(self) -> tuple[str, ...]:
        checks = (
            ("REQ-SGVCAL-001", self._immutability_is_valid()),
            ("REQ-SGVCAL-002", self._metric_declarations_are_valid()),
            ("REQ-SGVCAL-003", self._error_distribution_is_valid()),
            ("REQ-SGVCAL-004", self._coverage_is_valid()),
            ("REQ-SGVCAL-005", self._stability_is_valid()),
            ("REQ-SGVCAL-006", self._deformation_is_valid()),
        )
        return tuple(requirement for requirement, passed in checks if not passed)

    def _fail_closed(self) -> bool:
        return self.missing_or_invalid == "REJECT"

    def _immutability_is_valid(self) -> bool:
        return bool(
            _has_text(self.stratum_id)
            and _has_text(self.profile_id)
            and _is_sha256(self.profile_digest)
            and _strict_true((self.hard_invariants_immutable, self.profile_immutable))
            and self._fail_closed()
        )

    def _metric_declarations_are_valid(self) -> bool:
        if type(self.metric_declarations) is not tuple or not self.metric_declarations:
            return False
        if any(
            type(metric) is not tuple or len(metric) != 5
            for metric in self.metric_declarations
        ):
            return False
        metric_ids = tuple(metric[0] for metric in self.metric_declarations)
        return bool(
            all(
                all(_has_text(value) for value in metric)
                for metric in self.metric_declarations
            )
            and len(metric_ids) == len(set(metric_ids))
            and self._fail_closed()
        )

    def _error_distribution_is_valid(self) -> bool:
        return bool(
            self.transfer_error == "SYMMETRIC"
            and self.error_distribution == "ROBUST"
            and self._fail_closed()
        )

    def _coverage_is_valid(self) -> bool:
        return self.coverage_dimensions == ("leverage", "spatial_support") and self._fail_closed()

    def _stability_is_valid(self) -> bool:
        required = ("conditioning", "degeneracy", "leave_one_out_stability")
        return self.stability_checks == required and self._fail_closed()

    def _deformation_is_valid(self) -> bool:
        return self.local_deformation_measure == "ADAPTIVE_JACOBIAN" and self._fail_closed()


@dataclass(frozen=True)
class DeliveryGovernanceEvidence:
    authorized_task: str
    issue_ready: bool
    dedicated_branch: bool
    short_lived_worktree: bool
    pull_request_required: bool
    direct_main_prohibited: bool
    automerge_prohibited: bool
    sensitive_gate_decision_by_codex: bool

    def is_valid(self) -> bool:
        return bool(
            _has_text(self.authorized_task)
            and _strict_true(
                (
                    self.issue_ready,
                    self.dedicated_branch,
                    self.short_lived_worktree,
                    self.pull_request_required,
                    self.direct_main_prohibited,
                    self.automerge_prohibited,
                )
            )
            and type(self.sensitive_gate_decision_by_codex) is bool
            and not self.sensitive_gate_decision_by_codex
        )


class DecisionRejected(ValueError):
    """Raised with requirement IDs when supplied evidence is not conformant."""

    def __init__(self, failed_requirements: list[str]) -> None:
        self.failed_requirements = tuple(failed_requirements)
        super().__init__(", ".join(self.failed_requirements))


def validate_functional_slice(evidence: FunctionalSliceEvidence) -> None:
    """Reject first-slice evidence unless FS1-008 through FS1-010 pass."""
    failed = (
        list(evidence.failed_requirements())
        if isinstance(evidence, FunctionalSliceEvidence)
        else ["REQ-FS1-008", "REQ-FS1-009", "REQ-FS1-010"]
    )
    if failed:
        raise DecisionRejected(failed)


def validate_sgv_calibration(evidence: SGVCalibrationEvidence) -> None:
    """Reject calibration evidence unless SGVCAL-001 through SGVCAL-006 pass."""
    failed = (
        list(evidence.failed_requirements())
        if isinstance(evidence, SGVCalibrationEvidence)
        else [f"REQ-SGVCAL-{index:03d}" for index in range(1, 7)]
    )
    if failed:
        raise DecisionRejected(failed)


def validate_delivery_governance(evidence: DeliveryGovernanceEvidence) -> None:
    """Reject delivery evidence that permits direct main, automerge, or gate decisions."""
    if not isinstance(evidence, DeliveryGovernanceEvidence) or not evidence.is_valid():
        raise DecisionRejected(["REQ-GOV-004"])
