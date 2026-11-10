"""Sprint 002 HTTP and SDK integration on disposable PostgreSQL."""

import json
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener
from uuid import UUID, uuid4

import psycopg
import pytest
from conftest import PASSWORD
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
from dsgeorref.contexts.identity_access.adapters.local_identity.asgi import (
    create_development_app,
    create_production_app,
)
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import ValidatingOidcProvider
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest
from oidc_fixture import SignedProvider, config
from test_http import POLICY, ROOT, assert_problem, running_server, send

ORIGIN = "https://localhost"
HEADERS = {
    "Origin": ORIGIN,
    "Sec-Fetch-Site": "same-origin",
    "Idempotency-Key": "fixture-login-key-01",
}
LIMIT = 4


@pytest.fixture
def development(monkeypatch, installation, database, tmp_path):
    profile = asdict(installation.access.profile)
    profile.update(version="development-tests", approved=False)
    for field in ("session_absolute", "session_idle", "pat_lifetime", "oidc_lifetime"):
        profile[field] = profile[field].total_seconds()
    profile_path = tmp_path / "security.json"
    profile_path.write_text(json.dumps(profile), encoding="utf-8")
    throttle_path = tmp_path / "throttle.json"
    throttle_path.write_text(
        json.dumps(
            {
                "version": "development-tests",
                "limit_after": LIMIT,
                "lock_after": LIMIT + 1,
                "window_seconds": 120,
                "cooldown_seconds": 20,
                "lock_seconds": 40,
            }
        ),
        encoding="utf-8",
    )
    for name, value in {
        "DSN": database,
        "ORIGIN": ORIGIN,
        "MODE": "development",
        "SECURITY_PROFILE": str(profile_path),
        "THROTTLE_PROFILE": str(throttle_path),
        "THROTTLE_KEY_HEX": "aa" * 32,
        "REPLAY_KEY_HEX": "bb" * 32,
        "POLICY": str(POLICY),
    }.items():
        monkeypatch.setenv(f"DSGEOREF_IDENTITY_{name}", value)
    return throttle_path


def _post(base_url, path, body, headers=HEADERS):
    request = Request(
        base_url + "/api/v1" + path,
        method="POST",
        data=json.dumps(body).encode(),
        headers={**headers, "Content-Type": "application/json"},
    )
    try:
        return build_opener(ProxyHandler({})).open(request, timeout=10)
    except HTTPError as error:
        return error


def test_epic_009_superficie(development, runtime):
    project, target = uuid4(), uuid4()
    runtime.member(project)
    with runtime.uow() as store:
        account = store.get("accounts", {"id": runtime.account.id})
        store.insert(
            "accounts",
            {
                **account,
                "id": target,
                "username": "candidate",
                "administrator": False,
            },
        )

    def app():
        # The host project port is the fixture's declared project authority.
        return create_development_app(project_exists=lambda _store, candidate: candidate == project)

    with running_server(app()) as base_url:
        subprocess.run(
            ["node", str(Path(__file__).with_name("logout_sdk.mjs"))],
            cwd=ROOT,
            input=json.dumps(
                {
                    "development": True,
                    "baseUrl": f"{base_url}/api/v1",
                    "headers": HEADERS,
                    "password": PASSWORD,
                    "projectId": str(project),
                    "targetId": str(target),
                }
            ),
            text=True,
            check=True,
            timeout=25,
        )
        assert_problem(
            _post(base_url, "/auth/session", {"username": "candidate"}), 422, "validation_failed"
        )
        _exercise_contention(base_url)

    with running_server(app()) as base_url:
        _assert_block_survives_restart(base_url, runtime)
        _assert_audit_failure_is_closed(base_url, runtime, target)


def _exercise_contention(base_url):
    body = {"username": "absent-user", "password": "wrong-synthetic-password"}

    def attempt(_):
        with _post(base_url, "/auth/session", body) as response:
            assert response.headers.get("Set-Cookie") is None
            return response.status, json.load(response)["code"]

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(attempt, range(8)))
    assert results.count((401, "invalid_credentials")) == LIMIT
    assert results.count((429, "rate_limited")) == 8 - LIMIT


def _assert_block_survives_restart(base_url, runtime):
    body = {"username": "absent-user", "password": "wrong-synthetic-password"}
    assert_problem(_post(base_url, "/auth/session", body), 429, "rate_limited")
    operation = "post_auth_session"
    with runtime.uow() as store:
        rows = store.rows("throttle_buckets", {"operation": operation})
        (limited,) = [row for row in rows if row["state"] == "limited"]
        assert limited["failure_count"] == LIMIT
        assert limited["attempt_count"] == 9
        decisions = store.rows("throttle_decisions", {"bucket_digest": limited["bucket_digest"]})
        assert len(decisions) == 9
        for decision in decisions:
            (observation,) = store.rows("observations", {"correlation_id": decision["id"]})
            assert observation["outcome"] == "DENIED"
        store.update(
            "throttle_buckets",
            {"operation": operation, "bucket_digest": limited["bucket_digest"]},
            {"blocked_until": store.now() - timedelta(seconds=1)},
        )
    assert_problem(_post(base_url, "/auth/session", body), 401, "invalid_credentials")
    with runtime.uow() as store:
        locked = store.get(
            "throttle_buckets",
            {
                "operation": operation,
                "bucket_digest": limited["bucket_digest"],
            },
        )
        assert locked["state"] == "locked" and locked["failure_count"] == LIMIT + 1
        assert locked["revision"] > limited["revision"]


