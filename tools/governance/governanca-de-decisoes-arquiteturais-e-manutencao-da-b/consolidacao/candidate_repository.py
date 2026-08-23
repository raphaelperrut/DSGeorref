from __future__ import annotations

import json
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any


class CandidateView:
    """Read governed artifacts from one immutable Git candidate."""

    def __init__(self, repository_root: Path, revision: str) -> None:
        self.repository_root = repository_root
        self.revision = revision

    def blob(self, path: str) -> bytes:
        completed = subprocess.run(
            [
                "git",
                "-C",
                str(self.repository_root),
                "show",
                f"{self.revision}:{path}",
            ],
            check=False,
            capture_output=True,
        )
        if completed.returncode != 0:
            raise ValueError(f"candidate artifact is missing: {path}")
        return completed.stdout

    def json(self, path: str) -> Mapping[str, Any]:
        try:
            value = json.loads(self.blob(path))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"candidate artifact is invalid JSON: {path}") from error
        if not isinstance(value, Mapping):
            raise ValueError(f"candidate artifact must be a JSON object: {path}")
        return value

    def tracked_paths(self) -> tuple[str, ...]:
        completed = subprocess.run(
            [
                "git",
                "-C",
                str(self.repository_root),
                "ls-tree",
                "-r",
                "--name-only",
                self.revision,
            ],
            check=False,
            capture_output=True,
            encoding="utf-8",
        )
        if completed.returncode != 0:
            raise ValueError("candidate revision is not readable")
        return tuple(path for path in completed.stdout.splitlines() if path)
