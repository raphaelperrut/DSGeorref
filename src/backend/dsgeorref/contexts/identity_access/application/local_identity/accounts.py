"""One-time bootstrap and local authentication; no HTTP surface is added."""

from dataclasses import asdict
from uuid import UUID

from dsgeorref.contexts.identity_access.domain.local_identity.credentials import (
    digest,
    opaque,
    uuid7,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Account,
    Denied,
    IssuedSession,
    Session,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance

from .observations import audit_denial
from .ports import Store
from .throttling import LoginThrottle
from .transactions import IdentityTransactions


class LocalAccounts:
    def __init__(
        self, transactions: IdentityTransactions, throttle: LoginThrottle | None = None
    ) -> None:
        self.tx = transactions
        self.throttle = throttle
        length = self.tx.access.profile.min_password_length
        self._dummy_hash = self.tx.passwords.hash((opaque() * (length // 43 + 1))[:length])

    @audit_denial("post_auth_bootstrap")
    def bootstrap(
        self,
        username: str,
        password: str,
        key: str,
        request: Provenance,
        *,
        display_name: str | None = None,
    ) -> tuple[Account, IssuedSession, str]:
        self.tx.web.validate(request)
        if "instance:bootstrap" not in self.tx.access.policy.installation_actions:
            raise Denied("validation_failed")
        if not username or username != username.strip():
            raise Denied("validation_failed")
        with self.tx.access.uow() as store:
            state = store.get("bootstrap", {"singleton": True}, lock=True)
            if state is None:
                raise Denied("internal_error")
            self.tx.eligible(store, "post_auth_bootstrap", None)
            replay = self.tx.request(
                store,
                "post_auth_bootstrap",
                None,
                key,
                _bootstrap_payload(username, password, display_name),
            )
            if replay:
                prior_account = store.get("accounts", {"id": state["administrator_id"]})
                session = store.get("sessions", {"id": replay["outcome_id"]})
                if not prior_account or not session or prior_account["state"] != "active":
                    raise Denied("internal_error")
                if session["state"] != "active" or self.tx.access.expired(
                    Session(**session), store.now()
                ):
                    raise Denied("bootstrap_already_completed")
                return Account(**prior_account), IssuedSession(Session(**session), "", ""), ""
            if state["state"] != "available" or state["administrator_id"] is not None:
                raise Denied("bootstrap_already_completed")
            encoded = self.tx.passwords.hash(password)
            recovery = opaque()
            account = Account(uuid7(), username, encoded, digest(recovery), administrator=True)
            store.insert("accounts", asdict(account))
            issued = self.tx.session(store, account.id)
            store.update(
                "bootstrap",
                {"singleton": True},
                {
                    "state": "completed",
                    "administrator_id": account.id,
                    "revision": state["revision"] + 1,
                },
            )
            self.tx.finish(store, "post_auth_bootstrap", None, key, issued.session.id)
            self.tx.observe(store, account.id, "AdminBootstrapped", account.id)
            self.tx.observe(store, account.id, "SessionCreated", issued.session.id)
        return account, issued, recovery

    @audit_denial("post_auth_session")
    def login(self, username: str, password: str, key: str, request: Provenance) -> IssuedSession:
        self.tx.web.validate(request)
        if self.throttle is not None:
            return self._throttled_login(username, password, key)
        with self.tx.access.uow() as store:
            self.tx.eligible(store, "post_auth_session", None)
            account = self._authenticate(store, username, password)
            return self._login_session(store, account, key, username, password)

    def _authenticate(self, store: Store, username: str, password: str) -> UUID:
        row = store.get("accounts", {"username": username}, lock=True)
        if row and row["state"] == "locked":
            raise Denied("account_locked")
        valid = self._verify(password, row["password_hash"] if row else self._dummy_hash)
        if (
            not row
            or row["state"] != "active"
            or not valid
            or "session:create" not in self.tx.access.policy.authentication_actions
        ):
            raise Denied("invalid_credentials")
        return row["id"]

    def _throttled_login(self, username: str, password: str, key: str) -> IssuedSession:
        assert self.throttle is not None
        issued, failure = None, None
        with self.tx.access.uow() as store:
            before, current, now = self.throttle.begin(store, username)
            current["attempt_count"] += 1
            try:
                if current["state"] != "open":
                    raise Denied("rate_limited")
                account = self._authenticate(store, username, password)
                with store.savepoint():
                    issued = self._login_session(store, account, key, username, password)
                    if not issued.secret:
                        raise Denied("invalid_credentials")
            except Denied as error:
                failure = error
            self.throttle.finish(store, before, current, now, failure=failure)
        if failure:
            raise Denied(failure.code, observed=True) from failure
        assert issued is not None
        return issued

    def _verify(self, password: str, encoded: str) -> bool:
        try:
            return self.tx.passwords.verify(password, encoded)
        except Denied as exc:
            if exc.code == "password_policy_failed":
                return False
            raise

    def _login_session(
        self, store: Store, account: UUID, key: str, username: str, password: str
    ) -> IssuedSession:
        replay = self.tx.request(
            store, "post_auth_session", account, key, {"username": username, "password": password}
        )
        if replay:
            row = store.get("sessions", {"id": replay["outcome_id"]})
            if not row or row["state"] != "active":
                raise Denied("invalid_credentials")
            session = Session(**row)
            if self.tx.access.expired(session, store.now()):
                raise Denied("invalid_credentials")
            return IssuedSession(session, "", "")
        issued = self.tx.session(store, account)
        self.tx.finish(store, "post_auth_session", account, key, issued.session.id)
        self.tx.observe(store, account, "SessionCreated", issued.session.id)
        return issued


def _bootstrap_payload(username: str, password: str, display_name: str | None) -> dict[str, str]:
    payload = {"username": username, "password": password}
    if display_name is not None:
        payload["displayName"] = display_name
    return payload
