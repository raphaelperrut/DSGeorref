from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from artifact_validation import ACCEPTANCE_EVIDENCE, REQUIREMENT_TESTS, validate_repository
from validation_types import Finding


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate EPIC-003 foundation controls deterministically and read-only."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[5],
        help="Repository root containing the frozen EPIC-003 foundation artifacts.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Assert validation-only mode; no filesystem, service, or repository state is changed.",
    )
    return parser


def _report(findings: list[Finding], *, dry_run: bool) -> dict[str, object]:
    return {
        "acceptance_criteria": sorted(ACCEPTANCE_EVIDENCE),
        "automation": "EPIC-003_FOUNDATION_CONTROLS",
        "destructive_actions": 0,
        "findings": [finding.as_dict() for finding in findings],
        "mode": "DRY_RUN" if dry_run else "READ_ONLY",
        "requirements": sorted(REQUIREMENT_TESTS),
        "status": "FAIL" if findings else "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        findings = validate_repository(args.repository_root)
    except Exception as error:  # CLI boundary: never fail open or emit a traceback.
        findings = [Finding("VALIDATOR_INTERNAL_ERROR", ".", str(error))]
    print(json.dumps(_report(findings, dry_run=args.dry_run), ensure_ascii=False, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
