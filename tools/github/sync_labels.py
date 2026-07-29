#!/usr/bin/env python3
"""Create or update the controlled DSGeorref GitHub label taxonomy."""
from __future__ import annotations

import argparse
import sys
from urllib.parse import quote

from dsgeorref_github_common import (
    GovernanceError,
    find_repo_root,
    gh_rest,
    read_json,
    require_gh,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="OWNER/REPOSITORY")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = find_repo_root()
    require_gh(apply=args.apply)
    config = read_json(root / "config/github/labels.json")
    if not config:
        raise GovernanceError("config/github/labels.json não encontrado.")

    current = gh_rest(f"repos/{args.repo}/labels?per_page=100", paginate=True)
    if current and isinstance(current, list) and current and isinstance(current[0], list):
        current = [label for page in current for label in page]
    by_name = {label["name"].casefold(): label for label in (current or [])}

    print(f"MODE: {'APPLY' if args.apply else 'DRY-RUN'}")
    created = updated = unchanged = 0
    for desired in config["labels"]:
        name = desired["name"]
        existing = by_name.get(name.casefold())
        desired_color = desired["color"].lstrip("#").upper()
        desired_description = desired.get("description", "")
        if not existing:
            created += 1
            print(f"CREATE LABEL: {name} #{desired_color}")
            if args.apply:
                gh_rest(
                    f"repos/{args.repo}/labels",
                    method="POST",
                    body={"name": name, "color": desired_color, "description": desired_description},
                )
            continue
        changed = (
            str(existing.get("color", "")).upper() != desired_color
            or (existing.get("description") or "") != desired_description
            or existing.get("name") != name
        )
        if not changed:
            unchanged += 1
            print(f"OK LABEL: {name}")
            continue
        updated += 1
        print(f"UPDATE LABEL: {existing['name']} -> {name} #{desired_color}")
        if args.apply:
            gh_rest(
                f"repos/{args.repo}/labels/{quote(existing['name'], safe='')}",
                method="PATCH",
                body={"new_name": name, "color": desired_color, "description": desired_description},
            )

    print(f"Resumo: create={created}, update={updated}, unchanged={unchanged}")
    if not args.apply:
        print("Nenhuma alteração foi enviada. Acrescente --apply após revisar.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernanceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
