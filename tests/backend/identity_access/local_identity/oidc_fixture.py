"""Real signed JWTs; transport is isolated from the network and contains no real secrets."""

from datetime import UTC, datetime, timedelta

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import OidcConfig


class SignedProvider:
    def __init__(self, nonce: str) -> None:
        self.nonce = nonce
        self.signer = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public = self.signer.public_key()
        self.subject = "external-subject"
        self.audience = "test-client"
        self.issuer = "https://provider.example.test"
        self.outage = False

    def token(self, config, code):
        if self.outage:
            raise OSError("synthetic outage")
        now = datetime.now(UTC)
        return jwt.encode(
            {
                "iss": self.issuer,
                "aud": self.audience,
                "sub": self.subject,
                "nonce": self.nonce,
                "iat": now,
                "exp": now + timedelta(minutes=1),
            },
            self.signer,
            algorithm="RS256",
            headers={"kid": "test-key"},
        )

    def keys(self, config):
        key = jwt.algorithms.RSAAlgorithm.to_jwk(self.public, as_dict=True)
        return {"keys": [{**key, "kid": "test-key", "alg": "RS256", "use": "sig"}]}


def config() -> OidcConfig:
    return OidcConfig(
        True,
        "https://provider.example.test",
        "test-client",
        "https://identity.example.test/auth/oidc/callback",
        "https://provider.example.test/token",
        "https://provider.example.test/jwks",
        2,
    )
