from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, order=True)
class Finding:
    artifact: str
    code: str
    detail: str
    remediation: str


def finding(
    artifact: Path | str,
    code: str,
    detail: str,
    remediation: str,
) -> Finding:
    rendered = artifact.as_posix() if isinstance(artifact, Path) else artifact
    return Finding(rendered, code, detail, remediation)


def load_json(root: Path, relative: Path) -> tuple[Any | None, list[Finding]]:
    path = root / relative
    if not path.is_file():
        return None, [
            finding(
                relative,
                "ARTIFACT_MISSING",
                "required JSON artifact is absent",
                f"Restore the versioned artifact at {relative.as_posix()}.",
            )
        ]
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [
            finding(
                relative,
                "JSON_INVALID",
                str(exc).splitlines()[0],
                "Provide a readable UTF-8 JSON document with valid syntax.",
            )
        ]


def expect_equal(
    findings: list[Finding],
    *,
    artifact: Path,
    field: str,
    actual: Any,
    expected: Any,
    code: str,
) -> None:
    if actual != expected:
        findings.append(
            finding(
                artifact,
                code,
                f"{field} expected {expected!r}, found {actual!r}",
                f"Restore {field} to the frozen EPIC-110 contract value.",
            )
        )
