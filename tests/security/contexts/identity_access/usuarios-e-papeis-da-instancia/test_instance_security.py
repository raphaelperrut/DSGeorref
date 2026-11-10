"""AC-ISSUE-0154-01..04: BC-002 development HTTP, policy 1.1.0 and PostgreSQL."""

from collections.abc import Callable
from datetime import timedelta
from email.message import Message
from io import BytesIO
from time import sleep
from typing import Any
from urllib.request import HTTPSHandler, Request
from urllib.response import addinfourl
from uuid import UUID, uuid4

import pytest
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import (
    HttpsProviderTransport,
    ValidatingOidcProvider,
)
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.application.local_identity.tokens import Tokens
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest, opaque
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance
from psycopg import connect, sql
from tests.backend.identity_access.local_identity import conftest as identity
from tests.backend.identity_access.local_identity.oidc_fixture import SignedProvider, config

LOGIN = "/auth/session"
LIST = "project_member:list"
CREATE = "project_member:create"
PASSWORD = identity.PASSWORD
Snapshot = Callable[[], dict[str, list[tuple[Any, ...]]]]


def assert_problem(reply, status: int, code: str) -> None:
    assert reply.status == status
    assert reply.headers["content-type"] == "application/problem+json"
    assert reply.headers["cache-control"] == "no-store"
    assert "set-cookie" not in reply.headers
    assert reply.body == {
        "type": f"https://dsgeorref.local/problems/{code}",
        "title": code.replace("_", " "),
        "status": status,
        "code": code,
    }


def login(http, username: str) -> tuple[dict[str, str], UUID]:
    response = http.request("POST", LOGIN, body={"username": username, "password": PASSWORD})
    assert response.status == 202
    cookie = response.headers["set-cookie"]
    assert {"secure", "httponly", "samesite=strict"} <= {
        attribute.strip().lower() for attribute in cookie.split(";")[1:]
    }
    session = response.body["data"]
    return {
        "Origin": http.origin,
        "Cookie": cookie.split(";", 1)[0],
        "X-CSRF-Token": session["csrfToken"],
        "If-Match": response.headers["etag"],
    }, UUID(session["sessionId"])


def members(project: UUID) -> str:
    return f"/projects/{project}/members"


def decision(http, headers: dict[str, str], project: UUID, action: str, allowed: bool):
    path = f"/authorization/check?action={action}&resourceType=project&resourceId={project}"
    reply = http.request("GET", path, headers)
    assert reply.status == 200
    assert reply.body == {
        "data": {
            "allowed": allowed,
            "policyVersion": "1.1.0",
            "reasonCode": "allowed" if allowed else "forbidden",
        }
    }


def test_epic_009_seguranca_happy_path(instance, enrolled, transactions: IdentityTransactions):
    """REQ-ACC-001, REQ-AUTH-IMPL-001/003/004/006/010 and REQ-ID-002."""
    app, (first, second), _ = instance
    admin, viewer = enrolled
    with app() as http:
        headers, _ = login(http, "administrator")
        decision(http, headers, first, CREATE, True)
        decision(http, headers, second, LIST, False)
        body = {"userId": str(viewer), "role": "viewer"}
        key = {"Idempotency-Key": "story-0044-add-member-key"}
        result = http.request("POST", members(first), {**headers, **key}, body)
        assert result.status == 201
        assert result.body == {"data": {**body, "projectId": str(first), "revision": 1}}
        replay = http.request("POST", members(first), {**headers, **key}, body)
        assert replay.status == 201 and replay.body == result.body
        member_headers, _ = login(http, "member")
        decision(http, member_headers, first, LIST, True)
        decision(http, member_headers, first, CREATE, False)
        pat = Tokens(transactions).issue(
            headers["Cookie"].split("=", 1)[1],
            "session",
            [LIST],
            str(uuid4()),
            Provenance(headers["Origin"], "same-origin", headers["X-CSRF-Token"]),
            project=first,
        )
        result = http.request("GET", members(first), {"Authorization": f"Bearer {pat.secret}"})
        assert result.status == 200
        assert {item["userId"]: item["role"] for item in result.body["items"]} == {
            str(admin): "owner",
            str(viewer): "viewer",
        }
    with transactions.access.uow() as store:
        assert store.rows("memberships", {"project_id": second}) == [
            {"project_id": second, "account_id": viewer, "role": "owner", "revision": 1}
        ]
        stored = store.get("tokens", {"id": pat.token.id})
        assert stored is not None and stored["secret_hash"] == digest(pat.secret)
        assert stored["project_id"] == first and stored["scopes"] == [LIST]
        assert len(store.rows("observations", {"action": "MembershipChanged"})) == 1


