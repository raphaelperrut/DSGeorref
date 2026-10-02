"""Ten canonical tests against PostgreSQL and real cryptographic primitives."""

from dataclasses import asdict, replace
from datetime import timedelta

import psycopg
import pytest
from conftest import ORIGIN, PASSWORD, synthetic_profile
from cryptography.hazmat.primitives.asymmetric import rsa
from dsgeorref.contexts.identity_access.adapters.local_identity.crypto import ArgonPasswords
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import ValidatingOidcProvider
from dsgeorref.contexts.identity_access.adapters.local_identity.web import WebResponses
from dsgeorref.contexts.identity_access.application.local_identity.access import Access
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.application.local_identity.recovery import (
    AdministrativeRecovery,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import (
    digest,
    opaque,
    uuid7,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Denied,
    PersonalAccessToken,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance, WebPolicy
from oidc_fixture import SignedProvider, config


def rejected(code, call):
    with pytest.raises(Denied) as error:
        call()
    assert error.value.code == code


def test_req_auth_impl_001(runtime):
    r = runtime
    assert r.access.authenticate(session=r.issued.secret).account.id == r.account.id
    r.sessions.logout(r.issued.secret, "session", 1, "logout", r.browser())
    rejected("unauthorized", lambda: r.access.authenticate(session=r.issued.secret))
    with r.uow() as store:
        row = store.get("sessions", {"id": r.issued.session.id})
        assert row["state"] == "revoked" and row["revision"] == 2
        observations = store.rows("observations", {"target_id": r.issued.session.id})
        assert any(o["action"] == "SessionRevoked" for o in observations)
        assert r.issued.secret not in str(observations)
    unavailable = Access(
        type(r.uow)("host=127.0.0.1 port=1 dbname=absent user=absent"),
        r.access.policy,
        r.access.profile,
    )
    rejected("internal_error", lambda: unavailable.authenticate(session=r.issued.secret))


def test_req_auth_impl_002(runtime):
    profile = synthetic_profile()
    passwords = ArgonPasswords(profile)
    first, second = passwords.hash(PASSWORD), passwords.hash(PASSWORD)
    assert first != second and passwords.verify(PASSWORD, first)
    assert not passwords.verify("incorrect-password", first)
    assert "$argon2id$v=19$m=1024,t=1,p=1$" in first
    for invalid in (
        replace(profile, approved=False),
        replace(profile, approved=1),
        replace(profile, benchmark="absent"),
        replace(profile, memory_kib=1),
        replace(profile, session_idle=timedelta(0)),
        replace(profile, io_timeout=float("inf")),
        replace(profile, io_timeout=float("nan")),
    ):
        rejected("internal_error", lambda p=invalid: ArgonPasswords(p))
    rejected("internal_error", lambda: passwords.verify(PASSWORD, "$argon2i$invalid"))
    rejected("password_policy_failed", lambda: passwords.hash("short"))
    passwords._budget.acquire()
    try:
        rejected("internal_error", lambda: passwords.hash(PASSWORD))
    finally:
        passwords._budget.release()
    assert runtime.account.password_hash != PASSWORD


def test_req_auth_impl_003(runtime):
    r = runtime
    for request in (
        None,
        Provenance("https://evil.example", "same-origin", r.issued.csrf),
        Provenance(ORIGIN, "cross-site", r.issued.csrf),
        Provenance(ORIGIN, "same-origin", "wrong"),
    ):
        rejected(
            "forbidden",
            lambda q=request: r.tokens.issue(
                r.issued.secret, "session", ["authorization:check"], opaque(), q
            ),
        )
    rejected(
        "validation_failed",
        lambda: r.accounts.login(
            "admin", PASSWORD, "bad-origin", Provenance("https://evil.example", "cross-site")
        ),
    )
    pat = r.tokens.issue(r.issued.secret, "session", ["authorization:check"], "valid", r.browser())
    rejected("unauthorized", lambda: r.access.authenticate(session="wrong", pat=pat.secret))
    with r.uow() as store:
        assert len(store.rows("tokens", {"account_id": r.account.id})) == 1


def test_req_auth_impl_004(runtime):
    r = runtime
    project = uuid7()
    r.member(project)
    issued = r.tokens.issue(
        r.issued.secret, "session", ["project_member:list"], "pat", r.browser(), project
    )
    assert r.access.authenticate(pat=issued.secret).credential.id == issued.token.id
    rejected(
        "conflict",
        lambda: r.tokens.issue(
            r.issued.secret, "session", ["project_member:list"], "pat", r.browser(), project
        ),
    )
    rejected(
        "validation_failed",
        lambda: r.tokens.issue(
            r.issued.secret, "session", ["unregistered"], "unknown", r.browser(), project
        ),
    )
    rejected(
        "validation_failed",
        lambda: r.tokens.issue(r.issued.secret, "session", [], "empty", r.browser()),
    )
    with r.uow() as store:
        row = store.get("tokens", {"id": issued.token.id})
        assert row["secret_hash"] == digest(issued.secret)
        assert issued.secret not in str(row)
        store.update(
            "memberships",
            {"project_id": project, "account_id": r.account.id},
            {"role": "viewer", "revision": 2},
        )
    r.tokens.revoke(r.issued.secret, "session", issued.token.id, r.browser())
    rejected("unauthorized", lambda: r.access.authenticate(pat=issued.secret))
    with r.uow() as store:
        assert store.get("tokens", {"id": issued.token.id})["state"] == "revoked"


def test_req_auth_impl_005(runtime):
    r = runtime
    transport = SignedProvider("pending")
    for timeout in (float("inf"), float("nan"), 0):
        invalid = ValidatingOidcProvider(replace(config(), timeout=timeout), transport)
        rejected("oidc_exchange_failed", lambda p=invalid: p.exchange("code", "nonce"))
    provider = ValidatingOidcProvider(config(), transport)
    federation = Federation(r.tx, provider)
    state, nonce = federation.begin("browser", r.browser(), r.issued.secret)
    transport.nonce = nonce
    issued, linked = federation.callback(state, "browser", "synthetic-code")
    assert linked and r.access.authenticate(session=issued.secret).account.id == r.account.id
    rejected("oidc_state_invalid", lambda: federation.callback(state, "browser", "code"))
    state, nonce = federation.begin("browser", r.browser())
    transport.nonce = nonce
    _, linked = federation.callback(state, "browser", "code")
    assert not linked
    transport.subject = "no-link-no-auto-provision"
    state, transport.nonce = federation.begin("browser", r.browser())
    rejected("identity_link_conflict", lambda: federation.callback(state, "browser", "code"))
    for fault in ("browser", "nonce", "audience", "issuer", "signature", "outage"):
        transport = SignedProvider("pending")
        federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
        state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
        expected = "oidc_exchange_failed"
        browser = "browser"
        if fault == "browser":
            browser, expected = "other-browser", "oidc_state_invalid"
        if fault == "nonce":
            transport.nonce, expected = "wrong", "oidc_state_invalid"
        if fault == "audience":
            transport.audience = "other-client"
        if fault == "issuer":
            transport.issuer = "https://other.example"
        if fault == "signature":
            transport.public = rsa.generate_private_key(
                public_exponent=65537, key_size=2048
            ).public_key()
        if fault == "outage":
            transport.outage = True
        rejected(expected, lambda f=federation, s=state, b=browser: f.callback(s, b, "code"))
        with r.uow() as store:
            assert (
                store.get("oidc_transactions", {"state_hash": digest(state)})["state"] == "failed"
            )
    federation.unlink(r.issued.secret, issued.session.oidc_link_id, r.browser())
    rejected("unauthorized", lambda: r.access.authenticate(session=issued.secret))
    # A database failure after link insert must rollback the link and persist failed state.
    transport = SignedProvider("pending")
    transport.subject = "atomic-link"
    federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
    with psycopg.connect(r.dsn) as connection:
        connection.execute("""CREATE FUNCTION identity.fail_session() RETURNS trigger
          LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'synthetic session failure'; END $$;
          CREATE TRIGGER fail_session BEFORE INSERT ON identity.sessions
          FOR EACH ROW EXECUTE FUNCTION identity.fail_session()""")
    try:
        rejected("internal_error", lambda: federation.callback(state, "browser", "code"))
        with r.uow() as store:
            assert store.get("oidc_links", {"subject": "atomic-link"}) is None
            assert (
                store.get("oidc_transactions", {"state_hash": digest(state)})["state"] == "failed"
            )
    finally:
        with psycopg.connect(r.dsn) as connection:
            connection.execute(
                "DROP TRIGGER fail_session ON identity.sessions; "
                "DROP FUNCTION identity.fail_session()"
            )


def test_req_auth_impl_006(runtime):
    r = runtime
    project, other = uuid7(), uuid7()
    r.member(project)
    assert r.access.check(r.issued.secret, "session", "project_member:list", project)
    assert not r.access.check(r.issued.secret, "session", "project_member:list", other)
    rejected(
        "validation_failed", lambda: r.access.check(r.issued.secret, "session", "unknown", project)
    )
    pat = r.tokens.issue(
        r.issued.secret, "session", ["project_member:create"], "grant", r.browser(), project
    )
    with r.uow() as store:
        store.update(
            "memberships",
            {"project_id": project, "account_id": r.account.id},
            {"role": "viewer", "revision": 2},
        )
    rejected("forbidden", lambda: r.access.authenticate(pat=pat.secret))
    assert not r.access.check(r.issued.secret, "session", "project_member:create", project)
    with r.uow() as store:
        store.update("accounts", {"id": r.account.id}, {"state": "inactive", "revision": 2})
    rejected("unauthorized", lambda: r.access.authenticate(session=r.issued.secret))


def test_req_auth_impl_008(runtime):
    r = runtime
    replacement = r.sessions.rotate(r.issued.secret, 1, r.browser())
    assert replacement.secret != r.issued.secret and replacement.csrf != r.issued.csrf
    rejected("unauthorized", lambda: r.access.authenticate(session=r.issued.secret))
    rejected("forbidden", lambda: r.sessions.rotate(replacement.secret, 1, r.browser()))
    rejected(
        "precondition_failed",
        lambda: r.sessions.rotate(replacement.secret, 7, r.browser(replacement)),
    )
    r.sessions.logout(replacement.secret, "session", 1, "logout", r.browser(replacement))
    rejected("unauthorized", lambda: r.access.authenticate(session=replacement.secret))
    issued = r.accounts.login("admin", PASSWORD, "login", r.browser())
    replay = r.accounts.login("admin", PASSWORD, "login", r.browser())
    assert replay.session.id == issued.session.id and replay.secret == ""
    bearer = r.tokens.issue(
        issued.secret, "session", ["session:revoke"], "logout-bearer", r.browser(issued)
    )
    rejected(
        "session_not_found",
        lambda: r.sessions.logout(bearer.secret, "pat", 1, "absent-target", None),
    )
    r.sessions.logout(bearer.secret, "pat", 1, "explicit-target", None, issued.session.id)
    rejected("unauthorized", lambda: r.access.authenticate(session=issued.secret))
    with r.uow() as store:
        expired = replace(
            issued.session,
            id=uuid7(),
            secret_hash=digest("expired-session"),
            expires_at=store.now() - timedelta(seconds=1),
            idle_expires_at=store.now() - timedelta(seconds=2),
        )
        store.insert("sessions", asdict(expired))
    rejected("unauthorized", lambda: r.access.authenticate(session="expired-session"))
    with r.uow() as store:
        assert store.get("sessions", {"id": expired.id})["state"] == "expired"
    rejected(
        "bootstrap_already_completed",
        lambda: r.accounts.bootstrap("another", PASSWORD, "another", r.browser()),
    )
    with r.uow() as store:
        denied_bootstrap = store.rows("observations", {"action": "post_auth_bootstrap"})
        assert any(o["reason_code"] == "bootstrap_already_completed" for o in denied_bootstrap)
    rejected(
        "bootstrap_already_completed",
        lambda: r.accounts.bootstrap("admin", PASSWORD + "changed", "bootstrap", r.browser()),
    )


def test_req_auth_impl_009(runtime):
    r = runtime
    ceremony = uuid7()
    denied = AdministrativeRecovery(r.tx, lambda account, ceremony: False)
    rejected("forbidden", lambda: denied.recover(r.account.id, r.recovery, PASSWORD, ceremony))
    recovery = AdministrativeRecovery(r.tx, lambda account, cid: cid == ceremony)
    rejected("forbidden", lambda: recovery.recover(r.account.id, "wrong", PASSWORD, ceremony))
    pat = r.tokens.issue(
        r.issued.secret, "session", ["authorization:check"], "recover-pat", r.browser()
    )
    next_kit = recovery.recover(r.account.id, r.recovery, PASSWORD + "changed", ceremony)
    assert next_kit != r.recovery
    rejected("forbidden", lambda: recovery.recover(r.account.id, r.recovery, PASSWORD, ceremony))
    rejected("unauthorized", lambda: r.access.authenticate(session=r.issued.secret))
    rejected("unauthorized", lambda: r.access.authenticate(pat=pat.secret))
    rejected("invalid_credentials", lambda: r.accounts.login("admin", PASSWORD, "old", r.browser()))
    assert r.accounts.login("admin", PASSWORD + "changed", "new", r.browser()).secret
    with r.uow() as store:
        assert store.get("bootstrap", {"singleton": True})["state"] == "completed"
        evidence = store.rows("observations", {"action": "recover"})
        assert len([o for o in evidence if o["outcome"] == "COMMITTED"]) == 1
        assert len([o for o in evidence if o["outcome"] == "DENIED"]) >= 3
        assert r.recovery not in str(evidence)


def test_req_auth_impl_0010(runtime):
    web = WebResponses(WebPolicy(ORIGIN))
    headers = web.headers("https://evil.example")
    assert "Access-Control-Allow-Origin" not in headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["Cache-Control"] == "no-store"
    cookie = web.cookie(runtime.issued.secret)
    assert "Secure; HttpOnly; SameSite=Strict" in cookie and "Domain=" not in cookie
    assert "Max-Age=0" in web.clear_cookie()
    configured = WebResponses(WebPolicy(ORIGIN, frozenset({"https://allowed.example"})))
    assert (
        configured.headers("https://allowed.example")["Access-Control-Allow-Origin"]
        == "https://allowed.example"
    )
    for invalid in ("*", "http://unsafe.example", "https://safe.example/path"):
        rejected("internal_error", lambda u=invalid: WebPolicy(u))
    rejected("internal_error", lambda: web.cookie("injection; Domain=evil"))


def test_req_dbschema_003(runtime):
    r = runtime
    project, other = uuid7(), uuid7()
    r.member(project)
    rejected(
        "forbidden",
        lambda: r.tokens.issue(
            r.issued.secret, "session", ["project_member:list"], "wrong-project", r.browser(), other
        ),
    )
    with r.uow() as store:
        token = PersonalAccessToken(
            uuid7(),
            r.account.id,
            digest(opaque()),
            ["project_member:list"],
            store.now() + timedelta(minutes=1),
            other,
        )
    with psycopg.connect(r.dsn) as connection:
        with pytest.raises(psycopg.errors.ForeignKeyViolation), connection.transaction():
            connection.execute(
                """INSERT INTO identity.tokens VALUES
             (%s,%s,%s,%s,%s,%s,%s,%s)""",
                list(asdict(token).values()),
            )
        with pytest.raises(psycopg.errors.UniqueViolation), connection.transaction():
            connection.execute(
                "INSERT INTO identity.memberships VALUES (%s,%s,'owner',1)", (project, r.account.id)
            )
        with pytest.raises(psycopg.errors.CheckViolation), connection.transaction():
            connection.execute(
                "UPDATE identity.bootstrap SET state='available',administrator_id=NULL,revision=3"
            )
        constraints = connection.execute(
            "SELECT count(*) FROM pg_constraint WHERE connamespace='identity'::regnamespace"
        ).fetchone()[0]
        assert constraints >= 30
        assert r.account.id.version == 7 and r.issued.session.id.version == 7
