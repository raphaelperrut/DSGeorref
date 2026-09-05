from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from catalog_contract import CATALOG_PATH, CHECKPOINT_PATH, CORPUS_PATH
from catalog_validation import validate_paths


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the EPIC-006 capability catalog foundation"
    )
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--corpus", type=Path, default=CORPUS_PATH)
    parser.add_argument("--checkpoint", type=Path, default=CHECKPOINT_PATH)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    findings = validate_paths(args.catalog, args.corpus, args.checkpoint)
    report = {
        "catalog": args.catalog.as_posix(),
        "corpus": args.corpus.as_posix(),
        "findings": [asdict(finding) for finding in findings],
        "status": "FAIL" if findings else "PASS",
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 2 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
