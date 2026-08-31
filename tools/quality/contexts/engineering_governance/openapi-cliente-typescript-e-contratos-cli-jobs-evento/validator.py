from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from artifact_validation import validate_contracts
from registry_validation import REGISTERED_CONTRACTS
from repository_validation import ACCEPTANCE_EVIDENCE, validate_repository_controls
from validation_types import Finding


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate EPIC-004 versioned contract controls deterministically and read-only."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[5],
        help="Repository root containing the frozen EPIC-004 contract packages.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Assert validation-only mode; no filesystem or repository state is changed.",
    )
    return parser


def _report(
    findings: list[Finding], requirements: list[str], *, dry_run: bool
) -> dict[str, object]:
    return {
        "acceptance_criteria": sorted(ACCEPTANCE_EVIDENCE),
        "automation": "EPIC-004_VERSIONED_CONTRACT_CONTROLS",
        "contracts": sorted(REGISTERED_CONTRACTS),
        "destructive_actions": 0,
        "findings": [finding.as_dict() for finding in findings],
        "mode": "DRY_RUN" if dry_run else "READ_ONLY",
        "requirements": requirements,
        "status": "FAIL" if findings else "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        findings, requirements = validate_contracts(args.repository_root)
        findings = sorted(set(findings + validate_repository_controls(args.repository_root)))
    except Exception as error:  # CLI boundary: fail closed without leaking a traceback.
        findings = [Finding("VALIDATOR_INTERNAL_ERROR", ".", str(error))]
        requirements = []
    print(
        json.dumps(
            _report(findings, requirements, dry_run=args.dry_run),
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
