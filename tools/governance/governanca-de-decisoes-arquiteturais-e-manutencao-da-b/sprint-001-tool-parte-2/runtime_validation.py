from __future__ import annotations

import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from execution_evidence import EXECUTION_AUTHORITY_FIELDS, execution_provenance_findings
from governed_authority import AUTHORITY_FIELDS, authority_findings
from record_contract import strict_fields
from repository_surfaces import revision_paths
from slice_one import Finding, git_blob, load_json_bytes, resolve_governed_artifact, revision_is_ancestor


LANE_FIELDS = frozenset({"record_type", "version", "state", "stable", "gates"}) | AUTHORITY_FIELDS
GATE_FIELDS = frozenset({"gate", "result", "artifact"})
GATE_EVIDENCE_FIELDS = frozenset({"record_type", "version", "gate", "result", "approvals"}) | EXECUTION_AUTHORITY_FIELDS
GATE_APPROVAL_FIELDS = frozenset({"record_type", "version", "gate", "result"}) | AUTHORITY_FIELDS
RUNTIME_GATES = frozenset({
    "SEPARATE_LOCK_AND_OCI_IMAGE", "PYTHON_STACK_COMPATIBILITY",
    "NATIVE_STACK_ABI", "FULL_TEST_SUITE", "PERFORMANCE_AND_MEMORY",
    "SUPPLY_CHAIN_AND_ROLLBACK", "ARCHITECT_AND_REVIEWER_APPROVAL",
})


