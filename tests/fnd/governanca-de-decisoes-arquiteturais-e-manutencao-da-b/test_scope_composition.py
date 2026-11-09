"""Content, history and authority evidence for the compatible scope extension."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[3]
MODULE = (
    ROOT
    / "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b"
    / "frz-gov-adr-gov-dec-parte-1"
)
sys.path.insert(0, str(MODULE))
from scope_integration import (  # noqa: E402
    FrozenTaskAuthority,
    GitHubIntegrationAuthority,
    IntegrationProof,
)
from scope_validation import validate_effective_task_scope  # noqa: E402

TASK = ".codex/tasks/operations/TASK-9940.json"
EXTERNAL = ".codex/tasks/operations/TASK-9941.json"


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE, timeout=20
    ).strip()


def write(root: Path, path: str, value: bytes) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(value)


def commit(root: Path, message: str) -> str:
    git(root, "add", ".")
    git(root, "commit", "-m", message)
    return git(root, "rev-parse", "HEAD")


def envelope(
    root: Path, path: str, allow: list[str], deny: list[str], *, role: str = "Tech Lead",
) -> None:
    task = json.loads((ROOT / ".codex/tasks/operations/TASK-0785.json").read_bytes())
    task.update(task_id=Path(path).stem, role=role, allow_paths=allow, deny_paths=deny)
    task["phase_f_review"]["files"].update(allow_paths=allow, deny_paths=deny)
    write(root, path, (json.dumps(task) + "\n").encode())


@pytest.fixture
def history(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    root = tmp_path / "r"
    root.mkdir()
    git(root, "init", "-b", "seed")
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Test")
    git(root, "config", "core.autocrlf", "false")
    git(root, "config", "core.longpaths", "true")
    git(root, "remote", "add", "origin", "https://github.com/owner/repo.git")
    for path in (".codex/tasks/TASK_ENVELOPE.schema.json", ".codex/policies/file-scopes.yaml"):
        write(root, path, (ROOT / path).read_bytes())
    write(root, "data/task.txt", b"base\n")
    write(root, "data/external.txt", b"base\n")
    base = commit(root, "baseline")
    git(root, "checkout", "-b", "task")
    envelope(root, TASK, ["data/task.txt", "data/forbidden.txt"], ["data/forbidden.txt"])
    checkpoint = commit(root, "task checkpoint")
    write(root, "data/task.txt", b"task\n")
    task_candidate = commit(root, "task work")
    git(root, "checkout", "-b", "external", base)
    envelope(root, EXTERNAL, ["data/external.txt"], [])
    external_checkpoint = commit(root, "external checkpoint")
    write(root, "data/external.txt", b"external\n")
    external_candidate = commit(root, "external work")
    git(root, "checkout", "-b", "main", base)
    git(root, "merge", "--no-ff", "external", "-m", "Owner integration")
    integration = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "task")
    git(root, "merge", "--no-ff", "main", "-m", "sync")
    candidate = git(root, "rev-parse", "HEAD")
    proof = IntegrationProof(
        base, external_checkpoint, external_candidate, integration, EXTERNAL, 1
    )
    repo = {"id": 7, "full_name": "owner/repo", "owner": {"id": 42}, "default_branch": "main"}
    pr = {
        "number": 1,
        "merged": True,
        "merged_by": {"id": 42},
        "merge_commit_sha": integration,
        "head": {"sha": external_candidate},
        "base": {"ref": "main", "repo": {"id": 7}},
    }
    api = {"": repo, "pulls/1": pr, "branches/main": {"commit": {"sha": integration}}}
    monkeypatch.setattr(GitHubIntegrationAuthority, "_get", lambda self, resource: api[resource])
    return {
        "root": root,
        "base": base,
        "checkpoint": checkpoint,
        "task_candidate": task_candidate,
        "integration": integration,
        "candidate": candidate,
        "proof": proof,
        "api": api,
    }


def validate(h: dict, **overrides: object) -> list:
    arguments = {
        "base_revision": h["base"],
        "authority_checkpoint": h["checkpoint"],
        "candidate_revision": h["candidate"],
        "task_envelope_path": TASK,
        "integration_revision": h["integration"],
        "integration_proofs": (h["proof"],),
        "integration_authority": GitHubIntegrationAuthority("owner/repo", 42),
    }
    arguments.update(overrides)
    return validate_effective_task_scope(h["root"], **arguments)


def test_legacy_valid_and_advanced_main_rejected_without_composition(history: dict) -> None:
    h = history
    assert not validate(
        h,
        candidate_revision=h["task_candidate"],
        integration_revision=None,
        integration_proofs=(),
        integration_authority=None,
    )
    assert validate(h, integration_revision=None, integration_proofs=(), integration_authority=None)


def test_legitimate_main_composition_preserves_checkpoint_and_external_content(
    history: dict,
) -> None:
    assert not validate(history)
    h = history
    git(h["root"], "merge-base", "--is-ancestor", h["checkpoint"], h["candidate"])
    assert git(h["root"], "show", f"{h['candidate']}:data/external.txt") == "external"
    assert git(h["root"], "show", f"{h['candidate']}:data/task.txt") == "task"


@pytest.mark.parametrize("mutation", ["owner", "repository", "head", "merge", "unmerged", "branch"])
def test_external_changes_require_canonical_owner_authority(history: dict, mutation: str) -> None:
    api = history["api"]
    if mutation == "owner":
        api["pulls/1"]["merged_by"]["id"] = 99
    elif mutation == "repository":
        api[""]["id"] = 99
    elif mutation == "head":
        api["pulls/1"]["head"]["sha"] = history["base"]
    elif mutation == "merge":
        api["pulls/1"]["merge_commit_sha"] = history["base"]
    elif mutation == "unmerged":
        api["pulls/1"]["merged"] = False
    else:
        api["branches/main"]["commit"]["sha"] = history["base"]
    assert validate(history)


@pytest.mark.parametrize(
    "mutation",
    [
        "missing-proof",
        "missing-authority",
        "arbitrary-I",
        "wrong-K",
        "wrong-B",
        "mutable-I",
        "wrong-origin",
        "missing-api",
        "malformed-proof",
    ],
)
def test_missing_inconsistent_or_arbitrary_provenance_fails_closed(
    history: dict, mutation: str
) -> None:
    h = history
    args: dict = {}
    if mutation == "missing-proof":
        args["integration_proofs"] = ()
    elif mutation == "missing-authority":
        args["integration_authority"] = None
    elif mutation == "arbitrary-I":
        args["integration_revision"] = h["task_candidate"]
    elif mutation == "wrong-K":
        args["authority_checkpoint"] = h["proof"].authority_checkpoint
    elif mutation == "wrong-B":
        args["integration_proofs"] = (replace(h["proof"], base_revision=h["checkpoint"]),)
    elif mutation == "mutable-I":
        args["integration_revision"] = "main"
    elif mutation == "wrong-origin":
        git(h["root"], "remote", "set-url", "origin", "https://github.com/other/repo.git")
    elif mutation == "malformed-proof":
        args["integration_proofs"] = (object(),)
    else:
        h["api"].clear()
    assert validate(h, **args)


@pytest.mark.parametrize(
    "mutation",
    [
        "forbidden-merge",
        "envelope",
        "cancel-denied",
        "cancel-envelope",
        "policy-widening",
        "deny-overrides-allow",
        "mode-merge",
        "allowed-merge",
        "whitespace-path",
        "rename-outside",
    ],
)
def test_task_or_merge_cannot_hide_unauthorized_content(history: dict, mutation: str) -> None:
    h = history
    root = h["root"]
    if mutation in {"forbidden-merge", "mode-merge", "allowed-merge"}:
        if mutation == "forbidden-merge":
            write(root, "data/forbidden.txt", b"injected merge resolution")
            git(root, "add", ".")
        elif mutation == "allowed-merge":
            write(root, "data/task.txt", b"unauthorized resolution of allowed path")
            git(root, "add", ".")
        else:
            git(root, "update-index", "--chmod=+x", "data/task.txt")
        git(root, "commit", "--amend", "--no-edit")
    elif mutation in {"envelope", "cancel-envelope"}:
        original = (root / TASK).read_bytes()
        task = json.loads(original)
        task["allow_paths"].append("**")
        write(root, TASK, json.dumps(task).encode())
        commit(root, "mutate envelope after K")
        if mutation == "cancel-envelope":
            write(root, TASK, original)
            commit(root, "restore envelope")
    elif mutation in {"whitespace-path", "rename-outside"}:
        if mutation == "rename-outside":
            (root / "data/task.txt").rename(root / "outside.txt")
        else:
            path = " data/task.txt"
            write(root, path, b"unauthorized unusual path")
        commit(root, "unusual or renamed unauthorized path")
    else:
        path = (
            ".codex/policies/file-scopes.yaml"
            if mutation == "policy-widening"
            else "data/forbidden.txt"
        )
        write(root, path, b"unauthorized")
        commit(root, "unauthorized revision")
        if mutation == "cancel-denied":
            (root / path).unlink()
            commit(root, "cancel forbidden change in net diff")
    assert validate(h, candidate_revision=git(root, "rev-parse", "HEAD"))


def test_inherited_history_cannot_hide_unauthorized_revision(history: dict) -> None:
    h = history
    root = h["root"]
    proof = h["proof"]
    git(root, "checkout", "external")
    write(root, "unrelated.txt", b"unauthorized external change")
    commit(root, "external unauthorized revision")
    (root / "unrelated.txt").unlink()
    head = commit(root, "external cancellation")
    git(root, "checkout", "-B", "main", h["base"])
    git(root, "merge", "--no-ff", head, "-m", "new integration")
    integration = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "-B", "task", h["task_candidate"])
    git(root, "merge", "--no-ff", integration, "-m", "new sync")
    h["api"]["pulls/1"].update(head={"sha": head}, merge_commit_sha=integration)
    h["api"]["branches/main"]["commit"]["sha"] = integration
    assert validate(
        h,
        integration_revision=integration,
        candidate_revision=git(root, "rev-parse", "HEAD"),
        integration_proofs=(
            replace(proof, candidate_revision=head, integration_revision=integration),
        ),
    )


def test_collision_with_inherited_change_is_rejected_even_if_content_agrees(history: dict) -> None:
    h = history
    root = h["root"]
    git(root, "checkout", "-B", "task", h["base"])
    envelope(root, TASK, ["data/task.txt", "data/external.txt"], ["data/forbidden.txt"])
    original = (root / TASK).read_bytes()
    # The original frozen task authority explicitly includes both paths in this fixture.
    task = json.loads(original)
    task["allow_paths"] = ["data/task.txt", "data/external.txt"]
    write(root, TASK, json.dumps(task).encode())
    checkpoint = commit(root, "collision fixture checkpoint")
    write(root, "data/external.txt", b"external\n")
    commit(root, "task independently changes inherited path to identical bytes")
    git(root, "merge", "--no-ff", h["integration"], "-m", "colliding sync")
    findings = validate(
        h, authority_checkpoint=checkpoint, candidate_revision=git(root, "rev-parse", "HEAD")
    )
    assert findings
    assert "collide" in findings[0].detail


def test_candidate_must_preserve_original_checkpoint(history: dict) -> None:
    h = history
    findings = validate(h, candidate_revision=h["integration"])
    assert any(f.code == "CHECKPOINT_INVALID" for f in findings)


@pytest.mark.parametrize(
    "code,body,accepted",
    [(0, '{"id":42}', True), (1, "{}", False), (0, "[]", False), (0, "invalid", False)],
)
def test_github_adapter_pins_host_and_rejects_missing_evidence(
    monkeypatch: pytest.MonkeyPatch,
    code: int,
    body: str,
    accepted: bool,
) -> None:
    import scope_integration

    calls = []

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(command)
        assert kwargs["timeout"] == 20
        return SimpleNamespace(returncode=code, stdout=body)

    monkeypatch.setenv("GH_HOST", "untrusted.example")
    monkeypatch.setattr(scope_integration.subprocess, "run", run)
    authority = GitHubIntegrationAuthority("owner/repo", 42)
    if accepted:
        assert authority._get("") == {"id": 42}
    else:
        with pytest.raises(ValueError):
            authority._get("")
    assert calls == [["gh", "api", "--hostname", "github.com", "repos/owner/repo"]]


@pytest.mark.parametrize("custom_namespace", [False, True])
def test_replacement_refs_cannot_hide_unauthorized_merge_content(
    history: dict,
    monkeypatch: pytest.MonkeyPatch,
    custom_namespace: bool,
) -> None:
    h = history
    root = h["root"]
    write(root, "data/forbidden.txt", b"malicious merge resolution")
    git(root, "add", ".")
    git(root, "commit", "--amend", "--no-edit")
    bad = git(root, "rev-parse", "HEAD")
    assert validate(h, candidate_revision=bad)
    if custom_namespace:
        monkeypatch.setenv("GIT_REPLACE_REF_BASE", "refs/scope-replacement/")
    git(root, "replace", bad, h["candidate"])
    findings = validate(h, candidate_revision=bad)
    assert findings
    assert "replacement refs" in findings[0].detail


@pytest.mark.parametrize("environment_file", [False, True])
def test_graft_overlays_cannot_redefine_pinned_ancestry(
    history: dict,
    monkeypatch: pytest.MonkeyPatch,
    environment_file: bool,
) -> None:
    root = history["root"]
    if environment_file:
        graft = root / "custom-grafts"
        monkeypatch.setenv("GIT_GRAFT_FILE", str(graft))
    else:
        graft = root / ".git/info/grafts"
    graft.write_text("", encoding="utf-8")
    findings = validate(history)
    assert findings
    assert "graft overlays" in findings[0].detail


CONSUMER = ".codex/tasks/operations/TASK-9942.json"


@pytest.fixture
def nested_history(history: dict) -> dict:
    return compose_consumer(history)


def compose_consumer(history: dict) -> dict:
    h = history
    root = h["root"]
    git(root, "checkout", "main")
    git(root, "merge", "--no-ff", h["candidate"], "-m", "Owner nested integration")
    integration = git(root, "rev-parse", "HEAD")
    proof = IntegrationProof(
        h["base"], h["checkpoint"], h["candidate"], integration, TASK, 2,
        h["integration"], (h["proof"],),
    )
    api = h["api"]
    api["pulls/2"] = {
        **api["pulls/1"], "number": 2,
        "head": {"sha": h["candidate"]}, "merge_commit_sha": integration,
    }
    api["branches/main"]["commit"]["sha"] = integration
    git(root, "checkout", "-b", "consumer", h["base"])
    envelope(root, CONSUMER, ["data/consumer.txt"], [])
    checkpoint = commit(root, "consumer checkpoint")
    write(root, "data/consumer.txt", b"consumer\n")
    commit(root, "consumer work")
    git(root, "merge", "--no-ff", integration, "-m", "consumer sync")
    return {
        **h, "checkpoint": checkpoint, "integration": integration,
        "candidate": git(root, "rev-parse", "HEAD"), "nested_proof": proof,
    }


def validate_nested(h: dict, **overrides: object) -> list:
    child, parent = h["proof"], h["nested_proof"]
    args = {
        "task_envelope_path": CONSUMER,
        "integration_proofs": (child, parent),
        "integration_authority": GitHubIntegrationAuthority(
            "owner/repo", 42, task_authorities={
                1: FrozenTaskAuthority(h["base"], child.authority_checkpoint, EXTERNAL),
                2: FrozenTaskAuthority(h["base"], parent.authority_checkpoint, TASK),
            },
        ),
    }
    args.update(overrides)
    return validate(h, **args)


def test_nested_composition_preserves_original_authorities(nested_history: dict) -> None:
    h = nested_history
    assert not validate_nested(h)
    proof = h["nested_proof"]
    # Reproduce the old model: integration's first parent substituted for original B.
    flattened = replace(
        proof, base_revision=proof.composition_revision,
        composition_revision=None, composition_proofs=(),
    )
    findings = validate_nested(
        h, integration_proofs=(h["proof"], flattened),
        integration_authority=GitHubIntegrationAuthority("owner/repo", 42),
    )
    assert "checkpoint is not based on base" in findings[0].detail
    findings = validate_nested(h, integration_proofs=(h["proof"], flattened))
    assert "pinned task authority" in findings[0].detail


def test_nested_authority_cannot_be_taken_from_the_proof(nested_history: dict) -> None:
    h = nested_history
    missing = validate_nested(h, integration_authority=GitHubIntegrationAuthority("owner/repo", 42))
    assert "pinned task authority" in missing[0].detail
    proof = h["nested_proof"]
    substituted = replace(proof, authority_checkpoint=proof.candidate_revision)
    findings = validate_nested(h, integration_proofs=(h["proof"], substituted))
    assert "pinned task authority" in findings[0].detail


def test_nested_envelope_cannot_grant_its_own_role_authority(history: dict) -> None:
    h = history
    root = h["root"]
    git(root, "checkout", "-b", "unprivileged", h["base"])
    envelope(root, TASK, [TASK, "data/task.txt"], [], role="Backend")
    h["checkpoint"] = commit(root, "envelope without role authority")
    write(root, "data/task.txt", b"task\n")
    commit(root, "task work")
    git(root, "merge", "--no-ff", h["integration"], "-m", "sync")
    h["candidate"] = git(root, "rev-parse", "HEAD")
    findings = validate_nested(compose_consumer(h))
    assert "role-policy authority" in findings[0].detail


@pytest.mark.parametrize(
    "mutation",
    ["missing", "wrong-order", "wrong-I", "wrong-B", "wrong-K", "mutable-I",
     "bad-type", "orphan-proofs", "cycle", "owner", "head", "merge", "api"],
)
def test_nested_dependencies_fail_closed(nested_history: dict, mutation: str) -> None:
    h = nested_history
    proof = h["nested_proof"]
    child = h["proof"]
    if mutation == "missing":
        proof = replace(proof, composition_proofs=())
    elif mutation == "wrong-order":
        proof = replace(proof, composition_proofs=(child, child))
    elif mutation == "wrong-I":
        proof = replace(proof, composition_revision=h["base"])
    elif mutation == "wrong-B":
        proof = replace(proof, base_revision=proof.composition_revision)
    elif mutation == "wrong-K":
        proof = replace(proof, authority_checkpoint=h["checkpoint"])
    elif mutation == "mutable-I":
        proof = replace(proof, composition_revision="main")
    elif mutation == "bad-type":
        proof = replace(proof, composition_proofs=[child])
    elif mutation == "orphan-proofs":
        child = replace(child, composition_proofs=(child,))
    elif mutation == "cycle":
        cyclic = replace(child, integration_revision=proof.integration_revision)
        proof = replace(proof, composition_proofs=(cyclic,))
    elif mutation == "api":
        del h["api"]["pulls/1"]
    else:
        field, value = {
            "owner": ("merged_by", {"id": 99}),
            "head": ("head", {"sha": h["base"]}),
            "merge": ("merge_commit_sha", h["base"]),
        }[mutation]
        h["api"]["pulls/1"][field] = value
    findings = validate_nested(h, integration_proofs=(child, proof))
    assert findings
    if mutation == "cycle":
        assert "cycle" in findings[0].detail


def test_nested_depth_limit_is_enforced_before_authentication(
    nested_history: dict, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import scope_composition

    h = nested_history
    # Two real levels pass; reducing only the algorithm limit forces the next level closed.
    monkeypatch.setattr(scope_composition, "MAX_COMPOSITION_DEPTH", 2)
    assert not validate_nested(h)
    monkeypatch.setattr(scope_composition, "MAX_COMPOSITION_DEPTH", 1)
    findings = validate_nested(h)
    assert "maximum depth" in findings[0].detail


@pytest.mark.parametrize("mutation", ["owner", "head", "merge", "missing-api"])
def test_authentication_is_repeated_inside_nested_chain(
    nested_history: dict, monkeypatch: pytest.MonkeyPatch, mutation: str,
) -> None:
    h = nested_history
    calls: list[str] = []

    def get(self: GitHubIntegrationAuthority, resource: str) -> dict:
        calls.append(resource)
        if resource == "pulls/1" and calls.count(resource) == 2:
            if mutation == "missing-api":
                raise ValueError("authenticated GitHub authority evidence is unavailable")
            value = dict(h["api"][resource])
            field, wrong = {
                "owner": ("merged_by", {"id": 99}),
                "head": ("head", {"sha": h["base"]}),
                "merge": ("merge_commit_sha", h["base"]),
            }[mutation]
            value[field] = wrong
            return value
        return h["api"][resource]

    monkeypatch.setattr(GitHubIntegrationAuthority, "_get", get)
    findings = validate_nested(h)
    assert findings
    assert calls.count("pulls/1") == 2
    assert "GitHub" in findings[0].detail or "authenticated canonical" in findings[0].detail


@pytest.mark.parametrize(
    "mutation", ["deny", "cancel-deny", "cancel-envelope", "merge-tree", "policy"],
)
def test_nested_candidate_history_cannot_hide_changes(history: dict, mutation: str) -> None:
    h = history
    root = h["root"]
    if mutation == "merge-tree":
        write(root, "data/task.txt", b"unapproved merge resolution\n")
        git(root, "add", ".")
        git(root, "commit", "--amend", "--no-edit")
    elif mutation == "cancel-envelope":
        original = (root / TASK).read_bytes()
        write(root, TASK, original + b"\n")
        commit(root, "mutate inherited frozen envelope")
        write(root, TASK, original)
        commit(root, "restore inherited envelope")
    else:
        path = ".codex/policies/file-scopes.yaml" if mutation == "policy" else "data/forbidden.txt"
        write(root, path, b"unauthorized\n")
        commit(root, "unauthorized inherited candidate change")
        if mutation == "cancel-deny":
            (root / path).unlink()
            commit(root, "cancel inherited forbidden change")
    h["candidate"] = git(root, "rev-parse", "HEAD")
    findings = validate_nested(compose_consumer(h))
    assert findings
    expected = {
        "merge-tree": "merge resolution", "cancel-envelope": "TaskEnvelope changed",
        "deny": "DENIED_PATH_CHANGED", "cancel-deny": "DENIED_PATH_CHANGED",
        "policy": "PATH_OUTSIDE_EFFECTIVE_SCOPE",
    }[mutation]
    assert expected in findings[0].detail


def test_outer_collision_includes_transitive_inherited_paths(nested_history: dict) -> None:
    h = nested_history
    root = h["root"]
    git(root, "checkout", "-b", "collision", h["base"])
    envelope(root, CONSUMER, ["data/external.txt"], [])
    checkpoint = commit(root, "consumer allows transitive path")
    write(root, "data/external.txt", b"external\n")
    commit(root, "consumer changes transitive inherited path to same content")
    git(root, "merge", "--no-ff", h["integration"], "-m", "colliding nested sync")
    findings = validate_nested(
        h, authority_checkpoint=checkpoint, candidate_revision=git(root, "rev-parse", "HEAD"),
    )
    assert findings
    assert "collide" in findings[0].detail and "data/external.txt" in findings[0].detail


def test_default_depth_boundary_and_cycle_precede_authentication(history: dict) -> None:
    from scope_composition import MAX_COMPOSITION_DEPTH, _inherited_changes

    h = history
    assert MAX_COMPOSITION_DEPTH == 16
    authority = GitHubIntegrationAuthority(
        "owner/repo", 42, task_authorities={
            1: FrozenTaskAuthority(h["base"], h["proof"].authority_checkpoint, EXTERNAL),
        },
    )
    args = (h["root"], h["base"], h["integration"], (h["proof"],), authority)
    assert _inherited_changes(*args, active=(h["base"],) * 15)
    with pytest.raises(ValueError, match="maximum depth"):
        _inherited_changes(*args, active=(h["base"],) * 16)
    with pytest.raises(ValueError, match="cycle"):
        _inherited_changes(*args, active=(h["proof"].integration_revision,))
