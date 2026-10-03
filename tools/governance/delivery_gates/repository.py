"""Read immutable Git objects; working-tree evidence cannot release a gate."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from .model import GateError, parse, relative_path, require


class GitRepository:
    def __init__(self, root: Path, revision: str) -> None:
        self.root = root
        require(
            re.fullmatch(r"[0-9a-f]{40}", revision) is not None,
            "consumer base must be a full commit SHA",
        )
        self.revision = self.commit(revision)

    def git(self, *args: str) -> bytes:
        result = subprocess.run(
            ["git", "-C", str(self.root), *args], capture_output=True, check=False
        )
        if result.returncode:
            raise GateError(f"Git object unavailable: {' '.join(args)}")
        return result.stdout

    def commit(self, reference: str) -> str:
        require(not reference.startswith("-"), "invalid Git reference")
        return self.git("rev-parse", "--verify", f"{reference}^{{commit}}").decode().strip()

    def read(self, path: str, revision: str | None = None) -> bytes:
        path = relative_path(path)
        revision = revision or self.revision
        entry = self.git("ls-tree", revision, "--", path).decode().strip()
        require(
            entry.startswith("100644 blob ") or entry.startswith("100755 blob "),
            f"artifact is absent or not a regular Git blob: {path}",
        )
        return self.git("show", f"{revision}:{path}")

    def json(self, path: str, revision: str | None = None) -> dict[str, Any]:
        return parse(self.read(path, revision))

    def ancestor(self, earlier: str, later: str) -> bool:
        self.commit(earlier)
        self.commit(later)
        result = subprocess.run(
            ["git", "-C", str(self.root), "merge-base", "--is-ancestor", earlier, later],
            capture_output=True,
            check=False,
        )
        require(result.returncode in {0, 1}, "cannot verify Git ancestry")
        return result.returncode == 0

    def paths(self, prefix: str) -> list[str]:
        return (
            self.git("ls-tree", "-r", "--name-only", self.revision, "--", prefix)
            .decode("utf-8")
            .splitlines()
        )


class WorkingRepository:
    def __init__(self, root: Path) -> None:
        self.root = root

    def read(self, path: str) -> bytes:
        path = relative_path(path)
        resolved = (self.root / path).resolve()
        require(resolved.is_relative_to(self.root.resolve()), "path escapes repository")
        try:
            return resolved.read_bytes()
        except OSError as error:
            raise GateError(f"reference unavailable: {path}") from error

    def json(self, path: str) -> dict[str, Any]:
        return parse(self.read(path))

    def paths(self, prefix: str) -> list[str]:
        return sorted(
            path.relative_to(self.root).as_posix()
            for path in (self.root / prefix).glob("TASK-*.json")
        )
