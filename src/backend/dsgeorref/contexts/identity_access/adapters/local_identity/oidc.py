"""Configured HTTPS code exchange and strict RS256 ID-token validation."""

import hmac
import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from math import isfinite
from typing import Any, Protocol

import jwt
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest
from dsgeorref.contexts.identity_access.domain.local_identity.federation import ExternalIdentity
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied


@dataclass(frozen=True)
class OidcConfig:
    enabled: bool
    issuer: str
    client_id: str
    redirect_uri: str
    token_endpoint: str
    jwks_uri: str
    timeout: float

    def validate(self) -> None:
        urls = (self.issuer, self.redirect_uri, self.token_endpoint, self.jwks_uri)
        if (
            self.enabled is not True
            or not self.client_id
            or not isfinite(self.timeout)
            or self.timeout <= 0
        ):
            raise Denied("oidc_exchange_failed")
        for url in urls:
            parsed = urllib.parse.urlsplit(url)
            if (
                parsed.scheme != "https"
                or not parsed.hostname
                or parsed.username
                or parsed.fragment
            ):
                raise Denied("oidc_exchange_failed")


class ProviderTransport(Protocol):
    def token(self, config: OidcConfig, code: str) -> str: ...
    def keys(self, config: OidcConfig) -> dict[str, Any]: ...


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> None:
        raise Denied("oidc_exchange_failed")


class HttpsProviderTransport:
    def _json(self, request: urllib.request.Request, timeout: float) -> dict[str, Any]:
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(request, timeout=timeout) as response:
            # Bounded provider input protects the parser and key selector.
            payload = response.read(1_048_577)
        if len(payload) > 1_048_576:
            raise Denied("oidc_exchange_failed")
        result = json.loads(payload)
        if not isinstance(result, dict):
            raise Denied("oidc_exchange_failed")
        return result

    def token(self, config: OidcConfig, code: str) -> str:
        data = urllib.parse.urlencode(
            {
                "grant_type": "authorization_code",
                "code": code,
                "client_id": config.client_id,
                "redirect_uri": config.redirect_uri,
            }
        ).encode()
        request = urllib.request.Request(config.token_endpoint, data=data, method="POST")
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        result = self._json(request, config.timeout)
        token = result.get("id_token")
        if not isinstance(token, str):
            raise Denied("oidc_exchange_failed")
        return token

    def keys(self, config: OidcConfig) -> dict[str, Any]:
        return self._json(urllib.request.Request(config.jwks_uri), config.timeout)


class ValidatingOidcProvider:
    def __init__(self, config: OidcConfig, transport: ProviderTransport) -> None:
        self.config, self.transport = config, transport

    def exchange(self, code: str, nonce_hash: str) -> ExternalIdentity:
        self.config.validate()
        try:
            token = self.transport.token(self.config, code)
            header = jwt.get_unverified_header(token)
            if header.get("alg") != "RS256" or not isinstance(header.get("kid"), str):
                raise Denied("oidc_exchange_failed")
            key = self._key(header["kid"])
            claims = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=self.config.client_id,
                issuer=self.config.issuer,
                options={"require": ["iss", "sub", "aud", "exp", "iat", "nonce"]},
            )
            if not isinstance(claims["nonce"], str) or not hmac.compare_digest(
                digest(claims["nonce"]), nonce_hash
            ):
                raise Denied("oidc_state_invalid")
            if not isinstance(claims["sub"], str) or not claims["sub"]:
                raise Denied("oidc_exchange_failed")
            return ExternalIdentity(
                self.config.issuer,
                claims["sub"],
                self.config.client_id,
                datetime.fromtimestamp(claims["exp"], UTC),
                datetime.now(UTC),
            )
        except Denied:
            raise
        except (jwt.PyJWTError, OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
            raise Denied("oidc_exchange_failed") from exc

    def _key(self, kid: str) -> Any:
        keys = self.transport.keys(self.config).get("keys", [])
        candidates = [
            k
            for k in keys
            if k.get("kid") == kid
            and k.get("kty") == "RSA"
            and k.get("use", "sig") == "sig"
            and k.get("alg", "RS256") == "RS256"
        ]
        if len(candidates) != 1:
            raise Denied("oidc_exchange_failed")
        return jwt.PyJWK.from_dict(candidates[0], algorithm="RS256").key
