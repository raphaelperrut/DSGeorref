"""Closed delivery-gate records and canonical digest rules (ADR-006)."""

from __future__ import annotations

import hashlib
import re
from pathlib import PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError, ValidationError
from tools.governance.delivery_approval_authority.canonical import load_json_object
from tools.governance.delivery_approval_authority.crypto import digest

REGISTRY = "docs/06-delivery/DELIVERY_GATES.json"
SCHEMA = "docs/06-delivery/DELIVERY_GATES.schema.json"
TASK_SCHEMA = ".codex/tasks/TASK_ENVELOPE.schema.json"
GRAPH = "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"


class GateError(ValueError):
    """A gate cannot be validated or released; never implies satisfaction."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def relative_path(value: str) -> str:
    pure = PurePosixPath(value)
    require(bool(value) and not pure.is_absolute(), f"invalid relative path: {value}")
    require(not re.search(r"[\\:*?\[\]#\x00-\x1f]", value), f"unsafe path: {value}")
    require(
        not any(part in {"", ".", ".."} for part in value.split("/")), f"noncanonical path: {value}"
    )
    return value


def parse(content: bytes) -> dict[str, Any]:
    try:
        return load_json_object(content)
    except ValueError as error:
        raise GateError(f"invalid canonical JSON: {error}") from error


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def definition_digest(gate: dict[str, Any]) -> str:
    return digest(gate)


def validate_schema(document: Any, schema: dict[str, Any], kind: str = "Registry") -> None:
    try:
        Draft202012Validator.check_schema(schema)
        selected = (
            schema if kind == "Registry" else {"$ref": f"#/$defs/{kind}", "$defs": schema["$defs"]}
        )
        Draft202012Validator(selected, format_checker=FormatChecker()).validate(document)
    except (ValueError, SchemaError, ValidationError) as error:
        raise GateError(f"{kind} schema invalid: {error}") from error
