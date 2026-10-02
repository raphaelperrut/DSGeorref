"""Shared transactional operations within the local identity application."""

import hashlib
import hmac
import json
from collections.abc import Callable
from dataclasses import asdict
from uuid import UUID

from dsgeorref.contexts.identity_access.domain.local_identity.credentials import (
    digest,
    opaque,
    uuid7,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Denied,
    IssuedSession,
    Principal,
    Record,
    Session,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance, WebPolicy

from .access import Access
from .ports import Passwords, Store

Eligibility = Callable[[Store, str, UUID | None], bool]


class IdentityTransactions:
    def __init__(
        self,
        access: Access,
        passwords: Passwords,
        web: WebPolicy,
        eligibility: Eligibility,
        replay_key: bytes,
    ) -> None:
        if not replay_key or not callable(eligibility):
            raise Denied("internal_error")
        self.access, self.passwords, self.web = access, passwords, web
        self.eligibility, self._replay_key = eligibility, replay_key

    def eligible(self, store: Store, operation: str, actor: UUID | None) -> None:
        if self.eligibility(store, operation, actor) is not True:
            raise Denied("rate_limited")

    def request(
        self, store: Store, operation: str, actor: UUID | None, key: str, payload: Record
    ) -> Record | None:
        if not key:
            raise Denied("validation_failed")
        fingerprint = hmac.new(
            self._replay_key,
            json.dumps(payload, sort_keys=True, default=str).encode(),
            hashlib.sha256,
        ).hexdigest()
        identity = {"operation": operation, "principal_id": actor, "key_hash": digest(key)}
        prior = store.get("requests", identity, lock=True)
        if prior:
            if prior["payload_hash"] != fingerprint:
                raise Denied("conflict")
            return prior
        store.insert("requests", {**identity, "payload_hash": fingerprint, "outcome_id": None})
        return None

    def finish(
        self, store: Store, operation: str, actor: UUID | None, key: str, outcome: UUID
    ) -> None:
        store.update(
            "requests",
            {"operation": operation, "principal_id": actor, "key_hash": digest(key)},
            {"outcome_id": outcome},
        )

    def session(self, store: Store, account: UUID, link: UUID | None = None) -> IssuedSession:
        secret, csrf = opaque(), opaque()
        now = store.now()
        session = Session(
            uuid7(),
            account,
            digest(secret),
            digest(csrf),
            now + self.access.profile.session_absolute,
            now + self.access.profile.session_idle,
            oidc_link_id=link,
        )
        store.insert("sessions", asdict(session))
        return IssuedSession(session, secret, csrf)

    def browser_guard(self, principal: Principal, request: Provenance | None) -> None:
        if isinstance(principal.credential, Session):
            if request is None:
                raise Denied("forbidden")
            self.web.validate(request, principal.credential.csrf_hash)

    def observe(self, store: Store, actor: UUID | None, event: str, target: UUID) -> None:
        store.audit(actor, event, target, "COMMITTED", self.access.policy.version, uuid7())
