"""Hash-only, one-time issuance constrained by current policy and project scope."""

from dataclasses import asdict
from datetime import datetime
from uuid import UUID

from dsgeorref.contexts.identity_access.domain.local_identity.credentials import (
    digest,
    opaque,
    uuid7,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Denied,
    IssuedToken,
    PersonalAccessToken,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance

from .observations import audit_denial
from .transactions import IdentityTransactions


class Tokens:
    def __init__(self, transactions: IdentityTransactions) -> None:
        self.tx = transactions

    @audit_denial("post_auth_tokens")
    def issue(
        self,
        secret: str,
        kind: str,
        scopes: list[str],
        key: str,
        request: Provenance | None,
        project: UUID | None = None,
        expires: datetime | None = None,
    ) -> IssuedToken:
        with self.tx.access.uow() as store:
            principal = self.tx.access.load(store, secret, kind)
            self.tx.access.enforce(store, principal, "token:create")
            self.tx.browser_guard(principal, request)
            self.tx.eligible(store, "post_auth_tokens", principal.account.id)
            if not scopes or len(scopes) != len(set(scopes)):
                raise Denied("validation_failed")
            for scope in scopes:
                self.tx.access.enforce(store, principal, scope, project)
            now = store.now()
            expiry = expires or now + self.tx.access.profile.pat_lifetime
            if (
                expiry.tzinfo is None
                or not now < expiry <= now + self.tx.access.profile.pat_lifetime
            ):
                raise Denied("validation_failed")
            replay = self.tx.request(
                store,
                "post_auth_tokens",
                principal.account.id,
                key,
                {"scopes": scopes, "project": project, "expires": expires},
            )
            if replay:
                raise Denied("conflict")
            raw = "pat_" + opaque()
            token = PersonalAccessToken(
                uuid7(), principal.account.id, digest(raw), scopes, expiry, project
            )
            store.insert("tokens", asdict(token))
            self.tx.finish(store, "post_auth_tokens", principal.account.id, key, token.id)
            self.tx.observe(store, principal.account.id, "TokenIssued", token.id)
        return IssuedToken(token, raw)

    @audit_denial("revoke")
    def revoke(self, secret: str, kind: str, token_id: UUID, request: Provenance | None) -> None:
        with self.tx.access.uow() as store:
            principal = self.tx.access.load(store, secret, kind)
            self.tx.browser_guard(principal, request)
            row = store.get("tokens", {"id": token_id}, lock=True)
            if not row or row["account_id"] != principal.account.id:
                raise Denied("forbidden")
            if row["state"] == "active":
                store.update(
                    "tokens",
                    {"id": token_id},
                    {"state": "revoked", "revision": row["revision"] + 1},
                )
                self.tx.observe(store, principal.account.id, "revoke", token_id)
