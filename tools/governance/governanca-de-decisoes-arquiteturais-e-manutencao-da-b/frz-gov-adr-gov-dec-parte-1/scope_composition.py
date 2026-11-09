"""Attribute every revision and verify merge content under frozen scope authority."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from foundation_validation_types import Finding
from scope_authority import (
    _checkpoint_findings,
    _effective_path_findings,
    _git_bytes,
    _is_ancestor,
    _matches,
    _scope_authorities,
    _task_path_findings,
    validate_legacy_scope,
)
from scope_integration import GitHubIntegrationAuthority, IntegrationProof, full_commit, git_text

EVIDENCE_ERRORS = (ValueError, TypeError, KeyError, IndexError, OSError, subprocess.SubprocessError)
MAX_COMPOSITION_DEPTH = 16


def _reject_object_overlays(root: Path) -> None:
    # Replacement/graft overlays can change the bytes represented by a pinned SHA.
    if (
        os.environ.get("GIT_REPLACE_REF_BASE")
        or git_text(root, "replace", "--list")
        or git_text(root, "for-each-ref", "--format=%(refname)", "refs/replace/")
    ):
        raise ValueError("Git replacement refs invalidate immutable composition evidence")
    grafts = Path(git_text(root, "rev-parse", "--git-path", "info/grafts"))
    if not grafts.is_absolute():
        grafts = root / grafts
    if grafts.exists() or os.environ.get("GIT_GRAFT_FILE"):
        raise ValueError("Git graft overlays invalidate immutable composition evidence")


def _parents(root: Path, commit: str) -> tuple[str, ...]:
    return tuple(git_text(root, "show", "-s", "--format=%P", commit).split())


def _merge_content(root: Path, commit: str, parents: tuple[str, ...]) -> None:
    if len(parents) != 2:
        raise ValueError("only unambiguous two-parent composition merges are supported")
    bases = git_text(root, "merge-base", "--all", *parents).splitlines()
    if len(bases) != 1:
        raise ValueError("merge ancestry is ambiguous")
    automatic = git_text(root, "merge-tree", "--write-tree", *parents).splitlines()[0]
    actual = git_text(root, "rev-parse", f"{commit}^{{tree}}")
    if automatic != actual:
        raise ValueError("merge resolution changes content beyond the authorized parent trees")


def _revision_changes(root: Path, commit: str) -> tuple[str, ...]:
    parents = _parents(root, commit)
    if len(parents) > 1:
        _merge_content(root, commit, parents)
        return ()
    if not parents:
        raise ValueError("history crosses an unproven root")
    names = git_text(root, "diff", "--no-renames", "--name-only", "-z", parents[0], commit)
    return tuple(path for path in names.split("\0") if path)


def _history_scope(
    root: Path,
    base: str,
    checkpoint: str,
    candidate: str,
    path: str,
    *,
    exclude: str | None = None,
) -> set[str]:
    """Validate each edge, including modifications later cancelled in the net diff."""
    allow, deny, role_allow, role_deny, _, checkpoint_paths, frozen = _scope_authorities(
        root,
        base,
        checkpoint,
        candidate,
        path,
    )
    if not frozen:
        raise ValueError("TaskEnvelope differs from the original frozen checkpoint")
    control = (
        path in checkpoint_paths and _matches(path, role_allow) and not _matches(path, role_deny)
    )
    revisions = [candidate, f"^{base}"]
    if exclude is not None:
        revisions.append(f"^{exclude}")
    commits = git_text(root, "rev-list", "--reverse", "--topo-order", *revisions).splitlines()
    changed: set[str] = set()
    authority_bytes = _git_bytes(root, checkpoint, path)
    for commit in commits:
        changes = _revision_changes(root, commit)
        findings = _effective_path_findings(changes, allow, deny, path, control)
        if findings:
            raise ValueError(f"revision {commit} violates frozen scope: {findings}")
        if path in changes and not control:
            raise ValueError(
                "TaskEnvelope mutation lacks frozen checkpoint and role-policy authority"
            )
        if (path in changes or _is_ancestor(root, checkpoint, commit)) and (
            _git_bytes(root, commit, path) != authority_bytes
        ):
            raise ValueError(f"TaskEnvelope changed within history at {commit}")
        if path in changes and commit != checkpoint:
            raise ValueError(f"TaskEnvelope changed outside its original checkpoint at {commit}")
        changed.update(changes)
    return changed


def _inherited_changes(
    root: Path,
    base: str,
    integration: str,
    proofs: tuple[IntegrationProof, ...],
    authority: GitHubIntegrationAuthority,
    active: tuple[str, ...] = (),
) -> set[str]:
    previous = base
    changes: set[str] = set()
    if not isinstance(proofs, tuple) or not proofs:
        raise ValueError("integration requires complete authenticated task provenance")
    require_task_authority = authority.task_authorities is not None or any(
        isinstance(proof, IntegrationProof) and proof.composition_revision is not None
        for proof in proofs
    )
    for proof in proofs:
        if not isinstance(proof, IntegrationProof):
            raise ValueError("invalid integration proof type")
        for revision in (
            proof.base_revision,
            proof.authority_checkpoint,
            proof.candidate_revision,
            proof.integration_revision,
        ):
            full_commit(root, revision)
        parent = proof.composition_revision or proof.base_revision
        if parent != previous:
            raise ValueError("inherited provenance is incomplete or out of order")
        if proof.integration_revision in active:
            raise ValueError("inherited composition contains a cycle")
        if len(active) >= MAX_COMPOSITION_DEPTH:
            raise ValueError("inherited composition exceeds maximum depth")
        if require_task_authority:
            authority.verify_task_authority(proof)
        authority.authenticate(root, proof)
        if _parents(root, proof.integration_revision) != (previous, proof.candidate_revision):
            raise ValueError("integration parents do not match authenticated task provenance")
        changes.update(_inherited_task_changes(root, proof, authority, active))
        _merge_content(root, proof.integration_revision, _parents(root, proof.integration_revision))
        previous = proof.integration_revision
    if previous != integration:
        raise ValueError("proof does not terminate at the declared integration identity")
    return changes


def _inherited_task_changes(
    root: Path,
    proof: IntegrationProof,
    authority: GitHubIntegrationAuthority,
    active: tuple[str, ...],
) -> set[str]:
    arguments = {
        "base_revision": proof.base_revision,
        "authority_checkpoint": proof.authority_checkpoint,
        "candidate_revision": proof.candidate_revision,
        "task_envelope_path": proof.task_envelope_path,
    }
    if proof.composition_revision is not None:
        return _composed_changes(
            root,
            **arguments,
            integration_revision=proof.composition_revision,
            integration_proofs=proof.composition_proofs,
            integration_authority=authority,
            active=(*active, proof.integration_revision),
        )
    if proof.composition_proofs != ():
        raise ValueError("nested proofs require a composition revision")
    findings = validate_legacy_scope(root, **arguments)
    if findings:
        raise ValueError(f"inherited task lacks valid frozen scope: {findings}")
    return _history_scope(
        root, proof.base_revision, proof.authority_checkpoint,
        proof.candidate_revision, proof.task_envelope_path,
    )


def _composed_changes(
    root: Path,
    *,
    base_revision: str,
    authority_checkpoint: str,
    candidate_revision: str,
    task_envelope_path: str,
    integration_revision: str,
    integration_proofs: tuple[IntegrationProof, ...],
    integration_authority: GitHubIntegrationAuthority,
    active: tuple[str, ...] = (),
) -> set[str]:
    for revision in (base_revision, authority_checkpoint, candidate_revision, integration_revision):
        full_commit(root, revision)
    findings = _task_path_findings(task_envelope_path)
    findings.extend(
        _checkpoint_findings(root, base_revision, authority_checkpoint, candidate_revision)
    )
    if findings:
        raise ValueError(f"composition lacks valid checkpoint or envelope path: {findings}")
    if not _is_ancestor(root, integration_revision, candidate_revision):
        raise ValueError("integration is not an ancestor of the candidate")
    inherited = _inherited_changes(
        root, base_revision, integration_revision, integration_proofs,
        integration_authority, active,
    )
    task = _history_scope(
        root, base_revision, authority_checkpoint, candidate_revision,
        task_envelope_path, exclude=integration_revision,
    )
    if task & inherited:
        raise ValueError(f"task and inherited histories collide: {sorted(task & inherited)}")
    return task | inherited


def validate_composed_scope(
    repository_root: Path,
    *,
    base_revision: str,
    authority_checkpoint: str,
    candidate_revision: str,
    task_envelope_path: str,
    integration_revision: str,
    integration_proofs: tuple[IntegrationProof, ...],
    integration_authority: GitHubIntegrationAuthority | None,
) -> list[Finding]:
    try:
        _reject_object_overlays(repository_root)
        findings = _task_path_findings(task_envelope_path)
        findings.extend(
            _checkpoint_findings(
                repository_root,
                base_revision,
                authority_checkpoint,
                candidate_revision,
            )
        )
        if findings:
            return sorted(set(findings))
        if not isinstance(integration_authority, GitHubIntegrationAuthority):
            raise ValueError("authenticated integration authority is required")
        _composed_changes(
            repository_root,
            base_revision=base_revision,
            authority_checkpoint=authority_checkpoint,
            candidate_revision=candidate_revision,
            task_envelope_path=task_envelope_path,
            integration_revision=integration_revision,
            integration_proofs=integration_proofs,
            integration_authority=integration_authority,
        )
        return []
    except EVIDENCE_ERRORS as error:
        return [Finding("COMPOSITION_INVALID", "$", str(error))]
