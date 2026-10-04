"""Exercise bootstrap in a PR-like checkout with a real Git remote."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / ".github/scripts/bootstrap_openapi_base.py"


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


class BootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.origin, self.checkout = root / "origin", root / "checkout"
        self.origin.mkdir()
        git(self.origin, "init", "-q", "-b", "release")
        git(self.origin, "config", "user.name", "CI regression")
        git(self.origin, "config", "user.email", "ci@example.test")
        self.commit("base")
        self.base = git(self.origin, "rev-parse", "HEAD")
        self.commit("advanced base")
        git(
            root,
            "clone",
            "-q",
            "--depth=1",
            "--single-branch",
            self.origin.as_uri(),
            str(self.checkout),
        )
        git(self.checkout, "update-ref", "-d", "refs/remotes/origin/release")

    def commit(self, contents: str) -> None:
        (self.origin / "openapi.yaml").write_text(contents, encoding="utf-8")
        git(self.origin, "add", ".")
        git(self.origin, "commit", "-qm", contents)

    def run_bootstrap(
        self, ref: str, sha: str, event: str = "pull_request"
    ) -> subprocess.CompletedProcess:
        self.output = self.checkout / "github-env"
        env = dict(
            os.environ,
            PR_BASE_REF=ref,
            PR_BASE_SHA=sha,
            GITHUB_EVENT_NAME=event,
            GITHUB_ENV=str(self.output),
        )
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=self.checkout,
            env=env,
            capture_output=True,
            text=True,
        )

    def test_pr_without_initial_base_ref(self) -> None:
        result = self.run_bootstrap("release", self.base)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"OPENAPI_BASE_SHA={self.base}", self.output.read_text())
        self.assertEqual(git(self.checkout, "show", f"{self.base}:openapi.yaml"), "base")
        self.assertNotEqual(git(self.checkout, "rev-parse", "origin/release"), self.base)

    def test_existing_ref_uses_exact_pr_base(self) -> None:
        git(self.checkout, "fetch", "-q", "origin", "+release:refs/remotes/origin/release")
        self.test_pr_without_initial_base_ref()

    def test_pr_without_origin_main(self) -> None:
        git(self.origin, "branch", "-m", "release", "main")
        result = self.run_bootstrap("main", self.base)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"OPENAPI_BASE_SHA={self.base}", self.output.read_text())
        self.assertEqual(git(self.checkout, "show", f"{self.base}:openapi.yaml"), "base")

    def test_manual_run_uses_supplied_default_branch(self) -> None:
        result = self.run_bootstrap("release", "", "workflow_dispatch")
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = git(self.origin, "rev-parse", "HEAD")
        self.assertIn(f"OPENAPI_BASE_SHA={expected}", self.output.read_text())

    def test_absent_ref_or_sha_fails_closed(self) -> None:
        for ref, sha in (
            ("missing", self.base),
            ("release", "f" * 40),
            ("release", ""),
            ("", self.base),
            ("release", "HEAD"),
        ):
            with self.subTest(ref=ref, sha=sha):
                result = self.run_bootstrap(ref, sha)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.output.exists())

    @unittest.skipUnless(shutil.which("make"), "make is required to exercise the CI command")
    def test_semantic_diff_failure_stops_make(self) -> None:
        stub = self.checkout / "pnpm_stub.py"
        calls = self.checkout / "calls"
        stub.write_text(
            "import sys\nfrom pathlib import Path\n"
            "with Path('calls').open('a') as log: log.write(' '.join(sys.argv[1:]) + '\\n')\n"
            "if 'openapi:diff' in sys.argv: sys.exit(23)\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                "make",
                "-f",
                str(ROOT / "Makefile"),
                "frontend-quality",
                f'PNPM="{sys.executable}" "{stub}"',
                f"OPENAPI_BASE_SHA={self.base}",
            ],
            cwd=self.checkout,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        commands = calls.read_text().splitlines()
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[-1], f"--dir src/frontend openapi:diff {self.base}")


if __name__ == "__main__":
    unittest.main()
