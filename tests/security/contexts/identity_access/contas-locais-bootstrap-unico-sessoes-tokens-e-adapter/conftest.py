"""Real identity services; only persistence and upstream eligibility are test ports.

This fixture is not PostgreSQL evidence: no SQL constraints, locks or concurrency
are simulated. Copy-on-write isolates application effects and failure assertions.
Numeric values below are synthetic test inputs, not production calibration.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from dsgeorref.contexts.identity_access.adapters.local_identity.crypto import ArgonPasswords
from dsgeorref.contexts.identity_access.application.local_identity.access import Access
from dsgeorref.contexts.identity_access.application.local_identity.accounts import LocalAccounts
from dsgeorref.contexts.identity_access.application.local_identity.sessions import Sessions
from dsgeorref.contexts.identity_access.application.local_identity.tokens import Tokens
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import opaque
from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Denied,
    IssuedSession,
    Record,
)
from dsgeorref.contexts.identity_access.domain.local_identity.policy import (
    PUBLIC_ACTIONS,
    AuthorizationPolicy,
    SecurityProfile,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance, WebPolicy

PASSWORD = "synthetic-security-test-password"
ORIGIN = "https://identity.example.test"


class TransactionalRecords:
    """Test-only implementation of the existing private Store/UnitOfWork ports."""

    def __init__(self) -> None:
        self.data: dict[str, list[Record]] = {
            "bootstrap": [
                {"singleton": True, "state": "available", "administrator_id": None, "revision": 1}
            ]
        }
        self.clock = datetime.now(UTC)
        self.fail_commit = False

    @contextmanager
    def savepoint(self) -> Iterator[None]:
        before = deepcopy(self.data)
        try:
            yield
        except BaseException:
            self.data = before
            raise

    @contextmanager
    def __call__(self) -> Iterator["TransactionalRecords"]:
        with self.savepoint():
            yield self
            if self.fail_commit:
                self.fail_commit = False
                raise Denied("internal_error")

    def rows(self, table: str, key: Record) -> list[Record]:
        return deepcopy(
            [r for r in self.data.get(table, []) if all(r.get(k) == v for k, v in key.items())]
        )

    def get(self, table: str, key: Record, *, lock: bool = False) -> Record | None:
        rows = self.rows(table, key)
        assert len(rows) <= 1, "ambiguous fixture key"
        return rows[0] if rows else None

    def insert(self, table: str, record: Record) -> None:
        self.data.setdefault(table, []).append(deepcopy(record))

    def update(self, table: str, key: Record, changes: Record) -> None:
        rows = [r for r in self.data.get(table, []) if all(r.get(k) == v for k, v in key.items())]
        if len(rows) != 1:
            raise Denied("precondition_failed")
        rows[0].update(deepcopy(changes))

    def now(self) -> datetime:
        return self.clock

    def audit(
        self,
        actor: UUID | None,
        action: str,
        target: UUID | None,
        outcome: str,
        policy: str,
        correlation: UUID,
        reason: str | None = None,
    ) -> None:
        self.insert(
            "observations",
            {
                "actor_id": actor,
                "action": action,
                "target_id": target,
                "outcome": outcome,
                "policy_version": policy,
                "correlation_id": correlation,
                "reason_code": reason,
            },
        )


@dataclass
class Runtime:
    uow: TransactionalRecords
    access: Access
    tx: IdentityTransactions
    accounts: LocalAccounts
    sessions: Sessions
    tokens: Tokens

    def browser(self, session: IssuedSession | None = None) -> Provenance:
        return Provenance(ORIGIN, "same-origin", session.csrf if session else None)

    def bootstrap(self) -> tuple[IssuedSession, str]:
        account, session, kit = self.accounts.bootstrap(
            "security-admin", PASSWORD, "bootstrap", self.browser()
        )
        self.access.policy.account_grants[account.id] = PUBLIC_ACTIONS
        return session, kit


@pytest.fixture
def runtime() -> Runtime:
    profile = SecurityProfile(
        "synthetic-security-only",
        "BP-003",
        True,
        1024,
        1,
        1,
        1,
        12,
        256,
        timedelta(minutes=30),
        timedelta(minutes=10),
        timedelta(hours=1),
        timedelta(minutes=2),
        2.0,
    )
    policy = AuthorizationPolicy(
        "synthetic-security-only",
        {},
        {"owner": PUBLIC_ACTIONS},
        frozenset({"instance:bootstrap"}),
        frozenset({"session:create", "oidc:callback"}),
    )
    uow = TransactionalRecords()
    access = Access(uow, policy, profile)
    tx = IdentityTransactions(
        access,
        ArgonPasswords(profile),
        WebPolicy(ORIGIN),
        lambda store, operation, actor: True,
        opaque().encode(),
    )
    return Runtime(uow, access, tx, LocalAccounts(tx), Sessions(tx), Tokens(tx))
