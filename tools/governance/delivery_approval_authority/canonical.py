from __future__ import annotations

import json
import math
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any


class CanonicalizationError(ValueError):
    """Raised when bytes cannot enter the DAA canonical JSON profile."""


def _pairs_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalizationError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def load_json_object(data: bytes) -> dict[str, Any]:
    if data.startswith(b"\xef\xbb\xbf"):
        raise CanonicalizationError("UTF-8 BOM is not canonical")
    try:
        value = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_pairs_without_duplicates,
            parse_constant=lambda item: (_ for _ in ()).throw(
                CanonicalizationError(f"non-finite JSON number: {item}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CanonicalizationError("invalid UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise CanonicalizationError("JSON document must be an object")
    return value


def _normalize(value: Any) -> Any:
    if value is None or isinstance(value, bool | int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalizationError("non-finite JSON number")
        return value
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, Mapping):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("JSON object keys must be strings")
            normalized_key = unicodedata.normalize("NFC", key)
            if normalized_key in normalized:
                raise CanonicalizationError("duplicate key after NFC normalization")
            normalized[normalized_key] = _normalize(item)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, bytes | bytearray):
        return [_normalize(item) for item in value]
    raise CanonicalizationError(f"unsupported JSON value: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        _normalize(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
