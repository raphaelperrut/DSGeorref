from __future__ import annotations

import base64
import copy
import hashlib
from datetime import datetime
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .canonical import canonical_json_bytes


DOMAINS = {
    "profile": "DSGEOREF-DELIVERY-APPROVAL-TRUST-PROFILE-V1",
    "binding": "DSGEOREF-DELIVERY-APPROVAL-ROLE-BINDING-V1",
    "attestation": "DSGEOREF-DELIVERY-APPROVAL-ATTESTATION-V1",
}


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("instant must include an offset")
    return parsed


def usable(record: dict[str, Any], at: datetime, checked_at: datetime) -> str | None:
    if not (instant(record["valid_from"]) <= at < instant(record["valid_until"])):
        return "TEMPORAL_INVALID"
    revoked_at = record["revoked_at"]
    if revoked_at is not None and instant(revoked_at) <= checked_at:
        return "REVOKED"
    return None


def verify_signature(document: dict[str, Any], public_key: str, kind: str) -> bool:
    try:
        projection = copy.deepcopy(document)
        projection["signature"]["value"] = ""
        message = DOMAINS[kind].encode("ascii") + b"\x00" + canonical_json_bytes(projection)
        key_bytes = base64.urlsafe_b64decode(public_key + "=" * (-len(public_key) % 4))
        signature = document["signature"]["value"]
        signature_bytes = base64.urlsafe_b64decode(signature + "=" * (-len(signature) % 4))
        Ed25519PublicKey.from_public_bytes(key_bytes).verify(signature_bytes, message)
    except (InvalidSignature, ValueError, KeyError, TypeError):
        return False
    return True
