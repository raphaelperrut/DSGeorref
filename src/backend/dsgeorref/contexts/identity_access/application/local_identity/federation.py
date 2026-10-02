"""OIDC ACL: explicit authenticated linking, single-use browser-bound callback."""

import hmac
from uuid import UUID

from dsgeorref.contexts.identity_access.domain.local_identity.credentials import (
    digest,
    opaque,
    uuid7,
)
from dsgeorref.contexts.identity_access.domain.local_identity.federation import OidcProvider
from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Denied,
    IssuedSession,
    Record,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance

from .observations import audit_denial
from .ports import Store
from .transactions import IdentityTransactions


class Federation:
    def __init__(self, transactions: IdentityTransactions, provider: OidcProvider) -> None:
        self.tx, self.provider = transactions, provider

    @audit_denial("begin_oidc")
    def begin(
        self, browser: str, request: Provenance, linking_session: str | None = None
    ) -> tuple[str, str]:
        self.tx.web.validate(request)
        if not browser:
            raise Denied("oidc_state_invalid")
        state, nonce = opaque(), opaque()
        with self.tx.access.uow() as store:
            principal = (
                self.tx.access.load(store, linking_session, "session") if linking_session else None
            )
            if principal:
                self.tx.browser_guard(principal, request)
                self.tx.access.enforce(store, principal, "oidc:callback")
            elif "oidc:callback" not in self.tx.access.policy.authentication_actions:
                raise Denied("oidc_state_invalid")
            store.insert(
                "oidc_transactions",
                {
                    "id": uuid7(),
                    "state_hash": digest(state),
                    "nonce_hash": digest(nonce),
                    "browser_hash": digest(browser),
                    "account_id": principal.account.id if principal else None,
                    "session_id": principal.credential.id if principal else None,
                    "expires_at": store.now() + self.tx.access.profile.oidc_lifetime,
                    "state": "pending",
                },
            )
        return state, nonce

    @audit_denial("get_auth_oidc_callback")
    def callback(self, state: str, browser: str, code: str) -> tuple[IssuedSession, bool]:
        failure, issued, linked = None, None, False
        with self.tx.access.uow() as store:
            pending = store.get("oidc_transactions", {"state_hash": digest(state)}, lock=True)
            if not pending or pending["state"] != "pending":
                raise Denied("oidc_state_invalid")
            try:
                with store.savepoint():
                    if not browser or not hmac.compare_digest(
                        pending["browser_hash"], digest(browser)
                    ):
                        raise Denied("oidc_state_invalid")
                    if pending["expires_at"] <= store.now():
                        raise Denied("oidc_state_invalid")
                    self.tx.eligible(store, "get_auth_oidc_callback", pending["account_id"])
                    identity = self.provider.exchange(code, pending["nonce_hash"])
                    if identity.expires_at <= store.now():
                        raise Denied("oidc_exchange_failed")
                    account, link, linked = self._resolve(
                        store, pending, identity.issuer, identity.subject
                    )
                    issued = self.tx.session(store, account, link)
                    store.update("oidc_transactions", {"id": pending["id"]}, {"state": "consumed"})
                    self.tx.observe(store, account, "SessionCreated", issued.session.id)
            except Denied as exc:
                failure = Denied("identity_link_conflict") if exc.code == "conflict" else exc
                store.update("oidc_transactions", {"id": pending["id"]}, {"state": "failed"})
                store.audit(
                    None,
                    "get_auth_oidc_callback",
                    pending["id"],
                    "DENIED",
                    self.tx.access.policy.version,
                    uuid7(),
                )
        if failure:
            raise failure
        assert issued is not None
        return issued, linked

    def _resolve(
        self, store: Store, pending: Record, issuer: str, subject: str
    ) -> tuple[UUID, UUID, bool]:
        link = store.get("oidc_links", {"issuer": issuer, "subject": subject}, lock=True)
        account_id = pending["account_id"] or (link["account_id"] if link else None)
        if not isinstance(account_id, UUID):
            raise Denied("identity_link_conflict")
        account = store.get("accounts", {"id": account_id}, lock=True)
        if not account or account["state"] != "active":
            raise Denied("identity_link_conflict")
        self._link_authorized(store, pending, account_id)
        if link:
            if link["state"] != "linked" or link["account_id"] != account_id:
                raise Denied("identity_link_conflict")
            return account_id, link["id"], False
        if not pending["account_id"]:
            raise Denied("identity_link_conflict")
        link_id = uuid7()
        store.insert(
            "oidc_links",
            {
                "id": link_id,
                "account_id": account_id,
                "issuer": issuer,
                "subject": subject,
                "state": "linked",
                "revision": 1,
            },
        )
        self.tx.observe(store, account_id, "link", link_id)
        return account_id, link_id, True

    def _link_authorized(self, store: Store, pending: Record, account_id: UUID) -> None:
        if pending["account_id"]:
            session = store.get("sessions", {"id": pending["session_id"]}, lock=True)
            if not session or session["state"] != "active" or session["expires_at"] <= store.now():
                raise Denied("identity_link_conflict")
            if session["idle_expires_at"] <= store.now():
                raise Denied("identity_link_conflict")
            if "oidc:callback" not in self.tx.access.policy.account_grants.get(
                account_id, frozenset()
            ):
                raise Denied("identity_link_conflict")
        elif "oidc:callback" not in self.tx.access.policy.authentication_actions:
            raise Denied("oidc_state_invalid")

    @audit_denial("unlink")
    def unlink(self, secret: str, link_id: UUID, request: Provenance) -> None:
        with self.tx.access.uow() as store:
            principal = self.tx.access.load(store, secret, "session")
            self.tx.browser_guard(principal, request)
            self.tx.access.enforce(store, principal, "oidc:callback")
            link = store.get("oidc_links", {"id": link_id}, lock=True)
            if not link or link["account_id"] != principal.account.id or link["state"] != "linked":
                raise Denied("identity_link_conflict")
            store.update(
                "oidc_links",
                {"id": link_id},
                {"state": "revoked", "revision": link["revision"] + 1},
            )
            for row in store.rows("sessions", {"oidc_link_id": link_id, "state": "active"}):
                store.update(
                    "sessions",
                    {"id": row["id"]},
                    {"state": "revoked", "revision": row["revision"] + 1},
                )
            self.tx.observe(store, principal.account.id, "unlink", link_id)
