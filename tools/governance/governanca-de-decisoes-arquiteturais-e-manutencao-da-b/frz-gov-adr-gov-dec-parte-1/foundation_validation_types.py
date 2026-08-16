from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


class NormativeValidationError(ValueError):
    def __init__(self, findings: list[Finding] | tuple[Finding, ...]) -> None:
        ordered = tuple(sorted(findings))
        self.findings = ordered
        message = "; ".join(
            f"{finding.code} at {finding.field}: {finding.detail}"
            for finding in ordered
        )
        super().__init__(message)


def require_valid(findings: list[Finding] | tuple[Finding, ...]) -> None:
    if findings:
        raise NormativeValidationError(findings)
