"""Executable acceptance evidence for ISSUE-0140; no independent approval."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
SLUG = "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca"
TOOLS = ROOT / "tools/governance" / SLUG
DOCS = ROOT / "docs/03-engineering/contexts/engineering_governance" / SLUG


def _run(script: str, *arguments: object) -> tuple[int, dict[str, Any]]:
    completed = subprocess.run(
        [sys.executable, "-B", str(TOOLS / script), *(str(arg) for arg in arguments)],
        cwd=ROOT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"},
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert not completed.stderr, completed.stderr
    report = json.loads(completed.stdout)
    assert isinstance(report, dict)
    return completed.returncode, report


def test_epic_006_aceite_happy_path() -> None:
    result = _run("repository_integration.py", "--repository-root", ROOT)
    assert result == _run("repository_integration.py", "--repository-root", ROOT)
    returncode, report = result
    assert returncode == 0, report
    assert report["status"] == "PASS"
    assert report["findings"] == []
    assert report["control_plane"] == "SUBPROCESS_READ_ONLY"
    assert set(report["requirement_evidence"]) == {"REQ-AI-007", "REQ-TST-001"}

    task = json.loads((ROOT / ".codex/tasks/TASK-0030.json").read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(task)
    assert task["issue_id"] == "ISSUE-0140"
    assert task["dependencies"] == ["STORY-0029"]
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    assert task["deny_paths"] == task["phase_f_review"]["files"]["deny_paths"]
    assert task["evidence"] == task["phase_f_review"]["artifacts"]["evidence"]
    assert task["tests"] == [
        "test_epic_006_aceite_happy_path", "test_epic_006_aceite_negative_paths"
    ]


@pytest.mark.parametrize("case", ["missing_predecessors", "corpus_tampering", "fallback"])
def test_epic_006_aceite_negative_paths(tmp_path: Path, case: str) -> None:
    if case == "missing_predecessors":
        result = _run("repository_integration.py", "--repository-root", tmp_path)
        expected_code = 1
        expected_findings = {
            "DOCUMENT_INVALID", "FOUNDATION_VALIDATION_FAILED", "AUTOMATION_VALIDATION_FAILED"
        }
    else:
        source = DOCS / "test-corpus-manifest.json" if case == "corpus_tampering" else (
            TOOLS / "foundation-checkpoint.json"
        )
        document = json.loads(source.read_text(encoding="utf-8"))
        if case == "corpus_tampering":
            document["fixtures"][0]["sha256"] = "0" * 64
            option, finding = "--corpus", "CORPUS_HASH_MISMATCH"
        else:
            document["failure_policy"]["silent_fallback"] = True
            option, finding = "--checkpoint", "SILENT_FALLBACK_PROHIBITED"
        fixture = tmp_path / source.name
        fixture.write_text(json.dumps(document), encoding="utf-8")
        result = _run("validate_catalog.py", option, fixture)
        expected_code, expected_findings = 2, {finding}

    returncode, report = result
    assert returncode == expected_code, report
    assert report["status"] == "FAIL"
    assert expected_findings <= {item["code"] for item in report["findings"]}
