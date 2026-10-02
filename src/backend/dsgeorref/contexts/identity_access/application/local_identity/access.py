"""Authenticate on each use and centrally enforce current grants."""

from datetime import datetime
from uuid import UUID

from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest, uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Account,
    Denied,
    PersonalAccessToken,
    Principal,
    ProjectMembership,
    Session,
)
from dsgeorref.contexts.identity_access.domain.local_identity.policy import (
    PUBLIC_ACTIONS,
    AuthorizationPolicy,
    SecurityProfile,
)

from .ports import Store, UnitOfWork


class Access:
    def __init__(
        self, uow: UnitOfWork, policy: AuthorizationPolicy, profile: SecurityProfile
    ) -> None:
        policy.validate()
        profile.validate()
        self.uow, self.policy, self.profile = uow, policy, profile

    def load(self, store: Store, secret: str, kind: str) -> Principal:
        self.policy.validate()
        self.profile.validate()
        if kind not in {"session", "pat"} or not secret:
            raise Denied("unauthorized")
        table = "sessions" if kind == "session" else "tokens"
        row = store.get(table, {"secret_hash": digest(secret)}, lock=True)
        if row is None:
            raise Denied("unauthorized")
        credential = Session(**row) if kind == "session" else PersonalAccessToken(**row)
        account_row = store.get("accounts", {"id": credential.account_id}, lock=True)
        if account_row is None or account_row["state"] != "active":
            raise Denied("unauthorized")
        if credential.state != "active" or self.expired(credential, store.now()):
            raise Denied("unauthorized")
        principal = Principal(Account(**account_row), credential)
        self._source_valid(store, principal)
        return principal

    def _source_valid(self, store: Store, principal: Principal) -> None:
        credential = principal.credential
        if isinstance(credential, Session) and credential.oidc_link_id is not None:
            link = store.get("oidc_links", {"id": credential.oidc_link_id})
            if link is None or link["state"] != "linked":
                raise Denied("unauthorized")
        if isinstance(credential, PersonalAccessToken):
            for action in credential.scopes:
                self.enforce(store, principal, action, credential.project_id)

    def expired(self, credential: Session | PersonalAccessToken, now: datetime) -> bool:
        if credential.expires_at <= now:
            return True
        return isinstance(credential, Session) and credential.idle_expires_at <= now

    def enforce(
        self, store: Store, principal: Principal, action: str, project: UUID | None = None
    ) -> None:
        if action not in PUBLIC_ACTIONS:
            raise Denied("validation_failed")
        member = (
            store.get(
                "memberships",
                {"project_id": project, "account_id": principal.account.id},
                lock=True,
            )
            if project
            else None
        )
        membership = ProjectMembership(**member) if member else None
        if not self.policy.allows(principal, action, project, membership):
            raise Denied("forbidden")

    def authenticate(self, *, session: str | None = None, pat: str | None = None) -> Principal:
        if bool(session) == bool(pat):
            raise Denied("unauthorized")
        failure = None
        result = None
        with self.uow() as store:
            try:
                result = self.load(store, session or pat or "", "session" if session else "pat")
                if isinstance(result.credential, Session):
                    deadline = min(
                        result.credential.expires_at, store.now() + self.profile.session_idle
                    )
                    store.update(
                        "sessions", {"id": result.credential.id}, {"idle_expires_at": deadline}
                    )
            except Denied as exc:
                failure = exc
                store.audit(None, "authenticate", None, "DENIED", self.policy.version, uuid7())
                self._expire(store, session or pat or "", "sessions" if session else "tokens")
        if failure:
            raise failure
        assert result is not None
        return result

    def _expire(self, store: Store, secret: str, table: str) -> None:
        row = store.get(table, {"secret_hash": digest(secret)}, lock=True)
        if row is None or row["state"] != "active":
            return
        due = row["expires_at"] <= store.now()
        if table == "sessions":
            due = due or row["idle_expires_at"] <= store.now()
        if due:
            store.update(
                table, {"id": row["id"]}, {"state": "expired", "revision": row["revision"] + 1}
            )

    def check(self, secret: str, kind: str, action: str, project: UUID | None) -> bool:
        with self.uow() as store:
            principal = self.load(store, secret, kind)
            self.enforce(store, principal, "authorization:check")
            try:
                self.enforce(store, principal, action, project)
                return True
            except Denied as exc:
                if exc.code != "forbidden":
                    raise
                return False
