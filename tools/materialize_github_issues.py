#!/usr/bin/env python3
"""Materialize DSGeorref SAR issues on GitHub in safe, resumable batches.

The script is dry-run by default. It reads the canonical repository files,
creates Epic issues before Story issues, sets parent/sub-issue relationships,
optionally adds items to a GitHub Project and milestone, and can materialize
blocking relationships from the canonical dependency graphs.

Requirements:
  - Python 3.12+
  - GitHub CLI (`gh`) authenticated for the target repository
  - `project` OAuth scope when --project-title is used

Examples:
  python tools/materialize_github_issues.py \
    --repo OWNER/DSGeorref --sprint SPRINT-001 --kind epics

  python tools/materialize_github_issues.py \
    --repo OWNER/DSGeorref --sprint SPRINT-001 --kind epics \
    --project-title "DSGeorref Engineering" --apply

  python tools/materialize_github_issues.py \
    --repo OWNER/DSGeorref --sprint SPRINT-001 --kind stories \
    --project-title "DSGeorref Engineering" --max-items 25 --apply

  python tools/materialize_github_issues.py \
    --repo OWNER/DSGeorref --sprint SPRINT-001 --only-links \
    --link-dependencies --apply
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "docs/06-delivery/ISSUE_INDEX.csv"
STORY_GRAPH_PATH = ROOT / "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
EPIC_GRAPH_PATH = ROOT / "docs/06-delivery/DEPENDENCY_GRAPH.json"
DEFAULT_STATE_PATH = ROOT / ".github/dsgeorref-materialization-map.json"
ISSUE_PREFIX_RE = re.compile(r"^\[(ISSUE-\d{4})\]\s+")
ISSUE_NUMBER_RE = re.compile(r"/issues/(\d+)(?:\?.*)?$")
STORY_ID_RE = re.compile(r"STORY-\d{4}")


class MaterializationError(RuntimeError):
    """Raised when a safe materialization precondition is not satisfied."""


@dataclass(frozen=True)
class CanonicalIssue:
    issue_id: str
    kind: str
    epic_id: str
    sprint: str
    bounded_context: str
    owner_role: str
    risk_tier: str
    source_path: Path
    title: str
    story_id: str | None

    @property
    def is_epic(self) -> bool:
        return self.kind == "epic"

    @property
    def github_title(self) -> str:
        return f"[{self.issue_id}] {self.title}"


@dataclass
class RemoteIssue:
    number: int
    title: str
    url: str


def run_command(
    args: list[str],
    *,
    check: bool = True,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=capture,
        check=check,
    )


def require_repository_files() -> None:
    missing = [p for p in (INDEX_PATH, STORY_GRAPH_PATH, EPIC_GRAPH_PATH) if not p.is_file()]
    if missing:
        formatted = "\n".join(f"- {p.relative_to(ROOT)}" for p in missing)
        raise MaterializationError(
            "Execute o script na raiz do SAR DSGeorref. Arquivos ausentes:\n" + formatted
        )


def require_gh(*, project_requested: bool, apply: bool) -> None:
    if shutil.which("gh") is None:
        if apply:
            raise MaterializationError(
                "GitHub CLI (`gh`) não está instalado ou não está no PATH."
            )
        print("AVISO: `gh` não encontrado; dry-run será somente local.", file=sys.stderr)
        return

    if not apply:
        return

    status = run_command(["gh", "auth", "status"], check=False)
    if status.returncode != 0:
        raise MaterializationError(
            "GitHub CLI não está autenticado. Execute `gh auth login`.\n"
            + (status.stderr or status.stdout)
        )
    if project_requested:
        print(
            "INFO: o Project exige scope `project`. Se necessário, execute "
            "`gh auth refresh -s project`.",
            file=sys.stderr,
        )


def first_heading(path: Path) -> str:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            heading = line[2:].strip()
            if " — " in heading:
                return heading.split(" — ", 1)[1].strip()
            return heading
    raise MaterializationError(f"Documento sem heading H1: {path.relative_to(ROOT)}")


def resolve_source_path(row: dict[str, str]) -> Path:
    directory = "issues" if row["type"].lower().startswith("epic") else "stories"
    path = ROOT / "docs/06-delivery" / directory / row["file"]
    if not path.is_file():
        raise MaterializationError(
            f"Arquivo canônico ausente para {row['issue_id']}: {path.relative_to(ROOT)}"
        )
    return path


def load_canonical_issues() -> list[CanonicalIssue]:
    issues: list[CanonicalIssue] = []
    with INDEX_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "issue_id",
            "type",
            "epic_id",
            "sprint",
            "bounded_context",
            "owner_role",
            "file",
            "cto_risk_tier",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise MaterializationError(
                f"ISSUE_INDEX.csv sem colunas obrigatórias: {sorted(missing)}"
            )
        for row in reader:
            source_path = resolve_source_path(row)
            is_epic = row["type"].lower().startswith("epic")
            story_match = STORY_ID_RE.search(source_path.name)
            issues.append(
                CanonicalIssue(
                    issue_id=row["issue_id"],
                    kind="epic" if is_epic else "story",
                    epic_id=row["epic_id"],
                    sprint=row["sprint"],
                    bounded_context=row["bounded_context"],
                    owner_role=row["owner_role"],
                    risk_tier=row["cto_risk_tier"],
                    source_path=source_path,
                    title=first_heading(source_path),
                    story_id=story_match.group(0) if story_match else None,
                )
            )
    return issues


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "schema_version": "1.0.0",
            "issues": {},
            "dependency_edges": [],
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MaterializationError(f"State file inválido: {path}: {exc}") from exc
    data.setdefault("issues", {})
    data.setdefault("dependency_edges", [])
    return data


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def list_remote_issues(repo: str) -> dict[str, RemoteIssue]:
    if shutil.which("gh") is None:
        return {}
    result = run_command(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "all",
            "--limit",
            "1000",
            "--json",
            "number,title,url",
        ],
        check=False,
    )
    if result.returncode != 0:
        raise MaterializationError(
            "Não foi possível listar issues remotas:\n" + (result.stderr or result.stdout)
        )
    rows = json.loads(result.stdout or "[]")
    remote: dict[str, RemoteIssue] = {}
    for row in rows:
        match = ISSUE_PREFIX_RE.match(row["title"])
        if not match:
            continue
        stable_id = match.group(1)
        if stable_id in remote and remote[stable_id].number != row["number"]:
            raise MaterializationError(
                f"Duplicata remota para {stable_id}: #{remote[stable_id].number} e #{row['number']}"
            )
        remote[stable_id] = RemoteIssue(
            number=int(row["number"]),
            title=row["title"],
            url=row["url"],
        )
    return remote


def merge_remote_into_state(state: dict[str, Any], remote: dict[str, RemoteIssue]) -> None:
    for stable_id, issue in remote.items():
        state["issues"][stable_id] = {
            "number": issue.number,
            "url": issue.url,
            "title": issue.title,
        }


def canonical_epic_issue_ids(issues: Iterable[CanonicalIssue]) -> dict[str, str]:
    result: dict[str, str] = {}
    for issue in issues:
        if issue.is_epic:
            result[issue.epic_id] = issue.issue_id
    return result


def issue_number(state: dict[str, Any], stable_id: str) -> int | None:
    entry = state["issues"].get(stable_id)
    if not entry:
        return None
    return int(entry["number"])


def select_issues(
    issues: list[CanonicalIssue],
    *,
    sprint: str | None,
    epic: str | None,
    kind: str,
    existing_ids: set[str],
    max_items: int,
) -> list[CanonicalIssue]:
    selected = []
    for issue in issues:
        if sprint and issue.sprint != sprint:
            continue
        if epic and issue.epic_id != epic:
            continue
        expected_kind = {"epics": "epic", "stories": "story"}.get(kind)
        if expected_kind and issue.kind != expected_kind:
            continue
        if issue.issue_id in existing_ids:
            continue
        selected.append(issue)

    # Epics must always be materialized before their stories.
    selected.sort(key=lambda item: (0 if item.is_epic else 1, item.issue_id))
    if max_items > 0:
        selected = selected[:max_items]
    return selected


def build_body(issue: CanonicalIssue) -> str:
    original = issue.source_path.read_text(encoding="utf-8").rstrip()
    source = issue.source_path.relative_to(ROOT).as_posix()
    generated = (
        "\n\n---\n\n"
        "## Materialização GitHub\n\n"
        f"- **Stable ID:** `{issue.issue_id}`\n"
        f"- **Épico:** `{issue.epic_id}`\n"
        f"- **Sprint planejada:** `{issue.sprint}`\n"
        f"- **Bounded Context:** `{issue.bounded_context}`\n"
        f"- **Owner role:** `{issue.owner_role}`\n"
        f"- **Risk tier:** `{issue.risk_tier}`\n"
        f"- **Fonte canônica:** `{source}`\n\n"
        "Este item foi materializado do SAR. O arquivo versionado permanece a fonte "
        "autoritativa para o conteúdo normativo.\n"
    )
    return original + generated


def create_issue(
    issue: CanonicalIssue,
    *,
    repo: str,
    project_title: str | None,
    milestone: str | None,
    parent_number: int | None,
    use_issue_types: bool,
) -> RemoteIssue:
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".md",
        delete=False,
    ) as handle:
        handle.write(build_body(issue))
        body_path = Path(handle.name)

    command = [
        "gh",
        "issue",
        "create",
        "--repo",
        repo,
        "--title",
        issue.github_title,
        "--body-file",
        str(body_path),
    ]
    if project_title:
        command.extend(["--project", project_title])
    if milestone:
        command.extend(["--milestone", milestone])
    if parent_number is not None:
        command.extend(["--parent", str(parent_number)])
    if use_issue_types:
        command.extend(["--type", "Epic" if issue.is_epic else "Story"])

    try:
        result = run_command(command, check=False)
    finally:
        body_path.unlink(missing_ok=True)

    if result.returncode != 0:
        raise MaterializationError(
            f"Falha ao criar {issue.issue_id}:\n{result.stderr or result.stdout}"
        )
    url = (result.stdout or "").strip().splitlines()[-1]
    match = ISSUE_NUMBER_RE.search(url)
    if not match:
        raise MaterializationError(
            f"GitHub CLI não retornou URL reconhecível para {issue.issue_id}: {url!r}"
        )
    return RemoteIssue(number=int(match.group(1)), title=issue.github_title, url=url)


def load_dependency_edges(
    *,
    sprint: str | None,
    issues: list[CanonicalIssue],
) -> list[tuple[str, str]]:
    """Return (blocker_issue_id, blocked_issue_id) pairs."""
    story_to_issue = {i.story_id: i.issue_id for i in issues if i.story_id}
    epic_to_issue = {i.epic_id: i.issue_id for i in issues if i.is_epic}
    issue_sprints = {i.issue_id: i.sprint for i in issues}
    edges: list[tuple[str, str]] = []

    story_graph = json.loads(STORY_GRAPH_PATH.read_text(encoding="utf-8"))
    for edge in story_graph.get("edges", []):
        blocker = story_to_issue.get(edge.get("from"))
        blocked = story_to_issue.get(edge.get("to"))
        if not blocker or not blocked:
            continue
        if sprint and issue_sprints.get(blocked) != sprint:
            continue
        edges.append((blocker, blocked))

    epic_graph = json.loads(EPIC_GRAPH_PATH.read_text(encoding="utf-8"))
    for edge in epic_graph.get("edges", []):
        blocker = epic_to_issue.get(edge.get("from"))
        blocked = epic_to_issue.get(edge.get("to"))
        if not blocker or not blocked:
            continue
        if sprint and issue_sprints.get(blocked) != sprint:
            continue
        edges.append((blocker, blocked))

    return sorted(set(edges))


def link_dependencies(
    *,
    repo: str,
    state: dict[str, Any],
    edges: list[tuple[str, str]],
    apply: bool,
    sleep_seconds: float,
) -> tuple[int, int]:
    linked = set(state.get("dependency_edges", []))
    created = 0
    unavailable = 0
    for blocker_id, blocked_id in edges:
        edge_key = f"{blocker_id}->{blocked_id}"
        if edge_key in linked:
            continue
        blocker_number = issue_number(state, blocker_id)
        blocked_number = issue_number(state, blocked_id)
        if blocker_number is None or blocked_number is None:
            unavailable += 1
            continue
        print(
            f"DEPENDÊNCIA: {blocked_id} (#{blocked_number}) bloqueada por "
            f"{blocker_id} (#{blocker_number})"
        )
        if apply:
            result = run_command(
                [
                    "gh",
                    "issue",
                    "edit",
                    str(blocked_number),
                    "--repo",
                    repo,
                    "--add-blocked-by",
                    str(blocker_number),
                ],
                check=False,
            )
            if result.returncode != 0:
                raise MaterializationError(
                    f"Falha ao ligar {edge_key}:\n{result.stderr or result.stdout}"
                )
            linked.add(edge_key)
            state["dependency_edges"] = sorted(linked)
            created += 1
            time.sleep(sleep_seconds)
    return created, unavailable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materializa issues do SAR DSGeorref no GitHub em lotes seguros."
    )
    parser.add_argument("--repo", required=True, help="OWNER/REPO")
    parser.add_argument("--sprint", help="Ex.: SPRINT-001")
    parser.add_argument("--epic", help="Ex.: EPIC-001")
    parser.add_argument(
        "--kind",
        choices=("all", "epics", "stories"),
        default="all",
        help="Tipo de item a materializar.",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=25,
        help="Máximo de novos itens nesta execução; 0 significa sem limite.",
    )
    parser.add_argument("--project-title", help="Título exato do GitHub Project.")
    parser.add_argument("--milestone", help="Milestone opcional para os itens criados.")
    parser.add_argument(
        "--use-issue-types",
        action="store_true",
        help="Usa issue types Epic/Story; requer organização com esses tipos configurados.",
    )
    parser.add_argument(
        "--link-dependencies",
        action="store_true",
        help="Materializa relações blocked-by do grafo canônico.",
    )
    parser.add_argument(
        "--only-links",
        action="store_true",
        help="Não cria issues; somente materializa dependências já disponíveis.",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=DEFAULT_STATE_PATH,
        help="Mapa local estável ID → número/URL do GitHub.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.6,
        help="Intervalo entre escritas no GitHub.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Executa escritas. Sem esta flag, funciona como dry-run.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        require_repository_files()
        require_gh(project_requested=bool(args.project_title), apply=args.apply)
        issues = load_canonical_issues()
        state_path = args.state_file
        if not state_path.is_absolute():
            state_path = ROOT / state_path
        state = load_state(state_path)

        remote = list_remote_issues(args.repo) if shutil.which("gh") else {}
        merge_remote_into_state(state, remote)
        if args.apply:
            save_state(state_path, state)

        existing_ids = set(state["issues"])
        pending = [] if args.only_links else select_issues(
            issues,
            sprint=args.sprint,
            epic=args.epic,
            kind=args.kind,
            existing_ids=existing_ids,
            max_items=args.max_items,
        )
        epic_issue_ids = canonical_epic_issue_ids(issues)

        mode = "APPLY" if args.apply else "DRY-RUN"
        print(f"MODE: {mode}")
        print(f"Repository: {args.repo}")
        print(f"Existing materialized issues: {len(existing_ids)}")
        print(f"Pending in this batch: {len(pending)}")

        created_count = 0
        for issue in pending:
            parent_number = None
            if not issue.is_epic:
                parent_stable_id = epic_issue_ids[issue.epic_id]
                parent_number = issue_number(state, parent_stable_id)
                if parent_number is None:
                    raise MaterializationError(
                        f"{issue.issue_id} depende do épico {parent_stable_id}, ainda não "
                        "materializado. Execute primeiro com `--kind epics`."
                    )
            parent_text = f" parent=#{parent_number}" if parent_number else ""
            print(
                f"CREATE {issue.issue_id} [{issue.kind}] {issue.sprint} "
                f"{issue.epic_id}{parent_text}: {issue.title}"
            )
            if not args.apply:
                continue
            remote_issue = create_issue(
                issue,
                repo=args.repo,
                project_title=args.project_title,
                milestone=args.milestone,
                parent_number=parent_number,
                use_issue_types=args.use_issue_types,
            )
            state["issues"][issue.issue_id] = {
                "number": remote_issue.number,
                "url": remote_issue.url,
                "title": remote_issue.title,
                "kind": issue.kind,
                "epic_id": issue.epic_id,
                "sprint": issue.sprint,
            }
            save_state(state_path, state)
            created_count += 1
            time.sleep(args.sleep)

        dependency_created = 0
        dependency_unavailable = 0
        if args.link_dependencies:
            edges = load_dependency_edges(sprint=args.sprint, issues=issues)
            dependency_created, dependency_unavailable = link_dependencies(
                repo=args.repo,
                state=state,
                edges=edges,
                apply=args.apply,
                sleep_seconds=args.sleep,
            )
            if args.apply:
                save_state(state_path, state)

        print("\nSUMMARY")
        print(f"Created issues: {created_count if args.apply else 0}")
        print(f"Planned creates in dry-run: {len(pending) if not args.apply else 0}")
        print(f"Dependency links created: {dependency_created}")
        print(f"Dependency links waiting for missing issues: {dependency_unavailable}")
        print(f"State file: {state_path.relative_to(ROOT) if state_path.is_relative_to(ROOT) else state_path}")
        if not args.apply:
            print("Nenhuma escrita foi executada. Revise e repita com `--apply`.")
        return 0
    except MaterializationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Interrompido pelo usuário; o state file preserva o progresso.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
