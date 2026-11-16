"""Run the actual Gitleaks rules against public licenses and synthetic credentials."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / ".github/gitleaks.toml"
VALUE = "aB9cD2eF7gH4iJ6kL8mN1pQ3rS5tU0vW"
DIGEST = hashlib.sha256(b"TASK-0773 synthetic cache artifact").hexdigest()
CACHE_INVENTORY = (
    "evidence/operations/python-workspace-lock/linux-native-20261115/"
    "resume-after-checker/cache-files-before-offline.json"
)


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
                    ".",
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
                cwd=source,
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

    def test_cache_inventory_contains_only_sha256_values(self) -> None:
        content = (ROOT / CACHE_INVENTORY).read_text(encoding="utf-8")
        inventory = json.loads(content)
        self.assertEqual(len(inventory), 4110)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{64}", v) for v in inventory.values()))
        self.assertEqual(self.scan(content, CACHE_INVENTORY), (0, []))

    def test_cache_exception_rejects_non_digest_credentials(self) -> None:
        # Includes both affected rules and near-misses of the SHA-256 format.
        values = (VALUE, VALUE * 2, VALUE * 2 + "+", DIGEST + "f", DIGEST.upper())
        for value in values:
            with self.subTest(value=value):
                for field in ("api_key", "archive-v0/fixture/token.py", "confluent_secret"):
                    content = json.dumps({field: value}, indent=2)
                    baseline_code, baseline = self.scan(content)
                    self.assertEqual(baseline_code, 1)
                    code, findings = self.scan(content, CACHE_INVENTORY)
                    self.assertEqual(code, 1)
                    self.assertEqual(
                        {item["RuleID"] for item in findings},
                        {item["RuleID"] for item in baseline},
                    )

    def test_cache_exception_does_not_hide_another_secret_on_same_line(self) -> None:
        code, findings = self.scan(
            json.dumps({"api_key": DIGEST, "token": VALUE}), CACHE_INVENTORY,
        )
        self.assertEqual(code, 1)
        self.assertIn("generic-api-key", {item["RuleID"] for item in findings})

    def test_digest_exception_is_limited_to_exact_inventory_path(self) -> None:
        for name in ("fixture.json", CACHE_INVENTORY + ".bak", "other/" + CACHE_INVENTORY):
            with self.subTest(name=name):
                code, findings = self.scan(
                    json.dumps({"api_key": DIGEST, "confluent_secret": DIGEST}), name,
                )
                self.assertEqual(code, 1)
                self.assertIn("confluent-secret-key", {item["RuleID"] for item in findings})
                code, findings = self.scan(
                    json.dumps({"archive-v0/fixture/token.py": DIGEST}, indent=2), name,
                )
                self.assertEqual(code, 1)
                self.assertIn("generic-api-key", {item["RuleID"] for item in findings})


if __name__ == "__main__":
    unittest.main()
