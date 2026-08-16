from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from calendar import monthrange
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urldefrag, urljoin

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable

from contract_definition import (
    CONTRACT_REL,
    EXPECTED_CONTRACTS,
    EXPECTED_VERSION,
    MANIFEST_REL,
    OWNERSHIP_REL,
)
from manifest_validation import validate_manifest
from semantic_invariants import validate_semantics
from validation_types import Finding, expect


_RFC3339_DATE_TIME = re.compile(
    r"^(?P<year>[0-9]{4})-(?P<month>0[1-9]|1[0-2])-(?P<day>[0-9]{2})"
    r"[Tt](?P<hour>[01][0-9]|2[0-3]):(?P<minute>[0-5][0-9]):"
    r"(?P<second>[0-5][0-9]|60)(?:\.[0-9]+)?"
    r"(?P<timezone>[Zz]|(?P<offset_sign>[+-])"
    r"(?P<offset_hour>[01][0-9]|2[0-3]):(?P<offset_minute>[0-5][0-9]))$"
)


def _is_rfc3339_date_time(value: object) -> bool:
    if not isinstance(value, str):
        return True
    match = _RFC3339_DATE_TIME.fullmatch(value)
    if match is None:
        return False
    second = int(match.group("second"))
    try:
        local_time = datetime(
            year=int(match.group("year")),
            month=int(match.group("month")),
            day=int(match.group("day")),
            hour=int(match.group("hour")),
            minute=int(match.group("minute")),
            second=min(second, 59),
        )
    except ValueError:
        return False
    if second < 60:
        return True
    offset_minutes = 0
    if match.group("timezone").upper() != "Z":
        offset_minutes = 60 * int(match.group("offset_hour")) + int(
            match.group("offset_minute")
        )
        if match.group("offset_sign") == "-":
            offset_minutes = -offset_minutes
    try:
        utc_time = local_time - timedelta(minutes=offset_minutes)
    except OverflowError:
        return False
    is_last_minute_utc = utc_time.hour == 23 and utc_time.minute == 59
    is_month_end_utc = utc_time.day == monthrange(utc_time.year, utc_time.month)[1]
    return is_last_minute_utc and is_month_end_utc


def _story_format_checker() -> FormatChecker:
    checker = FormatChecker()
    checker.checks("date-time")(_is_rfc3339_date_time)
    return checker


def _load_json(path: Path, artifact: str) -> tuple[Any | None, list[Finding]]:
    if not path.is_file():
        return None, [Finding(artifact, "ARTIFACT_MISSING", "required JSON file is absent")]
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [Finding(artifact, "JSON_INVALID", str(exc))]


def _json_pointer(document: Any, fragment: str) -> bool:
    if not fragment:
        return True
    pointer = unquote(fragment)
    if not pointer.startswith("/"):
        return False
    current = document
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            return False
    return True


def _walk_refs(value: Any) -> list[str]:
    if isinstance(value, dict):
        refs = [value["$ref"]] if isinstance(value.get("$ref"), str) else []
        return refs + [ref for child in value.values() for ref in _walk_refs(child)]
    if isinstance(value, list):
        return [ref for child in value for ref in _walk_refs(child)]
    return []


def _schema_references(schemas: dict[str, dict[str, Any]]) -> list[Finding]:
    findings: list[Finding] = []
    ids = [schema.get("$id") for schema in schemas.values() if isinstance(schema.get("$id"), str)]
    if len(ids) != len(set(ids)):
        findings.append(Finding("schemas", "DUPLICATE_SCHEMA_ID", "$id values must be unique"))
    by_id = {
        schema.get("$id"): (artifact, schema)
        for artifact, schema in schemas.items()
        if isinstance(schema.get("$id"), str)
    }
    for artifact, schema in schemas.items():
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str):
            findings.append(Finding(artifact, "SCHEMA_ID_MISSING", "$id must be explicit"))
            continue
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            findings.append(
                Finding(artifact, "SCHEMA_DIALECT_INVALID", "Draft 2020-12 is required")
            )
        if not schema_id.endswith(f"/{EXPECTED_VERSION}"):
            findings.append(
                Finding(artifact, "SCHEMA_VERSION_INVALID", "$id must end with /1.0.0")
            )
        for ref in _walk_refs(schema):
            target_id, fragment = urldefrag(urljoin(schema_id, ref))
            target = by_id.get(target_id)
            if target is None or not _json_pointer(target[1], fragment):
                findings.append(Finding(artifact, "SCHEMA_REFERENCE_UNRESOLVABLE", ref))
    return findings


