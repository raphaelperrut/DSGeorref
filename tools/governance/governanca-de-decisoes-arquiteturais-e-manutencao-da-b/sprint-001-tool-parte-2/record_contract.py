from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from slice_one import Finding


REFERENCE_FIELDS = frozenset({"source_revision", "path", "sha256"})


def strict_fields(
    value: object,
    expected: frozenset[str],
    field: str,
) -> list[Finding]:
    if not isinstance(value, Mapping):
        return [Finding("RECORD_TYPE_INVALID", field, "expected an object")]
    string_keys = {key for key in value if isinstance(key, str)}
    invalid_keys = [key for key in value if not isinstance(key, str)]
    findings = [
        Finding("FIELD_MISSING", f"{field}.{name}", "required field is absent")
        for name in sorted(expected - string_keys)
    ]
    findings.extend(
        Finding("FIELD_UNKNOWN", f"{field}.{name}", "unknown field is forbidden")
        for name in sorted(string_keys - expected)
    )
    findings.extend(
        Finding("FIELD_UNKNOWN", field, f"non-string field is forbidden: {key!r}")
        for key in invalid_keys
    )
    return findings


def reference_findings(value: object, field: str) -> list[Finding]:
    findings = strict_fields(value, REFERENCE_FIELDS, field)
    if findings or not isinstance(value, Mapping):
        return findings
    for name in sorted(REFERENCE_FIELDS):
        if not isinstance(value.get(name), str) or not value[name]:
            findings.append(
                Finding("REFERENCE_FIELD_INVALID", f"{field}.{name}", "must be a string")
            )
    digest = value.get("sha256")
    if isinstance(digest, str) and (
        len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest)
    ):
        findings.append(
            Finding("REFERENCE_DIGEST_INVALID", f"{field}.sha256", "must be lowercase SHA-256")
        )
    return findings


def ordered_unique_strings(value: object, field: str) -> list[Finding]:
    if not isinstance(value, Sequence) or isinstance(value, str | bytes):
        return [Finding("SEQUENCE_INVALID", field, "expected an array")]
    if not all(isinstance(item, str) and item for item in value):
        return [Finding("SEQUENCE_ITEM_INVALID", field, "items must be non-empty strings")]
    items = list(value)
    if items != sorted(set(items)):
        return [Finding("SEQUENCE_NON_CANONICAL", field, "items must be sorted and unique")]
    return []


def as_mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None