def _assert_audit_failure_is_closed(base_url, runtime, target: UUID):
    with psycopg.connect(runtime.dsn) as connection:
        connection.execute(
            """ALTER TABLE identity.throttle_decisions ADD CONSTRAINT forced_audit_failure
               CHECK (false) NOT VALID"""
        )
    try:
        assert_problem(
            _post(base_url, "/auth/session", {"username": "candidate", "password": PASSWORD}),
            500,
            "internal_error",
        )
        with runtime.uow() as store:
            assert not store.rows("sessions", {"account_id": target})
            assert not store.rows(
                "requests", {"key_hash": digest(HEADERS["Idempotency-Key"]), "principal_id": target}
            )
    finally:
        with psycopg.connect(runtime.dsn) as connection:
            connection.execute(
                "ALTER TABLE identity.throttle_decisions DROP CONSTRAINT forced_audit_failure"
            )


def test_development_profile_cannot_enter_production(development, monkeypatch):
    with pytest.raises(RuntimeError, match="BC-002 runtime configuration"):
        create_production_app()
    with monkeypatch.context() as configuration:
        configuration.setenv(
            "DSGEOREF_IDENTITY_DSN",
            "dbname=fixture host=127.0.0.1 hostaddr=192.0.2.10",
        )
        with pytest.raises(RuntimeError, match="BC-002 development configuration"):
            create_development_app()
    development.write_text('{"version":"development-invalid"}', encoding="utf-8")
    with pytest.raises(RuntimeError, match="BC-002 development configuration"):
        create_development_app()


def test_bootstrap_requires_installation_capability(development, installation):
    body = {"username": "first-admin", "password": PASSWORD, "displayName": "Administrador"}
    with running_server(create_development_app(installation_authorized=True)) as base_url:
        assert_problem(_post(base_url, "/auth/bootstrap", body), 422, "validation_failed")

    def unavailable(_account, _kit):
        raise OSError("fixture custody failure")

    failing = create_development_app(installation_authorized=True, stage_recovery=unavailable)
    with running_server(failing) as base_url:
        assert_problem(_post(base_url, "/auth/bootstrap", body), 500, "internal_error")
    with installation.access.uow() as store:
        assert store.get("bootstrap", {"singleton": True})["state"] == "available"
        assert not store.get("accounts", {"username": body["username"]})

    staged = {}
    app = create_development_app(installation_authorized=True, stage_recovery=staged.__setitem__)
    with running_server(app) as base_url:
        with _post(base_url, "/auth/bootstrap", body) as response:
            assert response.status == 202
            assert response.headers.get("Set-Cookie") is None
            created = json.load(response)
        with _post(base_url, "/auth/bootstrap", body) as response:
            assert response.status == 202
            assert json.load(response) == created
        assert_problem(
            _post(base_url, "/auth/bootstrap", {**body, "displayName": "Outro"}),
            409,
            "bootstrap_already_completed",
        )
    account_id = UUID(created["data"]["administratorId"])
    with installation.access.uow() as store:
        assert list(staged) == [account_id]
        assert store.get("accounts", {"id": account_id})["recovery_hash"] == digest(
            staged[account_id]
        )


def test_oidc_callback_uses_browser_bound_transaction(development, runtime):
    transport = SignedProvider("pending")
    provider = ValidatingOidcProvider(config(), transport)
    federation = Federation(runtime.tx, provider)
    state, transport.nonce = federation.begin(
        "fixture-browser", runtime.browser(), runtime.issued.secret
    )
    path = f"/api/v1/auth/oidc/callback?code=fixture-code&state={state}"

    with running_server(create_development_app()) as base_url:
        assert_problem(send(base_url, {}, path, "GET"), 502, "oidc_exchange_failed")

    def browser_binding(request):
        return request.cookies.get("fixture_oidc_binding", "")

    with running_server(create_development_app(oidc=(provider, browser_binding))) as base_url:
        assert_problem(send(base_url, {}, path, "GET"), 400, "oidc_state_invalid")
        headers = {"Cookie": "fixture_oidc_binding=fixture-browser"}
        with send(base_url, headers, path, "GET") as response:
            assert response.status == 200
            assert "HttpOnly" in response.headers["Set-Cookie"]
            result = json.load(response)["data"]
            assert result["linked"] is True
            assert result["session"]["userId"] == str(runtime.account.id)
        assert_problem(send(base_url, headers, path, "GET"), 400, "oidc_state_invalid")


def test_react_identity_surface(development, runtime, monkeypatch, tmp_path):
    project = uuid4()
    runtime.member(project)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        origin = f"https://localhost:{listener.getsockname()[1]}"
    monkeypatch.setenv("DSGEOREF_IDENTITY_ORIGIN", origin)
    key, cert = _tls_files(tmp_path)
    app = create_development_app(project_exists=lambda _store, candidate: candidate == project)
    with running_server(app) as backend:
        subprocess.run(
            ["node", str(Path(__file__).with_name("identity_browser.mjs"))],
            cwd=ROOT,
            input=json.dumps(
                {
                    "backend": backend,
                    "origin": origin,
                    "key": str(key),
                    "cert": str(cert),
                    "password": PASSWORD,
                    "projectId": str(project),
                }
            ),
            text=True,
            check=True,
            timeout=55,
        )


def _tls_files(tmp_path):
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    now = datetime.now(UTC)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(minutes=10))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False)
        .sign(key, hashes.SHA256())
    )
    key_path, cert_path = tmp_path / "key.pem", tmp_path / "cert.pem"
    key_path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    cert_path.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    return key_path, cert_path
