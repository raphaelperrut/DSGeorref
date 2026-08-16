from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, order=True)
class Finding:
    artifact: str
    code: str
    detail: str


def closed_keys(
    value: Any, expected: set[str], artifact: str, section: str
) -> list[Finding]:
    if not isinstance(value, dict):
        return [Finding(artifact, "INVALID_STRUCTURE", f"{section} must be an object")]
    actual = set(value)
    findings = [
        Finding(artifact, "REQUIRED_PROPERTY_MISSING", f"{section}.{key} is required")
        for key in sorted(expected - actual)
    ]
    findings.extend(
        Finding(artifact, "UNKNOWN_PROPERTY", f"{section}.{key} is not allowed")
        for key in sorted(actual - expected)
    )
    return findings


def expect(
    actual: Any, expected: Any, artifact: str, field: str, code: str = "INVALID_VALUE"
) -> list[Finding]:
    if actual == expected:
        return []
    return [Finding(artifact, code, f"{field}: expected {expected!r}, found {actual!r}")]


def string_set(value: Any, artifact: str, field: str) -> tuple[set[str], list[Finding]]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        return set(), [
            Finding(artifact, "INVALID_STRUCTURE", f"{field} must be an array of strings")
        ]
    return set(value), []