@pytest.mark.parametrize(
    ("scenario", "status", "code"),
    [
        ("anonymous", 401, "unauthorized"),
        ("invalid-session", 401, "unauthorized"),
        ("invalid-pat", 401, "unauthorized"),
        ("ambiguous-credentials", 401, "unauthorized"),
        ("viewer-escalation", 403, "forbidden"),
        ("administrator-cross-project", 403, "forbidden"),
        ("unknown-role", 422, "validation_failed"),
        ("overwrite-existing-role", 409, "conflict"),
        ("cross-origin", 403, "forbidden"),
        ("invalid-csrf", 403, "forbidden"),
        ("no-project-authority", 500, "internal_error"),
        ("project-absent", 404, "not_found"),
    ],
)
def test_epic_009_seguranca_negative_paths(
    scenario: str,
    status: int,
    code: str,
    instance,
    enrolled,
    committed_state: Snapshot,
):
    """REQ-ACC-001 and REQ-AUTH-IMPL-001/003/006: failed mutations remain atomic."""
    app, (first, second), _ = instance
    admin, viewer = enrolled
    if scenario == "project-absent":
        application = app(project_exists=lambda _store, _project: False)
    else:
        application = app(authority=scenario != "no-project-authority")
    with application as http:
        headers, _ = login(http, "administrator")
        project, user, role = first, viewer, "owner"
        if scenario == "viewer-escalation":
            added = http.request(
                "POST",
                members(first),
                headers,
                {
                    "userId": str(viewer),
                    "role": "viewer",
                },
            )
            assert added.status == 201
            headers, _ = login(http, "member")
        elif scenario == "administrator-cross-project":
            project, user = second, admin
        elif scenario == "unknown-role":
            role = "administrator"
        elif scenario == "overwrite-existing-role":
            user, role = admin, "viewer"
        headers = {
            "anonymous": {},
            "invalid-session": {**headers, "Cookie": "dsgeorref_session=" + opaque()},
            "invalid-pat": {"Authorization": "Bearer pat_" + opaque()},
            "ambiguous-credentials": {**headers, "Authorization": "Bearer pat_" + opaque()},
            "cross-origin": {**headers, "Origin": "https://untrusted.example.test"},
            "invalid-csrf": {**headers, "X-CSRF-Token": opaque()},
        }.get(scenario, headers)
        before = committed_state()
        reply = http.request("POST", members(project), headers, {"userId": str(user), "role": role})
        assert_problem(reply, status, code)
        assert committed_state() == before


@pytest.mark.parametrize(
    ("credential", "fault", "status", "code"),
    [
        ("pat", "scope", 403, "forbidden"),
        ("pat", "project", 403, "forbidden"),
        ("pat", "role-changed", 403, "forbidden"),
        ("pat", "expired", 401, "unauthorized"),
        ("pat", "revoked", 401, "unauthorized"),
        ("session", "expired", 401, "unauthorized"),
        ("session", "revoked", 401, "unauthorized"),
    ],
)
def test_epic_009_seguranca_negative_paths_credentials(
    credential: str,
    fault: str,
    status: int,
    code: str,
    instance,
    enrolled,
    transactions: IdentityTransactions,
    committed_state: Snapshot,
):
    """REQ-AUTH-IMPL-001/004/006/008: valid identity alone confers no extra grant."""
    app, (first, second), _ = instance
    admin, viewer = enrolled
    with app() as http:
        username = "member" if fault == "project" else "administrator"
        headers, session_id = login(http, username)
        project, user = (second, admin) if fault == "project" else (first, viewer)
        if credential == "pat":
            if fault == "project":
                with transactions.access.uow() as store:
                    store.insert(
                        "memberships",
                        {
                            "project_id": first,
                            "account_id": viewer,
                            "role": "owner",
                            "revision": 1,
                        },
                    )
                decision(http, headers, second, CREATE, True)
            headers = restricted_pat(transactions, headers, first, admin, fault)
            if fault == "scope":
                assert http.request("GET", members(first), headers).status == 200
        elif fault == "revoked":
            assert http.request("DELETE", LOGIN, headers).status == 204
        else:
            with transactions.access.uow() as store:
                store.update(
                    "sessions",
                    {"id": session_id},
                    {
                        "idle_expires_at": store.now() - timedelta(seconds=1),
                    },
                )
        before = committed_state()
        assert_problem(
            http.request(
                "POST",
                members(project),
                headers,
                {
                    "userId": str(user),
                    "role": "viewer",
                },
            ),
            status,
            code,
        )
        assert committed_state() == before


