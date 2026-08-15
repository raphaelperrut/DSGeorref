#!/usr/bin/env python3
"""Shared GitHub helpers for the DSGeorref governance tooling.

Only the Python standard library and GitHub CLI are required.
"""
from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

TRANSIENT_MARKERS = (
    "dial tcp",
    "timed out",
    "timeout",
    "connection reset",
    "connection attempt failed",
    "temporarily unavailable",
    "502 bad gateway",
    "503 service unavailable",
    "504 gateway timeout",
    "secondary rate limit",
)


class GovernanceError(RuntimeError):
    """Raised when a safe governance precondition is not satisfied."""


def find_repo_root(start: Path | None = None) -> Path:
    """Find a DSGeorref repository root from the current path or this file."""
    candidates: list[Path] = []
    for initial in (start or Path.cwd(), Path(__file__).resolve()):
        current = initial if initial.is_dir() else initial.parent
        candidates.extend([current, *current.parents])
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if (resolved / "docs/06-delivery/ISSUE_INDEX.csv").is_file():
            return resolved
    raise GovernanceError(
        "Não foi possível localizar a raiz do DSGeorref. Execute o script dentro do "
        "repositório que contém docs/06-delivery/ISSUE_INDEX.csv."
    )


def require_gh(*, apply: bool = False) -> None:
    if shutil.which("gh") is None:
        raise GovernanceError("GitHub CLI (`gh`) não está instalado ou não está no PATH.")
    if apply:
        result = run_command(["gh", "auth", "status"], check=False, retries=1)
        if result.returncode != 0:
            raise GovernanceError(
                "GitHub CLI não está autenticado. Execute `gh auth login`.\n"
                + (result.stderr or result.stdout)
            )


