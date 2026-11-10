"""Bind the published own-account grants to a freshly authenticated principal."""

from dataclasses import replace
from uuid import UUID

from dsgeorref.contexts.identity_access.application.local_identity.access import Access
from dsgeorref.contexts.identity_access.application.local_identity.ports import Store, UnitOfWork
from dsgeorref.contexts.identity_access.domain.local_identity.models import Principal
from dsgeorref.contexts.identity_access.domain.local_identity.policy import (
    AuthorizationPolicy,
    SecurityProfile,
)


class InstanceAccess(Access):
    """Reuse the domain policy and PostgreSQL membership checks without a grant cache."""

    def __init__(
        self,
        uow: UnitOfWork,
        policy: AuthorizationPolicy,
        profile: SecurityProfile,
        self_service: frozenset[str],
    ) -> None:
        super().__init__(uow, policy, profile)
        self.self_service = self_service

    def enforce(
        self, store: Store, principal: Principal, action: str, project: UUID | None = None
    ) -> None:
        # Each operation loads active account/credential and the current membership
        # inside its UoW. No caller-supplied role or administrator bypass is used.
        policy = replace(self.policy, account_grants={principal.account.id: self.self_service})
        Access(self.uow, policy, self.profile).enforce(store, principal, action, project)
