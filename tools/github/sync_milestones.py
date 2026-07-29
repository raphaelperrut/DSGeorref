#!/usr/bin/env python3
"""Create/update milestones and associate materialized DSGeorref issues."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from urllib.parse import quote

from dsgeorref_github_common import (
    GovernanceError,
    find_repo_root,
    gh_rest,
    load_materialized_numbers,
    read_csv,
    read_json,
    require_gh,
    write_json_atomic,
)


def normalized_due(value: str | None) -> str | None:
    if not value:
        return None
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="OWNER/REPOSITORY")
    parser.add_argument("--sprint", action="append", help="Limita associação a uma ou mais sprints")
    parser.add_argument("--max-items", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = find_repo_root()
    require_gh(apply=args.apply)
    config = read_json(root / "config/github/milestones.json")
    if not config:
        raise GovernanceError("config/github/milestones.json não encontrado.")

    existing = gh_rest(f"repos/{args.repo}/milestones?state=all&per_page=100", paginate=True)
    if existing and isinstance(existing, list) and existing and isinstance(existing[0], list):
        existing = [item for page in existing for item in page]
    by_title = {item["title"].casefold(): item for item in (existing or [])}

    print(f"MODE: {'APPLY' if args.apply else 'DRY-RUN'}")
    milestone_numbers: dict[str, int] = {}
    for desired in config["milestones"]:
        title = desired["title"]
        current = by_title.get(title.casefold())
        body = {
            "title": title,
            "description": desired.get("description", ""),
            "state": desired.get("state", "open"),
            "due_on": normalized_due(desired.get("due_on")),
        }
        if current is None:
            print(f"CREATE MILESTONE: {title}")
            if args.apply:
                created = gh_rest(f"repos/{args.repo}/milestones", method="POST", body=body)
                milestone_numbers[title] = int(created["number"])
            continue
        milestone_numbers[title] = int(current["number"])
        changed = any(
            [
                (current.get("description") or "") != body["description"],
                current.get("state") != body["state"],
                normalized_due(current.get("due_on")) != body["due_on"],
                current.get("title") != title,
            ]
        )
        if changed:
            print(f"UPDATE MILESTONE: {title} (#{current['number']})")
            if args.apply:
                gh_rest(
                    f"repos/{args.repo}/milestones/{current['number']}",
                    method="PATCH",
                    body=body,
                )
        else:
            print(f"OK MILESTONE: {title} (#{current['number']})")

    if not args.apply:
        # Stable placeholder numbers are enough for the plan output.
        for title, current in by_title.items():
            milestone_numbers[current["title"]] = int(current["number"])

    sprint_map = config.get("sprint_map", {})
    allowed = set(args.sprint or sprint_map.keys())
    unknown = allowed - set(sprint_map)
    if unknown:
        raise GovernanceError(
            "Sprints sem mapeamento em config/github/milestones.json: " + ", ".join(sorted(unknown))
        )

    issue_rows = {row["issue_id"]: row for row in read_csv(root / "docs/06-delivery/ISSUE_INDEX.csv")}
    numbers = load_materialized_numbers(root / ".github/dsgeorref-materialization-map.json")
    state_path = root / ".github/dsgeorref-milestone-sync.json"
    state = read_json(state_path, default={}) or {"schema_version": "1.0.0", "synced": {}}
    state.setdefault("synced", {})

    pending: list[tuple[str, int, str, str]] = []
    for issue_id, number in sorted(numbers.items(), key=lambda pair: pair[1]):
        row = issue_rows.get(issue_id)
        if not row or row.get("sprint") not in allowed:
            continue
        milestone_title = sprint_map[row["sprint"]]
        digest = hashlib.sha256(
            f"{issue_id}|{number}|{row['sprint']}|{milestone_title}".encode("utf-8")
        ).hexdigest()
        if not args.force and state["synced"].get(issue_id) == digest:
            continue
        pending.append((issue_id, number, milestone_title, digest))
    if args.max_items > 0:
        pending = pending[: args.max_items]

    print(f"Pending milestone associations: {len(pending)}")
    for issue_id, number, title, digest in pending:
        milestone_number = milestone_numbers.get(title)
        if milestone_number is None and args.apply:
            raise GovernanceError(f"Milestone `{title}` não foi resolvido.")
        print(f"ASSOCIATE: {issue_id} (#{number}) -> {title}")
        if args.apply:
            gh_rest(
                f"repos/{args.repo}/issues/{number}",
                method="PATCH",
                body={"milestone": milestone_number},
            )
            state["synced"][issue_id] = digest
            write_json_atomic(state_path, state)

    if not args.apply:
        print("Nenhuma alteração foi enviada. Acrescente --apply após revisar.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernanceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
