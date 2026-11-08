"""Content, history and authority evidence for the compatible scope extension."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
MODULE = (
    ROOT
    / "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b"
    / "frz-gov-adr-gov-dec-parte-1"
)
sys.path.insert(0, str(MODULE))
from scope_integration import GitHubIntegrationAuthority, IntegrationProof  # noqa: E402
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


def envelope(root: Path, path: str, allow: list[str], deny: list[str]) -> None:
    task = json.loads((ROOT / ".codex/tasks/operations/TASK-0785.json").read_bytes())
    task.update(task_id=Path(path).stem, role="Tech Lead", allow_paths=allow, deny_paths=deny)
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
