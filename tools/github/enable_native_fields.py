#!/usr/bin/env python3
"""Audit visibility of Parent issue and Sub-issue progress in Project views.

The public Projects API can read view fields but does not expose a supported
mutation for changing a view's visible fields. This script produces an exact
audit and the minimal UI actions required for each affected view.
"""
from __future__ import annotations

import argparse
import sys
from typing import Any

from dsgeorref_github_common import (
    GovernanceError,
    find_repo_root,
    gh_graphql,
    project_owner_fragment,
    require_gh,
    resolve_project,
    write_json_atomic,
)

REQUIRED_NATIVE_FIELDS = ("Parent issue", "Sub-issue progress")


def get_views(owner: str, owner_type: str, project_number: int) -> list[dict[str, Any]]:
    root = project_owner_fragment(owner_type)
    query = f"""
    query($login: String!, $number: Int!) {{
      {root}(login: $login) {{
        projectV2(number: $number) {{
          id number title
          views(first: 100) {{
            nodes {{
              id number name layout
              fields(first: 100) {{
                nodes {{
                  __typename
                  ... on ProjectV2Field {{ id name }}
                  ... on ProjectV2SingleSelectField {{ id name }}
                  ... on ProjectV2IterationField {{ id name }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """
    data = gh_graphql(query, {"login": owner, "number": project_number})
    project = ((data.get(root) or {}).get("projectV2") or {})
    return [view for view in ((project.get("views") or {}).get("nodes", [])) if view]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--owner-type", choices=("user", "organization"), default="user")
    parser.add_argument("--project-number", type=int, required=True)
    parser.add_argument("--view", action="append", help="Audita somente views com este nome")
    parser.add_argument("--apply", action="store_true", help="Grava o relatório local; não altera a view")
    args = parser.parse_args()

    root_path = find_repo_root()
    require_gh(apply=args.apply)
    project = resolve_project(args.owner, args.owner_type, args.project_number)
    views = get_views(args.owner, args.owner_type, args.project_number)
    selected_names = set(args.view or [])
    if selected_names:
        views = [view for view in views if view.get("name") in selected_names]

    print(f"Project: {project['title']} (#{project['number']})")
    report_views: list[dict[str, Any]] = []
    for view in views:
        visible = {
            field.get("name")
            for field in ((view.get("fields") or {}).get("nodes", []))
            if field and field.get("name")
        }
        missing = [name for name in REQUIRED_NATIVE_FIELDS if name not in visible]
        report_views.append(
            {
                "number": view.get("number"),
                "name": view.get("name"),
                "layout": view.get("layout"),
                "visible_fields": sorted(visible),
                "missing_required_native_fields": missing,
            }
        )
        if missing:
            print(f"VIEW {view.get('number')} — {view.get('name')}: MISSING {', '.join(missing)}")
        else:
            print(f"VIEW {view.get('number')} — {view.get('name')}: OK")

    report = {
        "schema_version": "1.0.0",
        "project": project,
        "required_native_fields": list(REQUIRED_NATIVE_FIELDS),
        "views": report_views,
        "remote_mutation_supported": False,
        "manual_action": (
            "Abra a view em layout Table, clique no + da última coluna, abra Hidden fields "
            "e selecione Parent issue e Sub-issue progress."
        ),
    }
    if args.apply:
        write_json_atomic(root_path / "evidence/github/native-fields-audit.json", report)
        print("Relatório gravado em evidence/github/native-fields-audit.json")

    missing_count = sum(len(view["missing_required_native_fields"]) for view in report_views)
    if missing_count:
        print("\nAção manual por view:")
        print("1. Abra a view em formato Table.")
        print("2. Vá até a última coluna e clique em +.")
        print("3. Abra Hidden fields.")
        print("4. Marque Parent issue e Sub-issue progress.")
        print("5. Salve a view.")
    print(
        "\nNão foi aplicada alteração remota: a API pública atual não expõe mutação "
        "para editar os campos visíveis de uma Project view."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernanceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
