"""Authenticate inherited task provenance against canonical GitHub integrations.

Git objects establish content, never permission. This adapter establishes the
integration authority independently from the untrusted candidate and its proof.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class IntegrationProof:
    base_revision: str
    authority_checkpoint: str
    candidate_revision: str
    integration_revision: str
    task_envelope_path: str
    pull_request: int
    composition_revision: str | None = None
    composition_proofs: tuple[IntegrationProof, ...] = ()


def git_text(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        check=False,
        timeout=20,
        encoding="utf-8",
    )
    if result.returncode:
        raise ValueError(f"Git evidence unavailable: {args[0]}")
    return result.stdout.rstrip("\n")


def full_commit(root: Path, revision: str) -> None:
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("composition requires full immutable commit identities")
    if git_text(root, "cat-file", "-t", revision) != "commit":
        raise ValueError("revision is not a commit")


@dataclass(frozen=True)
class GitHubIntegrationAuthority:
    """Trusted invocation pins repository, human Owner ID and canonical branch.

    A proof cannot select a different repository, principal or branch. Restricting
    merge authority to that Owner is intentionally conservative. Live GitHub
    evidence is required; a candidate-controlled JSON receipt is not accepted.
    """

    repository: str
    owner_id: int
    branch: str = "main"

    def _get(self, resource: str) -> dict[str, Any]:
        endpoint = f"repos/{self.repository}" + (f"/{resource}" if resource else "")
        response = subprocess.run(
            ["gh", "api", "--hostname", "github.com", endpoint],
            capture_output=True,
            check=False,
            timeout=20,
            encoding="utf-8",
        )
        if response.returncode:
            raise ValueError("authenticated GitHub authority evidence is unavailable")
        value = json.loads(response.stdout)
        if not isinstance(value, dict):
            raise ValueError("GitHub authority response is not an object")
        return value

    def authenticate(self, root: Path, proof: IntegrationProof) -> None:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", self.repository):
            raise ValueError("invalid trusted repository identity")
        if not isinstance(self.owner_id, int) or self.owner_id <= 0 or self.branch != "main":
            raise ValueError("invalid trusted Owner or canonical branch")
        origin = git_text(root, "remote", "get-url", "origin")
        if origin not in {
            f"https://github.com/{self.repository}.git",
            f"https://github.com/{self.repository}",
            f"git@github.com:{self.repository}.git",
        }:
            raise ValueError("repository origin does not match trusted integration authority")
        if type(proof.pull_request) is not int or proof.pull_request <= 0:
            raise ValueError("invalid integration pull request identity")
        repo = self._get("")
        pr = self._get(f"pulls/{proof.pull_request}")
        branch = self._get(f"branches/{self.branch}")
        self._verify_metadata(repo, pr, proof)
        tip = branch["commit"]["sha"]
        full_commit(root, tip)
        git_text(root, "merge-base", "--is-ancestor", proof.integration_revision, tip)

    def _verify_metadata(
        self,
        repo: dict[str, Any],
        pr: dict[str, Any],
        proof: IntegrationProof,
    ) -> None:
        expected = (
            repo["full_name"] == self.repository,
            repo["owner"]["id"] == self.owner_id,
            repo["default_branch"] == self.branch,
            pr["number"] == proof.pull_request,
            pr["merged"] is True,
            pr["merged_by"]["id"] == self.owner_id,
            pr["merge_commit_sha"] == proof.integration_revision,
            pr["head"]["sha"] == proof.candidate_revision,
            pr["base"]["repo"]["id"] == repo["id"],
            pr["base"]["ref"] == self.branch,
        )
        if not all(expected):
            raise ValueError("integration is not an authenticated canonical Owner merge")
