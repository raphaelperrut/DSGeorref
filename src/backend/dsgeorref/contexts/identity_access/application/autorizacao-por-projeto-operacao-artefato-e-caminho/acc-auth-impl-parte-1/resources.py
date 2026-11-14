"""Own-account decision queries; execution services always recheck their guards."""

from collections.abc import Callable, Mapping
from uuid import UUID

from dsgeorref.contexts.identity_access.application.local_identity.observations import audit_denial
from dsgeorref.contexts.identity_access.application.local_identity.ports import Store
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied, Principal


class ResourceAuthorization:
    """Compose current BC-002 grants with resource identity, without caching an allow.

    project_exists is a trusted server port, evaluated inside the identity UoW.
    It must read authoritative project state, never claims supplied by a request.
    Artifact grants are absent in policy 1.1.0, so no manifest or path I/O is needed.
    """

    def __init__(
        self,
        tx: IdentityTransactions,
        project_exists: Callable[[Store, UUID], bool],
        action_resources: Mapping[str, str | None],
        artifact_action: str,
        policy_version: str,
    ) -> None:
        if not callable(project_exists):
            raise Denied("internal_error")
        self.tx, self.project_exists = tx, project_exists
        self.action_resources = dict(action_resources)
        self.artifact_action, self.policy_version = artifact_action, policy_version

    @audit_denial("get_authorization_check")
    def check(
        self, secret: str, kind: str, action: str, resource_type: str, resource_id: UUID
    ) -> dict[str, bool | str]:
        with self.tx.access.uow() as store:
            principal = self.tx.access.load(store, secret, kind)
            self.tx.access.enforce(store, principal, "authorization:check")
            if self.tx.access.policy.version != self.policy_version:
                raise Denied("internal_error")
            if not isinstance(action, str):
                raise Denied("validation_failed")
            if action not in self.action_resources and action != self.artifact_action:
                raise Denied("validation_failed")
            self.tx.eligible(store, "get_authorization_check", principal.account.id)
            allowed = self._allowed(store, principal, action, resource_type, resource_id)
            store.audit(
                principal.account.id,
                "get_authorization_check",
                resource_id if isinstance(resource_id, UUID) else None,
                "COMMITTED" if allowed else "DENIED",
                self.policy_version,
                uuid7(),
                reason=None if allowed else "access_denied",
            )
        return {
            "allowed": allowed,
            "policyVersion": self.policy_version,
            "reasonCode": "granted" if allowed else "access_denied",
        }

    def _allowed(
        self, store: Store, principal: Principal, action: str, kind: str, target: UUID
    ) -> bool:
        if not isinstance(target, UUID) or action == self.artifact_action:
            return False
        if not isinstance(kind, str) or kind != self.action_resources[action]:
            return False
        project = target if kind == "project" else None
        if kind == "account" and target != principal.account.id:
            return False
        try:
            self.tx.access.enforce(store, principal, action, project)
        except Denied as error:
            if error.code != "forbidden":
                raise
            return False
        if project is not None:
            exists = self.project_exists(store, project)
            if type(exists) is not bool:
                raise Denied("internal_error")
            return exists
        return True
