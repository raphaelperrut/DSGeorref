"""Fail-closed evidence controls for batch and first-slice admission."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from pathlib import Path, PureWindowsPath


def _has_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_sha256(value: object) -> bool:
    hexadecimal = "0123456789abcdef"
    return isinstance(value, str) and len(value) == 64 and all(c in hexadecimal for c in value)


def _all_strict_true(values: tuple[object, ...]) -> bool:
    return all(type(value) is bool and value for value in values)


def _path_is_authorized(path: object, root: object, roots: object) -> bool:
    if not (_has_text(path) and _has_text(root) and type(roots) is tuple):
        return False
    if not roots or not all(_has_text(item) for item in roots):
        return False
    windows_drives = tuple(PureWindowsPath(value).drive for value in (path, root))
    if any(
        drive.startswith("\\\\")
        and not (
            len(drive) == 6
            and drive.startswith("\\\\?\\")
            and drive[4].isalpha()
            and drive[5] == ":"
        )
        for drive in windows_drives
    ):
        return False
    candidate = Path(path)
    registered_root = Path(root)
    if not candidate.is_absolute() or not registered_root.is_absolute():
        return False
    if registered_root not in map(Path, roots):
        return False
    try:
        candidate.relative_to(registered_root)
    except ValueError:
        return False
    return candidate != registered_root and ".." not in candidate.parts


@dataclass(frozen=True)
class BatchExecutionEvidence:
    control_action: str
    request_scope: str
    work_unit_scope: str
    persistent_control_token: str
    safe_point_reached: bool
    lease_store: str
    lease_generation: int
    fencing_token: int
    lease_renewable: bool
    lease_owned: bool
    revision_valid: bool
    resource_budgets_satisfied: bool
    backpressure_applied: bool
    progress_history: tuple[int, ...]
    total_work_units: int
    progress_persisted: bool
    eta_seconds: float | None
    eta_confidence: float | None
    scale_ladder: tuple[int, ...]
    fault_injection_passed: bool
    invariant_results: tuple[bool, ...]

    def failed_requirements(self) -> tuple[str, ...]:
        scoped_control = bool(
            self.control_action in ("CANCEL", "PAUSE")
            and _has_text(self.request_scope)
            and self.request_scope == self.work_unit_scope
            and _has_text(self.persistent_control_token)
            and self.safe_point_reached is True
        )
        governed_concurrency = bool(
            self.lease_store == "POSTGRESQL"
            and type(self.lease_generation) is int
            and self.lease_generation > 0
            and type(self.fencing_token) is int
            and self.fencing_token > 0
            and _all_strict_true(
                (
                    self.lease_owned,
                    self.lease_renewable,
                    self.revision_valid,
                    self.resource_budgets_satisfied,
                    self.backpressure_applied,
                )
            )
        )
        progress = self._progress_is_valid()
        promotion = self._promotion_is_valid()
        checks = (
            ("REQ-BEX-007", scoped_control),
            ("REQ-BEX-008", governed_concurrency),
            ("REQ-BEX-009", progress),
            ("REQ-BEX-010", promotion),
        )
        return tuple(requirement for requirement, passed in checks if not passed)

    def _progress_is_valid(self) -> bool:
        units_are_valid = bool(
            type(self.total_work_units) is int
            and self.total_work_units > 0
            and type(self.progress_history) is tuple
            and self.progress_history
            and all(
                type(unit) is int and 0 <= unit <= self.total_work_units
                for unit in self.progress_history
            )
            and self.progress_history == tuple(sorted(self.progress_history))
        )
        eta_unknown = self.eta_seconds is None and self.eta_confidence is None
        eta_supported = bool(
            type(self.eta_seconds) in {int, float}
            and isfinite(self.eta_seconds)
            and self.eta_seconds >= 0
            and type(self.eta_confidence) in {int, float}
            and isfinite(self.eta_confidence)
            and 0 <= self.eta_confidence <= 1
        )
        return units_are_valid and self.progress_persisted is True and (eta_unknown or eta_supported)

    def _promotion_is_valid(self) -> bool:
        ladder = self.scale_ladder
        return bool(
            type(ladder) is tuple
            and len(ladder) >= 2
            and all(type(step) is int and step > 0 for step in ladder)
            and all(left < right for left, right in zip(ladder, ladder[1:]))
            and self.fault_injection_passed is True
            and type(self.invariant_results) is tuple
            and len(self.invariant_results) >= 2
            and _all_strict_true(self.invariant_results)
        )


@dataclass(frozen=True)
class ExternalFileEvidence:
    file_path: str
    registered_root: str
    registered_roots: tuple[str, ...]
    regular_file: bool
    symlink_free: bool
    size_within_limit: bool
    decompression_within_limit: bool
    scanner_available: bool
    scanner_clean: bool
    sha256_digest: str

    def path_is_authorized(self) -> bool:
        return bool(
            _path_is_authorized(self.file_path, self.registered_root, self.registered_roots)
            and self.regular_file is True
            and self.symlink_free is True
        )

    def is_safe(self) -> bool:
        return bool(
            self.path_is_authorized()
            and _all_strict_true(
                (
                    self.regular_file,
                    self.symlink_free,
                    self.size_within_limit,
                    self.decompression_within_limit,
                    self.scanner_available,
                    self.scanner_clean,
                )
            )
            and _is_sha256(self.sha256_digest)
        )


@dataclass(frozen=True)
class SprintFoundationAuthorization:
    authorized_sprints: tuple[str, ...]
    final_approval: bool
    foundation_gate_executable: bool
    foundation_gate_passed: bool
    functional_implementation_requested: bool

    def is_valid(self) -> bool:
        booleans_are_strict = all(
            type(value) is bool
            for value in (
                self.final_approval,
                self.foundation_gate_executable,
                self.foundation_gate_passed,
                self.functional_implementation_requested,
            )
        )
        functional_gate_satisfied = not self.functional_implementation_requested or self.foundation_gate_passed
        return bool(
            booleans_are_strict
            and type(self.authorized_sprints) is tuple
            and self.authorized_sprints == ("SPRINT-001",)
            and self.final_approval
            and self.foundation_gate_executable
            and functional_gate_satisfied
        )


@dataclass(frozen=True)
class FirstFunctionalSliceEvidence:
    target: ExternalFileEvidence
    reference: ExternalFileEvidence
    originals_preserved: bool
    metadata_complete: bool
    ingest_fail_closed: bool
    classic_pipeline_id: str
    pipeline_runs: tuple[str, ...]
    pipeline_substitutable: bool
    correspondence_audit_reference: str
    sgv_profile_id: str
    sgv_applied: bool
    sgv_result: str
    critical_metrics_complete: bool
    hard_gates_passed: bool
    grey_zone: bool

    def failed_requirements(self) -> tuple[str, ...]:
        local_inputs = self.target.path_is_authorized() and self.reference.path_is_authorized()
        ingest = bool(
            self.target.is_safe()
            and self.reference.is_safe()
            and self.originals_preserved is True
            and self.metadata_complete is True
            and self.ingest_fail_closed is True
        )
        deterministic_pipeline = bool(
            _has_text(self.classic_pipeline_id)
            and type(self.pipeline_runs) is tuple
            and len(self.pipeline_runs) >= 2
            and all(run == self.classic_pipeline_id for run in self.pipeline_runs)
            and self.pipeline_substitutable is True
            and _has_text(self.correspondence_audit_reference)
        )
        sgv = self._sgv_is_valid()
        checks = (
            ("REQ-FS1-002", local_inputs),
            ("REQ-FS1-003", ingest),
            ("REQ-FS1-005", deterministic_pipeline),
            ("REQ-FS1-007", sgv),
        )
        return tuple(requirement for requirement, passed in checks if not passed)

    def _sgv_is_valid(self) -> bool:
        booleans_are_strict = all(
            type(value) is bool
            for value in (
                self.sgv_applied,
                self.critical_metrics_complete,
                self.hard_gates_passed,
                self.grey_zone,
            )
        )
        expected_result = "REJECTED"
        if self.critical_metrics_complete and self.hard_gates_passed:
            expected_result = "REVIEWABLE" if self.grey_zone else "ACCEPTED"
        return bool(
            booleans_are_strict
            and _has_text(self.sgv_profile_id)
            and self.sgv_applied
            and self.sgv_result in ("ACCEPTED", "REVIEWABLE", "REJECTED")
            and self.sgv_result == expected_result
        )


class DecisionRejected(ValueError):
    """Raised with requirement IDs when supplied evidence is not conformant."""

    def __init__(self, failed_requirements: list[str]) -> None:
        self.failed_requirements = tuple(failed_requirements)
        super().__init__(", ".join(self.failed_requirements))


def validate_batch_execution(evidence: BatchExecutionEvidence) -> None:
    """Reject batch evidence unless BEX-007 through BEX-010 are satisfied."""
    failed = list(evidence.failed_requirements())
    if failed:
        raise DecisionRejected(failed)


def validate_external_file(evidence: ExternalFileEvidence) -> None:
    """Reject untrusted files unless path, limits, scanner and hash are valid."""
    if not evidence.is_safe():
        raise DecisionRejected(["REQ-EPIC-041"])


def validate_sprint_authorization(evidence: SprintFoundationAuthorization) -> None:
    """Reject approval beyond Sprint 001 or functional work before its gate."""
    if not evidence.is_valid():
        raise DecisionRejected(["REQ-FRZ-002"])


def validate_first_functional_slice(evidence: FirstFunctionalSliceEvidence) -> None:
    """Reject first-slice evidence unless every owned FS1 control is satisfied."""
    failed = list(evidence.failed_requirements())
    if failed:
        raise DecisionRejected(failed)
