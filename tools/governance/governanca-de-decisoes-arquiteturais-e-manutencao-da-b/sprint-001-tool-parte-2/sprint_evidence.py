from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from delivery_approval import DeliveryApprovalGate
from record_contract import ordered_unique_strings, reference_findings, strict_fields
from sprint_evidence_contract import (
    ARTIFACT_FIELDS,
    EVIDENCE_FIELDS,
    REQUIRED_DECISIONS,
    REQUIRED_EVIDENCE_KINDS,
    REQUIRED_REQUIREMENTS,
    REQUIRED_TESTS,
    TEST_FIELDS,
    ZERO_DIGEST,
)
from sprint_evidence_history import SprintEvidenceLedger
from sprint_evidence_payloads import (
    resolve_evidence_reference,
    test_payload_findings,
    validation_payload_findings,
)
from slice_one import (
    COMMIT_PATTERN,
    Finding,
    canonical_json_bytes,
    require_valid,
)


def build_sprint_evidence_set(
    repository_root: Path,
    *,
    schema_version: str,
    evidence_set_id: str,
    sprint_id: str,
    source_revision: str,
    artifacts: Sequence[Mapping[str, Any]],
    requirements: Sequence[str],
    tests: Sequence[Mapping[str, Any]],
    decisions: Sequence[int],
    digest_algorithm: str,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": schema_version,
        "record_type": "SPRINT_EVIDENCE_SET",
        "evidence_set_id": evidence_set_id,
        "sprint_id": sprint_id,
        "source_revision": source_revision,
        "artifacts": [dict(item) for item in artifacts],
        "requirements": list(requirements),
        "tests": [dict(item) for item in tests],
        "decisions": list(decisions),
        "digest_algorithm": digest_algorithm,
        "evidence_set_digest": ZERO_DIGEST,
    }
    record["evidence_set_digest"] = hashlib.sha256(canonical_json_bytes(record)).hexdigest()
    require_valid(
        validate_sprint_evidence_set(
            repository_root, record, delivery_gate=delivery_gate
        )
    )
    return record


def validate_sprint_evidence_set(
    repository_root: Path,
    record: Mapping[str, Any],
    *,
    delivery_gate: DeliveryApprovalGate | None = None,
) -> list[Finding]:
    findings = strict_fields(record, EVIDENCE_FIELDS, "$")
    if findings:
        return sorted(findings)
    findings.extend(_identity_findings(record))
    findings.extend(_collection_findings(repository_root, record, delivery_gate))
    projection = dict(record)
    projection["evidence_set_digest"] = ZERO_DIGEST
    expected = hashlib.sha256(canonical_json_bytes(projection)).hexdigest()
    if record.get("evidence_set_digest") != expected:
        findings.append(Finding("EVIDENCE_DIGEST_MISMATCH", "$.evidence_set_digest", "digest differs"))
    return sorted(findings)


