"""Only validated external identity values enter the BC-002 ACL."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class ExternalIdentity:
    issuer: str
    subject: str
    audience: str
    expires_at: datetime
    validated_at: datetime


class OidcProvider(Protocol):
    def exchange(self, code: str, nonce_hash: str) -> ExternalIdentity: ...
