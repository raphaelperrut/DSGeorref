from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from canonical_json import CanonicalizationError, canonical_json_bytes


class AppendOnlyRecordLedger:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str], bytes] = {}

    def append(self, record: Mapping[str, Any]) -> None:
        record_type = record.get("record_type")
        identity_fields = {
            "FOUNDATION_BASELINE": "baseline_id",
            "FOUNDATION_BASELINE_SUPERSESSION": "supersession_id",
            "FOUNDATION_CLOSURE_EVIDENCE_SET": "evidence_set_id",
            "FOUNDATION_CLOSURE": "closure_id",
            "FOUNDATION_REOPENING": "reopening_id",
        }
        identity_field = identity_fields.get(str(record_type))
        if identity_field is None or not isinstance(record.get(identity_field), str):
            raise ValueError("record has no recognized immutable identity")
        identity = str(record[identity_field])
        if record_type == "FOUNDATION_BASELINE":
            version = record.get("baseline_version")
            if not isinstance(version, str):
                raise ValueError("baseline record has no immutable version")
            identity = f"{identity}@{version}"
        key = (str(record_type), identity)
        encoded = canonical_json_bytes(record)
        existing = self._records.get(key)
        if existing is not None and existing != encoded:
            raise ValueError("silent replacement of an immutable record is forbidden")
        self._records[key] = encoded

    def contains_exactly(self, record: Mapping[str, Any]) -> bool:
        try:
            record_type = str(record["record_type"])
            field = {
                "FOUNDATION_BASELINE": "baseline_id",
                "FOUNDATION_BASELINE_SUPERSESSION": "supersession_id",
                "FOUNDATION_CLOSURE_EVIDENCE_SET": "evidence_set_id",
                "FOUNDATION_CLOSURE": "closure_id",
                "FOUNDATION_REOPENING": "reopening_id",
            }[record_type]
            identity = str(record[field])
            if record_type == "FOUNDATION_BASELINE":
                identity = f"{identity}@{record['baseline_version']}"
            return self._records[(record_type, identity)] == canonical_json_bytes(record)
        except (KeyError, CanonicalizationError):
            return False
