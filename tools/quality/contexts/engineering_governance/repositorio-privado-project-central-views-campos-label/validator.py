from __future__ import annotations

import argparse
import sys
from pathlib import Path

from artifact_validation import validate_bundles, validate_ownership
from contract_catalog import BUNDLES, EXPECTED_OWNER, EXPECTED_VERSION, OWNERSHIP_REL
from semantic_validation import validate_semantics
from validation_types import Finding


def validate(repository_root: Path) -> list[Finding]:
    root = repository_root.resolve()
    documents, findings = validate_bundles(root)
    findings.extend(validate_ownership(root))
    findings.extend(validate_semantics(root, documents))
    return sorted(set(findings))


def _requirement_count(repository_root: Path) -> int:
    documents, _findings = validate_bundles(repository_root.resolve())
    return sum(len(documents[name].manifest["requirements"]) for name in ("foundation", "worker"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the frozen EPIC-002 engineering governance contracts read-only."
    )
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicitly assert validation-only mode; no filesystem or GitHub state is changed.",
    )
    args = parser.parse_args(argv)
    findings = validate(args.repository_root)
    mode = "DRY_RUN" if args.dry_run else "READ_ONLY"
    if findings:
        print(f"VALIDATION FAILED ({len(findings)} finding(s))")
        print(f"mode={mode} destructive_actions=0")
        for finding in findings:
            print(f"ERROR [{finding.code}] {finding.artifact} :: {finding.detail}")
        return 1
    print("VALIDATION PASS")
    print(f"mode={mode} destructive_actions=0")
    print(f"bundles={','.join(bundle.name for bundle in BUNDLES)} version={EXPECTED_VERSION}")
    print(f"requirements={_requirement_count(args.repository_root)}")
    print(f"ownership={OWNERSHIP_REL.as_posix()} owner={EXPECTED_OWNER}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
