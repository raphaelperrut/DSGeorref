"""Consolidation evidence only: reuse merged BC-002 outputs in one PostgreSQL state."""

import csv
import hashlib
import json
import subprocess
from pathlib import Path
from xml.etree import ElementTree

import psycopg
import pytest
from conftest import Runtime
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import ValidatingOidcProvider
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from oidc_fixture import SignedProvider, config

ROOT = Path(__file__).resolve().parents[4]
OUTPUTS = ROOT / "evidence/implementation/contas-locais-bootstrap-unico-sessoes-tokens-e-ada"
SLICES = {
    "STORY-0712": ("ISSUE-0822", "auth-impl-dbschema-parte-1", "ba0b63d"),
    "STORY-0713": ("ISSUE-0823", "id-parte-2", "39afd61"),
}


def merged_coverage():
    with (ROOT / "docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv").open(
        encoding="utf-8", newline=""
    ) as source:
        rows = list(csv.DictReader(source))
    owners = {}
    for story, (issue, directory, merge) in SLICES.items():
        subprocess.run(["git", "merge-base", "--is-ancestor", merge, "HEAD"], cwd=ROOT, check=True)
        report = json.loads((OUTPUTS / directory / "VALIDATION-REPORT.json").read_text())
        assigned = next(row for row in rows if row["criterion_id"] == f"AC-{issue}-01")
        assert assigned["story_id"] == story
        requirements = assigned["requirement_ids"].split("/")
        junit = "mandatory-tests.xml" if story == "STORY-0712" else "focused-tests.xml"
        cases = ElementTree.parse(OUTPUTS / directory / junit).findall(".//testcase")
        assert cases and all(
            not list(case) or all(child.tag == "properties" for child in case) for case in cases
        )
        for requirement in requirements:
            assert requirement not in owners
            owners[requirement] = story
            if story == "STORY-0712":
                evidence = report["requirements"][requirement]
                assert evidence["implementation_evidence"] == "PASS"
                assert evidence["canonical_test"] in {case.attrib["name"] for case in cases}
            else:
                assert report[requirement.replace("-", "_")] == "PASS"
        if story == "STORY-0712":
            h1 = ElementTree.parse(OUTPUTS / directory / "h1-focused-tests.xml")
            assert len(h1.findall(".//testcase")) == 4
            assert not h1.findall(".//failure") and not h1.findall(".//error")
        else:
            for entry in report["source_manifest"]:
                content = (ROOT / entry["path"]).read_text(encoding="utf-8")
                assert hashlib.sha256(content.encode()).hexdigest() == entry["sha256_utf8_lf"]
    assert len(owners) == 12
    # No consolidation authority or duplicate use case: all production output is unchanged.
    assert not subprocess.check_output(
        ["git", "diff", "a2206c1", "--", "src/backend/dsgeorref/contexts/identity_access"],
        cwd=ROOT,
    )
    return owners


def test_story_0037_slice_consolidation(runtime: Runtime, record_property):
    owners = merged_coverage()
    r = runtime
    transport = SignedProvider("pending")
    federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
    assert federation.tx is r.accounts.tx is r.tokens.tx
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
    federated, linked = federation.callback(state, "browser", "signed-code")
    assert linked
    token = r.tokens.issue(
        federated.secret, "session", ["authorization:check"], "consolidation", r.browser(federated)
    )
    assert r.access.authenticate(pat=token.secret).account.id == r.account.id
    with r.uow() as store:
        assert store.get("bootstrap", {"singleton": True})["administrator_id"] == r.account.id
        assert store.get("tokens", {"id": token.token.id})["secret_hash"] == digest(token.secret)
        assert store.get("sessions", {"id": federated.session.id})["oidc_link_id"]
        pending = store.get("oidc_transactions", {"state_hash": digest(state)})
        assert (
            pending["account_id"] == r.account.id and pending["session_id"] == r.issued.session.id
        )
        assert pending["state"] == "consumed"
    # Slice-1 token authority accepts the slice-2 OIDC session; unlink revokes only linked sessions.
    r.tokens.revoke(federated.secret, "session", token.token.id, r.browser(federated))
    federation.unlink(r.issued.secret, federated.session.oidc_link_id, r.browser())
    for credential in ({"session": federated.secret}, {"pat": token.secret}):
        with pytest.raises(Denied) as denied:
            r.access.authenticate(**credential)
        assert denied.value.code == "unauthorized"
    assert r.access.authenticate(session=r.issued.secret).account.id == r.account.id
    with r.uow() as store:
        assert store.get("tokens", {"id": token.token.id})["state"] == "revoked"
        assert store.get("sessions", {"id": federated.session.id})["state"] == "revoked"
        assert len(store.rows("accounts", {"administrator": True})) == 1
        for action, target in (
            ("revoke", token.token.id),
            ("unlink", federated.session.oidc_link_id),
        ):
            assert (
                len(
                    store.rows(
                        "observations",
                        {"action": action, "target_id": target, "outcome": "COMMITTED"},
                    )
                )
                == 1
            )
    with psycopg.connect(r.dsn) as connection:
        assert connection.execute(
            "SELECT version_num FROM identity.alembic_version"
        ).fetchone() == ("identity_link_binding_v2",)
        assert connection.execute("""SELECT convalidated FROM pg_constraint
            WHERE conname='oidc_transaction_session_owner_fk'""").fetchone() == (True,)
    record_property("coverage", json.dumps(owners, sort_keys=True))
    record_property(
        "runtime_observed",
        "same account/bootstrap; explicit OIDC link -> session -> "
        "PAT -> durable token revoke + unlink; both denied; local session valid; "
        "one audit per mutation; existing validated v2 schema",
    )
