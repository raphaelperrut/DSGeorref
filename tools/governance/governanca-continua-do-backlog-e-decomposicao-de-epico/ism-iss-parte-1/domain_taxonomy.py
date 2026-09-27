from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import cast

from policy_validation import _reject_constant, _strict_object

DOMAIN_CODE = re.compile(r"^[A-Z]{3}$")
EPIC_INDEX = "docs/06-delivery/EPIC_INDEX.csv"
STORY_INDEX = "docs/06-delivery/STORY_INDEX.csv"


def _index_domains(path: Path) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "domain" not in reader.fieldnames:
            raise ValueError(f"DOMAIN_REGISTRY_INVALID: missing domain column in {path}")
        domains = {row.get("domain") for row in reader}
    if not domains or any(
        not isinstance(domain, str) or DOMAIN_CODE.fullmatch(domain) is None for domain in domains
    ):
        raise ValueError(f"DOMAIN_REGISTRY_INVALID: invalid domain code in {path}")
    return cast(set[str], domains)


def load_canonical_domains(registry_path: Path, repository_root: Path) -> set[str]:
    root = repository_root.resolve()
    if not registry_path.resolve().is_relative_to(root):
        raise ValueError("DOMAIN_REGISTRY_INVALID: registry path escapes repository")
    try:
        registry = json.loads(
            registry_path.read_text(encoding="utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
        if not isinstance(registry, dict) or set(registry) != {
            "schema_version",
            "owner",
            "epic_index",
            "story_index",
            "domains",
        }:
            raise ValueError("invalid registry fields")
        if (
            registry["schema_version"] != "1.0.0"
            or registry["owner"] != "BC-001"
            or registry["epic_index"] != EPIC_INDEX
            or registry["story_index"] != STORY_INDEX
        ):
            raise ValueError("invalid registry authority or source")
        domains = registry["domains"]
        if (
            not isinstance(domains, list)
            or not domains
            or any(not isinstance(code, str) for code in domains)
            or domains != sorted(set(domains))
        ):
            raise ValueError("invalid or duplicate domain codes")
        expected = _index_domains(root / EPIC_INDEX)
        if _index_domains(root / STORY_INDEX) != expected or set(domains) != expected:
            raise ValueError("registry diverges from versioned delivery indexes")
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        raise ValueError(f"DOMAIN_REGISTRY_INVALID: {error}") from error
    return set(domains)
