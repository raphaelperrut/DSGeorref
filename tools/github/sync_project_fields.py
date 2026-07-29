#!/usr/bin/env python3
"""Create/validate DSGeorref Project fields and populate materialized issues.

Dry-run is the default. Use --apply to write. The script reads the canonical SAR
indexes plus .github/dsgeorref-materialization-map.json. It is resumable and
stores hashes in .github/dsgeorref-project-field-sync.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from dsgeorref_github_common import (
    GovernanceError,
    add_project_item,
    find_repo_root,
    get_issue_node_id,
    get_project_fields,
    get_project_items,
    gh_graphql,
    load_materialized_numbers,
    read_csv,
    read_json,
    require_gh,
    resolve_project,
    write_json_atomic,
)

STATUS_MAP = {
    "planned": "Backlog",
    "backlog": "Backlog",
    "ready": "Ready",
    "in-progress": "In progress",
    "in_progress": "In progress",
    "in-review": "In review",
    "blocked": "Blocked",
    "blocked-external": "Blocked",
    "done": "Done",
    "closed": "Done",
    "canceled": "Canceled",
    "cancelled": "Canceled",
}


def normalize_gate(raw: str) -> str:
    """Use the highest exit gate when an epic is governed by more than one gate."""
    gates = re.findall(r"G[0-7]", raw or "")
    return max(gates, key=lambda value: int(value[1:])) if gates else ""


def canonical_values(root: Path, overrides_path: Path) -> dict[str, dict[str, str]]:
    issue_rows = read_csv(root / "docs/06-delivery/ISSUE_INDEX.csv")
    epic_rows = read_csv(root / "docs/06-delivery/EPIC_INDEX.csv")
    story_rows = read_csv(root / "docs/06-delivery/STORY_INDEX.csv")

    gate_by_epic = {row["epic_id"]: normalize_gate(row.get("gate", "")) for row in epic_rows}
    story_by_issue = {row["issue_id"]: row for row in story_rows}
    overrides: dict[str, dict[str, str]] = {}
    if overrides_path.exists():
        overrides = {row["issue_id"]: row for row in read_csv(overrides_path) if row.get("issue_id")}

    values: dict[str, dict[str, str]] = {}
    for row in issue_rows:
        issue_id = row["issue_id"]
        story = story_by_issue.get(issue_id)
        override = overrides.get(issue_id, {})
        work_type = "Epic" if row.get("type", "").lower().startswith("epic") else "Story"
        task_id = (story or {}).get("task_id", "")
        values[issue_id] = {
            "Stable ID": issue_id,
            "Work Type": work_type,
            "Planned Sprint": row.get("sprint", ""),
            "Priority": override.get("priority", "").strip(),
            "Gate": gate_by_epic.get(row.get("epic_id", ""), ""),
            "Bounded Context": row.get("bounded_context", ""),
            "Owner Role": row.get("owner_role", ""),
            "Risk Tier": row.get("cto_risk_tier", ""),
            "Size": override.get("size", "").strip(),
            "ADR IDs": row.get("governing_adrs", ""),
            "TaskEnvelope": f".codex/tasks/{task_id}.json" if task_id else "",
            "Status": STATUS_MAP.get(row.get("status", "").strip().lower(), ""),
        }
    return values


def create_field(project_id: str, spec: dict[str, Any]) -> None:
    mutation = """
    mutation($input: CreateProjectV2FieldInput!) {
      createProjectV2Field(input: $input) {
        projectV2Field {
          __typename
          ... on ProjectV2Field { id name dataType }
          ... on ProjectV2SingleSelectField { id name dataType options { id name } }
        }
      }
    }
    """
    field_input: dict[str, Any] = {
        "projectId": project_id,
        "name": spec["name"],
        "dataType": spec["data_type"],
    }
    if spec["data_type"] == "SINGLE_SELECT":
        field_input["singleSelectOptions"] = [
            {
                "name": option["name"],
                "description": option.get("description", ""),
                "color": option.get("color", "GRAY"),
            }
            for option in spec.get("options", [])
        ]
    gh_graphql(mutation, {"input": field_input})


def merged_single_select_options(
    field: dict[str, Any],
    spec: dict[str, Any],
) -> list[dict[str, str]]:
    """Merge configured options while preserving IDs and unknown existing options.

    updateProjectV2Field replaces the complete option list. Existing option IDs
    must therefore be sent back to GitHub or item values using those options may
    be cleared.
    """
    configured = {option["name"]: option for option in spec.get("options", [])}
    merged: list[dict[str, str]] = []
    seen: set[str] = set()

    for existing in field.get("options", []):
        name = existing["name"]
        desired = configured.get(name, {})
        merged.append(
            {
                "id": existing["id"],
                "name": name,
                "description": desired.get(
                    "description", existing.get("description", "") or ""
                ),
                "color": desired.get("color", existing.get("color", "GRAY") or "GRAY"),
            }
        )
        seen.add(name)

    for option in spec.get("options", []):
        if option["name"] in seen:
            continue
        merged.append(
            {
                "name": option["name"],
                "description": option.get("description", ""),
                "color": option.get("color", "GRAY"),
            }
        )
    return merged


def update_single_select_field_options(
    field: dict[str, Any],
    spec: dict[str, Any],
) -> None:
    mutation = """
    mutation($input: UpdateProjectV2FieldInput!) {
      updateProjectV2Field(input: $input) {
        projectV2Field {
          __typename
          ... on ProjectV2SingleSelectField { id name options { id name } }
        }
      }
    }
    """
    gh_graphql(
        mutation,
        {
            "input": {
                "fieldId": field["id"],
                "singleSelectOptions": merged_single_select_options(field, spec),
            }
        },
    )


def update_item_fields(
    project_id: str,
    item_id: str,
    desired: dict[str, str],
    fields_by_name: dict[str, dict[str, Any]],
) -> None:
    declarations = ["$project: ID!", "$item: ID!"]
    operations: list[str] = []
    variables: dict[str, Any] = {"project": project_id, "item": item_id}
    index = 0
    for name, value in desired.items():
        if not value:
            continue
        field = fields_by_name[name]
        field_id_var = f"field{index}"
        value_var = f"value{index}"
        declarations.extend([f"${field_id_var}: ID!", f"${value_var}: String!"])
        variables[field_id_var] = field["id"]
        if field.get("__typename") == "ProjectV2SingleSelectField":
            options = {option["name"]: option["id"] for option in field.get("options", [])}
            option_id = options.get(value)
            if not option_id:
                raise GovernanceError(
                    f"Campo `{name}` não possui a opção `{value}`. "
                    "Edite as opções no Project antes de reaplicar."
                )
            variables[value_var] = option_id
            value_expression = f"{{singleSelectOptionId: ${value_var}}}"
        else:
            variables[value_var] = value
            value_expression = f"{{text: ${value_var}}}"
        operations.append(
            f"u{index}: updateProjectV2ItemFieldValue(input: {{"
            f"projectId: $project, itemId: $item, fieldId: ${field_id_var}, "
            f"value: {value_expression}}}) {{ projectV2Item {{ id }} }}"
        )
        index += 1
    if not operations:
        return
    mutation = "mutation(" + ", ".join(declarations) + ") {\n" + "\n".join(operations) + "\n}"
    gh_graphql(mutation, variables)


def value_hash(values: dict[str, str]) -> str:
    raw = json.dumps(values, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="OWNER/REPOSITORY")
    parser.add_argument("--owner", required=True, help="Owner do Project")
    parser.add_argument("--owner-type", choices=("user", "organization"), default="user")
    parser.add_argument("--project-number", type=int, required=True)
    parser.add_argument("--sprint", action="append", help="Limita a uma ou mais sprints")
    parser.add_argument("--max-items", type=int, default=0, help="Máximo por execução; 0 = todos")
    parser.add_argument("--create-missing-fields", action="store_true")
    parser.add_argument(
        "--sync-field-options",
        action="store_true",
        help="Acrescenta opções ausentes preservando IDs e opções já existentes",
    )
    parser.add_argument("--add-missing-items", action="store_true")
    parser.add_argument("--force", action="store_true", help="Ignora hashes do checkpoint")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = find_repo_root()
    require_gh(apply=args.apply)
    config_path = root / "config/github/project_fields.json"
    overrides_path = root / "config/github/project_field_overrides.csv"
    materialization_path = root / ".github/dsgeorref-materialization-map.json"
    state_path = root / ".github/dsgeorref-project-field-sync.json"

    config = read_json(config_path)
    if not config:
        raise GovernanceError(f"Configuração ausente: {config_path.relative_to(root)}")
    specs = {field["name"]: field for field in config["fields"]}
    canonical = canonical_values(root, overrides_path)
    numbers = load_materialized_numbers(materialization_path)
    state = read_json(state_path, default={}) or {}
    state.setdefault("schema_version", "1.0.0")
    state.setdefault("synced", {})

    selected: list[str] = []
    allowed_sprints = set(args.sprint or [])
    for issue_id, number in sorted(numbers.items(), key=lambda pair: pair[1]):
        values = canonical.get(issue_id)
        if not values:
            print(f"AVISO: {issue_id} está no mapa, mas não no ISSUE_INDEX.csv.", file=sys.stderr)
            continue
        if allowed_sprints and values["Planned Sprint"] not in allowed_sprints:
            continue
        selected.append(issue_id)

    project = resolve_project(args.owner, args.owner_type, args.project_number)
    print(f"MODE: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Project: {project['title']} (#{project['number']})")
    print(f"Materialized issues selected: {len(selected)}")

    current_fields = get_project_fields(project["id"])
    fields_by_name = {field.get("name"): field for field in current_fields if field.get("name")}
    missing = [spec for name, spec in specs.items() if name not in fields_by_name]
    for spec in missing:
        if not spec.get("create", False):
            raise GovernanceError(
                f"Campo nativo/obrigatório ausente: `{spec['name']}`. Crie-o ou restaure-o no Project."
            )
        print(f"CREATE FIELD: {spec['name']} ({spec['data_type']})")
        if args.apply:
            if not args.create_missing_fields:
                raise GovernanceError(
                    f"Campo `{spec['name']}` ausente. Reexecute com --create-missing-fields --apply."
                )
            create_field(project["id"], spec)

    if args.apply and missing:
        current_fields = get_project_fields(project["id"])
        fields_by_name = {field.get("name"): field for field in current_fields if field.get("name")}

    for name, spec in specs.items():
        field = fields_by_name.get(name)
        if not field:
            continue
        expected_type = spec["data_type"]
        actual_type = field.get("dataType")
        if actual_type and actual_type != expected_type:
            raise GovernanceError(
                f"Campo `{name}` tem tipo {actual_type}, mas o pacote exige {expected_type}."
            )

    # Synchronize missing single-select options before the first item mutation.
    # GitHub replaces the entire list in updateProjectV2Field, therefore the
    # helper preserves all existing option IDs and unknown custom options.
    option_updates: list[tuple[str, dict[str, Any], dict[str, Any], list[str]]] = []
    for name, spec in specs.items():
        field = fields_by_name.get(name)
        if not field or field.get("__typename") != "ProjectV2SingleSelectField":
            continue
        available = {option["name"] for option in field.get("options", [])}
        configured_names = {option["name"] for option in spec.get("options", [])}
        required = {canonical[issue_id].get(name, "") for issue_id in selected}
        required.discard("")
        missing_required = sorted(required - available)
        missing_configured = sorted(configured_names - available)
        if missing_required or missing_configured:
            option_updates.append((name, field, spec, missing_configured))
            print(
                f"UPDATE FIELD OPTIONS: {name} (+{', '.join(missing_configured)})"
            )

    if option_updates and args.apply:
        if not args.sync_field_options:
            details = "\n- ".join(
                f"{name}: {', '.join(missing)}"
                for name, _field, _spec, missing in option_updates
            )
            raise GovernanceError(
                "Opções single-select ausentes no Project:\n- "
                + details
                + "\nReexecute com --sync-field-options --apply para acrescentá-las "
                "preservando as opções e IDs atuais."
            )
        for name, field, spec, _missing in option_updates:
            update_single_select_field_options(field, spec)
            print(f"UPDATED FIELD OPTIONS: {name}")
        current_fields = get_project_fields(project["id"])
        fields_by_name = {
            field.get("name"): field for field in current_fields if field.get("name")
        }

    # Final validation. In dry-run the missing options are planned but not sent.
    if args.apply:
        option_errors: list[str] = []
        for name, field in fields_by_name.items():
            if field.get("__typename") != "ProjectV2SingleSelectField":
                continue
            available = {option["name"] for option in field.get("options", [])}
            required = {canonical[issue_id].get(name, "") for issue_id in selected}
            required.discard("")
            missing_options = sorted(required - available)
            if missing_options:
                option_errors.append(f"{name}: {', '.join(missing_options)}")
        if option_errors:
            raise GovernanceError(
                "Opções single-select continuam ausentes após a sincronização:\n- "
                + "\n- ".join(option_errors)
            )

    items = get_project_items(project["id"])
    repo_key = args.repo.casefold()
    items_by_number: dict[int, str] = {}
    for item in items:
        content = item.get("content") or {}
        repository = ((content.get("repository") or {}).get("nameWithOwner") or "").casefold()
        number = content.get("number")
        if repository == repo_key and isinstance(number, int):
            items_by_number[number] = item["id"]

    pending: list[tuple[str, int, dict[str, str], str]] = []
    for issue_id in selected:
        desired = canonical[issue_id]
        digest = value_hash(desired)
        if not args.force and state["synced"].get(issue_id) == digest:
            continue
        pending.append((issue_id, numbers[issue_id], desired, digest))
    if args.max_items > 0:
        pending = pending[: args.max_items]
    print(f"Pending field sync in this batch: {len(pending)}")

    for issue_id, number, desired, digest in pending:
        item_id = items_by_number.get(number)
        if not item_id:
            print(f"ADD PROJECT ITEM: {issue_id} (#{number})")
            if not args.apply:
                continue
            if not args.add_missing_items:
                raise GovernanceError(
                    f"{issue_id} (#{number}) não está no Project. "
                    "Reexecute com --add-missing-items --apply."
                )
            issue_node_id = get_issue_node_id(args.repo, number)
            item_id = add_project_item(project["id"], issue_node_id)
            items_by_number[number] = item_id

        rendered = ", ".join(f"{key}={value}" for key, value in desired.items() if value)
        print(f"SYNC {issue_id} (#{number}): {rendered}")
        if args.apply:
            update_item_fields(project["id"], item_id, desired, fields_by_name)
            state["project"] = {
                "id": project["id"],
                "number": project["number"],
                "owner": args.owner,
                "owner_type": args.owner_type,
            }
            state["synced"][issue_id] = digest
            write_json_atomic(state_path, state)

    print("Concluído.")
    if not args.apply:
        print("Nenhuma alteração foi enviada. Acrescente --apply após revisar o plano.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernanceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
