from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .repository import governed_schema


class SchemaSet:
    def __init__(self, repository: Path, revision: str) -> None:
        self._validators: dict[str, Draft202012Validator] = {}
        for name in ("anchors", "profile", "binding", "attestation", "verdict", "task"):
            schema = governed_schema(repository, revision, name)
            Draft202012Validator.check_schema(schema)
            self._validators[name] = Draft202012Validator(
                schema,
                format_checker=FormatChecker(),
            )

    def code(self, name: str, record: Any) -> str | None:
        errors = sorted(
            self._validators[name].iter_errors(record),
            key=lambda error: [str(item) for item in error.path],
        )
        if not errors:
            return None
        if list(errors[0].path)[-1:] == ["trust_scope"]:
            return "TRUST_SCOPE_INVALID"
        return "SCHEMA_INVALID"

    def validate_verdict(self, verdict: dict[str, Any]) -> None:
        self._validators["verdict"].validate(verdict)
