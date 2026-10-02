"""Wire-format web defaults; provenance decisions remain in the domain policy."""

from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from dsgeorref.contexts.identity_access.domain.local_identity.web import WebPolicy


class WebResponses:
    def __init__(self, policy: WebPolicy) -> None:
        self.policy = policy

    def headers(self, request_origin: str | None = None) -> dict[str, str]:
        result = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'",
            "Referrer-Policy": "no-referrer",
            "Cache-Control": "no-store",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        }
        if request_origin in self.policy.cors_allowlist:
            result.update(
                {
                    "Access-Control-Allow-Origin": request_origin,
                    "Access-Control-Allow-Credentials": "true",
                    "Vary": "Origin",
                }
            )
        return result

    def cookie(self, secret: str) -> str:
        if any(
            c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
            for c in secret
        ):
            raise Denied("internal_error")
        return f"dsgeorref_session={secret}; Path=/; Secure; HttpOnly; SameSite=Strict"

    def clear_cookie(self) -> str:
        return self.cookie("") + "; Max-Age=0"
