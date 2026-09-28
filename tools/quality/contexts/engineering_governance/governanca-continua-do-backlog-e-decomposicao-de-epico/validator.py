from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from artifact_validation import validate_profile
from contract_definition import (
    EXAMPLE_REL,
    EXPECTED_REQUIREMENTS,
    MANIFEST_REL,
    SCHEMA_REL,
)
from manifest_validation import validate_manifest
from validation_types import finding


def build_report(repository_root: Path) -> dict[str, Any]:
    root = repository_root.resolve()
    findings = sorted(set(validate_manifest(root) + validate_profile(root)))
    requirement_evidence = [
        {
            "requirement_id": requirement_id,
            "control": expectation["control"],
            "test": expectation["test"],
            "source": MANIFEST_REL.as_posix(),
        }
        for requirement_id, expectation in sorted(EXPECTED_REQUIREMENTS.items())
    ]
    return {
        "schema_version": "1.0.0",
        "control_id": "EPIC-110-CONTINUOUS-BACKLOG-GOVERNANCE",
        "status": "FAIL" if findings else "PASS",
        "failure_policy": "FAIL_CLOSED",
        "execution_mode": "READ_ONLY",
        "destructive_actions": False,
        "dry_run": "NOT_APPLICABLE_READ_ONLY",
        "contract": {
            "manifest": MANIFEST_REL.as_posix(),
            "schema": SCHEMA_REL.as_posix(),
            "example": EXAMPLE_REL.as_posix(),
            "version": "1.0.0",
            "owner": "BC-001",
        },
        "requirement_evidence": requirement_evidence,
        "findings": [asdict(item) for item in findings],
    }


def _unexpected_report(exc: Exception) -> dict[str, Any]:
    item = finding(
        "validator",
        "UNEXPECTED_VALIDATION_ERROR",
        f"{type(exc).__name__}: {exc}",
        "Inspect the named error and restore readable versioned inputs.",
    )
    return {
        "schema_version": "1.0.0",
        "control_id": "EPIC-110-CONTINUOUS-BACKLOG-GOVERNANCE",
        "status": "FAIL",
        "failure_policy": "FAIL_CLOSED",
        "execution_mode": "READ_ONLY",
        "destructive_actions": False,
        "dry_run": "NOT_APPLICABLE_READ_ONLY",
        "contract": {"manifest": MANIFEST_REL.as_posix()},
        "requirement_evidence": [],
        "findings": [asdict(item)],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the frozen EPIC-110 backlog governance profile."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[5],
    )
    args = parser.parse_args(argv)
    try:
        report = build_report(args.repository_root)
    except Exception as exc:  # pragma: no cover - last-resort fail-closed boundary
        report = _unexpected_report(exc)
    print(json.dumps(report, ensure_ascii=True, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
