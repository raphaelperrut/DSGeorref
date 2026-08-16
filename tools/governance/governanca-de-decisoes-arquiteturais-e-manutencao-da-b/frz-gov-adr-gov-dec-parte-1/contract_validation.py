from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

from canonical_json import CanonicalizationError, load_json_bytes
from foundation_validation_types import Finding


SCHEMA_RELATIVE_PATH = Path(
    "docs/03-engineering/contexts/engineering_governance/"
    "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "frz-gov-adr-gov-dec-parte-1/foundation-baseline-lifecycle.schema.json"
)


def load_contract(repository_root: Path) -> dict[str, Any]:
    schema_path = repository_root / SCHEMA_RELATIVE_PATH
    try:
        schema = load_json_bytes(schema_path.read_bytes())
    except (OSError, CanonicalizationError) as error:
        raise ValueError(f"invalid lifecycle contract: {error}") from error
    if not isinstance(schema, dict):
        raise ValueError("lifecycle contract must be a JSON object")
    profile = schema.get("x-dsgeorref-profile")
    expected = {
        "owner": "STORY-0688",
        "bounded_context": "BC-001",
    }
    if not isinstance(profile, dict) or any(profile.get(k) != v for k, v in expected.items()):
        raise ValueError("lifecycle contract has an unexpected owner profile")
    digest_profile = profile.get("baseline_digest")
    canonicalization = (
        digest_profile.get("canonicalization") if isinstance(digest_profile, dict) else None
    )
    if not isinstance(canonicalization, str) or not canonicalization.startswith(
        "SPEC-001 project JCS profile"
    ):
        raise ValueError("lifecycle contract does not bind SPEC-001 canonicalization")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise ValueError(f"invalid lifecycle JSON Schema: {error.message}") from error
    return schema


def schema_findings(repository_root: Path, record: dict[str, Any]) -> list[Finding]:
    try:
        validator = Draft202012Validator(
            load_contract(repository_root), format_checker=FormatChecker()
        )
    except ValueError as error:
        return [Finding("CONTRACT_INVALID", "$", str(error))]
    findings = []
    for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
        field = "$" + "".join(f"[{part!r}]" for part in error.path)
        findings.append(Finding("SCHEMA_INVALID", field, error.message))
    return findings
