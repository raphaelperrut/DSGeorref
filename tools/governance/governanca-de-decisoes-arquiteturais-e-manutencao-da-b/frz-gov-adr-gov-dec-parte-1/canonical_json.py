from __future__ import annotations

import json
import math
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any


class CanonicalizationError(ValueError):
    pass


def _pairs_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalizationError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def load_json_bytes(data: bytes) -> Any:
    if data.startswith(b"\xef\xbb\xbf"):
        raise CanonicalizationError("UTF-8 BOM is not canonical")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CanonicalizationError("content is not UTF-8") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=_pairs_without_duplicates,
            parse_constant=lambda value: (_ for _ in ()).throw(
                CanonicalizationError(f"non-finite JSON number: {value}")
            ),
        )
    except json.JSONDecodeError as error:
        raise CanonicalizationError(f"invalid JSON: {error.msg}") from error


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
                raise CanonicalizationError(
                    f"duplicate key after NFC normalization: {normalized_key!r}"
                )
            normalized[normalized_key] = _normalize(item)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, bytes | bytearray):
        return [_normalize(item) for item in value]
    raise CanonicalizationError(f"unsupported JSON value: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    normalized = _normalize(value)
    return json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