def validate_python_runtime(
    repository_root: Path,
    source_revision: str,
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> list[Finding]:
    findings: list[Finding] = []
    try:
        paths = revision_paths(repository_root, source_revision)
        python_version = git_blob(repository_root, source_revision, ".python-version").decode("utf-8").strip()
        pyproject = tomllib.loads(git_blob(repository_root, source_revision, "pyproject.toml").decode("utf-8"))
    except (UnicodeDecodeError, ValueError, tomllib.TOMLDecodeError) as error:
        return [Finding("PYTHON_BASELINE_INVALID", source_revision, str(error))]
    expected = {
        ".python-version": (python_version, "3.12.13"),
        "requires_python": (pyproject.get("project", {}).get("requires-python"), ">=3.12,<3.13"),
        "ruff_target": (pyproject.get("tool", {}).get("ruff", {}).get("target-version"), "py312"),
        "mypy_python_version": (pyproject.get("tool", {}).get("mypy", {}).get("python_version"), "3.12"),
    }
    for field, (observed, required) in expected.items():
        if observed != required:
            findings.append(Finding("PYTHON_BASELINE_INVALID", field, f"repository value must equal {required}"))
    lane_paths = tuple(path for path in paths if path.startswith("evidence/operations/runtime/python-") and path.endswith(".json"))
    by_version: dict[str, Mapping[str, Any]] = {}
    for path in lane_paths:
        try:
            lane = load_json_bytes(git_blob(repository_root, source_revision, path))
        except ValueError as error:
            findings.append(Finding("PYTHON_LANE_EVIDENCE_INVALID", path, str(error)))
            continue
        findings.extend(strict_fields(lane, LANE_FIELDS, path))
        if not isinstance(lane, Mapping):
            continue
        version = lane.get("version")
        expected_version = path.removeprefix("evidence/operations/runtime/python-").removesuffix(".json")
        if version not in {"3.13", "3.14"} or version != expected_version:
            findings.append(Finding("PYTHON_LANES_INVALID", path, "only repository-bound 3.13 and 3.14 lanes are governed"))
        elif version not in by_version:
            by_version[version] = lane
        else:
            findings.append(Finding("PYTHON_LANES_INVALID", path, "duplicate lane"))
        findings.extend(
            _lane_findings(
                repository_root, source_revision, lane, path, delivery_gate
            )
        )
    lane_313, lane_314 = by_version.get("3.13"), by_version.get("3.14")
    if lane_314 and lane_314.get("state") in {"PROMOTED", "STABLE"}:
        if not lane_313 or lane_313.get("state") != "STABLE" or lane_313.get("stable") is not True:
            findings.append(Finding("PYTHON_314_PRECONDITION_MISSING", "$.lanes[1]", "3.13 must be stable first"))
    return sorted(findings)


def _lane_findings(
    repository_root: Path,
    source_revision: str,
    lane: Mapping[str, Any],
    field: str,
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    findings: list[Finding] = []
    if lane.get("record_type") != "PYTHON_RUNTIME_LANE_EVIDENCE":
        findings.append(Finding("PYTHON_LANE_EVIDENCE_INVALID", field, "wrong record type"))
    findings.extend(authority_findings(repository_root, delivery_gate=delivery_gate, artifact_path=field, artifact_revision=source_revision, payload=lane, expected_role="DevOps", required_reference="REQ-TOOL-001", field=field))
    state = lane.get("state")
    if state not in {"INACTIVE", "PROMOTED", "STABLE"}:
        findings.append(Finding("PYTHON_LANE_STATE_INVALID", f"{field}.state", "unknown state"))
    if not isinstance(lane.get("stable"), bool):
        findings.append(Finding("PYTHON_LANE_STATE_INVALID", f"{field}.stable", "must be boolean"))
    gates = lane.get("gates")
    if not isinstance(gates, list):
        return findings + [Finding("PYTHON_RUNTIME_GATE_INVALID", f"{field}.gates", "must be an array")]
    observed: dict[str, str] = {}
    for index, gate in enumerate(gates):
        gate_field = f"{field}.gates[{index}]"
        findings.extend(strict_fields(gate, GATE_FIELDS, gate_field))
        if isinstance(gate, Mapping) and isinstance(gate.get("gate"), str):
            if gate["gate"] in observed:
                findings.append(Finding("PYTHON_RUNTIME_GATE_INVALID", gate_field, "duplicate gate"))
            observed[gate["gate"]] = str(gate.get("result"))
            findings.extend(_runtime_gate_evidence_findings(repository_root, source_revision, lane, gate, gate_field, delivery_gate))
    if state in {"PROMOTED", "STABLE"} and (set(observed) != RUNTIME_GATES or any(result != "PASS" for result in observed.values())):
        findings.append(Finding("PYTHON_RUNTIME_GATE_INCOMPLETE", f"{field}.gates", "all AP-001 gates must PASS"))
    if state == "INACTIVE" and gates:
        findings.append(Finding("PYTHON_RUNTIME_GATE_REDUNDANT", f"{field}.gates", "inactive lane must not claim gates"))
    if state == "STABLE" and lane.get("stable") is not True:
        findings.append(Finding("PYTHON_LANE_STATE_INVALID", f"{field}.stable", "stable state requires true"))
    if state != "STABLE" and lane.get("stable") is not False:
        findings.append(Finding("PYTHON_LANE_STATE_INVALID", f"{field}.stable", "non-stable state requires false"))
    return findings


def _runtime_gate_evidence_findings(repository_root: Path, source_revision: str, lane: Mapping[str, Any], gate: Mapping[str, Any], field: str, delivery_gate: DeliveryApprovalGate | None) -> list[Finding]:
    reference = gate.get("artifact")
    if not isinstance(reference, Mapping):
        return [Finding("PYTHON_RUNTIME_GATE_EVIDENCE_INVALID", field, "artifact is required")]
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        payload = artifact.json_object()
    except ValueError as error:
        return [Finding("PYTHON_RUNTIME_GATE_EVIDENCE_INVALID", field, str(error))]
    findings = strict_fields(payload, GATE_EVIDENCE_FIELDS, field)
    expected = {"record_type": "PYTHON_RUNTIME_GATE_EVIDENCE", "version": lane.get("version"), "gate": gate.get("gate"), "result": "PASS"}
    if any(payload.get(key) != value for key, value in expected.items()):
        findings.append(Finding("PYTHON_RUNTIME_GATE_EVIDENCE_INVALID", field, "payload mismatch"))
    if not revision_is_ancestor(repository_root, artifact.source_revision, source_revision):
        findings.append(Finding("PYTHON_RUNTIME_GATE_EVIDENCE_INVALID", field, "revision is divergent"))
    findings.extend(execution_provenance_findings(repository_root, delivery_gate=delivery_gate, artifact_path=artifact.path, artifact_revision=artifact.source_revision, payload=payload, result_id=f"{lane.get('version')}:{gate.get('gate')}", expected_role="QA", required_reference="REQ-TOOL-001", field=field))
    findings.extend(_runtime_approval_findings(repository_root, payload, artifact.source_revision, field, delivery_gate))
    return findings


def _runtime_approval_findings(repository_root: Path, payload: Mapping[str, Any], gate_evidence_revision: str, field: str, delivery_gate: DeliveryApprovalGate | None) -> list[Finding]:
    references = payload.get("approvals")
    if payload.get("gate") != "ARCHITECT_AND_REVIEWER_APPROVAL":
        return [] if references == [] else [Finding("PYTHON_RUNTIME_GATE_EVIDENCE_INVALID", field, "unexpected approvals")]
    if not isinstance(references, list) or len(references) != 2:
        return [Finding("PYTHON_RUNTIME_GATE_EVIDENCE_INVALID", field, "two approvals required")]
    findings: list[Finding] = []
    for index, expected_role in enumerate(("Arquiteto", "Reviewer")):
        reference = references[index]
        proof_field = f"{field}.approvals[{index}]"
        try:
            artifact = resolve_governed_artifact(repository_root, reference)
            proof = artifact.json_object()
        except (TypeError, ValueError) as error:
            findings.append(Finding("PYTHON_RUNTIME_GATE_EVIDENCE_INVALID", proof_field, str(error)))
            continue
        findings.extend(strict_fields(proof, GATE_APPROVAL_FIELDS, proof_field))
        if artifact.source_revision == gate_evidence_revision or not revision_is_ancestor(repository_root, artifact.source_revision, gate_evidence_revision):
            findings.append(Finding("PYTHON_RUNTIME_GATE_EVIDENCE_INVALID", proof_field, "approval must strictly precede gate evidence"))
        expected = {"record_type": "PYTHON_RUNTIME_GATE_APPROVAL", "version": payload.get("version"), "gate": payload.get("gate"), "result": "PASS", "authority_role": expected_role, "reviewed_candidate_commit": payload.get("reviewed_candidate_commit")}
        if any(proof.get(name) != value for name, value in expected.items()):
            findings.append(Finding("PYTHON_RUNTIME_GATE_EVIDENCE_INVALID", proof_field, "approval mismatch"))
        findings.extend(authority_findings(repository_root, delivery_gate=delivery_gate, artifact_path=artifact.path, artifact_revision=artifact.source_revision, payload=proof, expected_role=expected_role, required_reference="REQ-TOOL-001", field=proof_field))
    return findings
