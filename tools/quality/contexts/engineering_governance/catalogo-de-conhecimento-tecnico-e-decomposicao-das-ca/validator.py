from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from automation_validation import ACCEPTANCE_EVIDENCE, REQUIREMENT_EVIDENCE, Finding, validate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate EPIC-006 capability catalog controls.")
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[5],
        help="Repository root containing the frozen EPIC-006 foundation.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Assert validation-only mode; no filesystem or repository state is changed.",
    )
    return parser


def _report(findings: list[Finding], *, dry_run: bool) -> dict[str, object]:
    return {
        "acceptance_evidence": ACCEPTANCE_EVIDENCE,
        "automation": "EPIC-006_CAPABILITY_CATALOG_CONTROLS",
        "destructive_actions": 0,
        "findings": [finding.as_dict() for finding in findings],
        "mode": "DRY_RUN" if dry_run else "READ_ONLY",
        "requirement_evidence": REQUIREMENT_EVIDENCE,
        "status": "FAIL" if findings else "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        findings = validate(args.repository_root)
    except Exception as error:  # CLI boundary is fail-closed and emits one stable diagnostic.
        findings = [Finding("VALIDATOR_INTERNAL_ERROR", ".", str(error))]
    print(json.dumps(_report(findings, dry_run=args.dry_run), sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
