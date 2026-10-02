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
from .transactions import IdentityTransactions


class LocalAccounts:
    def __init__(self, transactions: IdentityTransactions) -> None:
        self.tx = transactions
        length = self.tx.access.profile.min_password_length
        self._dummy_hash = self.tx.passwords.hash((opaque() * (length // 43 + 1))[:length])

    @audit_denial("post_auth_bootstrap")
    def bootstrap(
        self, username: str, password: str, key: str, request: Provenance
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
                {"username": username, "password": password},
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
        return account, issued, recovery

    @audit_denial("post_auth_session")
    def login(self, username: str, password: str, key: str, request: Provenance) -> IssuedSession:
        self.tx.web.validate(request)
        failure, issued = None, None
        with self.tx.access.uow() as store:
            self.tx.eligible(store, "post_auth_session", None)
            row = store.get("accounts", {"username": username}, lock=True)
            valid = self._verify(password, row["password_hash"] if row else self._dummy_hash)
            if row and row["state"] == "locked":
                failure = Denied("account_locked")
            elif (
                not row
                or row["state"] != "active"
                or not valid
                or "session:create" not in self.tx.access.policy.authentication_actions
            ):
                failure = Denied("invalid_credentials")
            if failure:
                store.audit(
                    None,
                    "post_auth_session",
                    None,
                    "DENIED",
                    self.tx.access.policy.version,
                    uuid7(),
                )
            else:
                assert row is not None
                issued = self._login_session(store, row["id"], key, username, password)
        if failure:
            raise failure
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
