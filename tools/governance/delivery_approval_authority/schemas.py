from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .repository import governed_json, governed_schema


class SchemaSet:
    def __init__(self, repository: Path, revision: str) -> None:
        self._repository = repository
        self._revision = revision
        self._validators: dict[str, Draft202012Validator] = {}
        for name in ("anchors", "profile", "binding", "attestation", "verdict", "task"):
            schema = governed_schema(repository, revision, name)
            Draft202012Validator.check_schema(schema)
            self._validators[name] = Draft202012Validator(
                schema,
                format_checker=FormatChecker(),
            )

    def for_contract_version(self, version: str) -> SchemaSet:
        """Use governed schemas matching the verifier trust version."""
        if version not in {"1.0.0", "2.0.0"}:
            raise ValueError("unsupported delivery approval contract version")

        active = self._validators["verdict"].schema["properties"]["schema_version"]["const"]
        if active == version:
            return self

        filenames = {
            "profile": "trust-profile.schema.json",
            "binding": "role-binding.schema.json",
            "attestation": "approval-attestation.schema.json",
            "verdict": "verification-verdict.schema.json",
        }
        prefix = "v2/" if version == "2.0.0" else ""
        contract_root = "contracts/assurance/delivery-approval-authority"

        selected = SchemaSet.__new__(SchemaSet)
        selected._repository = self._repository
        selected._revision = self._revision
        selected._validators = dict(self._validators)

        for name, filename in filenames.items():
            schema = governed_json(
                self._repository,
                self._revision,
                f"{contract_root}/{prefix}{filename}",
            )
            Draft202012Validator.check_schema(schema)
            if schema["properties"]["schema_version"]["const"] != version:
                raise ValueError("governed schema version mismatch")
            selected._validators[name] = Draft202012Validator(
                schema,
                format_checker=FormatChecker(),
            )

        return selected

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
