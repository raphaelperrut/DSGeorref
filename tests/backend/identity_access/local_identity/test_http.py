"""Production composition over HTTP and a disposable PostgreSQL database."""

import json
import socket
import subprocess
import threading
import time
from dataclasses import asdict
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener

import pytest
from conftest import ORIGIN
from dsgeorref.contexts.identity_access.adapters.local_identity.asgi import create_production_app
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest, opaque
from uvicorn import Config, Server

ROOT = Path(__file__).resolve().parents[4]
POLICY = ROOT / "contracts/contexts/identity_access/plt/usuarios-e-papeis-da-instancia/policy.json"
PATH = "/api/v1/auth/session"
KEY = "logout-idempotency-001"


@pytest.fixture
def production_app(monkeypatch, runtime, tmp_path):
    profile = asdict(runtime.access.profile)
    for field in ("session_absolute", "session_idle", "pat_lifetime", "oidc_lifetime"):
        profile[field] = profile[field].total_seconds()
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(json.dumps(profile), encoding="utf-8")
    for name, value in {
        "DSN": runtime.dsn,
        "SECURITY_PROFILE": str(profile_path),
        "ORIGIN": ORIGIN,
        "REPLAY_KEY_HEX": opaque().encode().hex(),
        "POLICY": str(POLICY),
    }.items():
        monkeypatch.setenv(f"DSGEOREF_IDENTITY_{name}", value)
    return create_production_app()


@pytest.fixture
def server(production_app):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        port = listener.getsockname()[1]
        service = Server(Config(production_app, access_log=False, log_level="warning"))
        thread = threading.Thread(target=service.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        try:
            deadline = time.monotonic() + 10
            while not service.started and thread.is_alive() and time.monotonic() < deadline:
                time.sleep(0.01)
            assert service.started
            yield f"http://127.0.0.1:{port}"
        finally:
            service.should_exit = True
            thread.join(timeout=10)
            assert not thread.is_alive()


@pytest.fixture
def headers(runtime):
    return {
        "Cookie": f"dsgeorref_session={runtime.issued.secret}",
        "Origin": ORIGIN,
        "Sec-Fetch-Site": "same-origin",
        "X-CSRF-Token": runtime.issued.csrf,
        "If-Match": f'"{runtime.issued.session.revision}"',
        "Idempotency-Key": KEY,
    }


def send(server, headers, path=PATH, method="DELETE"):
    opener = build_opener(ProxyHandler({}))
    try:
        return opener.open(Request(server + path, headers=headers, method=method), timeout=10)
    except HTTPError as error:
        return error


def assert_problem(response, status, code):
    with response:
        assert response.status == status
        assert response.headers["Content-Type"] == "application/problem+json"
        assert response.headers["Cache-Control"] == "no-store"
        assert "Set-Cookie" not in response.headers
        assert json.load(response) == {
            "type": f"https://dsgeorref.local/problems/{code}",
            "title": code.replace("_", " "),
            "status": status,
            "code": code,
        }


def test_logout_revokes_once_and_clears_cookie(server, headers, runtime):
    with send(server, headers) as response:
        assert response.status == 204
        assert response.read() == b""
        assert response.headers["Cache-Control"] == "no-store"
        assert response.headers["Set-Cookie"] == (
            "dsgeorref_session=; Path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=0"
        )
    assert_problem(send(server, headers), 401, "unauthorized")
    with runtime.uow() as store:
        session = store.get("sessions", {"id": runtime.issued.session.id})
        assert session["state"] == "revoked" and session["revision"] == 2
        assert len(store.rows("requests", {"operation": "delete_auth_session"})) == 1
        assert len(store.rows("observations", {"action": "SessionRevoked"})) == 1


@pytest.mark.parametrize(("header", "value"), [
    ("X-CSRF-Token", None),
    ("X-CSRF-Token", "invalid"),
    ("Origin", "https://attacker.example"),
    ("Sec-Fetch-Site", "cross-site"),
    ("Cookie", "dsgeorref_session=invalid"),
    ("Cookie", "dsgeorref_session=x; dsgeorref_session=y"),
    ("Authorization", "Bearer pat_ambiguous"),
])
def test_rejects_unauthorized_logout_without_mutation(server, headers, runtime, header, value):
    if value is None:
        del headers[header]
    else:
        headers[header] = value
    assert_problem(send(server, headers), 401, "unauthorized")
    with runtime.uow() as store:
        assert store.get("sessions", {"id": runtime.issued.session.id})["state"] == "active"
        assert not store.rows("requests", {"operation": "delete_auth_session"})


@pytest.mark.parametrize(("header", "value"), [
    ("If-Match", None),
    ("If-Match", 'W/"1"'),
    ("If-Match", '"2"'),
    ("Idempotency-Key", "short"),
])
def test_preconditions_use_published_problem(server, headers, runtime, header, value):
    if value is None:
        del headers[header]
    else:
        headers[header] = value
    assert_problem(send(server, headers), 500, "internal_error")
    with runtime.uow() as store:
        assert store.get("sessions", {"id": runtime.issued.session.id})["revision"] == 1
        assert not store.rows("requests", {"operation": "delete_auth_session"})


def test_expired_session_cannot_logout(server, headers, runtime):
    with runtime.uow() as store:
        store.update(
            "sessions", {"id": runtime.issued.session.id}, {"idle_expires_at": store.now()}
        )
    assert_problem(send(server, headers), 401, "unauthorized")


@pytest.mark.parametrize(("scope", "status", "code"), [
    ("authorization:check", 401, "unauthorized"),
    ("session:revoke", 404, "session_not_found"),
])
def test_pat_cannot_infer_target_session(server, headers, runtime, scope, status, code):
    issued = runtime.tokens.issue(
        runtime.issued.secret, "session", [scope], "fixture-token-key", runtime.browser()
    )
    del headers["Cookie"]
    headers["Authorization"] = f"Bearer {issued.secret}"
    assert_problem(send(server, headers), status, code)
    with runtime.uow() as store:
        assert store.get("sessions", {"id": runtime.issued.session.id})["state"] == "active"


def test_idempotency_conflict_keeps_session_active(server, headers, runtime):
    with runtime.uow() as store:
        store.insert("requests", {
            "operation": "delete_auth_session",
            "principal_id": runtime.account.id,
            "key_hash": digest(KEY),
            "payload_hash": digest("different prior payload"),
            "outcome_id": runtime.issued.session.id,
        })
    assert_problem(send(server, headers), 500, "internal_error")
    with runtime.uow() as store:
        assert store.get("sessions", {"id": runtime.issued.session.id})["state"] == "active"


def test_sdk_logout(server, headers):
    subprocess.run(
        ["node", str(Path(__file__).with_name("logout_sdk.mjs"))],
        cwd=ROOT,
        input=json.dumps({"baseUrl": f"{server}/api/v1", "headers": headers}),
        text=True,
        check=True,
        timeout=20,
    )


def test_only_supported_contract_operation_is_registered(production_app):
    assert [(route.path, route.methods) for route in production_app.routes] == [(PATH, {"DELETE"})]


def test_startup_requires_configuration(monkeypatch):
    monkeypatch.delenv("DSGEOREF_IDENTITY_DSN", raising=False)
    with pytest.raises(RuntimeError, match="Invalid or missing BC-002 runtime configuration"):
        create_production_app()
