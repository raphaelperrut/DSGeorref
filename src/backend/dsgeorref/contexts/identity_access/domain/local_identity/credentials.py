"""Secret digests, entropy and UUIDv7 identities owned by BC-002."""

import hashlib
import secrets
import time
from uuid import UUID


def digest(secret: str) -> str:
    return hashlib.sha256(secret.encode()).hexdigest()


def opaque() -> str:
    return secrets.token_urlsafe(32)


def uuid7() -> UUID:
    bits = ((time.time_ns() // 1_000_000) << 80) | (7 << 76)
    bits |= secrets.randbits(12) << 64
    bits |= (2 << 62) | secrets.randbits(62)
    return UUID(int=bits)
