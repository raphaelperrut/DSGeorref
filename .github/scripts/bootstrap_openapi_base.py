"""Fetch the PR's exact comparison base without changing OpenAPI diff semantics."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


def git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], check=True, capture_output=True, text=True
    ).stdout.strip()


def bootstrap(base_ref: str, base_sha: str, event: str) -> str:
    if not base_ref or (event == "pull_request" and not base_sha):
        raise ValueError("comparison base ref/SHA missing")
    if base_sha and re.fullmatch(r"[0-9a-f]{40}", base_sha) is None:
        raise ValueError("comparison base SHA must be a full commit SHA")
    git("check-ref-format", f"refs/heads/{base_ref}")
    remote_ref = f"refs/remotes/origin/{base_ref}"
    git("fetch", "--no-tags", "origin", f"+refs/heads/{base_ref}:{remote_ref}")
    if base_sha:
        # A branch may advance after the PR event; its tip is not the PR base.
        git("fetch", "--no-tags", "origin", base_sha)
    return git("rev-parse", "--verify", "--end-of-options", f"{base_sha or remote_ref}^{{commit}}")


if __name__ == "__main__":
    sha = bootstrap(
        os.environ.get("PR_BASE_REF", ""),
        os.environ.get("PR_BASE_SHA", ""),
        os.environ.get("GITHUB_EVENT_NAME", ""),
    )
    with Path(os.environ["GITHUB_ENV"]).open("a", encoding="utf-8") as output:
        output.write(f"OPENAPI_BASE_SHA={sha}\n")
    print(f"OpenAPI comparison base: {sha}")
