"""Consolidate integrated slices without introducing a second authorization service."""

import csv
from importlib import import_module

import pytest
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied

from .conftest import ADAPTER, CONTRACT, ROOT


def test_story_0047_slice_consolidation(runtime):
    """Both builders share current grants, contract, UoW and durable decisions."""
    r = runtime
    project = uuid7()
    r.member(project)
    original = import_module(ADAPTER).build_authorization
    cpu = import_module(ADAPTER.replace("acc-auth-impl-parte-1", "hw-parte-2"))
    services = (
        original(r.tx, lambda store, pid: True, CONTRACT),
        cpu.build_authorization(r.tx, lambda store, pid: True, CONTRACT),
        cpu.build_authorization(r.tx, lambda store, pid: True, CONTRACT, execution_mode="cpu"),
    )
    assert all(type(service) is type(services[0]) for service in services)
    assert all(service.tx is r.tx for service in services)

    def decisions(action, kind, target, allowed):
        expected = {
            "allowed": allowed,
            "policyVersion": "1.1.0",
            "reasonCode": "granted" if allowed else "access_denied",
        }
        for service in services:
            assert service.check(r.issued.secret, "session", action, kind, target) == expected

    decisions("project_member:create", "project", project, True)
    with r.uow() as store:
        store.update(
            "memberships",
            {"project_id": project, "account_id": r.account.id},
            {"role": "viewer", "revision": 2},
        )
    decisions("project_member:create", "project", project, False)
    decisions("project_member:list", "project", project, True)
    decisions("project_member:list", "project", uuid7(), False)
    for kind in ("artifact", "artifact_path", "physical_path"):
        decisions("artifact_manifest:read", kind, uuid7(), False)
    with r.uow() as store:
        rows = store.rows("observations", {"action": "get_authorization_check"})
        assert len(rows) == 21
        assert sum(row["outcome"] == "COMMITTED" for row in rows) == 6
        assert sum(row["outcome"] == "DENIED" for row in rows) == 15
        assert all(row["policy_version"] == "1.1.0" for row in rows)
        assert all(row["actor_id"] == r.account.id for row in rows)
        assert r.issued.secret not in str(rows)
    r.sessions.logout(r.issued.secret, "session", 1, "logout", r.browser())
    for service in services:
        with pytest.raises(Denied, match="unauthorized"):
            service.check(r.issued.secret, "session", "project_member:list", "project", project)


def test_consolidation_preserves_requirement_ownership():
    """Consolidation adds no requirements; slice ownership remains disjoint."""
    matrix = ROOT / "docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv"
    with matrix.open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))

    def requirements(story):
        return {
            requirement
            for row in rows
            if row["story_id"] == story
            for requirement in row["requirement_ids"].split("/")
            if requirement
        }

    identity = {"REQ-ACC-001"} | {
        f"REQ-AUTH-IMPL-{number:03}" for number in (1, 2, 3, 4, 5, 6, 8, 9, 10)
    }
    assert requirements("STORY-0716") == identity
    assert requirements("STORY-0717") == {"REQ-HW-001"}
    assert not requirements("STORY-0047")
    assert requirements("STORY-0716").isdisjoint(requirements("STORY-0717"))
    # Quantitative throttling remains in its explicit calibration story.
    assert requirements("STORY-0762") == {"REQ-AUTH-IMPL-007"}
