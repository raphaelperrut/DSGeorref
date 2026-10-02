"""Atomic rotation and deterministic owner logout."""

from uuid import UUID

from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Denied,
    IssuedSession,
    Session,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance

from .observations import audit_denial
from .transactions import IdentityTransactions


class Sessions:
    def __init__(self, transactions: IdentityTransactions) -> None:
        self.tx = transactions

    @audit_denial("rotate")
    def rotate(self, secret: str, revision: int, request: Provenance) -> IssuedSession:
        with self.tx.access.uow() as store:
            principal = self.tx.access.load(store, secret, "session")
            self.tx.browser_guard(principal, request)
            self.tx.access.enforce(store, principal, "session:create")
            session = principal.credential
            assert isinstance(session, Session)
            if session.revision != revision:
                raise Denied("precondition_failed")
            issued = self.tx.session(store, principal.account.id, session.oidc_link_id)
            store.update(
                "sessions",
                {"id": session.id, "revision": revision},
                {"state": "rotated", "revision": revision + 1},
            )
            self.tx.observe(store, principal.account.id, "rotate", session.id)
        return issued

    @audit_denial("delete_auth_session")
    def logout(
        self,
        secret: str,
        kind: str,
        revision: int,
        key: str,
        request: Provenance | None,
        target: UUID | None = None,
    ) -> None:
        with self.tx.access.uow() as store:
            principal = self.tx.access.load(store, secret, kind)
            self.tx.access.enforce(store, principal, "session:revoke")
            self.tx.browser_guard(principal, request)
            if target is None and isinstance(principal.credential, Session):
                target = principal.credential.id
            row = store.get("sessions", {"id": target}, lock=True) if target else None
            if not row or row["account_id"] != principal.account.id:
                raise Denied("session_not_found")
            assert target is not None
            if row["revision"] != revision or row["state"] != "active":
                raise Denied("internal_error")
            self.tx.request(
                store,
                "delete_auth_session",
                principal.account.id,
                key,
                {"target": target, "revision": revision},
            )
            store.update(
                "sessions",
                {"id": target, "revision": revision},
                {"state": "revoked", "revision": revision + 1},
            )
            self.tx.finish(store, "delete_auth_session", principal.account.id, key, target)
            self.tx.observe(store, principal.account.id, "SessionRevoked", target)
