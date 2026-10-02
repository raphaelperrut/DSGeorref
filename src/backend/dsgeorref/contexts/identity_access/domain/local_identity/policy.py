"""Explicit versioned policy and bounded calibration; no production defaults."""

from dataclasses import dataclass
from datetime import timedelta
from math import isfinite
from uuid import UUID

from .models import Denied, PersonalAccessToken, Principal, ProjectMembership

ROLES = frozenset({"owner", "editor", "reviewer", "viewer"})
PUBLIC_ACTIONS = frozenset(
    {
        "instance:bootstrap",
        "session:create",
        "session:revoke",
        "token:create",
        "oidc:callback",
        "project_member:list",
        "project_member:create",
        "authorization:check",
    }
)


@dataclass(frozen=True)
class SecurityProfile:
    version: str
    benchmark: str
    approved: bool
    memory_kib: int
    iterations: int
    lanes: int
    hash_concurrency: int
    min_password_length: int
    max_password_bytes: int
    session_absolute: timedelta
    session_idle: timedelta
    pat_lifetime: timedelta
    oidc_lifetime: timedelta
    io_timeout: float

    def validate(self) -> None:
        numbers = (
            self.memory_kib,
            self.iterations,
            self.lanes,
            self.hash_concurrency,
            self.min_password_length,
            self.max_password_bytes,
        )
        times = (self.session_absolute, self.session_idle, self.pat_lifetime, self.oidc_lifetime)
        if self.approved is not True or self.benchmark != "BP-003" or not self.version:
            raise Denied("internal_error")
        if any(type(n) is not int or n <= 0 for n in numbers):
            raise Denied("internal_error")
        if self.memory_kib < 8 * self.lanes or self.max_password_bytes < self.min_password_length:
            raise Denied("internal_error")
        valid_times = all(t > timedelta(0) for t in times)
        if not all((valid_times, isfinite(self.io_timeout), self.io_timeout > 0)):
            raise Denied("internal_error")
        if self.session_idle > self.session_absolute:
            raise Denied("internal_error")

    def password_eligible(self, password: str) -> None:
        if not isinstance(password, str):
            raise Denied("password_policy_failed")
        if len(password) < self.min_password_length:
            raise Denied("password_policy_failed")
        if len(password.encode()) > self.max_password_bytes:
            raise Denied("password_policy_failed")


@dataclass(frozen=True)
class AuthorizationPolicy:
    version: str
    account_grants: dict[UUID, frozenset[str]]
    role_grants: dict[str, frozenset[str]]
    installation_actions: frozenset[str]
    authentication_actions: frozenset[str]

    def validate(self) -> None:
        if not self.version or not set(self.role_grants) <= ROLES:
            raise Denied("internal_error")
        grants = (
            *self.account_grants.values(),
            *self.role_grants.values(),
            self.installation_actions,
            self.authentication_actions,
        )
        if any(not g <= PUBLIC_ACTIONS for g in grants):
            raise Denied("internal_error")

    def allows(
        self,
        principal: Principal,
        action: str,
        project: UUID | None,
        membership: ProjectMembership | None,
    ) -> bool:
        if action not in PUBLIC_ACTIONS or principal.account.state != "active":
            return False
        if principal.credential.state != "active":
            return False
        grants = self.account_grants.get(principal.account.id, frozenset())
        if project is not None:
            if membership is None or membership.project_id != project:
                return False
            if membership.account_id != principal.account.id:
                return False
            grants = self.role_grants.get(membership.role, frozenset())
        token = principal.credential
        if isinstance(token, PersonalAccessToken) and (
            token.project_id != project or action not in token.scopes
        ):
            return False
        return action in grants
