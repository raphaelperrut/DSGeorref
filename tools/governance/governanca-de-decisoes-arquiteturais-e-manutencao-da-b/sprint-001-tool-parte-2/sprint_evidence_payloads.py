from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from execution_evidence import execution_provenance_findings
from record_contract import reference_findings, strict_fields
from sprint_evidence_contract import (
    EVIDENCE_VALIDATOR_PATHS,
    TEST_EVIDENCE_FIELDS,
    VALIDATION_EVIDENCE_FIELDS,
)
from slice_one import Finding, resolve_governed_artifact, revision_is_ancestor


def resolve_evidence_reference(
    repository_root: Path,
    reference: Mapping[str, Any],
    field: str,
    source_revision: object,
) -> list[Finding]:
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
    except ValueError as error:
        return [Finding("GOVERNED_ARTIFACT_INVALID", field, str(error))]
    if not isinstance(source_revision, str) or not revision_is_ancestor(
        repository_root, artifact.source_revision, source_revision
    ):
        return [
            Finding(
                "EVIDENCE_REVISION_DIVERGENT",
                field,
                "artifact revision is not an ancestor",
            )
        ]
    return []


def validation_payload_findings(
    repository_root: Path,
    reference: Mapping[str, Any],
    field: str,
    evidence_type: object,
    source_revision: object,
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        payload = artifact.json_object()
    except ValueError as error:
        return [Finding("EVIDENCE_PAYLOAD_INVALID", field, str(error))]
    findings = strict_fields(payload, VALIDATION_EVIDENCE_FIELDS, field)
    expected = {
        "record_type": "SPRINT_VALIDATION_EVIDENCE",
        "evidence_type": evidence_type,
        "finding_codes": [],
    }
    if any(payload.get(name) != value for name, value in expected.items()):
        findings.append(
            Finding(
                "EVIDENCE_PAYLOAD_INVALID",
                field,
                "governed payload does not match the declared evidence",
            )
        )
    findings.extend(
        _validation_references(
            repository_root, payload, field, evidence_type, source_revision
        )
    )
    findings.extend(
        execution_provenance_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=payload,
            result_id=str(evidence_type),
            expected_role="QA",
            required_reference="STORY-0689",
            field=field,
        )
    )
    return findings


def _validation_references(
    repository_root: Path,
    payload: Mapping[str, Any],
    field: str,
    evidence_type: object,
    source_revision: object,
) -> list[Finding]:
    findings: list[Finding] = []
    for name in ("subject", "validator"):
        nested = payload.get(name)
        findings.extend(reference_findings(nested, f"{field}.{name}"))
        if isinstance(nested, Mapping):
            findings.extend(
                resolve_evidence_reference(
                    repository_root, nested, f"{field}.{name}", source_revision
                )
            )
    validator = payload.get("validator")
    candidate = payload.get("reviewed_candidate_commit")
    expected_path = EVIDENCE_VALIDATOR_PATHS.get(str(evidence_type))
    if not isinstance(validator, Mapping) or not str(
        validator.get("path", "")
    ).endswith(f"/{expected_path}"):
        findings.append(
            Finding(
                "EVIDENCE_PAYLOAD_INVALID",
                f"{field}.validator",
                "validator does not match the governed evidence kind",
            )
        )
    for name in ("subject", "validator"):
        nested = payload.get(name)
        if not isinstance(nested, Mapping) or nested.get("source_revision") != candidate:
            findings.append(
                Finding(
                    "EVIDENCE_PAYLOAD_INVALID",
                    f"{field}.{name}",
                    "subject and validator must come from the reviewed candidate",
                )
            )
    return findings


def test_payload_findings(
    repository_root: Path,
    reference: Mapping[str, Any],
    field: str,
    test_id: object,
    source_revision: object,
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        payload = artifact.json_object()
    except ValueError as error:
        return [Finding("EVIDENCE_PAYLOAD_INVALID", field, str(error))]
    findings = strict_fields(payload, TEST_EVIDENCE_FIELDS, field)
    if payload.get("record_type") != "SPRINT_TEST_EVIDENCE" or payload.get(
        "test_id"
    ) != test_id:
        findings.append(
            Finding("EVIDENCE_PAYLOAD_INVALID", field, "test identity is invalid")
        )
    findings.extend(
        execution_provenance_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=payload,
            result_id=str(test_id),
            expected_role="QA",
            required_reference="STORY-0689",
            field=field,
            report_key="report",
        )
    )
    return findings
