"""REQ-HW-001: real CPU decisions without an optional accelerator dependency."""

import sys
from importlib import import_module

import pytest
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied

from .conftest import ADAPTER, CONTRACT

HARDWARE = ADAPTER.replace("acc-auth-impl-parte-1", "hw-parte-2")


def test_cpu_baseline_gpu_optional_no_silent_fallback(runtime, monkeypatch):
    class NoAccelerators:
        def find_spec(self, fullname, path=None, target=None):
            if fullname.split(".")[0] in {"torch", "cupy", "tensorflow", "pycuda"}:
                pytest.fail(f"CPU authorization attempted accelerator import: {fullname}")

    monkeypatch.setattr(sys, "meta_path", [NoAccelerators(), *sys.meta_path])
    r = runtime
    project = uuid7()
    r.member(project)
    build = import_module(HARDWARE).build_authorization
    default = build(r.tx, lambda store, pid: True, CONTRACT)
    explicit = build(r.tx, lambda store, pid: True, CONTRACT, execution_mode="cpu")
    original = import_module(ADAPTER).build_authorization(r.tx, lambda store, pid: True, CONTRACT)
    for action, kind, target, allowed in (
        ("project_member:list", "project", project, True),
        ("project_member:list", "project", uuid7(), False),
        ("token:create", "account", r.account.id, True),
        ("artifact_manifest:read", "artifact_path", uuid7(), False),
    ):
        expected = original.check(r.issued.secret, "session", action, kind, target)
        assert expected["allowed"] is allowed
        for service in (default, explicit):
            assert service.check(r.issued.secret, "session", action, kind, target) == expected
    with r.uow() as store:
        rows = store.rows("observations", {"action": "get_authorization_check"})
        assert len(rows) == 12
        assert {row["outcome"] for row in rows} == {"COMMITTED", "DENIED"}
        assert all(row["policy_version"] == "1.1.0" for row in rows)
        assert r.issued.secret not in str(rows)
    r.sessions.logout(r.issued.secret, "session", 1, "logout", r.browser())
    with pytest.raises(Denied, match="unauthorized"):
        explicit.check(r.issued.secret, "session", "project_member:list", "project", project)


@pytest.mark.parametrize("mode", ["gpu", "cuda", "auto", "CPU", "", None, True, 1])
def test_unsupported_execution_mode_fails_before_cpu_composition(mode, monkeypatch):
    adapter = import_module(HARDWARE)

    def forbidden_import(*args, **kwargs):
        pytest.fail("unsupported mode silently reached CPU composition")

    monkeypatch.setattr(adapter, "import_module", forbidden_import)
    with pytest.raises(Denied, match="validation_failed"):
        adapter.build_authorization(None, None, None, execution_mode=mode)


def test_cpu_preserves_composition_and_authority_failures(runtime, tmp_path):
    build = import_module(HARDWARE).build_authorization
    with pytest.raises(Denied, match="internal_error"):
        build(runtime.tx, lambda store, pid: True, tmp_path / "missing")
    service = build(runtime.tx, lambda store, pid: True, CONTRACT)
    runtime.tx.eligibility = lambda store, operation, actor: False
    with pytest.raises(Denied, match="rate_limited"):
        service.check(
            runtime.issued.secret, "session", "token:create", "account", runtime.account.id
        )
    runtime.tx.access.uow = type(runtime.uow)("host=127.0.0.1 port=1 dbname=absent user=absent")
    with pytest.raises(Denied, match="internal_error"):
        service.check(
            runtime.issued.secret, "session", "token:create", "account", runtime.account.id
        )
