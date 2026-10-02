"""Web provenance is required on browser entry and cookie mutations."""

import hmac
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from .credentials import digest
from .models import Denied


@dataclass(frozen=True)
class Provenance:
    origin: str
    fetch_site: str
    csrf: str | None = field(default=None, repr=False)


@dataclass(frozen=True)
class WebPolicy:
    origin: str
    cors_allowlist: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        for origin in (self.origin, *self.cors_allowlist):
            parsed = urlsplit(origin)
            if parsed.scheme != "https" or not parsed.netloc or parsed.path:
                raise Denied("internal_error")
            if parsed.query or parsed.fragment or parsed.username or parsed.password:
                raise Denied("internal_error")

    def validate(self, request: Provenance, csrf_hash: str | None = None) -> None:
        if request.origin != self.origin or request.fetch_site != "same-origin":
            raise Denied("forbidden")
        if csrf_hash is not None and (
            not request.csrf or not hmac.compare_digest(digest(request.csrf), csrf_hash)
        ):
            raise Denied("forbidden")
