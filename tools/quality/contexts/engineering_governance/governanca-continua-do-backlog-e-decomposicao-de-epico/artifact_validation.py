from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from contract_definition import EXAMPLE_REL, SCHEMA_REL
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from jsonschema.exceptions import SchemaError  # type: ignore[import-untyped]
from validation_types import Finding, finding, load_json


def _safe_reference(reference: Any) -> Path | None:
    if not isinstance(reference, str) or not reference:
        return None
    relative = Path(reference)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    if not relative.parts or relative.parts[0] != "contracts":
        return None
    return relative


def _referenced_pairs(profile: dict[str, Any]) -> list[tuple[Any, Any]]:
    controls = profile.get("controls")
    if not isinstance(controls, dict):
        return []
    names = (
        "portfolio_catalog",
        "forecast",
        "integration_checkpoint",
        "foundation_boundaries",
    )
    selected = [controls.get(name) for name in names]
    if not all(isinstance(control, dict) for control in selected):
        return []
    portfolio, forecast, checkpoint, boundaries = (
        cast(dict[str, Any], control) for control in selected
    )
    return [
        (portfolio.get("schema"), portfolio.get("example")),
        (forecast.get("schema"), forecast.get("example")),
        (checkpoint.get("profile_schema"), checkpoint.get("profile_example")),
        (boundaries.get("schema"), boundaries.get("example")),
    ]


def _schema_errors(schema: Any, artifact: Path) -> tuple[Any | None, list[Finding]]:
    if not isinstance(schema, dict):
        return None, [
            finding(
                artifact,
                "SCHEMA_STRUCTURE_INVALID",
                "schema root must be an object",
                "Restore a JSON Schema Draft 2020-12 object.",
            )
        ]
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return None, [
            finding(
                artifact,
                "SCHEMA_INVALID",
                str(exc).splitlines()[0],
                "Restore a valid JSON Schema Draft 2020-12 document.",
            )
        ]
    return schema, []


def _validate_pair(
    root: Path,
    schema_rel: Path,
    example_rel: Path,
    violation_code: str,
) -> list[Finding]:
    schema, findings = load_json(root, schema_rel)
    example, example_findings = load_json(root, example_rel)
    findings.extend(example_findings)
    checked_schema, schema_findings = _schema_errors(schema, schema_rel)
    findings.extend(schema_findings)
    if checked_schema is None or example is None:
        return findings
    errors = sorted(
        Draft202012Validator(checked_schema).iter_errors(example),
        key=lambda error: list(error.absolute_path),
    )
    for error in errors:
        location = "/" + "/".join(str(part) for part in error.absolute_path)
        findings.append(
            finding(
                example_rel,
                violation_code,
                f"{location}: {error.message}",
                f"Make {example_rel.as_posix()} conform to {schema_rel.as_posix()}.",
            )
        )
    return findings


def validate_profile(root: Path) -> list[Finding]:
    findings = _validate_pair(
        root,
        SCHEMA_REL,
        EXAMPLE_REL,
        "PROFILE_SCHEMA_VIOLATION",
    )
    profile, load_findings = load_json(root, EXAMPLE_REL)
    if load_findings or not isinstance(profile, dict):
        return findings
    if any(item.artifact == EXAMPLE_REL.as_posix() for item in findings):
        return findings
    pairs = _referenced_pairs(profile)
    if len(pairs) != 4:
        findings.append(
            finding(
                EXAMPLE_REL,
                "CONTRACT_REFERENCE_SET_INVALID",
                "four schema/example reference pairs are required",
                "Restore every reference required by the frozen profile schema.",
            )
        )
        return findings
    for schema_ref, example_ref in pairs:
        schema_rel = _safe_reference(schema_ref)
        example_rel = _safe_reference(example_ref)
        if schema_rel is None or example_rel is None:
            findings.append(
                finding(
                    EXAMPLE_REL,
                    "CONTRACT_REFERENCE_UNSAFE",
                    f"invalid schema/example reference: {schema_ref!r}, {example_ref!r}",
                    "Use repository-relative paths under contracts/ without traversal.",
                )
            )
            continue
        findings.extend(
            _validate_pair(
                root,
                schema_rel,
                example_rel,
                "REFERENCED_EXAMPLE_SCHEMA_VIOLATION",
            )
        )
    return findings
