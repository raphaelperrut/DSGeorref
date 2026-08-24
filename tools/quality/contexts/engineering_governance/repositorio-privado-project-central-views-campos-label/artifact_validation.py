from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from contract_catalog import (
    BUNDLES,
    CONTRACT_ROOT,
    EXPECTED_OWNER,
    EXPECTED_VERSION,
    OWNERSHIP_REL,
    ContractBundle,
    expected_artifacts,
)
from validation_types import Finding, mismatch


@dataclass(frozen=True)
class BundleDocuments:
    manifest: dict[str, Any]
    schema: dict[str, Any]
    example: dict[str, Any]


def _load_json(path: Path, artifact: str) -> tuple[dict[str, Any] | None, list[Finding]]:
    if not path.is_file():
        return None, [Finding(artifact, "ARTIFACT_MISSING", "required JSON file is absent")]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [Finding(artifact, "JSON_INVALID", str(exc))]
    if not isinstance(value, dict):
        return None, [Finding(artifact, "INVALID_STRUCTURE", "JSON root must be an object")]
    return value, []


def _load_yaml(path: Path, artifact: str) -> tuple[dict[str, Any] | None, list[Finding]]:
    if not path.is_file():
        return None, [Finding(artifact, "ARTIFACT_MISSING", "required YAML file is absent")]
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return None, [Finding(artifact, "YAML_INVALID", str(exc))]
    if not isinstance(value, dict):
        return None, [Finding(artifact, "INVALID_STRUCTURE", "YAML root must be an object")]
    return value, []


def _manifest_findings(manifest: dict[str, Any], bundle: ContractBundle) -> list[Finding]:
    artifact = bundle.manifest.as_posix()
    findings: list[Finding] = []
    expected_keys = {
        "schema_version",
        "contract_version",
        "status",
        "owner",
        "identity",
        "contract",
        "compatibility",
        "runtime",
        "acceptance_criteria",
        "proof",
        "slices" if bundle.name == "consolidation" else "requirements",
    }
    findings.extend(
        mismatch(
            set(manifest),
            expected_keys,
            artifact,
            "manifest keys",
            "MANIFEST_SHAPE_INVALID",
        )
    )
    expected = {
        "schema_version": EXPECTED_VERSION,
        "contract_version": EXPECTED_VERSION,
        "status": "FROZEN",
        "owner": EXPECTED_OWNER,
        "identity": bundle.identity,
    }
    for field, value in expected.items():
        findings.extend(mismatch(manifest.get(field), value, artifact, field))
    contract = manifest.get("contract")
    expected_contract = {
        "id": bundle.contract_id,
        "schema": bundle.schema.as_posix(),
        "example": bundle.example.as_posix(),
    }
    findings.extend(mismatch(contract, expected_contract, artifact, "contract"))
    expected_compatibility = {
        "policy": "SEMVER",
        "compatible_change": "OPTIONAL_ADDITION_WITHIN_CURRENT_MAJOR",
        "breaking_change": "NEW_MAJOR_AND_ARCHITECT_REVIEW",
        "unknown_properties": "REJECT",
    }
    findings.extend(
        mismatch(
            manifest.get("compatibility"),
            expected_compatibility,
            artifact,
            "compatibility",
            "FAIL_OPEN_POLICY",
        )
    )
    expected_runtime = {
        "implementation": "NOT_INCLUDED",
        "http": "NOT_APPLICABLE",
        "persistence": "NOT_APPLICABLE",
        "migration": "NOT_APPLICABLE",
        "operational_rollback": "NOT_APPLICABLE",
        "contract_rollback": "REVERT_BEFORE_CONSUMPTION_OR_SUPERSEDE_WITH_NEW_VERSION",
    }
    findings.extend(
        mismatch(
            manifest.get("runtime"),
            expected_runtime,
            artifact,
            "runtime",
            "RUNTIME_SCOPE_INVALID",
        )
    )
    return findings


def _schema_findings(
    schema: dict[str, Any], example: dict[str, Any], bundle: ContractBundle
) -> list[Finding]:
    artifact = bundle.schema.as_posix()
    findings: list[Finding] = []
    findings.extend(
        mismatch(
            schema.get("$schema"),
            "https://json-schema.org/draft/2020-12/schema",
            artifact,
            "$schema",
            "SCHEMA_DIALECT_INVALID",
        )
    )
    schema_id = schema.get("$id")
    if not isinstance(schema_id, str) or not schema_id.endswith(f"/{EXPECTED_VERSION}"):
        findings.append(Finding(artifact, "SCHEMA_VERSION_INVALID", "$id must end in /1.0.0"))
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(example),
            key=lambda error: list(error.absolute_path),
        )
    except SchemaError as exc:
        return findings + [Finding(artifact, "SCHEMA_INVALID", str(exc).splitlines()[0])]
    for error in errors:
        location = "/" + "/".join(str(part) for part in error.absolute_path)
        findings.append(
            Finding(
                bundle.example.as_posix(),
                "EXAMPLE_SCHEMA_INVALID",
                f"{location}: {error.message}",
            )
        )
    return findings


def validate_bundles(root: Path) -> tuple[dict[str, BundleDocuments], list[Finding]]:
    documents: dict[str, BundleDocuments] = {}
    findings: list[Finding] = []
    for bundle in BUNDLES:
        manifest, manifest_errors = _load_yaml(root / bundle.manifest, bundle.manifest.as_posix())
        schema, schema_errors = _load_json(root / bundle.schema, bundle.schema.as_posix())
        example, example_errors = _load_json(root / bundle.example, bundle.example.as_posix())
        bundle_findings = manifest_errors + schema_errors + example_errors
        if manifest is None or schema is None or example is None:
            findings.extend(bundle_findings)
            continue
        bundle_findings.extend(_manifest_findings(manifest, bundle))
        bundle_findings.extend(_schema_findings(schema, example, bundle))
        findings.extend(bundle_findings)
        if not bundle_findings:
            documents[bundle.name] = BundleDocuments(manifest, schema, example)
    return documents, findings


def validate_ownership(root: Path) -> list[Finding]:
    artifact = OWNERSHIP_REL.as_posix()
    try:
        with (root / OWNERSHIP_REL).open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as exc:
        return [Finding(artifact, "OWNERSHIP_REGISTRY_INVALID", str(exc))]
    prefix = CONTRACT_ROOT.as_posix() + "/"
    scoped = [row for row in rows if row.get("contract", "").startswith(prefix)]
    expected = {path.as_posix() for path in expected_artifacts()}
    actual = {row.get("contract", "") for row in scoped}
    counts = Counter(row.get("contract", "") for row in scoped)
    findings = [
        Finding(artifact, "OWNERSHIP_REFERENCE_MISSING", item)
        for item in sorted(expected - actual)
    ]
    findings.extend(
        Finding(artifact, "OWNERSHIP_REFERENCE_UNEXPECTED", item)
        for item in sorted(actual - expected)
    )
    findings.extend(
        Finding(artifact, "OWNERSHIP_REFERENCE_DUPLICATE", item)
        for item, count in sorted(counts.items())
        if count > 1
    )
    for row in scoped:
        metadata = (
            row.get("owner_context"),
            row.get("contract_type"),
            row.get("status"),
            row.get("shared_model"),
        )
        if metadata != (EXPECTED_OWNER, "contexts", "VERSIONED", "NO"):
            findings.append(Finding(artifact, "OWNER_INVALID", row.get("contract", "<missing>")))
    return findings
