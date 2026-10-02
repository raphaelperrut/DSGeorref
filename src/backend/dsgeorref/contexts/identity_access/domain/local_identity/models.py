"""BC-002 internal aggregates; never exported across context boundaries."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID


class Denied(Exception):
    """Stable failure reason; transport mapping remains operation-specific."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class Account:
    id: UUID
    username: str
    password_hash: str = field(repr=False)
    recovery_hash: str = field(repr=False)
    state: str = "active"
    revision: int = 1
    administrator: bool = False


@dataclass(frozen=True)
class Session:
    id: UUID
    account_id: UUID
    secret_hash: str = field(repr=False)
    csrf_hash: str = field(repr=False)
    expires_at: datetime
    idle_expires_at: datetime
    state: str = "active"
    revision: int = 1
    oidc_link_id: UUID | None = None


@dataclass(frozen=True)
class PersonalAccessToken:
    id: UUID
    account_id: UUID
    secret_hash: str = field(repr=False)
    scopes: list[str]
    expires_at: datetime
    project_id: UUID | None
    state: str = "active"
    revision: int = 1


@dataclass(frozen=True)
class ProjectMembership:
    project_id: UUID
    account_id: UUID
    role: str
    revision: int = 1


@dataclass(frozen=True)
class IssuedSession:
    session: Session
    secret: str = field(repr=False)
    csrf: str = field(repr=False)


@dataclass(frozen=True)
class IssuedToken:
    token: PersonalAccessToken
    secret: str = field(repr=False)


@dataclass(frozen=True)
class Principal:
    account: Account
    credential: Session | PersonalAccessToken


Record = dict[str, Any]