def run_command(
    args: list[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
    check: bool = True,
    retries: int = 5,
    capture: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a command with retry for transient GitHub/network failures."""
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    last: subprocess.CompletedProcess[str] | None = None
    for attempt in range(1, retries + 1):
        last = subprocess.run(
            args,
            cwd=cwd,
            input=input_text,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=capture,
            env=merged_env,
            check=False,
        )
        if last.returncode == 0:
            return last
        combined = ((last.stderr or "") + "\n" + (last.stdout or "")).lower()
        transient = any(marker in combined for marker in TRANSIENT_MARKERS)
        if not transient or attempt == retries:
            break
        delay = min(2 ** attempt, 30)
        print(
            f"AVISO: falha transitória (tentativa {attempt}/{retries}); "
            f"nova tentativa em {delay}s.",
            file=sys.stderr,
        )
        time.sleep(delay)
    assert last is not None
    if check:
        raise GovernanceError(
            f"Comando falhou ({last.returncode}): {' '.join(args)}\n"
            + (last.stderr or last.stdout or "sem saída")
        )
    return last


def gh_graphql(query: str, variables: dict[str, Any]) -> dict[str, Any]:
    """Execute GraphQL through `gh api graphql` using JSON input."""
    payload = json.dumps({"query": query, "variables": variables}, ensure_ascii=False)
    result = run_command(
        ["gh", "api", "graphql", "--input", "-"],
        input_text=payload,
        retries=5,
    )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise GovernanceError(f"Resposta GraphQL inválida: {exc}\n{result.stdout}") from exc
    if data.get("errors"):
        raise GovernanceError(
            "GraphQL retornou erros:\n" + json.dumps(data["errors"], ensure_ascii=False, indent=2)
        )
    return data.get("data", {})


def gh_rest(
    endpoint: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    paginate: bool = False,
) -> Any:
    """Execute a REST request through `gh api`."""
    cmd = ["gh", "api", "--method", method]
    if paginate:
        cmd.extend(["--paginate", "--slurp"])
    if body is not None:
        cmd.extend(["--input", "-"])
    cmd.append(endpoint)
    result = run_command(
        cmd,
        input_text=json.dumps(body, ensure_ascii=False) if body is not None else None,
        retries=5,
    )
    if not result.stdout.strip():
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise GovernanceError(f"Resposta REST inválida: {exc}\n{result.stdout}") from exc


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path, *, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GovernanceError(f"JSON inválido em {path}: {exc}") from exc


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        delete=False,
        dir=path.parent,
        suffix=".tmp",
    ) as handle:
        json.dump(
            value,
            handle,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        handle.write("\n")
        temporary = Path(handle.name)

    try:
        attempts = 7

        for attempt in range(attempts):
            try:
                temporary.replace(path)
                return
            except PermissionError:
                if attempt == attempts - 1:
                    raise

                delay = min(0.2 * (2 ** attempt), 2.0)
                time.sleep(delay)
    finally:
        if temporary.exists():
            try:
                temporary.unlink()
            except OSError:
                pass


def parse_repo(repo: str) -> tuple[str, str]:
    parts = repo.strip().split("/")
    if len(parts) != 2 or not all(parts):
        raise GovernanceError("Use --repo no formato OWNER/REPOSITORY.")
    return parts[0], parts[1]


def project_owner_fragment(owner_type: str) -> str:
    if owner_type == "user":
        return "user"
    if owner_type == "organization":
        return "organization"
    raise GovernanceError("--owner-type deve ser `user` ou `organization`.")


def resolve_project(owner: str, owner_type: str, project_number: int) -> dict[str, Any]:
    root = project_owner_fragment(owner_type)
    query = f"""
    query($login: String!, $number: Int!) {{
      {root}(login: $login) {{
        projectV2(number: $number) {{ id number title url }}
      }}
    }}
    """
    data = gh_graphql(query, {"login": owner, "number": project_number})
    container = data.get(root)
    project = container.get("projectV2") if container else None
    if not project:
        raise GovernanceError(
            f"Project #{project_number} não encontrado para {owner_type} `{owner}`."
        )
    return project


def get_project_fields(project_id: str) -> list[dict[str, Any]]:
    query = """
    query($id: ID!) {
      node(id: $id) {
        ... on ProjectV2 {
          fields(first: 100) {
            nodes {
              __typename
              ... on ProjectV2Field { id name dataType }
              ... on ProjectV2SingleSelectField {
                id name dataType
                options { id name description color }
              }
              ... on ProjectV2IterationField { id name dataType }
            }
          }
        }
      }
    }
    """
    data = gh_graphql(query, {"id": project_id})
    node = data.get("node") or {}
    return [field for field in (node.get("fields") or {}).get("nodes", []) if field]


def get_project_items(project_id: str) -> list[dict[str, Any]]:
    query = """
    query($id: ID!, $after: String) {
      node(id: $id) {
        ... on ProjectV2 {
          items(first: 100, after: $after) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id type
              content {
                __typename
                ... on Issue {
                  id number title state
                  repository { nameWithOwner }
                }
                ... on PullRequest {
                  id number title state
                  repository { nameWithOwner }
                }
              }
              fieldValues(first: 100) {
                nodes {
                  __typename
                  ... on ProjectV2ItemFieldTextValue {
                    text
                    field {
                      ... on ProjectV2Field { name }
                    }
                  }
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field {
                      ... on ProjectV2SingleSelectField { name }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    items: list[dict[str, Any]] = []
    after: str | None = None
    while True:
        data = gh_graphql(query, {"id": project_id, "after": after})
        connection = ((data.get("node") or {}).get("items") or {})
        items.extend(node for node in connection.get("nodes", []) if node)
        page = connection.get("pageInfo") or {}
        if not page.get("hasNextPage"):
            break
        after = page.get("endCursor")
    return items


def add_project_item(project_id: str, content_id: str) -> str:
    mutation = """
    mutation($project: ID!, $content: ID!) {
      addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
        item { id }
      }
    }
    """
    data = gh_graphql(mutation, {"project": project_id, "content": content_id})
    item = (data.get("addProjectV2ItemById") or {}).get("item") or {}
    item_id = item.get("id")
    if not item_id:
        raise GovernanceError("GitHub não retornou o ID do item adicionado ao Project.")
    return item_id


def get_issue_node_id(repo: str, number: int) -> str:
    result = run_command(
        ["gh", "issue", "view", str(number), "--repo", repo, "--json", "id", "--jq", ".id"]
    )
    node_id = result.stdout.strip()
    if not node_id:
        raise GovernanceError(f"Não foi possível resolver o node ID da issue #{number}.")
    return node_id


def stable_issue_number(entry: Any) -> int | None:
    """Read an issue number from the importer state format."""
    if isinstance(entry, int):
        return entry
    if isinstance(entry, dict):
        for key in ("number", "github_number", "issue_number"):
            value = entry.get(key)
            if isinstance(value, int):
                return value
            if isinstance(value, str) and value.isdigit():
                return int(value)
        url = str(entry.get("url") or entry.get("github_url") or "")
        tail = url.rstrip("/").rsplit("/", 1)[-1]
        if tail.isdigit():
            return int(tail)
    return None


def load_materialized_numbers(path: Path) -> dict[str, int]:
    state = read_json(path, default={}) or {}
    raw = state.get("issues", state)
    if not isinstance(raw, dict):
        raise GovernanceError(f"Mapa de materialização inválido: {path}")
    numbers: dict[str, int] = {}
    for stable_id, entry in raw.items():
        number = stable_issue_number(entry)
        if number is not None:
            numbers[str(stable_id)] = number
    return numbers


def chunks(values: list[Any], size: int) -> Iterable[list[Any]]:
    for offset in range(0, len(values), size):
        yield values[offset : offset + size]
