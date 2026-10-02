"""REQ-ID-001/002 acceptance through existing BC-002 services and PostgreSQL."""

import json
from dataclasses import asdict, replace

import psycopg
import pytest
from conftest import PASSWORD
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import ValidatingOidcProvider
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.application.local_identity.recovery import (
    AdministrativeRecovery,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest, uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from oidc_fixture import SignedProvider, config


def denied(code, action):
    with pytest.raises(Denied) as failure:
        action()
    assert failure.value.code == code


def evidence(record_property, action, expected, observed):
    record_property("runtime_evidence", json.dumps([action, expected, observed]))


def test_network_authentication_local_oidc(runtime, record_property):
    r = runtime
    transport = SignedProvider("pending")
    federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
    federated, linked = federation.callback(state, "browser", "signed-test-code")
    assert linked and r.access.authenticate(session=federated.secret).account.id == r.account.id
    state, transport.nonce = federation.begin("browser", r.browser())
    resolved, linked = federation.callback(state, "browser", "signed-test-code")
    assert not linked and resolved.session.oidc_link_id == federated.session.oidc_link_id
    evidence(
        record_property,
        "explicit link then login",
        "same issuer+subject account",
        "linked=true then false; same persisted link/account",
    )

    # An identical subject at a different valid issuer never matches the old link.
    other_config = replace(config(), issuer="https://other-provider.example.test")
    transport.issuer = other_config.issuer
    other = Federation(r.tx, ValidatingOidcProvider(other_config, transport))
    state, transport.nonce = other.begin("browser", r.browser())
    denied("identity_link_conflict", lambda: other.callback(state, "browser", "code"))
    transport.issuer = config().issuer
    competitor = replace(r.account, id=uuid7(), username="second-local", administrator=False)
    with r.uow() as store:
        store.insert("accounts", asdict(competitor))
    r.access.policy.account_grants[competitor.id] = r.access.policy.account_grants[r.account.id]
    local = r.accounts.login(competitor.username, PASSWORD, "second-login", r.browser())
    state, transport.nonce = federation.begin("browser", r.browser(local), local.secret)
    denied("identity_link_conflict", lambda: federation.callback(state, "browser", "code"))
    with r.uow() as store:
        links = store.rows("oidc_links", {"issuer": config().issuer})
        assert len(links) == 1 and links[0]["account_id"] == r.account.id
    evidence(
        record_property,
        "other issuer / competing account",
        "deny; no implicit linking",
        "identity_link_conflict; original unique link unchanged",
    )

    # Removing application permission takes effect even for a valid OIDC identity.
    r.access.policy.account_grants[r.account.id] -= {"token:create"}
    denied(
        "forbidden",
        lambda: r.tokens.issue(
            federated.secret,
            "session",
            ["authorization:check"],
            "denied-admin",
            r.browser(federated),
        ),
    )
    evidence(
        record_property,
        "remove administrative application grant",
        "deny valid OIDC caller",
        "forbidden; IdP identity grants no administrative permission",
    )
    federation.unlink(r.issued.secret, federated.session.oidc_link_id, r.browser())
    denied("unauthorized", lambda: r.access.authenticate(session=federated.secret))
    denied("unauthorized", lambda: r.access.authenticate(session=resolved.secret))
    state, transport.nonce = federation.begin("browser", r.browser())
    denied("identity_link_conflict", lambda: federation.callback(state, "browser", "code"))
    with r.uow() as store:
        link = store.get("oidc_links", {"id": federated.session.oidc_link_id})
        assert link["state"] == "revoked" and link["revision"] == 2
        assert any(
            o["outcome"] == "COMMITTED"
            for o in store.rows("observations", {"target_id": link["id"], "action": "unlink"})
        )
    assert r.accounts.login("admin", PASSWORD, "local-after-unlink", r.browser()).secret
    evidence(
        record_property,
        "unlink / subsequent OIDC use / local login",
        "revoked audited; OIDC denied; local usable",
        "revoked revision=2; unauthorized/identity_link_conflict; local login succeeds",
    )


def test_bootstrap_session_token_recovery(runtime, record_property):
    r = runtime
    with r.uow() as store:
        state = store.get("bootstrap", {"singleton": True})
        assert state["state"] == "completed" and state["administrator_id"] == r.account.id
        assert store.rows("observations", {"action": "AdminBootstrapped"})
    denied(
        "bootstrap_already_completed",
        lambda: r.accounts.bootstrap("another-admin", PASSWORD, "second-bootstrap", r.browser()),
    )
    denied(
        "bootstrap_already_completed",
        lambda: r.accounts.bootstrap("changed-payload", PASSWORD, "bootstrap", r.browser()),
    )
    # Frozen contract allows an exact nonsecret idempotency status replay, no second bootstrap.
    account, replay, kit = r.accounts.bootstrap("admin", PASSWORD, "bootstrap", r.browser())
    assert account.id == r.account.id and replay.secret == "" and kit == ""
    with r.uow() as store:
        assert len(store.rows("accounts", {"administrator": True})) == 1
        assert len(store.rows("observations", {"action": "AdminBootstrapped"})) == 1
    evidence(
        record_property,
        "bootstrap / reuse / exact status replay",
        "one administrator only",
        "completed audited; distinct/changed reuse rejected; replay discloses no secret",
    )

    pat = r.tokens.issue(r.issued.secret, "session", ["authorization:check"], "pat", r.browser())
    assert r.access.authenticate(pat=pat.secret).account.id == r.account.id
    r.tokens.revoke(r.issued.secret, "session", pat.token.id, r.browser())
    denied("unauthorized", lambda: r.access.authenticate(pat=pat.secret))
    r.sessions.logout(r.issued.secret, "session", 1, "logout", r.browser())
    denied("unauthorized", lambda: r.access.authenticate(session=r.issued.secret))
    with r.uow() as store:
        for table, target, action in (
            ("tokens", pat.token.id, "revoke"),
            ("sessions", r.issued.session.id, "SessionRevoked"),
        ):
            assert store.get(table, {"id": target})["state"] == "revoked"
            assert store.rows("observations", {"target_id": target, "action": action})
    evidence(
        record_property,
        "persist / revoke session and token / reuse",
        "durable revocation and audited denial",
        "revoked rows/audits; unauthorized on both",
    )

    session = r.accounts.login("admin", PASSWORD, "pre-recovery", r.browser())
    pat = r.tokens.issue(
        session.secret, "session", ["authorization:check"], "recovery-pat", r.browser(session)
    )
    recovery = AdministrativeRecovery(r.tx, lambda account, ceremony: True)
    denied("forbidden", lambda: recovery.recover(r.account.id, "invalid-kit", PASSWORD, uuid7()))
    ceremony = uuid7()
    next_kit = recovery.recover(r.account.id, r.recovery, PASSWORD + "-changed", ceremony)
    assert next_kit != r.recovery
    denied("forbidden", lambda: recovery.recover(r.account.id, r.recovery, PASSWORD, uuid7()))
    denied("conflict", lambda: recovery.recover(r.account.id, next_kit, PASSWORD, ceremony))
    denied("unauthorized", lambda: r.access.authenticate(session=session.secret))
    denied("unauthorized", lambda: r.access.authenticate(pat=pat.secret))
    denied("invalid_credentials", lambda: r.accounts.login("admin", PASSWORD, "old", r.browser()))
    assert r.accounts.login("admin", PASSWORD + "-changed", "new", r.browser()).secret
    with r.uow() as store:
        assert store.get("ceremonies", {"id": ceremony})["kit_hash"] == digest(r.recovery)
        assert store.get("accounts", {"id": r.account.id})["recovery_hash"] == digest(next_kit)
        assert store.get("bootstrap", {"singleton": True})["state"] == "completed"
        observations = store.rows("observations", {"action": "recover"})
        assert len([o for o in observations if o["outcome"] == "COMMITTED"]) == 1
        assert len([o for o in observations if o["outcome"] == "DENIED"]) == 3
        assert all(secret not in str(observations) for secret in (PASSWORD, r.recovery, next_kit))
    evidence(
        record_property,
        "recovery / revoke old kit and credentials / reuse",
        "one audited ceremony; old password/kit/session/PAT denied; bootstrap remains completed",
        "rotated hash; forbidden/conflict/unauthorized/invalid_credentials; "
        "new local login succeeds",
    )


@pytest.mark.parametrize(
    "fault",
    ["disabled", "subject", "issuer", "audience", "nonce", "browser", "ambiguous-keys", "outage"],
)
def test_oidc_invalid_fails_without_local_fallback(runtime, fault):
    r = runtime
    transport = SignedProvider("pending")
    provider_config = replace(config(), enabled=False) if fault == "disabled" else config()
    federation = Federation(r.tx, ValidatingOidcProvider(provider_config, transport))
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
    browser, expected = "browser", "oidc_exchange_failed"
    if fault == "subject":
        transport.subject = ""
    elif fault == "issuer":
        transport.issuer = "https://invalid.example.test"
    elif fault == "audience":
        transport.audience = "another-client"
    elif fault == "nonce":
        transport.nonce, expected = "wrong-nonce", "oidc_state_invalid"
    elif fault == "browser":
        browser, expected = "wrong-browser", "oidc_state_invalid"
    elif fault == "ambiguous-keys":
        keys = transport.keys(config())
        transport.keys = lambda config: {"keys": keys["keys"] * 2}
    elif fault == "outage":
        transport.outage = True
    denied(expected, lambda: federation.callback(state, browser, "synthetic-code"))
    denied("oidc_state_invalid", lambda: federation.callback(state, "browser", "code"))
    with r.uow() as store:
        assert store.get("oidc_transactions", {"state_hash": digest(state)})["state"] == "failed"
        assert not store.rows("oidc_links", {"account_id": r.account.id})
        assert len(store.rows("sessions", {"account_id": r.account.id})) == 1
        assert store.rows("observations", {"action": "get_auth_oidc_callback", "outcome": "DENIED"})
    assert r.accounts.login("admin", PASSWORD, "independent-local", r.browser()).secret


def test_pending_link_cannot_use_revoked_identity(runtime):
    r = runtime
    transport = SignedProvider("pending")
    federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
    source, _ = federation.callback(state, "browser", "code")
    transport.subject = "new-subject"
    state, transport.nonce = federation.begin("browser", r.browser(source), source.secret)
    # An authoritative link revocation invalidates use even before session cleanup.
    with r.uow() as store:
        store.update(
            "oidc_links", {"id": source.session.oidc_link_id}, {"state": "revoked", "revision": 2}
        )
        r.tx.observe(store, r.account.id, "unlink", source.session.oidc_link_id)
    denied("unauthorized", lambda: r.access.authenticate(session=source.secret))
    denied("identity_link_conflict", lambda: federation.callback(state, "browser", "code"))
    with r.uow() as store:
        assert not store.rows("oidc_links", {"subject": "new-subject"})
        assert store.get("oidc_transactions", {"state_hash": digest(state)})["state"] == "failed"


def test_linking_transaction_session_owner_constraint(runtime):
    r = runtime
    competitor = replace(r.account, id=uuid7(), username="other-owner", administrator=False)
    with r.uow() as store:
        store.insert("accounts", asdict(competitor))
        pending = {
            "id": uuid7(),
            "state_hash": digest("state"),
            "nonce_hash": digest("nonce"),
            "browser_hash": digest("browser"),
            "account_id": competitor.id,
            "session_id": r.issued.session.id,
            "expires_at": r.issued.session.expires_at,
            "state": "pending",
        }
    with (
        psycopg.connect(r.dsn) as connection,
        pytest.raises(psycopg.errors.ForeignKeyViolation),
        connection.transaction(),
    ):
        connection.execute(
            """INSERT INTO identity.oidc_transactions
              (id,state_hash,nonce_hash,browser_hash,account_id,session_id,expires_at,state)
              VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            list(pending.values()),
        )
