from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Finding:
    artifact: str
    code: str
    detail: str


def mismatch(
    actual: object,
    expected: object,
    artifact: str,
    field: str,
    code: str = "INVALID_VALUE",
) -> list[Finding]:
    if actual == expected:
        return []
    return [Finding(artifact, code, f"{field}: expected {expected!r}, found {actual!r}")]
