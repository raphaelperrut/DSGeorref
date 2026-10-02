"""Private BC-002 persistence and cryptographic ports."""

from collections.abc import Callable
from contextlib import AbstractContextManager
from datetime import datetime
from typing import Protocol
from uuid import UUID

from dsgeorref.contexts.identity_access.domain.local_identity.models import Record


class Store(Protocol):
    def savepoint(self) -> AbstractContextManager[None]: ...
    def get(self, table: str, key: Record, *, lock: bool = False) -> Record | None: ...
    def insert(self, table: str, record: Record) -> None: ...
    def update(self, table: str, key: Record, changes: Record) -> None: ...
    def rows(self, table: str, key: Record) -> list[Record]: ...
    def now(self) -> datetime: ...
    def audit(
        self,
        actor: UUID | None,
        action: str,
        target: UUID | None,
        outcome: str,
        policy: str,
        correlation: UUID,
        reason: str | None = None,
    ) -> None: ...


class Passwords(Protocol):
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, encoded: str) -> bool: ...


UnitOfWork = Callable[[], AbstractContextManager[Store]]