def restricted_pat(
    tx: IdentityTransactions,
    headers: dict[str, str],
    project: UUID,
    admin: UUID,
    fault: str,
) -> dict[str, str]:
    session = headers["Cookie"].split("=", 1)[1]
    provenance = Provenance(headers["Origin"], "same-origin", headers["X-CSRF-Token"])
    tokens = Tokens(tx)
    expiry = None
    if fault == "expired":
        with tx.access.uow() as store:
            expiry = store.now() + timedelta(seconds=3)
    token = tokens.issue(
        session,
        "session",
        [LIST if fault == "scope" else CREATE],
        str(uuid4()),
        provenance,
        project=project,
        expires=expiry,
    )
    if fault == "revoked":
        tokens.revoke(session, "session", token.token.id, provenance)
    elif fault == "expired":
        assert expiry is not None
        with tx.access.uow() as store:
            remaining = (expiry - store.now()).total_seconds()
        sleep(max(0, remaining) + 0.05)
    elif fault == "role-changed":
        with tx.access.uow() as store:
            store.update(
                "memberships",
                {"project_id": project, "account_id": admin},
                {
                    "role": "viewer",
                    "revision": 2,
                },
            )
    return {"Authorization": f"Bearer {token.secret}"}


@pytest.mark.parametrize("scenario", ["replay", "nonce", "browser", "outage", "redirect"])
def test_epic_009_seguranca_negative_paths_oidc(
    scenario: str,
    instance,
    enrolled,
    transactions: IdentityTransactions,
    committed_state: Snapshot,
    monkeypatch: pytest.MonkeyPatch,
):
    """REQ-AUTH-IMPL-005 and ADR-029/032: validate signed claims and restrict egress."""
    app, (project, _), custody = instance
    admin, _ = enrolled
    code, binding = opaque(), opaque()
    signed = SignedProvider("uninitialized")
    provider = ValidatingOidcProvider(config(), signed)
    if scenario == "redirect":
        provider = ValidatingOidcProvider(config(), HttpsProviderTransport())
    destinations: list[str] = []

    def redirect(_handler: HTTPSHandler, request: Request) -> addinfourl:
        destinations.append(request.full_url)
        headers = Message()
        headers["Location"] = "https://unexpected.example.test/token"
        response = addinfourl(BytesIO(), headers, request.full_url, 303)
        response.msg = "See Other"
        return response

    def outage(_config, submitted_code: str) -> str:
        raise OSError(f"upstream failure for {submitted_code}")

    if scenario == "redirect":
        monkeypatch.setattr(HTTPSHandler, "https_open", redirect)
        monkeypatch.setenv("no_proxy", "*")
    elif scenario == "outage":
        monkeypatch.setattr(signed, "token", outage)
    with app(oidc=(provider, lambda request: request.cookies.get("oidc_binding", ""))) as http:
        headers, _ = login(http, "administrator")
        session = headers["Cookie"].split("=", 1)[1]
        csrf = headers["X-CSRF-Token"]
        state, nonce = Federation(transactions, provider).begin(
            binding,
            Provenance(headers["Origin"], "same-origin", csrf),
            session,
        )
        signed.nonce = opaque() if scenario == "nonce" else nonce
        path = f"/auth/oidc/callback?code={code}&state={state}"
        cookie = {"Cookie": f"oidc_binding={opaque() if scenario == 'browser' else binding}"}
        if scenario == "replay":
            success = http.request("GET", path, cookie)
            assert success.status == 200
            assert success.body["data"]["session"]["userId"] == str(admin)
            assert success.body["data"]["linked"] is True
            oidc_session = {"Cookie": success.headers["set-cookie"].split(";", 1)[0]}
            decision(http, oidc_session, project, "project_member:list", True)
        before = committed_state()
        reply = http.request("GET", path, cookie)
        if scenario in {"outage", "redirect"}:
            assert_problem(reply, 502, "oidc_exchange_failed")
        else:
            assert_problem(reply, 400, "oidc_state_invalid")
        assert committed_state() == before
    if scenario == "redirect":
        assert destinations == [config().token_endpoint]
    with transactions.access.uow() as store:
        row = store.get("oidc_transactions", {"state_hash": digest(state)})
        assert row is not None and row["state"] == (
            "consumed" if scenario == "replay" else "failed"
        )
        assert row["nonce_hash"] == digest(nonce) and row["browser_hash"] == digest(binding)
        denied = store.rows(
            "observations", {"action": "get_auth_oidc_callback", "outcome": "DENIED"}
        )
        assert denied
        assert_redacted(reply, denied, code, state, nonce, binding, session, csrf, custody[admin])


