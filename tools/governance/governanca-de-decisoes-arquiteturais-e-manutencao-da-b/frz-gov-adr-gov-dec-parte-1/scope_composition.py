"""Attribute every revision and verify merge content under frozen scope authority."""

from __future__ import annotations

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
        if (path in changes or _is_ancestor(root, checkpoint, commit)) and (
            _git_bytes(root, commit, path) != authority_bytes
        ):
            raise ValueError(f"TaskEnvelope changed within history at {commit}")
        changed.update(changes)
    return changed


def _inherited_changes(
    root: Path,
    base: str,
    integration: str,
    proofs: tuple[IntegrationProof, ...],
    authority: GitHubIntegrationAuthority,
) -> set[str]:
    previous = base
    changes: set[str] = set()
    if not isinstance(proofs, tuple) or not proofs:
        raise ValueError("integration requires complete authenticated task provenance")
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
        if proof.base_revision != previous:
            raise ValueError("inherited provenance is incomplete or out of order")
        authority.authenticate(root, proof)
        if _parents(root, proof.integration_revision) != (previous, proof.candidate_revision):
            raise ValueError("integration parents do not match authenticated task provenance")
        findings = validate_legacy_scope(
            root,
            base_revision=previous,
            authority_checkpoint=proof.authority_checkpoint,
            candidate_revision=proof.candidate_revision,
            task_envelope_path=proof.task_envelope_path,
        )
        if findings:
            raise ValueError(f"inherited task lacks valid frozen scope: {findings}")
        changes.update(
            _history_scope(
                root,
                previous,
                proof.authority_checkpoint,
                proof.candidate_revision,
                proof.task_envelope_path,
            )
        )
        _merge_content(root, proof.integration_revision, _parents(root, proof.integration_revision))
        previous = proof.integration_revision
    if previous != integration:
        raise ValueError("proof does not terminate at the declared integration identity")
    return changes


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
    try:
        for revision in (
            base_revision,
            authority_checkpoint,
            candidate_revision,
            integration_revision,
        ):
            full_commit(repository_root, revision)
        if not isinstance(integration_authority, GitHubIntegrationAuthority):
            raise ValueError("authenticated integration authority is required")
        if not _is_ancestor(repository_root, integration_revision, candidate_revision):
            raise ValueError("integration is not an ancestor of the candidate")
        inherited = _inherited_changes(
            repository_root,
            base_revision,
            integration_revision,
            integration_proofs,
            integration_authority,
        )
        task = _history_scope(
            repository_root,
            base_revision,
            authority_checkpoint,
            candidate_revision,
            task_envelope_path,
            exclude=integration_revision,
        )
        if task & inherited:
            raise ValueError(f"task and inherited histories collide: {sorted(task & inherited)}")
        return []
    except EVIDENCE_ERRORS as error:
        return [Finding("COMPOSITION_INVALID", "$", str(error))]
