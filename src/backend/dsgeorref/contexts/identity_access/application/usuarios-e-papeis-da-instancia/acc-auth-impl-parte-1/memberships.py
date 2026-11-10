"""Transactional membership operations under the frozen instance policy."""

from collections.abc import Callable
from dataclasses import asdict
from uuid import UUID

from dsgeorref.contexts.identity_access.application.local_identity.observations import audit_denial
from dsgeorref.contexts.identity_access.application.local_identity.ports import Store
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Denied,
    ProjectMembership,
)
from dsgeorref.contexts.identity_access.domain.local_identity.policy import ROLES
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance

ProjectExists = Callable[[Store, UUID], bool]


class Memberships:
    def __init__(self, transactions: IdentityTransactions, project_exists: ProjectExists) -> None:
        if not callable(project_exists):
            raise Denied("internal_error")
        self.tx, self.project_exists = transactions, project_exists

    def _project(self, store: Store, project: UUID) -> None:
        result = self.project_exists(store, project)
        if result is False:
            raise Denied("not_found")
        if result is not True:
            raise Denied("internal_error")

    @audit_denial("get_projects_projectid_members")
    def list(self, secret: str, kind: str, project: UUID) -> list[ProjectMembership]:
        if not isinstance(project, UUID):
            raise Denied("validation_failed")
        with self.tx.access.uow() as store:
            principal = self.tx.access.load(store, secret, kind)
            self.tx.access.enforce(store, principal, "project_member:list", project)
            self._project(store, project)
            self.tx.eligible(store, "get_projects_projectid_members", principal.account.id)
            return [
                ProjectMembership(**row)
                for row in store.rows("memberships", {"project_id": project})
            ]

    @audit_denial("post_projects_projectid_members")
    def add(
        self,
        secret: str,
        kind: str,
        project: UUID,
        account: UUID,
        role: str,
        key: str,
        request: Provenance | None,
    ) -> ProjectMembership:
        if not isinstance(project, UUID) or not isinstance(account, UUID) or not key:
            raise Denied("validation_failed")
        with self.tx.access.uow() as store:
            principal = self.tx.access.load(store, secret, kind)
            self.tx.access.enforce(store, principal, "project_member:create", project)
            self.tx.browser_guard(principal, request)
            self._project(store, project)
            if store.get("accounts", {"id": account}, lock=True) is None:
                raise Denied("not_found")
            if not isinstance(role, str) or role not in ROLES:
                raise Denied("validation_failed")
            self.tx.eligible(store, "post_projects_projectid_members", principal.account.id)
            replay = self.tx.request(
                store,
                "post_projects_projectid_members",
                principal.account.id,
                key,
                {"projectId": project, "userId": account, "role": role},
            )
            current = store.get("memberships", {"project_id": project, "account_id": account})
            if replay:
                if not current or current["role"] != role:
                    raise Denied("conflict")
                return ProjectMembership(**current)
            if current:
                raise Denied("conflict")
            member = ProjectMembership(project, account, role)
            store.insert("memberships", asdict(member))
            self.tx.finish(
                store, "post_projects_projectid_members", principal.account.id, key, account
            )
            self.tx.observe(store, principal.account.id, "MembershipChanged", account)
        return member
