#!/usr/bin/env python3
"""Audit GitHub Project built-in workflows and print manual setup guidance.

GitHub's public API does not expose a supported mutation to create or edit the
built-in Project workflows. This tool therefore audits the current workflows
and prints the exact built-in workflows that still require UI activation.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

from dsgeorref_github_common import (
    GovernanceError,
    find_repo_root,
    gh_graphql,
    require_gh,
    resolve_project,
    write_json_atomic,
)

MANUAL_WORKFLOWS = [
    "Item added to project → Status = Backlog",
    "Issue closed → Status = Done",
    "Issue reopened → Status = Backlog",
    "Status changed to Done → close issue",
    "Auto-add items matching repository raphaelperrut/DSGeorref",
    "Auto-archive completed items after the retention period you choose",
]


def audit_workflows(project_id: str) -> list[dict[str, Any]]:
    query = """
    query($id: ID!) {
      node(id: $id) {
        ... on ProjectV2 {
          workflows(first: 100) {
            nodes { id name number enabled }
          }
        }
      }
    }
    """
    data = gh_graphql(query, {"id": project_id})
    return [
        node
        for node in (((data.get("node") or {}).get("workflows") or {}).get("nodes", []))
        if node
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", help="Owner do Project")
    parser.add_argument("--owner-type", choices=("user", "organization"), default="user")
    parser.add_argument("--project-number", type=int)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Persiste o relatório de auditoria em evidence/github/.",
    )
    args = parser.parse_args()

    if not args.owner or args.project_number is None:
        parser.error("--owner e --project-number são obrigatórios")

    root = find_repo_root()
    require_gh(apply=args.apply)
    project = resolve_project(args.owner, args.owner_type, args.project_number)
    workflows = audit_workflows(project["id"])

    print(f"MODE: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Project: {project['title']} (#{project['number']})")
    print("Built-in workflows detectados:")
    if workflows:
        for workflow in workflows:
            print(
                f"- #{workflow.get('number')} {workflow.get('name')}: "
                f"enabled={workflow.get('enabled')}"
            )
    else:
        print("- nenhum workflow retornado pela API")

    report = {
        "schema_version": "1.0.0",
        "project": project,
        "built_in_workflows": workflows,
        "manual_workflows_required": MANUAL_WORKFLOWS,
    }
    if args.apply:
        write_json_atomic(root / "evidence/github/project-workflows-audit.json", report)

    print("\nConfiguração manual ainda obrigatória em Project → … → Workflows:")
    for item in MANUAL_WORKFLOWS:
        print(f"- {item}")
    print(
        "\nA API pública permite consultar workflows, mas não oferece uma mutação "
        "suportada para criar/editar esses workflows built-in."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernanceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from None
