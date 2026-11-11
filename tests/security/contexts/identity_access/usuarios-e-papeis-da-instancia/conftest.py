"""Development HTTP and existing disposable PostgreSQL fixtures for BC-002."""

import json
import socket
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict
from http.client import HTTPConnection
from importlib import import_module
from pathlib import Path
from threading import Thread
from typing import Any, NamedTuple
from uuid import UUID, uuid4

import pytest
from dsgeorref.contexts.identity_access.adapters.local_identity.asgi import (
    _INSTANCE_RUNTIME,
    create_development_app,
)
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest, opaque
from dsgeorref.contexts.identity_access.domain.local_identity.web import WebPolicy
from fastapi import FastAPI
from psycopg import connect, sql
from tests.backend.identity_access.local_identity import conftest as identity
from uvicorn import Config, Server

database = identity.database
installation = identity.installation
ORIGIN = "https://localhost"
PASSWORD = identity.PASSWORD
LIMIT = 3
ROOT = Path(__file__).resolve().parents[5]
POLICY = ROOT / "contracts/contexts/identity_access/plt/usuarios-e-papeis-da-instancia/policy.json"


class Reply(NamedTuple):
    status: int
    headers: dict[str, str]
    body: Any


class Http:
    origin = ORIGIN

    def __init__(self, port: int) -> None:
        self.port = port

    def request(
        self,
        method: str,
        path: str,
        headers: dict[str, str] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Reply:
        request_headers = {
            "Origin": ORIGIN,
            "Sec-Fetch-Site": "same-origin",
            "Idempotency-Key": str(uuid4()),
            "Content-Type": "application/json",
            **(headers or {}),
        }
        connection = HTTPConnection("127.0.0.1", self.port, timeout=10)
        try:
            connection.request(
                method,
                "/api/v1" + path,
                json.dumps(body) if body is not None else None,
                request_headers,
            )
            response = connection.getresponse()
            raw = response.read()
            return Reply(
                response.status,
                {key.lower(): value for key, value in response.getheaders()},
                json.loads(raw) if raw else None,
            )
        finally:
            connection.close()


@contextmanager
def serve(app: FastAPI) -> Iterator[Http]:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        server = Server(Config(app, access_log=False, proxy_headers=False, log_level="warning"))
        thread = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        try:
            deadline = time.monotonic() + 10
            while not server.started and thread.is_alive() and time.monotonic() < deadline:
                time.sleep(0.01)
            assert server.started
            yield Http(listener.getsockname()[1])
        finally:
            server.should_exit = True
            thread.join(timeout=10)
            assert not thread.is_alive()


@pytest.fixture
def transactions(
    installation: IdentityTransactions,
    database: str,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> IdentityTransactions:
    profile = installation.access.profile
    configuration = asdict(profile)
    configuration.update(version="development-story-0044", approved=False)
    for key in ("session_absolute", "session_idle", "pat_lifetime", "oidc_lifetime"):
        configuration[key] = configuration[key].total_seconds()
    profiles = {
        "SECURITY_PROFILE": configuration,
        "THROTTLE_PROFILE": {
            "version": "development-story-0044",
            "limit_after": LIMIT,
            "lock_after": LIMIT + 1,
            "window_seconds": 120,
            "cooldown_seconds": 20,
            "lock_seconds": 40,
        },
    }
    replay_key = opaque().encode()
    for name, values in profiles.items():
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(values), encoding="utf-8")
        monkeypatch.setenv(f"DSGEOREF_IDENTITY_{name}", str(path))
    for name, value in {
        "DSN": database,
        "MODE": "development",
        "ORIGIN": ORIGIN,
        "POLICY": str(POLICY),
        "REPLAY_KEY_HEX": replay_key.hex(),
        "THROTTLE_KEY_HEX": opaque().encode().hex(),
    }.items():
        monkeypatch.setenv(f"DSGEOREF_IDENTITY_{name}", value)
    # The existing eligibility fixture is used only by service calls without a public
    # development route (project-bound PAT issue/revoke and OIDC initiation).
    runtime = import_module(_INSTANCE_RUNTIME)
    result: IdentityTransactions = runtime.build_transactions(
        database, profile, WebPolicy(ORIGIN), installation.eligibility, replay_key, POLICY
    )
    return result


@pytest.fixture
def committed_state(database: str):
    def read() -> dict[str, list[tuple[Any, ...]]]:
        # Failed OIDC may record a claim without issuing a session. Audit and throttle
        # may also advance on denial. All other requests and business rows must match.
        tables = (
            "accounts",
            "bootstrap",
            "sessions",
            "tokens",
            "memberships",
            "oidc_links",
            "ceremonies",
            "requests",
        )
        with connect(database) as connection:
            return {
                table: connection.execute(
                    sql.SQL("SELECT * FROM {} AS row {} ORDER BY to_jsonb(row)::text").format(
                        sql.Identifier("identity", table),
                        sql.SQL(
                            "WHERE operation <> 'get_auth_oidc_callback' OR outcome_id IS NOT NULL"
                            if table == "requests"
                            else ""
                        ),
                    )
                ).fetchall()
                for table in tables
            }

    return read


@pytest.fixture
def instance(transactions: IdentityTransactions):
    projects = uuid4(), uuid4()
    custody: dict[UUID, str] = {}

    def app(*, authority: bool = True, **options: Any):
        if authority:
            options.setdefault("project_exists", lambda _store, project: project in projects)
        return serve(
            create_development_app(
                installation_authorized=True, stage_recovery=custody.__setitem__, **options
            )
        )

    return app, projects, custody


@pytest.fixture
def enrolled(instance, transactions: IdentityTransactions):
    app, (first, second), custody = instance
    with app() as http:
        response = http.request(
            "POST",
            "/auth/bootstrap",
            body={
                "username": "administrator",
                "password": PASSWORD,
                "displayName": "Administrator",
            },
        )
    assert response.status == 202
    assert "set-cookie" not in response.headers
    assert set(response.body["data"]) == {"administratorId", "sessionId", "createdAt"}
    admin = UUID(response.body["data"]["administratorId"])
    assert list(custody) == [admin]
    viewer = uuid4()
    with transactions.access.uow() as store:
        account = store.get("accounts", {"id": admin})
        assert account is not None and account["recovery_hash"] == digest(custody[admin])
        # No public user provisioning or BC-003 project creation in this surface.
        store.insert(
            "accounts",
            {
                **account,
                "id": viewer,
                "username": "member",
                "administrator": False,
                "recovery_hash": digest(opaque()),
            },
        )
        for project, user, role in ((first, admin, "owner"), (second, viewer, "owner")):
            store.insert(
                "memberships",
                {
                    "project_id": project,
                    "account_id": user,
                    "role": role,
                    "revision": 1,
                },
            )
    return admin, viewer


@pytest.fixture
def login_limit() -> int:
    return LIMIT