def assert_redacted(reply, audit: object, *secrets: str) -> None:
    rendered = repr((reply, audit))
    for secret in secrets:
        assert secret not in rendered, "sensitive fixture value was serialized"


def test_epic_009_seguranca_negative_paths_abuse(
    instance,
    enrolled,
    transactions: IdentityTransactions,
    committed_state: Snapshot,
    login_limit: int,
):
    """REQ-ID-002 and REQ-AUTH-IMPL-007/010: persist denials without issuing credentials."""
    app, _, custody = instance
    admin, _ = enrolled
    invalid_password = opaque()
    before = committed_state()
    with app() as http:
        bootstrap = http.request(
            "POST",
            "/auth/bootstrap",
            body={
                "username": "second-administrator",
                "password": PASSWORD,
                "displayName": "Replay",
            },
        )
        assert_problem(bootstrap, 409, "bootstrap_already_completed")
        assert committed_state() == before and list(custody) == [admin]
        for _ in range(login_limit):
            wrong = http.request(
                "POST",
                LOGIN,
                body={
                    "username": "administrator",
                    "password": invalid_password,
                },
            )
            assert_problem(wrong, 401, "invalid_credentials")
            assert committed_state() == before
    with app() as restarted:
        throttled = restarted.request(
            "POST",
            LOGIN,
            body={
                "username": "administrator",
                "password": PASSWORD,
            },
        )
        assert_problem(throttled, 429, "rate_limited")
    assert committed_state() == before
    with transactions.access.uow() as store:
        (bucket,) = store.rows("throttle_buckets", {"operation": "post_auth_session"})
        assert bucket["failure_count"] == login_limit and bucket["state"] == "limited"
        (denial,) = [
            row
            for row in store.rows("throttle_decisions", {"reason": "rate_limited"})
            if row["before_state"]["state"] == "limited"
        ]
        assert denial["allowed"] is False
        (audit,) = store.rows("observations", {"correlation_id": denial["id"]})
        assert audit["outcome"] == "DENIED"
        assert_redacted(
            throttled, (audit, bucket, denial), PASSWORD, invalid_password, custody[admin]
        )


def test_epic_009_seguranca_negative_paths_postgres_failure(
    instance,
    enrolled,
    database: str,
    transactions: IdentityTransactions,
    committed_state: Snapshot,
) -> None:
    """ADR-030/032: a failed authoritative write rolls back and redacts diagnostics."""
    app, (project, _), _ = instance
    _, viewer = enrolled
    diagnostic = opaque()
    with app() as http:
        headers, _ = login(http, "administrator")
        before = committed_state()
        with connect(database) as connection:
            connection.execute(
                sql.SQL(
                    "ALTER TABLE identity.memberships ADD CONSTRAINT {} CHECK (false) NOT VALID"
                ).format(sql.Identifier(diagnostic))
            )
        try:
            reply = http.request(
                "POST", members(project), headers, {"userId": str(viewer), "role": "viewer"}
            )
            assert_problem(reply, 500, "internal_error")
            assert committed_state() == before
            with transactions.access.uow() as store:
                (audit,) = store.rows(
                    "observations",
                    {
                        "action": "post_projects_projectid_members",
                        "outcome": "DENIED",
                    },
                )
                assert audit["reason_code"] == "internal_error"
                assert_redacted(reply, audit, diagnostic, headers["X-CSRF-Token"])
        finally:
            with connect(database) as connection:
                connection.execute(
                    sql.SQL("ALTER TABLE identity.memberships DROP CONSTRAINT {}").format(
                        sql.Identifier(diagnostic)
                    )
                )