def _validate_schema_pairs(root: Path) -> tuple[dict[str, dict[str, Any]], list[Finding]]:
    findings: list[Finding] = []
    schemas: dict[str, dict[str, Any]] = {}
    examples: dict[str, dict[str, Any]] = {}
    for contract_id, contract in sorted(EXPECTED_CONTRACTS.items()):
        for kind, destination in (("schema", schemas), ("example", examples)):
            rel = contract[kind]
            loaded, load_findings = _load_json(root / rel, rel.as_posix())
            findings.extend(load_findings)
            if isinstance(loaded, dict):
                destination[contract_id] = loaded
            elif loaded is not None:
                findings.append(
                    Finding(rel.as_posix(), "INVALID_STRUCTURE", f"{kind} must be an object")
                )
    schema_docs = {
        EXPECTED_CONTRACTS[key]["schema"].as_posix(): value
        for key, value in schemas.items()
    }
    reference_findings = _schema_references(schema_docs)
    findings.extend(reference_findings)
    unresolved_artifacts = {
        finding.artifact
        for finding in reference_findings
        if finding.code == "SCHEMA_REFERENCE_UNRESOLVABLE"
    }
    registry = Registry()
    valid_schemas: dict[str, dict[str, Any]] = {}
    for contract_id, schema in sorted(schemas.items()):
        artifact = EXPECTED_CONTRACTS[contract_id]["schema"].as_posix()
        if artifact in unresolved_artifacts:
            continue
        try:
            Draft202012Validator.check_schema(schema)
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        except (SchemaError, KeyError) as exc:
            findings.append(Finding(artifact, "SCHEMA_INVALID", str(exc).splitlines()[0]))
        else:
            valid_schemas[contract_id] = schema
    valid_examples: dict[str, dict[str, Any]] = {}
    format_checker = _story_format_checker()
    for contract_id in sorted(set(valid_schemas) & set(examples)):
        rel = EXPECTED_CONTRACTS[contract_id]["example"].as_posix()
        validator = Draft202012Validator(
            valid_schemas[contract_id], registry=registry, format_checker=format_checker
        )
        try:
            errors = sorted(
                validator.iter_errors(examples[contract_id]),
                key=lambda error: list(error.absolute_path),
            )
        except Unresolvable as exc:
            schema_artifact = EXPECTED_CONTRACTS[contract_id]["schema"].as_posix()
            findings.append(
                Finding(schema_artifact, "SCHEMA_REFERENCE_UNRESOLVABLE", str(exc))
            )
            continue
        for error in errors:
            location = "/" + "/".join(str(part) for part in error.absolute_path)
            findings.append(Finding(rel, "EXAMPLE_SCHEMA_INVALID", f"{location}: {error.message}"))
        if not errors:
            valid_examples[contract_id] = examples[contract_id]
    return valid_examples, findings


def _validate_ownership(root: Path) -> list[Finding]:
    artifact = OWNERSHIP_REL.as_posix()
    path = root / OWNERSHIP_REL
    if not path.is_file():
        return [Finding(artifact, "ARTIFACT_MISSING", "ownership registry is absent")]
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames or []
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        return [Finding(artifact, "OWNERSHIP_REGISTRY_INVALID", str(exc))]
    expected_fields = {"contract", "owner_context", "contract_type", "status", "shared_model"}
    findings = expect(set(fields), expected_fields, artifact, "header", "UNKNOWN_PROPERTY")
    published = {MANIFEST_REL.as_posix()}
    published.update(
        contract[field].as_posix()
        for contract in EXPECTED_CONTRACTS.values()
        for field in ("schema", "example")
    )
    namespace_prefix = CONTRACT_REL.as_posix() + "/"
    namespace_references = [
        row.get("contract", "")
        for row in rows
        if row.get("contract") == MANIFEST_REL.as_posix()
        or row.get("contract", "").startswith(namespace_prefix)
    ]
    actual = set(namespace_references)
    findings.extend(
        Finding(artifact, "OWNERSHIP_REFERENCE_MISSING", reference)
        for reference in sorted(published - actual)
    )
    findings.extend(
        Finding(artifact, "OWNERSHIP_REFERENCE_UNEXPECTED", reference)
        for reference in sorted(actual - published)
    )
    findings.extend(
        Finding(
            artifact,
            "OWNERSHIP_REFERENCE_DUPLICATE",
            f"{reference}: found {count} registry rows",
        )
        for reference, count in sorted(Counter(namespace_references).items())
        if count > 1
    )
    for reference in sorted(published & actual):
        matches = [row for row in rows if row.get("contract") == reference]
        if len(matches) != 1:
            continue
        row = matches[0]
        expected = {
            "owner_context": "BC-001",
            "contract_type": "contexts",
            "status": "VERSIONED",
            "shared_model": "NO",
        }
        for field, value in expected.items():
            if row.get(field) != value:
                findings.append(
                    Finding(
                        artifact,
                        "OWNER_INVALID",
                        f"{reference}: {field} must be {value}",
                    )
                )
    return findings


def validate(repository_root: Path) -> list[Finding]:
    root = repository_root.resolve()
    findings = validate_manifest(root)
    examples, schema_findings = _validate_schema_pairs(root)
    findings.extend(schema_findings)
    findings.extend(_validate_ownership(root))
    example_paths = {
        contract_id: contract["example"].as_posix()
        for contract_id, contract in EXPECTED_CONTRACTS.items()
    }
    findings.extend(validate_semantics(examples, example_paths))
    return sorted(set(findings))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the frozen EPIC-001 engineering governance contracts."
    )
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[5])
    args = parser.parse_args(argv)
    findings = validate(args.repository_root)
    if findings:
        print(f"VALIDATION FAILED ({len(findings)} finding(s))")
        for finding in findings:
            print(f"ERROR [{finding.code}] {finding.artifact} :: {finding.detail}")
        return 1
    print("VALIDATION PASS")
    print(f"manifest={MANIFEST_REL.as_posix()} version={EXPECTED_VERSION}")
    print("contracts=" + ",".join(sorted(EXPECTED_CONTRACTS)))
    print(f"ownership={OWNERSHIP_REL.as_posix()} owner=BC-001")
    return 0


if __name__ == "__main__":
    sys.exit(main())
