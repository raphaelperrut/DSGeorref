from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from decision_evidence_validation import (
    validate_contract_exercises,
    validate_diagnostic_claim,
)
from governed_authority import (
    AUTHORITY_FIELDS,
    authority_findings,
)
from record_contract import reference_findings, strict_fields
from repository_surfaces import python_capabilities, revision_paths
from slice_one import (
    Finding,
    resolve_governed_artifact,
    revision_is_ancestor,
    validate_foundation_closure,
)
from sprint_evidence_history import governed_sprint_evidence
from toolchain_validation import validate_make_ci_parity


CLOSURE_FIELDS = frozenset(
    {"record_type", "closure_id", "sprint_id", "closure_basis", "evidence_set"}
) | AUTHORITY_FIELDS


def validate_ci_capabilities(
    repository_root: Path, source_revision: str
) -> list[Finding]:
    try:
        paths = revision_paths(repository_root, source_revision)
    except ValueError as error:
        return [Finding("CI_CAPABILITIES_INVALID", source_revision, str(error))]
    capabilities = python_capabilities(paths)
    if not capabilities:
        return [
            Finding(
                "CI_CAPABILITIES_INVALID",
                source_revision,
                "repository revision has no present Python capabilities",
            )
        ]
    findings: list[Finding] = []
    for capability in capabilities:
        test_prefix = f"tests/{capability}/"
        if not any(
            path.startswith(test_prefix) and path.endswith(".py") for path in paths
        ):
            findings.append(
                Finding(
                    "CI_CAPABILITY_MISMATCH",
                    capability,
                    "present capability lacks repository-bound tests",
                )
            )
    findings.extend(validate_make_ci_parity(repository_root, source_revision))
    return sorted(findings)


