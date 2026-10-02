"""Private BC-002 store. SQL identifiers are closed; values are bound parameters."""

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from typing import cast
from uuid import UUID

import psycopg
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied, Record
from psycopg import sql
from psycopg.rows import dict_row

TABLES = {
    "accounts": "id username password_hash recovery_hash state revision administrator",
    "sessions": (
        "id account_id secret_hash csrf_hash expires_at idle_expires_at state revision oidc_link_id"
    ),
    "tokens": "id account_id secret_hash scopes expires_at project_id state revision",
    "memberships": "project_id account_id role revision",
    "bootstrap": "singleton state administrator_id revision",
    "requests": "key_hash operation principal_id payload_hash outcome_id",
    "oidc_links": "id account_id issuer subject state revision",
    "oidc_transactions": (
        "id state_hash nonce_hash browser_hash account_id session_id expires_at state"
    ),
    "ceremonies": "id account_id kit_hash",
    "observations": (
        "id actor_id action target_id outcome policy_version correlation_id observed_at reason_code"
    ),
}


class PostgresStore:
    def __init__(self, connection: psycopg.Connection[Record]) -> None:
        self.connection = connection

    @contextmanager
    def savepoint(self) -> Iterator[None]:
        try:
            with self.connection.transaction():
                yield
        except psycopg.errors.UniqueViolation as exc:
            raise Denied("conflict") from exc
        except psycopg.Error as exc:
            raise Denied("internal_error") from exc

    def _columns(self, table: str, fields: Record) -> None:
        if table not in TABLES or not set(fields) <= set(TABLES[table].split()):
            raise Denied("internal_error")

    def _where(self, table: str, key: Record) -> sql.Composed:
        self._columns(table, key)
        if not key:
            raise Denied("internal_error")
        return sql.SQL(" AND ").join(
            sql.SQL("{} IS NOT DISTINCT FROM %s").format(sql.Identifier(k)) for k in key
        )

    def get(self, table: str, key: Record, *, lock: bool = False) -> Record | None:
        query = sql.SQL("SELECT * FROM identity.{} WHERE {}{}").format(
            sql.Identifier(table), self._where(table, key), sql.SQL(" FOR UPDATE" if lock else "")
        )
        return self.connection.execute(query, list(key.values())).fetchone()

    def rows(self, table: str, key: Record) -> list[Record]:
        query = sql.SQL("SELECT * FROM identity.{} WHERE {}").format(
            sql.Identifier(table), self._where(table, key)
        )
        return list(self.connection.execute(query, list(key.values())).fetchall())

    def insert(self, table: str, record: Record) -> None:
        self._columns(table, record)
        query = sql.SQL("INSERT INTO identity.{} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(",").join(map(sql.Identifier, record)),
            sql.SQL(",").join(sql.Placeholder() for _ in record),
        )
        self.connection.execute(query, list(record.values()))

    def update(self, table: str, key: Record, changes: Record) -> None:
        self._columns(table, changes)
        assignments = sql.SQL(",").join(sql.SQL("{}=%s").format(sql.Identifier(k)) for k in changes)
        query = sql.SQL("UPDATE identity.{} SET {} WHERE {}").format(
            sql.Identifier(table), assignments, self._where(table, key)
        )
        cursor = self.connection.execute(query, [*changes.values(), *key.values()])
        if cursor.rowcount != 1:
            raise Denied("precondition_failed")

    def now(self) -> datetime:
        row = self.connection.execute("SELECT clock_timestamp() AS now").fetchone()
        assert row is not None
        return cast(datetime, row["now"])

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
                "id": uuid7(),
                "actor_id": actor,
                "action": action,
                "target_id": target,
                "outcome": outcome,
                "policy_version": policy,
                "correlation_id": correlation,
                "observed_at": self.now(),
                "reason_code": reason,
            },
        )


class PostgresUnitOfWork:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    @contextmanager
    def __call__(self) -> Iterator[PostgresStore]:
        try:
            with (
                psycopg.connect(self.dsn, row_factory=dict_row, connect_timeout=5) as conn,
                conn.transaction(),
            ):
                conn.execute("SET LOCAL lock_timeout = '5s'")
                conn.execute("SET LOCAL statement_timeout = '10s'")
                yield PostgresStore(conn)
        except psycopg.errors.UniqueViolation as exc:
            raise Denied("conflict") from exc
        except psycopg.Error as exc:
            raise Denied("internal_error") from exc
