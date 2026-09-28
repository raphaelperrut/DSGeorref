from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from contract_definition import (
    EXAMPLE_REL,
    EXPECTED_IDENTITY,
    EXPECTED_REQUIREMENTS,
    MANIFEST_REL,
    SCHEMA_REL,
)
from validation_types import Finding, expect_equal, finding


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _load(root: Path) -> tuple[dict[str, Any] | None, list[Finding]]:
    path = root / MANIFEST_REL
    if not path.is_file():
        return None, [
            finding(
                MANIFEST_REL,
                "ARTIFACT_MISSING",
                "frozen contract manifest is absent",
                f"Restore the versioned manifest at {MANIFEST_REL.as_posix()}.",
            )
        ]
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return None, [
            finding(
                MANIFEST_REL,
                "MANIFEST_INVALID",
                str(exc).splitlines()[0],
                "Provide a readable UTF-8 YAML mapping with valid syntax.",
            )
        ]
    if not isinstance(loaded, dict):
        return None, [
            finding(
                MANIFEST_REL,
                "MANIFEST_STRUCTURE_INVALID",
                "manifest root must be a mapping",
                "Replace the manifest root with the frozen contract mapping.",
            )
        ]
    return loaded, []


def _validate_header(manifest: dict[str, Any]) -> list[Finding]:
    contract = _mapping(manifest.get("contract"))
    compatibility = _mapping(manifest.get("compatibility"))
    authority = _mapping(manifest.get("authority"))
    runtime = _mapping(manifest.get("runtime"))
    expectations = (
        ("schema_version", manifest.get("schema_version"), "1.0.0"),
        ("contract_version", manifest.get("contract_version"), "1.0.0"),
        ("status", manifest.get("status"), "FROZEN"),
        ("owner", manifest.get("owner"), "BC-001"),
        ("identity", manifest.get("identity"), EXPECTED_IDENTITY),
        ("contract.id", contract.get("id"), "backlog-governance-profile"),
        ("contract.schema", contract.get("schema"), SCHEMA_REL.as_posix()),
        ("contract.example", contract.get("example"), EXAMPLE_REL.as_posix()),
        ("compatibility.policy", compatibility.get("policy"), "SEMVER"),
        (
            "compatibility.unknown_properties",
            compatibility.get("unknown_properties"),
            "REJECT",
        ),
        (
            "authority.contract_source",
            authority.get("contract_source"),
            "VERSIONED_REPOSITORY",
        ),
        ("runtime.implementation", runtime.get("implementation"), "NOT_INCLUDED"),
    )
    findings: list[Finding] = []
    for field, actual, expected in expectations:
        expect_equal(
            findings,
            artifact=MANIFEST_REL,
            field=field,
            actual=actual,
            expected=expected,
            code="MANIFEST_CONTRACT_MISMATCH",
        )
    return findings


def _validate_requirement_entry(
    requirement_id: str,
    expectation: dict[str, str],
    entry: dict[str, Any],
) -> list[Finding]:
    findings: list[Finding] = []
    for field in ("control", "test"):
        expect_equal(
            findings,
            artifact=MANIFEST_REL,
            field=f"requirements.{requirement_id}.{field}",
            actual=entry.get(field),
            expected=expectation[field],
            code="REQUIREMENT_MAPPING_MISMATCH",
        )
    modes = entry.get("failure_modes")
    if (
        not isinstance(modes, list)
        or not modes
        or not all(isinstance(mode, str) and mode for mode in modes)
    ):
        findings.append(
            finding(
                MANIFEST_REL,
                "FAILURE_MODE_MISSING",
                f"{requirement_id} has no explicit failure modes",
                f"Restore failure_modes for {requirement_id} in the frozen manifest.",
            )
        )
    return findings


def _validate_requirements(manifest: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    entries = manifest.get("requirements")
    if not isinstance(entries, list):
        entries = []
        findings.append(
            finding(
                MANIFEST_REL,
                "REQUIREMENT_MAPPING_INVALID",
                "requirements must be a list",
                "Restore the five frozen requirement-to-control mappings.",
            )
        )
    mapped = {
        entry.get("id"): entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }
    expect_equal(
        findings,
        artifact=MANIFEST_REL,
        field="requirements.ids",
        actual=set(mapped),
        expected=set(EXPECTED_REQUIREMENTS),
        code="REQUIREMENT_MAPPING_MISMATCH",
    )
    for requirement_id, expectation in EXPECTED_REQUIREMENTS.items():
        entry = mapped.get(requirement_id)
        if entry is not None:
            findings.extend(_validate_requirement_entry(requirement_id, expectation, entry))
    proof_tests = _mapping(manifest.get("proof")).get("required_tests")
    expect_equal(
        findings,
        artifact=MANIFEST_REL,
        field="proof.required_tests",
        actual=set(proof_tests) if isinstance(proof_tests, list) else proof_tests,
        expected={value["test"] for value in EXPECTED_REQUIREMENTS.values()},
        code="PROOF_SET_MISMATCH",
    )
    return findings


def validate_manifest(root: Path) -> list[Finding]:
    manifest, findings = _load(root)
    if manifest is None:
        return findings
    findings.extend(_validate_header(manifest))
    findings.extend(_validate_requirements(manifest))
    return findings
