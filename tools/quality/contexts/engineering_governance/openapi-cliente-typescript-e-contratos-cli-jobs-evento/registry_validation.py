from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from validation_types import Finding


SLUG = "openapi-cliente-typescript-e-contratos-cli-jobs-evento"
CONTRACT_ROOT = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
REGISTRY_REL = CONTRACT_ROOT / (
    "runtime-scm-tool-parte-2/schema-compatibility-checkpoint.json"
)
REGISTERED_CONTRACTS = {
    (
        CONTRACT_ROOT / "crs-dbschema-epic-parte-1/contract-foundation.schema.json"
    ).as_posix(): "DATABASE",
    "contracts/http/openapi.yaml": "API",
    "contracts/events/job-event.schema.json": "EVENT",
    "contracts/artifacts/artifact-set-manifest.schema.json": "MANIFEST",
    "contracts/domain/processing-plan.schema.json": "ARTIFACT",
    "contracts/domain/quality-report.schema.json": "ARTIFACT",
    "contracts/domain/failure-diagnostic.schema.json": "ARTIFACT",
}
OPENAPI_COMPONENTS = {
    "ProcessingPlan",
    "Job",
    "JobEvent",
    "QualityReport",
    "FailureDiagnostic",
    "ArtifactSetManifest",
}


def _finding(code: str, artifact: Path, detail: str) -> Finding:
    return Finding(code, artifact.as_posix(), detail)


def _load_document(
    root: Path, relative: Path, *, yaml_document: bool = False
) -> tuple[object | None, list[Finding]]:
    try:
        text = (root / relative).read_text(encoding="utf-8")
        return (yaml.safe_load(text) if yaml_document else json.loads(text)), []
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as error:
        return None, [_finding("CONTRACT_UNREADABLE", relative, str(error))]


def _schema_major(document: dict[str, Any]) -> int | None:
    schema_id = document.get("$id")
    match = (
        re.search(r"/(\d+)\.\d+\.\d+/?$", schema_id)
        if isinstance(schema_id, str)
        else None
    )
    return int(match.group(1)) if match else None


def _openapi_findings(
    document: object, artifact: Path
) -> tuple[int | None, list[Finding]]:
    if not isinstance(document, dict):
        return None, [_finding("OPENAPI_INVALID", artifact, "OpenAPI object required")]
    components = document.get("components")
    schemas = components.get("schemas") if isinstance(components, dict) else None
    servers = document.get("servers")
    urls = [item.get("url") for item in servers or [] if isinstance(item, dict)]
    majors = {
        int(match.group(1))
        for url in urls
        if isinstance(url, str) and (match := re.fullmatch(r"/api/v(\d+)", url))
    }
    valid = (
        document.get("openapi") == "3.1.0"
        and isinstance(schemas, dict)
        and OPENAPI_COMPONENTS <= set(schemas)
        and len(majors) == 1
    )
    findings = [] if valid else [
        _finding(
            "OPENAPI_INVALID",
            artifact,
            "versioned components and /api/vN server required",
        )
    ]
    return (next(iter(majors)) if len(majors) == 1 else None), findings


def _entry_findings(root: Path, entry: dict[str, Any]) -> list[Finding]:
    relative = Path(entry["contract"])
    document, findings = _load_document(
        root, relative, yaml_document=relative.suffix == ".yaml"
    )
    if document is None:
        return findings
    if entry["category"] == "API":
        major, openapi_findings = _openapi_findings(document, relative)
        findings.extend(openapi_findings)
    elif isinstance(document, dict):
        major = _schema_major(document)
        try:
            Draft202012Validator.check_schema(document)
        except SchemaError as error:
            findings.append(_finding("CONTRACT_SCHEMA_INVALID", relative, error.message))
    else:
        return findings + [
            _finding("CONTRACT_SCHEMA_INVALID", relative, "schema object required")
        ]
    reader, writer = entry.get("reader"), entry.get("writer")
    supported = reader.get("supported_majors") if isinstance(reader, dict) else None
    checkpoints = (
        reader.get("compatibility_checkpoints", {})
        if isinstance(reader, dict)
        else {}
    )
    valid = (
        isinstance(reader, dict)
        and isinstance(writer, dict)
        and reader.get("policy") == "REGISTERED_MAJOR_ONLY"
        and writer.get("policy") == "CURRENT_REGISTERED_MAJOR_ONLY"
        and isinstance(supported, list)
        and supported == sorted(set(supported))
        and writer.get("major") == major
        and set(supported) == {major, *(int(value) for value in checkpoints)}
    )
    if not valid:
        findings.append(
            _finding("REGISTRY_INVALID", relative, "reader/writer major window invalid")
        )
    return findings


def validate_registry(root: Path) -> list[Finding]:
    try:
        registry = json.loads((root / REGISTRY_REL).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [_finding("REGISTRY_UNREADABLE", REGISTRY_REL, str(error))]
    entries = registry.get("entries") if isinstance(registry, dict) else None
    actual = {
        entry.get("contract"): entry.get("category")
        for entry in entries or []
        if isinstance(entry, dict)
    }
    valid = (
        isinstance(registry, dict)
        and registry.get("schema_version") == "1.0.0"
        and registry.get("checkpoint_version") == "1.0.0"
        and registry.get("status") == "FROZEN"
        and actual == REGISTERED_CONTRACTS
        and len(entries or []) == len(REGISTERED_CONTRACTS)
    )
    if not valid:
        return [
            _finding(
                "REGISTRY_INVALID",
                REGISTRY_REL,
                "exact frozen contract registry required",
            )
        ]
    return sorted(
        finding
        for entry in entries
        for finding in _entry_findings(root, entry)
    )
