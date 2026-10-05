"""TASK-0039: four executable security cases against existing identity services.

SignedProvider/config are the attributed STORY-0037 JWT transport fixtures;
signature verification, Argon2id, HMAC, policy and application flows are real.
"""

import base64
import json
import secrets
from dataclasses import asdict, replace
from datetime import UTC, datetime, timedelta

import jwt
import pytest
from conftest import ORIGIN, PASSWORD
from dsgeorref.contexts.identity_access.adapters.local_identity.crypto import ArgonPasswords
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import (
    NoRedirect,
    ValidatingOidcProvider,
)
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.application.local_identity.recovery import (
    AdministrativeRecovery,
)
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import (
    digest,
    opaque,
    uuid7,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance
from oidc_fixture import SignedProvider, config


def denied(code, action):
    with pytest.raises(Denied) as failure:
        action()
    assert failure.value.code == code
    assert str(failure.value) == code


def evidence(record_property, action, expected, observed):
    record_property("runtime_evidence", json.dumps([action, expected, observed]))
    print(f"{action} → {expected} → {observed}")


def test_secret_permissions_rotation_redaction_fail_closed(runtime, record_property):
    r = runtime
    for size in (0, 1, 31):
        denied(
            "internal_error",
            lambda size=size: IdentityTransactions(
                r.access, r.tx.passwords, r.tx.web, r.tx.eligibility, secrets.token_bytes(size)
            ),
        )
        evidence(record_property, f"replay_key {size} bytes", "startup denied", "internal_error")
    key = secrets.token_bytes(32)
    tx = IdentityTransactions(r.access, r.tx.passwords, r.tx.web, r.tx.eligibility, key)
    assert tx.access is r.access and len(key) == 32
    assert key.hex() not in repr(tx)
    for invalid in (None, "x" * 32, bytearray(32)):
        denied(
            "internal_error",
            lambda invalid=invalid: IdentityTransactions(
                r.access, r.tx.passwords, r.tx.web, r.tx.eligibility, invalid
            ),
        )
    evidence(record_property, "CSPRNG replay_key 32 bytes", "startup accepted", "accepted")
    raw = opaque()
    assert len(base64.urlsafe_b64decode(raw + "=")) == 32
    denied("internal_error", lambda: ArgonPasswords(replace(r.access.profile, approved=False)))
    session, kit = r.bootstrap()
    account = r.access.authenticate(session=session.secret).account
    # Current grants, rather than administrator labels, govern credential permissions.
    r.access.policy.account_grants[account.id] -= {"token:create"}
    denied(
        "forbidden",
        lambda: r.tokens.issue(
            session.secret, "session", ["authorization:check"], "no", r.browser(session)
        ),
    )
    assert not r.uow.rows("tokens", {})
    r.access.policy.account_grants[account.id] |= {"token:create"}
    rotated = r.sessions.rotate(session.secret, 1, r.browser(session))
    assert rotated.secret != session.secret and rotated.csrf != session.csrf
    assert r.access.authenticate(session=rotated.secret).account.id == account.id
    denied("unauthorized", lambda: r.access.authenticate(session=session.secret))
    assert r.uow.get("sessions", {"id": session.session.id})["state"] == "rotated"
    # Secret-bearing values, request fingerprints and allowlisted audits disclose no plaintext.
    metadata = str(r.uow.data) + repr((account, session, rotated, tx))
    for secret in (PASSWORD, kit, session.secret, session.csrf, rotated.secret, rotated.csrf):
        assert secret not in metadata
    assert all(o["outcome"] in {"COMMITTED", "DENIED"} for o in r.uow.rows("observations", {}))
    evidence(
        record_property,
        "remove grant / rotate / inspect metadata",
        "deny escalation; old session denied; no plaintext",
        "forbidden; rotated + unauthorized; plaintext absent",
    )


def test_one_time_bootstrap_no_default_credentials_secret_generation_expiry_and_recovery(
    runtime, record_property
):
    r = runtime
    assert not r.uow.rows("accounts", {})
    denied(
        "invalid_credentials", lambda: r.accounts.login("admin", "admin", "default", r.browser())
    )
    session, kit = r.bootstrap()
    account = r.access.authenticate(session=session.secret).account
    assert account.password_hash.startswith("$argon2id$") and account.recovery_hash == digest(kit)
    assert len(base64.urlsafe_b64decode(kit + "=")) == 32
    denied(
        "bootstrap_already_completed",
        lambda: r.accounts.bootstrap("second", PASSWORD, "second", r.browser()),
    )
    replay_account, replay, replay_kit = r.accounts.bootstrap(
        "security-admin", PASSWORD, "bootstrap", r.browser()
    )
    assert replay_account.id == account.id and replay.secret == replay.csrf == replay_kit == ""
    assert len(r.uow.rows("accounts", {})) == 1
    assert len(r.uow.rows("observations", {"action": "AdminBootstrapped"})) == 1
    token = r.tokens.issue(
        session.secret, "session", ["authorization:check"], "recover-pat", r.browser(session)
    )
    recovery = AdministrativeRecovery(r.tx, lambda account, ceremony: False)
    denied("forbidden", lambda: recovery.recover(account.id, kit, PASSWORD, uuid7()))
    recovery = AdministrativeRecovery(r.tx, lambda account, ceremony: True)
    denied("forbidden", lambda: recovery.recover(account.id, "invalid-kit", PASSWORD, uuid7()))
    ceremony = uuid7()
    next_kit = recovery.recover(account.id, kit, PASSWORD + "-new", ceremony)
    assert next_kit != kit
    denied("forbidden", lambda: recovery.recover(account.id, kit, PASSWORD, uuid7()))
    denied("conflict", lambda: recovery.recover(account.id, next_kit, PASSWORD, ceremony))
    denied("unauthorized", lambda: r.access.authenticate(session=session.secret))
    denied("unauthorized", lambda: r.access.authenticate(pat=token.secret))
    denied(
        "invalid_credentials",
        lambda: r.accounts.login("security-admin", PASSWORD, "old", r.browser()),
    )
    replacement = r.accounts.login("security-admin", PASSWORD + "-new", "new", r.browser())
    assert r.access.authenticate(session=replacement.secret).account.id == account.id
    r.uow.clock += r.access.profile.session_idle
    denied("unauthorized", lambda: r.access.authenticate(session=replacement.secret))
    assert r.uow.get("sessions", {"id": replacement.session.id})["state"] == "expired"
    assert r.uow.get("bootstrap", {"singleton": True})["state"] == "completed"
    assert r.uow.get("accounts", {"id": account.id})["recovery_hash"] == digest(next_kit)
    assert len(r.uow.rows("ceremonies", {})) == 1
    assert all(s not in str(r.uow.data) for s in (PASSWORD, kit, next_kit, token.secret))
    evidence(
        record_property,
        "bootstrap / recovery / credential reuse / idle expiry",
        "no defaults; one administrator; one-use kit; revoked/expired credentials denied",
        "invalid_credentials; one admin; rotated kit; forbidden/conflict/unauthorized; expired",
    )


def test_epic_008_seguranca_happy_path(runtime, record_property):
    r = runtime
    local, _ = r.bootstrap()
    account = r.access.authenticate(session=local.secret).account
    transport = SignedProvider("pending")
    federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
    state, transport.nonce = federation.begin("browser", r.browser(local), local.secret)
    federated, linked = federation.callback(state, "browser", "signed-fixture-code")
    assert linked and r.access.authenticate(session=federated.secret).account.id == account.id
    state, transport.nonce = federation.begin("browser", r.browser())
    login, linked = federation.callback(state, "browser", "signed-fixture-code")
    assert not linked and login.session.oidc_link_id == federated.session.oidc_link_id
    token = r.tokens.issue(
        federated.secret, "session", ["authorization:check"], "pat", r.browser(federated)
    )
    assert r.access.authenticate(pat=token.secret).account.id == account.id
    assert r.access.check(token.secret, "pat", "authorization:check", None)
    assert r.uow.get("tokens", {"id": token.token.id})["secret_hash"] == digest(token.secret)
    r.tokens.revoke(local.secret, "session", token.token.id, r.browser(local))
    denied("unauthorized", lambda: r.access.authenticate(pat=token.secret))
    federation.unlink(local.secret, federated.session.oidc_link_id, r.browser(local))
    denied("unauthorized", lambda: r.access.authenticate(session=federated.secret))
    denied("unauthorized", lambda: r.access.authenticate(session=login.secret))
    r.sessions.logout(local.secret, "session", 1, "logout", r.browser(local))
    denied("unauthorized", lambda: r.access.authenticate(session=local.secret))
    independent = r.accounts.login("security-admin", PASSWORD, "independent-local", r.browser())
    assert r.access.authenticate(session=independent.secret).account.id == account.id
    assert all(s not in str(r.uow.data) for s in (local.secret, federated.secret, token.secret))
    evidence(
        record_property,
        "local bootstrap / signed OIDC link+login / PAT / revoke+unlink+logout",
        "same account; scoped PAT; terminal credentials denied; explicit local login works",
        "same account; authorization true; unauthorized after revocation; local login succeeds",
    )


def test_epic_008_seguranca_negative_paths(runtime, record_property):
    r = runtime
    _bootstrap_failures(r)
    session, _ = r.bootstrap()
    _authorization_failures(r, session)
    _oidc_failures(r, session)
    # Egress surface exists only in configured OIDC HTTPS transport; paths are not accepted.
    for url in (
        "http://provider.example.test",
        "https://user:password@provider.example.test",
        "https://provider.example.test/#fragment",
    ):
        denied(
            "oidc_exchange_failed", lambda url=url: replace(config(), token_endpoint=url).validate()
        )
    denied(
        "oidc_exchange_failed",
        lambda: NoRedirect().redirect_request(
            None, None, 302, "redirect", {}, "https://other.test"
        ),
    )
    evidence(
        record_property,
        "abuse / authorization / invalid OIDC / unsafe config + redirect",
        "deny; no unauthorized credentials/link or silent fallback; reject insecure egress",
        "asserted published denials; counts unchanged; failed single-use state; redirects denied",
    )


def _bootstrap_failures(r):
    r.tx.eligibility = lambda store, operation, actor: False
    denied(
        "internal_error",
        lambda: r.accounts.bootstrap("security-admin", PASSWORD, "limited", r.browser()),
    )
    assert not r.uow.rows("accounts", {})
    r.tx.eligibility = lambda store, operation, actor: True
    r.uow.fail_commit = True
    denied(
        "internal_error",
        lambda: r.accounts.bootstrap("security-admin", PASSWORD, "failed-commit", r.browser()),
    )
    assert not r.uow.rows("accounts", {}) and not r.uow.rows("sessions", {})
    assert r.uow.get("bootstrap", {"singleton": True})["state"] == "available"
    assert not r.uow.rows("observations", {"action": "AdminBootstrapped"})
    r.access.policy = replace(r.access.policy, installation_actions=frozenset())
    denied(
        "validation_failed",
        lambda: r.accounts.bootstrap("security-admin", PASSWORD, "no-permission", r.browser()),
    )
    r.access.policy = replace(
        r.access.policy, installation_actions=frozenset({"instance:bootstrap"})
    )


def _authorization_failures(r, session):
    account = r.access.authenticate(session=session.secret).account
    denied("unauthorized", lambda: r.access.authenticate(session=session.secret, pat="other"))
    denied("unauthorized", lambda: r.access.authenticate())
    for request in (
        Provenance("https://attacker.test", "same-origin", session.csrf),
        Provenance(ORIGIN, "cross-site", session.csrf),
        Provenance(ORIGIN, "same-origin", "wrong-csrf"),
    ):
        denied(
            "forbidden",
            lambda request=request: r.tokens.issue(
                session.secret, "session", ["authorization:check"], opaque(), request
            ),
        )
    for scopes in ([], ["unknown"], ["authorization:check", "authorization:check"]):
        denied(
            "validation_failed",
            lambda scopes=scopes: r.tokens.issue(
                session.secret, "session", scopes, opaque(), r.browser(session)
            ),
        )
    denied(
        "forbidden",
        lambda: r.tokens.issue(
            session.secret,
            "session",
            ["project_member:list"],
            "cross-project",
            r.browser(session),
            uuid7(),
        ),
    )
    r.tx.eligibility = lambda store, operation, actor: 1
    denied(
        "rate_limited",
        lambda: r.tokens.issue(
            session.secret, "session", ["authorization:check"], "nonbool", r.browser(session)
        ),
    )
    r.tx.eligibility = lambda store, operation, actor: True
    token = r.tokens.issue(
        session.secret, "session", ["authorization:check"], "once", r.browser(session)
    )
    denied(
        "conflict",
        lambda: r.tokens.issue(
            session.secret, "session", ["authorization:check"], "once", r.browser(session)
        ),
    )
    denied("unauthorized", lambda: r.access.authenticate(session="bad-cookie", pat=token.secret))
    competitor = replace(account, id=uuid7(), username="other", administrator=False)
    r.uow.insert("accounts", asdict(competitor))
    r.access.policy.account_grants[competitor.id] = r.access.policy.account_grants[account.id]
    other = r.accounts.login("other", PASSWORD, "other-login", r.browser())
    denied(
        "forbidden",
        lambda: r.tokens.revoke(other.secret, "session", token.token.id, r.browser(other)),
    )
    r.access.policy.account_grants[account.id] -= {"authorization:check"}
    denied("forbidden", lambda: r.access.authenticate(pat=token.secret))
    r.access.policy.account_grants[account.id] |= {"authorization:check"}
    r.uow.clock += r.access.profile.pat_lifetime
    denied("unauthorized", lambda: r.access.authenticate(pat=token.secret))
    assert r.uow.get("tokens", {"id": token.token.id})["state"] == "expired"
    r.uow.clock -= r.access.profile.pat_lifetime
    for state in ("inactive", "locked", "unknown"):
        r.uow.update("accounts", {"id": account.id}, {"state": state})
        denied("unauthorized", lambda: r.access.authenticate(session=session.secret))
    r.uow.update("accounts", {"id": account.id}, {"state": "active"})


def _oidc_failures(r, session):
    for fault in (
        "disabled",
        "issuer",
        "audience",
        "subject",
        "nonce",
        "browser",
        "signature",
        "outage",
        "expiry",
        "jwt-expiry",
    ):
        transport = SignedProvider("pending")
        provider_config = replace(config(), enabled=False) if fault == "disabled" else config()
        federation = Federation(r.tx, ValidatingOidcProvider(provider_config, transport))
        before = len(r.uow.rows("sessions", {}))
        state, transport.nonce = federation.begin("browser", r.browser(session), session.secret)
        browser, expected = "browser", "oidc_exchange_failed"
        if fault in {"issuer", "audience", "subject", "nonce"}:
            setattr(transport, fault, "" if fault == "subject" else "invalid")
            if fault == "nonce":
                expected = "oidc_state_invalid"
        elif fault == "browser":
            browser, expected = "other-browser", "oidc_state_invalid"
        elif fault == "signature":
            transport.signer = SignedProvider("unused").signer
        elif fault == "outage":
            transport.outage = True
        elif fault == "jwt-expiry":
            claims = jwt.decode(
                transport.token(provider_config, "fixture"), options={"verify_signature": False}
            )
            claims["exp"] = datetime.now(UTC) - timedelta(seconds=1)
            expired = jwt.encode(
                claims, transport.signer, algorithm="RS256", headers={"kid": "test-key"}
            )
            transport.token = lambda config, code, expired=expired: expired
        elif fault == "expiry":
            r.uow.clock += r.access.profile.oidc_lifetime
            expected = "oidc_state_invalid"
        denied(
            expected,
            lambda federation=federation, state=state, browser=browser: federation.callback(
                state, browser, "synthetic-code"
            ),
        )
        denied(
            "oidc_state_invalid",
            lambda federation=federation, state=state: federation.callback(
                state, "browser", "reuse"
            ),
        )
        assert r.uow.get("oidc_transactions", {"state_hash": digest(state)})["state"] == "failed"
        assert not r.uow.rows("oidc_links", {})
        assert len(r.uow.rows("sessions", {})) == before
        if fault == "expiry":
            r.uow.clock -= r.access.profile.oidc_lifetime