def validate_sprint_closure(
    repository_root: Path,
    closure_reference: Mapping[str, Any],
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> list[Finding]:
    closure, closure_revision, findings = _governed_closure(
        repository_root, closure_reference, delivery_gate
    )
    if closure is None or closure_revision is None:
        return sorted(findings)
    findings.extend(strict_fields(closure, CLOSURE_FIELDS, "$"))
    if closure.get("record_type") != "SPRINT_CLOSURE" or closure.get("sprint_id") != "SPRINT-001":
        findings.append(Finding("CLOSURE_IDENTITY_INVALID", "$", "closure identity is invalid"))
    if closure.get("closure_basis") != "EVIDENCE":
        findings.append(Finding("CLOSURE_NOT_EVIDENCE_BASED", "$.closure_basis", "calendar closure is forbidden"))
    findings.extend(reference_findings(closure.get("evidence_set"), "$.evidence_set"))
    if isinstance(closure.get("evidence_set"), Mapping):
        evidence_set, evidence_findings = governed_sprint_evidence(
            repository_root,
            closure["evidence_set"],
            delivery_gate=delivery_gate,
        )
        findings.extend(evidence_findings)
        evidence_revision = closure["evidence_set"].get("source_revision")
        if (
            evidence_set is None
            or not isinstance(evidence_revision, str)
            or not revision_is_ancestor(
                repository_root, evidence_revision, closure_revision
            )
        ):
            findings.append(
                Finding(
                    "CLOSURE_EVIDENCE_DIVERGENT",
                    "$.evidence_set",
                    "governed evidence must precede the closure record",
                )
            )
    return sorted(findings)


def validate_cutover_preconditions(
    repository_root: Path,
    closure_reference: Mapping[str, Any],
    foundation_closure_reference: Mapping[str, Any],
    foundation_baseline: Mapping[str, Any],
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> list[Finding]:
    findings = validate_sprint_closure(
        repository_root, closure_reference, delivery_gate=delivery_gate
    )
    closure, _closure_revision, closure_findings = _governed_closure(
        repository_root, closure_reference, delivery_gate
    )
    findings.extend(closure_findings)
    evidence_set: Mapping[str, Any] = {}
    if closure is not None and isinstance(closure.get("evidence_set"), Mapping):
        governed, evidence_findings = governed_sprint_evidence(
            repository_root,
            closure["evidence_set"],
            delivery_gate=delivery_gate,
        )
        findings.extend(evidence_findings)
        if governed is not None:
            evidence_set = governed
    foundation_evidence_set, foundation_findings = _foundation_closure(
        repository_root,
        foundation_closure_reference,
        foundation_baseline,
        delivery_gate,
    )
    if foundation_findings:
        findings.append(
            Finding(
                "CUTOVER_FOUNDATION_EVIDENCE_INVALID",
                "foundation_evidence_set",
                "Foundation closure evidence is invalid",
            )
        )
        findings.extend(foundation_findings)
    proofs = foundation_evidence_set.get("proofs")
    if not isinstance(proofs, Mapping) or "G1_FOUNDATION_GATE_RESULT" not in proofs:
        findings.append(
            Finding("CUTOVER_G1_NOT_APPROVED", "foundation_evidence_set", "G1 proof is absent")
        )
    if not isinstance(proofs, Mapping) or "FIRST_SLICE_AUTHORIZATION" not in proofs:
        findings.append(
            Finding(
                "CUTOVER_NOT_AUTHORIZED",
                "foundation_evidence_set",
                "explicit first-slice authorization is absent",
            )
        )
    candidate = foundation_evidence_set.get("reviewed_candidate_commit")
    source_revision = evidence_set.get("source_revision")
    if not isinstance(candidate, str) or not isinstance(source_revision, str) or not (
        revision_is_ancestor(repository_root, candidate, source_revision)
    ):
        findings.append(
            Finding(
                "CUTOVER_COMMIT_LINK_MISMATCH",
                "foundation_evidence_set",
                "Sprint evidence is not descended from the reviewed foundation candidate",
            )
        )
    return sorted(findings)


def _foundation_closure(
    repository_root: Path,
    reference: Mapping[str, Any],
    baseline: Mapping[str, Any],
    delivery_gate: DeliveryApprovalGate | None,
) -> tuple[Mapping[str, Any], list[Finding]]:
    field = "foundation_closure_reference"
    findings = reference_findings(reference, field)
    try:
        closure_artifact = resolve_governed_artifact(repository_root, reference)
        closure = closure_artifact.json_object()
    except ValueError as error:
        findings.append(
            Finding(
                "CUTOVER_FOUNDATION_EVIDENCE_INVALID",
                field,
                str(error),
            )
        )
        return {}, findings
    evidence_reference = closure.get("evidence_set")
    findings.extend(reference_findings(evidence_reference, f"{field}.evidence_set"))
    if not isinstance(evidence_reference, Mapping):
        return {}, findings
    try:
        evidence_artifact = resolve_governed_artifact(
            repository_root, evidence_reference
        )
        record = evidence_artifact.json_object()
    except ValueError as error:
        findings.append(
            Finding(
                "CUTOVER_FOUNDATION_EVIDENCE_INVALID",
                f"{field}.evidence_set",
                str(error),
            )
        )
        return {}, findings
    if not revision_is_ancestor(
        repository_root,
        evidence_artifact.source_revision,
        closure_artifact.source_revision,
    ):
        findings.append(
            Finding(
                "CUTOVER_FOUNDATION_EVIDENCE_INVALID",
                f"{field}.evidence_set",
                "foundation evidence must precede its governed closure record",
            )
        )
    findings.extend(
        validate_foundation_closure(
            repository_root, dict(closure), record, baseline
        )
    )
    required_proofs = (
        ("G1_FOUNDATION_GATE_RESULT", "Reviewer", "G1 Foundation"),
        ("FIRST_SLICE_AUTHORIZATION", "Product Owner", "REQ-SPRINT-001-010"),
    )
    proof_entries = record.get("proofs")
    if not isinstance(proof_entries, Mapping):
        return record, findings
    for proof_name, role, required_reference in required_proofs:
        proof_entry = proof_entries.get(proof_name)
        if not isinstance(proof_entry, Mapping) or not isinstance(
            proof_entry.get("artifact"), Mapping
        ):
            continue
        try:
            proof_artifact = resolve_governed_artifact(
                repository_root, proof_entry["artifact"]
            )
            proof = proof_artifact.json_object()
        except ValueError as error:
            findings.append(
                Finding("CUTOVER_G1_NOT_APPROVED", field, str(error))
            )
        else:
            findings.extend(
                authority_findings(
                    repository_root,
                    delivery_gate=delivery_gate,
                    artifact_path=proof_artifact.path,
                    artifact_revision=proof_artifact.source_revision,
                    payload=proof,
                    expected_role=role,
                    required_reference=required_reference,
                    field=f"{field}.{proof_name}",
                )
            )
    return record, findings


def _governed_closure(
    repository_root: Path,
    reference: Mapping[str, Any],
    delivery_gate: DeliveryApprovalGate | None,
) -> tuple[Mapping[str, Any] | None, str | None, list[Finding]]:
    findings = reference_findings(reference, "closure_reference")
    try:
        artifact = resolve_governed_artifact(repository_root, reference)
        closure = artifact.json_object()
    except ValueError as error:
        findings.append(
            Finding("CLOSURE_RECORD_INVALID", "closure_reference", str(error))
        )
        return None, None, findings
    findings.extend(
        authority_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=closure,
            expected_role="QA",
            required_reference="REQ-SPRINT-001-009",
            field="closure_reference",
        )
    )
    return closure, artifact.source_revision, findings
