from __future__ import annotations

import argparse
import json
from pathlib import Path

from control_validation import EXPECTED_ACCEPTANCE_IDS, EXPECTED_BLOCKERS, Finding, validate

REQUIREMENT_EVIDENCE = {
    "REQ-CIT-001": ["foundation:citation", "test_epic_007_automacao"],
    "REQ-EPIC-042": ["foundation:checkpoint", "test_epic_007_automacao"],
    "REQ-OSS-001": ["foundation:licensing-and-dependencies", "test_epic_007_automacao"],
    "REQ-PUB-002": ["publication-gate-and-dco", "test_epic_007_automacao"],
}
ACCEPTANCE_EVIDENCE = dict.fromkeys(EXPECTED_ACCEPTANCE_IDS, "test_epic_007_automacao")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate EPIC-007 publication governance controls."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[5],
        help="Repository root containing the frozen EPIC-007 foundation.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Assert validation-only mode; no filesystem or repository state is changed.",
    )
    parser.add_argument(
        "--external-commit-range",
        help="External contribution range in base..head form; every commit must carry DCO signoff.",
    )
    return parser


def _report(findings: list[Finding], *, dry_run: bool) -> dict[str, object]:
    gate_decision = "UNVERIFIED" if findings else "BLOCKED"
    return {
        "acceptance_evidence": ACCEPTANCE_EVIDENCE,
        "automation": "EPIC-007_LICENSE_PUBLICATION_GOVERNANCE_CONTROLS",
        "destructive_actions": 0,
        "findings": [finding.as_dict() for finding in findings],
        "mode": "DRY_RUN" if dry_run else "READ_ONLY",
        "publication_gate": {
            "decision": gate_decision,
            "expected_blockers": EXPECTED_BLOCKERS,
            "failure_mode": "FAIL_CLOSED",
        },
        "requirement_evidence": REQUIREMENT_EVIDENCE,
        "status": "FAIL" if findings else "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    findings = validate(
        args.repository_root,
        external_commit_range=args.external_commit_range,
    )
    print(json.dumps(_report(findings, dry_run=args.dry_run), indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
