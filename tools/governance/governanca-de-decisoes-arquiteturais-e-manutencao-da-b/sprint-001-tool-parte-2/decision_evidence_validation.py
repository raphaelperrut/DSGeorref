from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from execution_evidence import EXECUTION_AUTHORITY_FIELDS, execution_provenance_findings
from governed_authority import AUTHORITY_FIELDS, authority_findings
from record_contract import reference_findings, strict_fields
from slice_one import Finding, canonical_json_bytes, resolve_governed_artifact


DIAGNOSTIC_FIELDS = frozenset(
    {
        "record_type",
        "synthetic",
        "end_to_end",
        "functional_georeferencing_claimed",
        "result",
    }
) | EXECUTION_AUTHORITY_FIELDS
CONTRACT_MANIFEST_FIELDS = frozenset({"record_type", "contracts"}) | AUTHORITY_FIELDS
EXERCISE_FIELDS = frozenset({"contract", "evidence"})
CONTRACT_EVIDENCE_FIELDS = frozenset(
    {"record_type", "contract_sha256", "result"}
) | EXECUTION_AUTHORITY_FIELDS


def validate_contract_exercises(
    repository_root: Path,
    manifest_reference: Mapping[str, Any],
    exercises: Sequence[Mapping[str, Any]],
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> list[Finding]:
    required_contracts, findings = _essential_contracts(
        repository_root, manifest_reference, delivery_gate
    )
    required_keys: list[bytes] = []
    for index, reference in enumerate(required_contracts):
        field = f"required_contracts[{index}]"
        findings.extend(reference_findings(reference, field))
        findings.extend(_resolve(repository_root, reference, field))
        required_keys.append(canonical_json_bytes(reference))
    if not required_keys or len(required_keys) != len(set(required_keys)):
        findings.append(
            Finding(
                "CONTRACT_SET_INVALID",
                "required_contracts",
                "must be non-empty and unique",
            )
        )
    exercised_keys: list[bytes] = []
    for index, exercise in enumerate(exercises):
        field = f"exercises[{index}]"
        findings.extend(strict_fields(exercise, EXERCISE_FIELDS, field))
        if not isinstance(exercise, Mapping):
            continue
        contract = exercise.get("contract")
        evidence = exercise.get("evidence")
        findings.extend(reference_findings(contract, f"{field}.contract"))
        findings.extend(reference_findings(evidence, f"{field}.evidence"))
        if isinstance(contract, Mapping):
            exercised_keys.append(canonical_json_bytes(contract))
            findings.extend(_resolve(repository_root, contract, f"{field}.contract"))
        if isinstance(evidence, Mapping):
            findings.extend(
                _contract_evidence_findings(
                    repository_root, evidence, contract, f"{field}.evidence"
                    , delivery_gate
                )
            )
    if sorted(exercised_keys) != sorted(required_keys):
        findings.append(
            Finding(
                "CONTRACT_EXERCISE_MISMATCH",
                "exercises",
                "must exercise exactly essential contracts",
            )
        )
    return sorted(findings)


def validate_diagnostic_claim(
    repository_root: Path,
    evidence_reference: Mapping[str, Any],
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> list[Finding]:
    findings = reference_findings(evidence_reference, "$")
    try:
        artifact = resolve_governed_artifact(repository_root, evidence_reference)
        record = artifact.json_object()
    except ValueError as error:
        findings.append(Finding("DIAGNOSTIC_EVIDENCE_INVALID", "$", str(error)))
        return sorted(findings)
    findings.extend(strict_fields(record, DIAGNOSTIC_FIELDS, "$"))
    expected = {
        "record_type": "SYNTHETIC_DIAGNOSTIC_EVIDENCE",
        "synthetic": True,
        "end_to_end": True,
        "functional_georeferencing_claimed": False,
        "result": "PASS",
    }
    for field, value in expected.items():
        if record.get(field) != value:
            code = (
                "FUNCTIONAL_GEOREFERENCE_CLAIMED"
                if field == "functional_georeferencing_claimed"
                else "DIAGNOSTIC_EVIDENCE_INVALID"
            )
            findings.append(Finding(code, f"$.{field}", f"must equal {value!r}"))
    findings.extend(
        execution_provenance_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=record,
            result_id="REQ-SPRINT-001-006",
            expected_role="QA",
            required_reference="REQ-SPRINT-001-006",
            field="$",
        )
    )
    return sorted(findings)


def _essential_contracts(
    repository_root: Path,
    reference: Mapping[str, Any],
    delivery_gate: DeliveryApprovalGate | None,
) -> tuple[list[Mapping[str, Any]], list[Finding]]:
    findings = reference_findings(reference, "manifest_reference")
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        manifest = artifact.json_object()
    except ValueError as error:
        findings.append(
            Finding("CONTRACT_MANIFEST_INVALID", "manifest_reference", str(error))
        )
        return [], findings
    findings.extend(strict_fields(manifest, CONTRACT_MANIFEST_FIELDS, "manifest"))
    findings.extend(
        authority_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=manifest,
            expected_role="Arquiteto",
            required_reference="REQ-SPRINT-001-005",
            field="manifest",
        )
    )
    contracts = manifest.get("contracts")
    if not isinstance(contracts, list):
        findings.append(
            Finding("CONTRACT_MANIFEST_INVALID", "manifest.contracts", "array required")
        )
        return [], findings
    candidate = manifest.get("reviewed_candidate_commit")
    governed: list[Mapping[str, Any]] = []
    for index, contract in enumerate(contracts):
        field = f"manifest.contracts[{index}]"
        findings.extend(reference_findings(contract, field))
        if isinstance(contract, Mapping):
            governed.append(contract)
            findings.extend(_resolve(repository_root, contract, field))
            if contract.get("source_revision") != candidate:
                findings.append(
                    Finding(
                        "CONTRACT_MANIFEST_INVALID",
                        field,
                        "contract must come from the reviewed candidate",
                    )
                )
    return governed, findings


def _resolve(
    repository_root: Path, reference: Mapping[str, Any], field: str
) -> list[Finding]:
    try:
        resolve_governed_artifact(repository_root, reference)
    except ValueError as error:
        return [Finding("GOVERNED_ARTIFACT_INVALID", field, str(error))]
    return []


def _contract_evidence_findings(
    repository_root: Path,
    reference: Mapping[str, Any],
    contract: object,
    field: str,
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        payload = artifact.json_object()
    except ValueError as error:
        return [Finding("CONTRACT_EVIDENCE_INVALID", field, str(error))]
    findings = strict_fields(payload, CONTRACT_EVIDENCE_FIELDS, field)
    expected_digest = contract.get("sha256") if isinstance(contract, Mapping) else None
    expected = {
        "record_type": "CONTRACT_EXERCISE_EVIDENCE",
        "contract_sha256": expected_digest,
        "result": "PASS",
    }
    for name, value in expected.items():
        if payload.get(name) != value:
            findings.append(
                Finding(
                    "CONTRACT_EVIDENCE_INVALID",
                    f"{field}.{name}",
                    "evidence does not match exercise",
                )
            )
    findings.extend(
        execution_provenance_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=payload,
            result_id=str(expected_digest),
            expected_role="QA",
            required_reference="REQ-SPRINT-001-005",
            field=field,
        )
    )
    return findings
