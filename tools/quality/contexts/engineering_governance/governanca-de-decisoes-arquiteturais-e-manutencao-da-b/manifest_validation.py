from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from contract_definition import EXPECTED_CONTRACTS, EXPECTED_VERSION, MANIFEST_REL
from validation_types import Finding, closed_keys, expect, string_set


def _load_manifest(path: Path, artifact: str) -> tuple[Any | None, list[Finding]]:
    if not path.is_file():
        return None, [Finding(artifact, "ARTIFACT_MISSING", "required YAML file is absent")]
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return None, [Finding(artifact, "YAML_INVALID", str(exc))]


def _sections(manifest: dict[str, Any], artifact: str) -> list[Finding]:
    findings: list[Finding] = []
    expected_top = {
        "schema_version",
        "contract_version",
        "status",
        "owner",
        "identity",
        "compatibility",
        "runtime",
        "traceability",
        "contracts",
        "proof",
    }
    findings.extend(closed_keys(manifest, expected_top, artifact, "manifest"))
    exact_sections = {
        "identity": {
            "epic_id": "EPIC-001",
            "story_id": "STORY-0001",
            "issue_id": "ISSUE-0111",
            "task_id": "TASK-0001",
        },
        "compatibility": {
            "policy": "SEMVER",
            "backward_compatible_changes": "OPTIONAL_ADDITIONS_WITHIN_CURRENT_MAJOR",
            "breaking_change": "NEW_MAJOR_OR_REPLACEMENT_ADR",
            "unknown_properties": "REJECT",
        },
        "runtime": {
            "implementation": "NOT_INCLUDED",
            "http": "NOT_APPLICABLE",
            "persistence": "NOT_APPLICABLE",
            "migration": "NOT_APPLICABLE",
            "operational_rollback": "NOT_APPLICABLE",
        },
    }
    for section, expected in exact_sections.items():
        findings.extend(closed_keys(manifest.get(section), set(expected), artifact, section))
        findings.extend(expect(manifest.get(section), expected, artifact, section))
    findings.extend(
        expect(manifest.get("schema_version"), EXPECTED_VERSION, artifact, "schema_version")
    )
    findings.extend(
        expect(
            manifest.get("contract_version"), EXPECTED_VERSION, artifact, "contract_version"
        )
    )
    findings.extend(expect(manifest.get("status"), "FROZEN", artifact, "status"))
    findings.extend(
        expect(manifest.get("owner"), "BC-001", artifact, "owner", "OWNER_INVALID")
    )
    return findings


def _traceability(manifest: dict[str, Any], artifact: str) -> list[Finding]:
    traceability = manifest.get("traceability")
    findings = closed_keys(
        traceability,
        {"requirements", "acceptance_criteria"},
        artifact,
        "traceability",
    )
    if isinstance(traceability, dict):
        requirements, structure = string_set(
            traceability.get("requirements"), artifact, "traceability.requirements"
        )
        findings.extend(structure)
        findings.extend(
            expect(
                requirements,
                {"REQ-ISM-004", "REQ-ISS-002", "REQ-SPRINT-001-004"},
                artifact,
                "traceability.requirements",
            )
        )
        criteria, structure = string_set(
            traceability.get("acceptance_criteria"),
            artifact,
            "traceability.acceptance_criteria",
        )
        findings.extend(structure)
        findings.extend(
            expect(
                criteria,
                {f"AC-ISSUE-0111-0{number}" for number in range(1, 5)},
                artifact,
                "traceability.acceptance_criteria",
            )
        )
    proof = manifest.get("proof")
    findings.extend(closed_keys(proof, {"tests"}, artifact, "proof"))
    if isinstance(proof, dict):
        expected_tests = {
            "test_versioned_issue_portfolio_catalog_github_reconciliation",
            "test_issue_forecast_min_mode_max_confidence_and_snapshot_variance",
            "test_sprint_zero_baseline_decision_04",
            "test_epic_001_contrato",
        }
        tests, structure = string_set(proof.get("tests"), artifact, "proof.tests")
        findings.extend(structure)
        findings.extend(expect(tests, expected_tests, artifact, "proof.tests"))
    return findings


def _contract_entry(
    entry: dict[str, Any], artifact: str, allowed: set[str]
) -> list[Finding]:
    contract_id = entry.get("contract_id")
    section = f"contracts[{contract_id!r}]"
    findings = closed_keys(entry, allowed, artifact, section)
    if not isinstance(contract_id, str):
        findings.append(
            Finding(artifact, "INVALID_STRUCTURE", f"{section}.contract_id must be a string")
        )
        return findings
    expected = EXPECTED_CONTRACTS.get(contract_id)
    if expected is None:
        return findings
    for field in ("schema", "example"):
        findings.extend(
            expect(
                entry.get(field),
                expected[field].as_posix(),
                artifact,
                f"{section}.{field}",
                "REFERENCE_INVALID",
            )
        )
    for field, value in (
        ("owner", "BC-001"),
        ("version", EXPECTED_VERSION),
        ("requirement", expected["requirement"]),
    ):
        findings.extend(expect(entry.get(field), value, artifact, f"{section}.{field}"))
    expected_lists = (
        ("acceptance_criteria", {f"AC-ISSUE-0111-0{number}" for number in range(1, 4)}),
        ("invariants", expected["invariants"]),
        ("failure_modes", expected["failure_modes"]),
    )
    for field, expected_values in expected_lists:
        values, structure = string_set(entry.get(field), artifact, f"{section}.{field}")
        findings.extend(structure)
        findings.extend(expect(values, expected_values, artifact, f"{section}.{field}"))
    return findings


def _contracts(manifest: dict[str, Any], artifact: str) -> list[Finding]:
    entries = manifest.get("contracts")
    if not isinstance(entries, list):
        return [Finding(artifact, "INVALID_STRUCTURE", "contracts must be an array")]
    findings: list[Finding] = []
    ids = [
        entry.get("contract_id")
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("contract_id"), str)
    ]
    findings.extend(expect(set(ids), set(EXPECTED_CONTRACTS), artifact, "contract ids"))
    findings.extend(
        expect(len(ids), len(set(ids)), artifact, "contract ids", "DUPLICATE_CONTRACT")
    )
    allowed = {
        "contract_id",
        "owner",
        "version",
        "schema",
        "example",
        "requirement",
        "acceptance_criteria",
        "invariants",
        "failure_modes",
    }
    for entry in entries:
        if isinstance(entry, dict):
            findings.extend(_contract_entry(entry, artifact, allowed))
        else:
            findings.append(
                Finding(artifact, "INVALID_STRUCTURE", "each contract must be an object")
            )
    return findings


def validate_manifest(root: Path) -> list[Finding]:
    artifact = MANIFEST_REL.as_posix()
    manifest, findings = _load_manifest(root / MANIFEST_REL, artifact)
    if manifest is None:
        return findings
    if not isinstance(manifest, dict):
        return findings + [
            Finding(artifact, "INVALID_STRUCTURE", "manifest must be an object")
        ]
    findings.extend(_sections(manifest, artifact))
    findings.extend(_traceability(manifest, artifact))
    findings.extend(_contracts(manifest, artifact))
    for contract in EXPECTED_CONTRACTS.values():
        for field in ("schema", "example"):
            reference = contract[field]
            target = (root / reference).resolve()
            if root not in target.parents or not target.is_file():
                findings.append(
                    Finding(
                        artifact,
                        "REFERENCE_UNRESOLVABLE",
                        reference.as_posix(),
                    )
                )
    return findings