def _identity_findings(record: Mapping[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "schema_version": "1.0.0",
        "record_type": "SPRINT_EVIDENCE_SET",
        "sprint_id": "SPRINT-001",
        "digest_algorithm": "SHA-256",
    }
    for field, expected in expected_values.items():
        if record.get(field) != expected:
            findings.append(Finding("EVIDENCE_IDENTITY_INVALID", f"$.{field}", f"must equal {expected}"))
    if not isinstance(record.get("evidence_set_id"), str) or not record["evidence_set_id"]:
        findings.append(Finding("EVIDENCE_IDENTITY_INVALID", "$.evidence_set_id", "must be non-empty"))
    revision = record.get("source_revision")
    if not isinstance(revision, str) or COMMIT_PATTERN.fullmatch(revision) is None:
        findings.append(Finding("EVIDENCE_REVISION_INVALID", "$.source_revision", "full commit required"))
    return findings


def _collection_findings(
    repository_root: Path,
    record: Mapping[str, Any],
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_artifact_findings(repository_root, record, delivery_gate))
    findings.extend(ordered_unique_strings(record.get("requirements"), "$.requirements"))
    if record.get("requirements") != list(REQUIRED_REQUIREMENTS):
        findings.append(
            Finding(
                "EVIDENCE_REQUIREMENTS_INCOMPLETE",
                "$.requirements",
                "applicable Slice 2 requirements must be exact",
            )
        )
    decisions = record.get("decisions")
    if decisions != list(REQUIRED_DECISIONS):
        findings.append(Finding("EVIDENCE_DECISIONS_INCOMPLETE", "$.decisions", "AP-008 decisions are incomplete"))
    findings.extend(_test_findings(repository_root, record, delivery_gate))
    return findings


def _artifact_findings(
    repository_root: Path,
    record: Mapping[str, Any],
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    artifacts = record.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return [Finding("EVIDENCE_INCOMPLETE", "$.artifacts", "at least one governed artifact is required")]
    findings: list[Finding] = []
    keys: list[tuple[str, str, str, str]] = []
    for index, artifact in enumerate(artifacts):
        field = f"$.artifacts[{index}]"
        findings.extend(strict_fields(artifact, ARTIFACT_FIELDS, field))
        if not isinstance(artifact, Mapping):
            continue
        reference = {name: artifact.get(name) for name in ("source_revision", "path", "sha256")}
        findings.extend(reference_findings(reference, field))
        kind = artifact.get("kind")
        if not isinstance(kind, str) or not kind:
            findings.append(Finding("EVIDENCE_KIND_INVALID", f"{field}.kind", "must be non-empty"))
        keys.append((str(kind), str(artifact.get("path")), str(artifact.get("source_revision")), str(artifact.get("sha256"))))
        findings.extend(resolve_evidence_reference(repository_root, reference, field, record.get("source_revision")))
    if keys != sorted(set(keys)):
        findings.append(Finding("EVIDENCE_ARTIFACTS_NON_CANONICAL", "$.artifacts", "must be sorted and unique"))
    kinds = [key[0] for key in keys]
    if kinds != list(REQUIRED_EVIDENCE_KINDS):
        findings.append(
            Finding(
                "EVIDENCE_KINDS_INCOMPLETE",
                "$.artifacts",
                "required validation evidence kinds must be exact",
            )
        )
    for index, artifact in enumerate(artifacts):
        if isinstance(artifact, Mapping):
            findings.extend(
                validation_payload_findings(
                    repository_root,
                    artifact,
                    f"$.artifacts[{index}]",
                    artifact.get("kind"),
                    record.get("source_revision"),
                    delivery_gate,
                )
            )
    return findings


def _test_findings(
    repository_root: Path,
    record: Mapping[str, Any],
    delivery_gate: DeliveryApprovalGate | None,
) -> list[Finding]:
    tests = record.get("tests")
    if not isinstance(tests, list) or not tests:
        return [Finding("EVIDENCE_INCOMPLETE", "$.tests", "at least one passing test is required")]
    findings: list[Finding] = []
    identifiers: list[str] = []
    for index, test in enumerate(tests):
        field = f"$.tests[{index}]"
        findings.extend(strict_fields(test, TEST_FIELDS, field))
        if not isinstance(test, Mapping):
            continue
        test_id = test.get("test_id")
        if not isinstance(test_id, str) or not test_id:
            findings.append(Finding("TEST_EVIDENCE_INVALID", f"{field}.test_id", "must be non-empty"))
        identifiers.append(str(test_id))
        if test.get("result") != "PASS":
            findings.append(Finding("TEST_EVIDENCE_INVALID", f"{field}.result", "must be PASS"))
        findings.extend(reference_findings(test.get("artifact"), f"{field}.artifact"))
        if isinstance(test.get("artifact"), Mapping):
            findings.extend(resolve_evidence_reference(repository_root, test["artifact"], f"{field}.artifact", record.get("source_revision")))
    if identifiers != sorted(set(identifiers)):
        findings.append(Finding("TEST_EVIDENCE_NON_CANONICAL", "$.tests", "must be sorted and unique"))
    if identifiers != list(REQUIRED_TESTS):
        findings.append(
            Finding(
                "TEST_EVIDENCE_INCOMPLETE",
                "$.tests",
                "all canonical Slice 2 tests require evidence",
            )
        )
    for index, test in enumerate(tests):
        if isinstance(test, Mapping) and isinstance(test.get("artifact"), Mapping):
            findings.extend(
                test_payload_findings(
                    repository_root,
                    test["artifact"],
                    f"$.tests[{index}].artifact",
                    test.get("test_id"),
                    record.get("source_revision"),
                    delivery_gate,
                )
            )
    return findings


def sprint_evidence_human_summary(record: Mapping[str, Any]) -> str:
    requirements = ", ".join(str(item) for item in record.get("requirements", []))
    return (
        f"{record.get('evidence_set_id')} @ {record.get('source_revision')}: "
        f"{len(record.get('artifacts', []))} artifacts; "
        f"{len(record.get('tests', []))} passing tests; requirements {requirements}."
    )
