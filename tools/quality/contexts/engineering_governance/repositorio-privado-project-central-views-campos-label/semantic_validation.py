from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from artifact_validation import BundleDocuments
from contract_catalog import BUNDLES
from validation_types import Finding, mismatch


def _requirement_evidence(documents: dict[str, BundleDocuments]) -> tuple[set[str], list[Finding]]:
    requirement_ids: set[str] = set()
    findings: list[Finding] = []
    for name in ("foundation", "worker"):
        manifest = documents[name].manifest
        artifact = BUNDLES[0 if name == "foundation" else 1].manifest.as_posix()
        requirements = manifest.get("requirements")
        proof = manifest.get("proof")
        if not isinstance(requirements, list) or not isinstance(proof, dict):
            findings.append(
                Finding(
                    artifact,
                    "REQUIREMENT_EVIDENCE_MISSING",
                    "requirements and proof are required",
                )
            )
            continue
        tests: set[str] = set()
        for entry in requirements:
            if not isinstance(entry, dict):
                findings.append(
                    Finding(
                        artifact,
                        "REQUIREMENT_EVIDENCE_MISSING",
                        "invalid requirement entry",
                    )
                )
                continue
            requirement = entry.get("id")
            test = entry.get("test")
            failure_modes = entry.get("failure_modes")
            if not isinstance(requirement, str) or not isinstance(test, str) or not failure_modes:
                findings.append(Finding(artifact, "REQUIREMENT_EVIDENCE_MISSING", repr(entry)))
                continue
            if requirement in requirement_ids:
                findings.append(Finding(artifact, "REQUIREMENT_DUPLICATE", requirement))
            requirement_ids.add(requirement)
            tests.add(test)
        findings.extend(
            mismatch(
                set(proof.get("required_tests", [])),
                tests,
                artifact,
                "proof.required_tests",
                "REQUIREMENT_EVIDENCE_MISSING",
            )
        )
    return requirement_ids, findings


def _lineage(root: Path, consolidation: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    expected_paths = {
        artifact.as_posix()
        for bundle in BUNDLES[:2]
        for artifact in (bundle.manifest, bundle.schema, bundle.example)
    }
    records = [artifact for item in consolidation["slices"] for artifact in item["artifacts"]]
    actual_paths = {record["path"] for record in records}
    if len(actual_paths) != len(records):
        findings.append(
            Finding(
                BUNDLES[2].example.as_posix(),
                "LINEAGE_INVENTORY_INVALID",
                "artifact paths must be unique",
            )
        )
    findings.extend(
        Finding(BUNDLES[2].example.as_posix(), "LINEAGE_INVENTORY_INVALID", item)
        for item in sorted(expected_paths.symmetric_difference(actual_paths))
    )
    for record in records:
        path = root / record["path"]
        if not path.is_file():
            continue
        normalized = path.read_bytes().replace(b"\r\n", b"\n")
        digest = hashlib.sha256(normalized).hexdigest()
        if digest != record["sha256"]:
            findings.append(Finding(record["path"], "LINEAGE_DIGEST_MISMATCH", digest))
    return findings


def _references(root: Path, documents: dict[str, BundleDocuments]) -> list[Finding]:
    references = (
        documents["foundation"].example["controls"]["foundation_boundaries"]["contract"],
        documents["worker"].example["controls"]["task_envelope"]["contract"],
    )
    return [
        Finding(reference, "REFERENCE_MISSING", "required published contract is absent")
        for reference in references
        if not (root / reference).is_file()
    ]


def validate_semantics(root: Path, documents: dict[str, BundleDocuments]) -> list[Finding]:
    if set(documents) != {"foundation", "worker", "consolidation"}:
        return []
    requirements, findings = _requirement_evidence(documents)
    consolidation = documents["consolidation"].example
    coverage = consolidation["coverage"]
    findings.extend(
        mismatch(
            set(coverage["requirement_ids"]),
            requirements,
            BUNDLES[2].example.as_posix(),
            "coverage.requirement_ids",
            "COVERAGE_INVALID",
        )
    )
    if coverage["duplicates"] or coverage["unassigned"]:
        findings.append(
            Finding(
                BUNDLES[2].example.as_posix(),
                "COVERAGE_INVALID",
                "duplicates and unassigned must be empty",
            )
        )
    profile_ids = {documents[name].example["profile_id"] for name in ("foundation", "worker")}
    integration = consolidation["integration"]
    findings.extend(
        mismatch(
            set(integration["control_namespaces"]),
            profile_ids,
            BUNDLES[2].example.as_posix(),
            "integration.control_namespaces",
            "INTEGRATION_INVALID",
        )
    )
    if integration["contract_collisions"] or integration["redundant_implementations"]:
        findings.append(
            Finding(
                BUNDLES[2].example.as_posix(),
                "INTEGRATION_INVALID",
                "collisions and redundant implementations must be empty",
            )
        )
    gate = consolidation["review_gate"]
    if gate["candidate_state"] != "READY_FOR_INDEPENDENT_REVIEW" or gate["released_dependents"]:
        findings.append(
            Finding(
                BUNDLES[2].example.as_posix(),
                "SELF_RELEASE_PROHIBITED",
                "candidate cannot release dependents",
            )
        )
    findings.extend(_lineage(root, consolidation))
    findings.extend(_references(root, documents))
    return findings
