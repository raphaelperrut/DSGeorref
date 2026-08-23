from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from governed_authority import (
    AUTHORITY_FIELDS,
    authority_findings,
)
from record_contract import reference_findings, strict_fields
from slice_one import Finding, resolve_governed_artifact, revision_is_ancestor


EXECUTION_AUTHORITY_FIELDS = frozenset(
    {
        "authority_role",
        "task_id",
        "issue_id",
        "story_id",
        "reviewed_candidate_commit",
        "execution_report",
        "execution_authority",
    }
)


def execution_provenance_findings(
    repository_root: Path,
    *,
    delivery_gate: DeliveryApprovalGate | None,
    artifact_path: str,
    artifact_revision: str,
    payload: Mapping[str, Any],
    result_id: str,
    expected_role: str,
    required_reference: str,
    field: str,
    report_key: str = "execution_report",
) -> list[Finding]:
    findings = authority_findings(
        repository_root,
        delivery_gate=delivery_gate,
        artifact_path=artifact_path,
        artifact_revision=artifact_revision,
        payload=payload,
        expected_role=expected_role,
        required_reference=required_reference,
        field=field,
    )
    report = payload.get(report_key)
    execution_authority = payload.get("execution_authority")
    report_field = f"{field}.{report_key}"
    findings.extend(reference_findings(report, report_field))
    findings.extend(
        strict_fields(
            execution_authority,
            AUTHORITY_FIELDS,
            f"{field}.execution_authority",
        )
    )
    if not isinstance(report, Mapping) or not isinstance(
        execution_authority, Mapping
    ):
        return findings
    try:
        artifact = resolve_governed_artifact(repository_root, report)
        content = artifact.content.decode("utf-8")
    except (UnicodeDecodeError, ValueError) as error:
        return findings + [Finding("EXECUTION_PROVENANCE_INVALID", report_field, str(error))]
    if artifact.source_revision == artifact_revision or not revision_is_ancestor(
        repository_root, artifact.source_revision, artifact_revision
    ):
        findings.append(
            Finding(
                "EXECUTION_PROVENANCE_INVALID",
                report_field,
                "execution report must strictly precede its assurance artifact",
            )
        )
    if f"{result_id}: PASS" not in content.splitlines():
        findings.append(
            Finding(
                "EXECUTION_PROVENANCE_INVALID",
                report_field,
                "report has no exact governed PASS result",
            )
        )
    findings.extend(
        authority_findings(
            repository_root,
            delivery_gate=delivery_gate,
            artifact_path=artifact.path,
            artifact_revision=artifact.source_revision,
            payload=execution_authority,
            expected_role="DevOps",
            required_reference=required_reference,
            field=report_field,
            approval_revision=artifact_revision,
        )
    )
    if execution_authority.get("reviewed_candidate_commit") != payload.get(
        "reviewed_candidate_commit"
    ):
        findings.append(
            Finding(
                "EXECUTION_PROVENANCE_INVALID",
                f"{field}.execution_authority",
                "execution and assurance must review the same candidate",
            )
        )
    return findings
