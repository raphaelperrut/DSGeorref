#!/usr/bin/env python3
"""Install Actions-based Project status automation and audit built-in workflows.

GitHub's public API does not expose a supported mutation to create or edit the
built-in Project workflows. This tool therefore:
  1. audits built-in workflows;
  2. installs a repository Actions workflow for issue opened/reopened/closed;
  3. optionally sets repository variables;
  4. prints the exact built-in workflows that still require UI activation.

The --runtime mode is called by the installed Actions workflow.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from dsgeorref_github_common import (
    GovernanceError,
    add_project_item,
    find_repo_root,
    get_project_fields,
    get_project_items,
    gh_graphql,
    project_owner_fragment,
    read_json,
    require_gh,
    resolve_project,
    run_command,
    write_json_atomic,
)

WORKFLOW = """name: dsgeorref-project-automation

on:
  issues:
    types: [opened, reopened, closed]
  workflow_dispatch:

permissions:
  contents: read
  issues: read

jobs:
  synchronize-project-status:
    runs-on: ubuntu-latest
    env:
      GH_TOKEN: ${{ secrets.DSGEO_PROJECT_TOKEN }}
      DSGEO_PROJECT_OWNER: ${{ vars.DSGEO_PROJECT_OWNER }}
      DSGEO_PROJECT_OWNER_TYPE: ${{ vars.DSGEO_PROJECT_OWNER_TYPE }}
      DSGEO_PROJECT_NUMBER: ${{ vars.DSGEO_PROJECT_NUMBER }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Synchronize issue with Project
        run: python tools/github/configure_project_automations.py --runtime
"""

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
    return [node for node in (((data.get("node") or {}).get("workflows") or {}).get("nodes", [])) if node]


def set_repo_variable(repo: str, name: str, value: str) -> None:
    run_command(["gh", "variable", "set", name, "--repo", repo, "--body", value])


def update_status(project_id: str, item_id: str, field_id: str, option_id: str) -> None:
    mutation = """
    mutation($project: ID!, $item: ID!, $field: ID!, $option: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $project,
        itemId: $item,
        fieldId: $field,
        value: {singleSelectOptionId: $option}
      }) { projectV2Item { id } }
    }
    """
    gh_graphql(
        mutation,
        {"project": project_id, "item": item_id, "field": field_id, "option": option_id},
    )


def runtime() -> int:
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        raise GovernanceError("GITHUB_EVENT_PATH não está definido.")
    event = read_json(Path(event_path), default={}) or {}
    issue = event.get("issue")
    if not issue:
        print("workflow_dispatch sem issue: nenhuma alteração necessária.")
        return 0

    repo = os.getenv("GITHUB_REPOSITORY", "")
    owner = os.getenv("DSGEO_PROJECT_OWNER", "")
    owner_type = os.getenv("DSGEO_PROJECT_OWNER_TYPE", "user")
    raw_number = os.getenv("DSGEO_PROJECT_NUMBER", "")
    if not all((repo, owner, raw_number)):
        raise GovernanceError(
            "Configure DSGEO_PROJECT_OWNER, DSGEO_PROJECT_OWNER_TYPE e "
            "DSGEO_PROJECT_NUMBER como repository variables."
        )
    try:
        project_number = int(raw_number)
    except ValueError as exc:
        raise GovernanceError("DSGEO_PROJECT_NUMBER deve ser inteiro.") from exc

    action = event.get("action")
    desired_status = {"opened": "Backlog", "reopened": "Backlog", "closed": "Done"}.get(action)
    if not desired_status:
        print(f"Ação `{action}` não requer sincronização.")
        return 0

    project = resolve_project(owner, owner_type, project_number)
    fields = get_project_fields(project["id"])
    status_field = next((field for field in fields if field.get("name") == "Status"), None)
    if not status_field or status_field.get("__typename") != "ProjectV2SingleSelectField":
        raise GovernanceError("Campo single-select `Status` não encontrado no Project.")
    options = {option["name"]: option["id"] for option in status_field.get("options", [])}
    option_id = options.get(desired_status)
    if not option_id:
        raise GovernanceError(f"Status `{desired_status}` não existe no Project.")

    issue_node_id = issue.get("node_id")
    issue_number = int(issue["number"])
    project_items = get_project_items(project["id"])
    item_id = None
    for item in project_items:
        content = item.get("content") or {}
        if content.get("id") == issue_node_id:
            item_id = item["id"]
            break
    if not item_id:
        item_id = add_project_item(project["id"], issue_node_id)
        print(f"Issue #{issue_number} adicionada ao Project.")
    update_status(project["id"], item_id, status_field["id"], option_id)
    print(f"Issue #{issue_number}: Status = {desired_status}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--repo", help="OWNER/REPOSITORY")
    parser.add_argument("--owner", help="Owner do Project")
    parser.add_argument("--owner-type", choices=("user", "organization"), default="user")
    parser.add_argument("--project-number", type=int)
    parser.add_argument("--install-actions-workflow", action="store_true")
    parser.add_argument("--set-variables", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if args.runtime:
        return runtime()
    if not args.repo or not args.owner or args.project_number is None:
        parser.error("--repo, --owner e --project-number são obrigatórios fora de --runtime")

    root = find_repo_root()
    require_gh(apply=args.apply)
    project = resolve_project(args.owner, args.owner_type, args.project_number)
    workflows = audit_workflows(project["id"])

    print(f"MODE: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Project: {project['title']} (#{project['number']})")
    print("Built-in workflows detectados:")
    if workflows:
        for workflow in workflows:
            print(f"- #{workflow.get('number')} {workflow.get('name')}: enabled={workflow.get('enabled')}")
    else:
        print("- nenhum workflow retornado pela API")

    workflow_path = root / ".github/workflows/project-automation.yml"
    if args.install_actions_workflow:
        print(f"WRITE: {workflow_path.relative_to(root)}")
        if args.apply:
            workflow_path.parent.mkdir(parents=True, exist_ok=True)
            workflow_path.write_text(WORKFLOW, encoding="utf-8")

    if args.set_variables:
        for name, value in (
            ("DSGEO_PROJECT_OWNER", args.owner),
            ("DSGEO_PROJECT_OWNER_TYPE", args.owner_type),
            ("DSGEO_PROJECT_NUMBER", str(args.project_number)),
        ):
            print(f"SET VARIABLE: {name}={value}")
            if args.apply:
                set_repo_variable(args.repo, name, value)

    report = {
        "schema_version": "1.0.0",
        "project": project,
        "built_in_workflows": workflows,
        "manual_workflows_required": MANUAL_WORKFLOWS,
        "actions_workflow": str(workflow_path.relative_to(root)),
    }
    if args.apply:
        write_json_atomic(root / "evidence/github/project-workflows-audit.json", report)

    print("\nConfiguração manual ainda obrigatória em Project → … → Workflows:")
    for item in MANUAL_WORKFLOWS:
        print(f"- {item}")
    print(
        "\nA API pública permite consultar/remover workflows, mas não oferece uma mutação "
        "suportada para criar/editar esses workflows built-in."
    )
    if args.install_actions_workflow:
        print(
            "\nAntes de executar o workflow, cadastre o secret DSGEO_PROJECT_TOKEN com "
            "um classic PAT que tenha scopes project e repo."
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernanceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
