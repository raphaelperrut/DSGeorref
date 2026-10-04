"""Run the actual Gitleaks rules against public licenses and synthetic credentials."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / ".github/gitleaks.toml"
VALUE = "aB9cD2eF7gH4iJ6kL8mN1pQ3rS5tU0vW"


class SecretScanTests(unittest.TestCase):
    def scan(self, content: str, name: str = "fixture.json") -> tuple[int, list]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            report = root / "report.json"
            result = subprocess.run(
                [
                    os.environ["GITLEAKS_BINARY"],
                    "dir",
                    str(source),
                    "--config",
                    str(CONFIG),
                    "--redact",
                    "--no-banner",
                    "--report-format",
                    "json",
                    "--report-path",
                    str(report),
                ],
                capture_output=True,
                text=True,
            )
            self.assertIn(result.returncode, (0, 1), result.stderr)
            return result.returncode, json.loads(report.read_text())

    def test_public_spdx_and_immutable_license_evidence(self) -> None:
        code, findings = self.scan(
            json.dumps({"license": "AGPL-3.0-or-later", "openapi_license": "AGPL-3.0-or-later"})
        )
        self.assertEqual((code, findings), (0, []))
        matches = list(ROOT.glob("evidence/**/direct-dependency-review.json"))
        self.assertGreaterEqual(len(matches), 2)
        for source in matches:
            with self.subTest(path=str(source)):
                code, findings = self.scan(
                    source.read_text(encoding="utf-8"),
                    "evidence/license/direct-dependency-review.json",
                )
                self.assertEqual((code, findings), (0, []))

    def test_non_spdx_strings_remain_scanned(self) -> None:
        for value in ("AGPL-3.0-or-laterx", "AGPL-3.0-or-later-suffix"):
            with self.subTest(value=value):
                code, findings = self.scan(json.dumps({"api_key": value}))
                self.assertEqual(code, 1)
                self.assertIn("generic-api-key", {item["RuleID"] for item in findings})

    def test_generic_keys_bearer_tokens_and_passwords_fail(self) -> None:
        for field in ("api_key", "token", "password"):
            with self.subTest(field=field):
                code, findings = self.scan(json.dumps({field: VALUE}))
                self.assertEqual(code, 1)
                self.assertIn("generic-api-key", {item["RuleID"] for item in findings})
        code, findings = self.scan(
            'curl -H "Authorization: Bearer ' + VALUE + '" https://example.test\n'
        )
        self.assertEqual(code, 1)
        self.assertIn("curl-auth-header", {item["RuleID"] for item in findings})

    def test_spdx_does_not_exempt_another_secret_on_same_line(self) -> None:
        code, findings = self.scan(
            json.dumps({"openapi_license": "AGPL-3.0-or-later", "api_key": VALUE})
        )
        self.assertEqual(code, 1)
        self.assertEqual(len(findings), 1)


if __name__ == "__main__":
    unittest.main()
