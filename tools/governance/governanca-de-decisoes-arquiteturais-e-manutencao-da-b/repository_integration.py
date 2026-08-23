from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


TASK_PATH = Path(".codex/tasks/TASK-0004.json")
STORY_PATH = Path(
    "docs/06-delivery/stories/"
    "STORY-0004-ISSUE-0114-integrar-a-capacidade-ao-fluxo-do-repositorio-"
    "governanca-de-decisoes-arqui.md"
)
GRAPH_PATH = Path("docs/06-delivery/STORY_DEPENDENCY_GRAPH.json")
WORKFLOW_PATH = Path(
    ".github/workflows/"
    "governanca-de-decisoes-arquiteturais-e-manutencao-da-b.yaml"
)
TOOL_ROOT = Path(
    "tools/governance/"
    "governanca-de-decisoes-arquiteturais-e-manutencao-da-b"
)
EXPECTED_ALLOW_PATHS = (
    f"{TOOL_ROOT.as_posix()}/**",
    "docs/03-engineering/contexts/engineering_governance/"
    "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/**",
    "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "test_integration.py",
    WORKFLOW_PATH.as_posix(),
    "evidence/implementation/epic-001/story-0004/**",
)
EXPECTED_DENY_PATHS = ("src/**/epic-*", "src/**/issue-*")
EXPECTED_AC_IDS = tuple(f"AC-ISSUE-0114-{number:02d}" for number in range(1, 5))
EXPECTED_DEPENDENCIES = ("STORY-0002", "STORY-0759")
REQUIRED_SURFACES = (
    TOOL_ROOT / "consolidacao/slice_consolidation.py",
    Path(
        "tools/quality/contexts/engineering_governance/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/validator.py"
    ),
    Path(
        "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "test_automation.py"
    ),
)
WORKFLOW_TOKENS = (
    f"{TOOL_ROOT.as_posix()}/repository_integration.py",
    EXPECTED_ALLOW_PATHS[2],
    "test_epic_001_integracao",
)


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str


def _load_json(root: Path, path: Path) -> tuple[Mapping[str, Any] | None, list[Finding]]:
    try:
        value = json.loads((root / path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [Finding("JSON_INVALID", path.as_posix(), str(error))]
    if not isinstance(value, Mapping):
        return None, [Finding("JSON_INVALID", path.as_posix(), "object required")]
    return value, []


def validate_repository_integration(repository_root: Path) -> tuple[Finding, ...]:
    root = repository_root.resolve()
    task, task_load_findings = _load_json(root, TASK_PATH)
    graph, graph_load_findings = _load_json(root, GRAPH_PATH)
    findings = [*task_load_findings, *graph_load_findings]
    if task is not None:
        findings.extend(_task_findings(task))
    findings.extend(_story_findings(root))
    if graph is not None:
        findings.extend(_graph_findings(graph))
    findings.extend(_workflow_findings(root))
    findings.extend(
        Finding("SURFACE_MISSING", path.as_posix(), "required dependency is absent")
        for path in REQUIRED_SURFACES
        if not (root / path).is_file()
    )
    findings.extend(_module_findings(root))
    return tuple(sorted(set(findings)))


def _task_findings(task: Mapping[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    identity = tuple(task.get(key) for key in ("task_id", "issue_id", "story_id"))
    if identity != ("TASK-0004", "ISSUE-0114", "STORY-0004"):
        findings.append(Finding("TASK_IDENTITY_INVALID", TASK_PATH.as_posix(), str(identity)))
    expected = {
        "allow_paths": EXPECTED_ALLOW_PATHS,
        "deny_paths": EXPECTED_DENY_PATHS,
        "acceptance_criterion_ids": EXPECTED_AC_IDS,
        "dependencies": EXPECTED_DEPENDENCIES,
        "tests": ("test_epic_001_integracao",),
        "governing_adrs": ("ADR-003", "ADR-006", "ADR-007", "ADR-008"),
        "applicable_specifications": ("SPEC-001", "SPEC-004"),
        "evidence": (
            "evidence/implementation/epic-001/story-0004/",
            "commit candidato e relatório de testes",
        ),
    }
    for field, required in expected.items():
        actual = task.get(field)
        if not isinstance(actual, list) or tuple(actual) != required:
            findings.append(Finding("TASK_SCOPE_INVALID", field, "exact governed values required"))
    phase_review = task.get("phase_f_review")
    phase_files = phase_review.get("files") if isinstance(phase_review, Mapping) else None
    phase_scope_valid = isinstance(phase_files, Mapping) and tuple(
        phase_files.get("allow_paths", ())
    ) == EXPECTED_ALLOW_PATHS and tuple(
        phase_files.get("deny_paths", ())
    ) == EXPECTED_DENY_PATHS
    if not phase_scope_valid:
        findings.append(Finding("TASK_SCOPE_INVALID", "phase_f_review.files", "scope drift"))
    criteria = task.get("acceptance_criteria")
    if not isinstance(criteria, list) or len(criteria) != len(EXPECTED_AC_IDS):
        findings.append(Finding("TASK_ACCEPTANCE_INVALID", "acceptance_criteria", "four required"))
    if task.get("bounded_context") != "BC-001":
        findings.append(Finding("TASK_IDENTITY_INVALID", "bounded_context", "BC-001 required"))
    return findings


def _story_findings(root: Path) -> list[Finding]:
    try:
        text = (root / STORY_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [Finding("STORY_INVALID", STORY_PATH.as_posix(), str(error))]
    identifiers = (*EXPECTED_AC_IDS, "test_epic_001_integracao")
    missing = [identifier for identifier in identifiers if identifier not in text]
    if missing:
        return [Finding("STORY_TRACEABILITY_INVALID", STORY_PATH.as_posix(), ",".join(missing))]
    return []


def _graph_findings(graph: Mapping[str, Any]) -> list[Finding]:
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return [
            Finding(
                "DEPENDENCY_GRAPH_INVALID",
                GRAPH_PATH.as_posix(),
                "nodes and edges required",
            )
        ]
    node_ids = [node.get("id") for node in nodes if isinstance(node, Mapping)]
    incoming = sorted(
        str(edge.get("from"))
        for edge in edges
        if isinstance(edge, Mapping)
        and edge.get("relation") == "blocks"
        and edge.get("to") == "STORY-0004"
    )
    findings: list[Finding] = []
    if len(node_ids) != len(set(node_ids)) or not set(EXPECTED_DEPENDENCIES).issubset(node_ids):
        findings.append(
            Finding(
                "DEPENDENCY_GRAPH_INVALID",
                GRAPH_PATH.as_posix(),
                "node identity drift",
            )
        )
    if tuple(incoming) != EXPECTED_DEPENDENCIES:
        findings.append(Finding("DEPENDENCY_GRAPH_MISMATCH", "STORY-0004", str(incoming)))
    return findings


def _workflow_findings(root: Path) -> list[Finding]:
    try:
        text = (root / WORKFLOW_PATH).read_text(encoding="utf-8")
        document = yaml.safe_load(text)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return [Finding("CONTROL_PLANE_INVALID", WORKFLOW_PATH.as_posix(), str(error))]
    if not isinstance(document, Mapping):
        return [Finding("CONTROL_PLANE_INVALID", WORKFLOW_PATH.as_posix(), "mapping required")]
    values: list[object] = [document]
    commands: list[str] = []
    while values:
        value = values.pop()
        if isinstance(value, Mapping):
            commands.extend(
                item
                for key, item in value.items()
                if key == "run" and isinstance(item, str)
            )
            values.extend(item for key, item in value.items() if key != "run")
        elif isinstance(value, list):
            values.extend(value)
    command_surface = "\n".join(commands)
    missing = [token for token in WORKFLOW_TOKENS if token not in command_surface]
    if missing:
        return [Finding("CONTROL_PLANE_INVALID", WORKFLOW_PATH.as_posix(), ",".join(missing))]
    permissions = document.get("permissions")
    if not isinstance(permissions, Mapping) or permissions.get("contents") != "read":
        return [Finding("CONTROL_PLANE_INVALID", WORKFLOW_PATH.as_posix(), "read-only required")]
    return []


def _module_findings(root: Path) -> list[Finding]:
    files = sorted((root / TOOL_ROOT).rglob("*.py"))
    stems: dict[str, Path] = {}
    graph: dict[str, set[str]] = {}
    digests: dict[str, str] = {}
    findings: list[Finding] = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        if path.stem in stems:
            findings.append(Finding("MODULE_NAME_DUPLICATE", relative, stems[path.stem].as_posix()))
        stems[path.stem] = path
    for stem, path in sorted(stems.items()):
        relative = path.relative_to(root).as_posix()
        try:
            content = path.read_bytes()
            tree = ast.parse(content, filename=relative)
        except (OSError, SyntaxError) as error:
            findings.append(Finding("PYTHON_MODULE_INVALID", relative, str(error)))
            continue
        digest = hashlib.sha256(content).hexdigest()
        if len(content) > 200 and digest in digests:
            findings.append(Finding("RULE_DUPLICATED", relative, digests[digest]))
        digests[digest] = relative
        graph[stem] = _imported_names(tree).intersection(stems)
    residual = _cyclic_nodes(graph)
    if residual:
        findings.append(Finding("PYTHON_IMPORT_CYCLE", TOOL_ROOT.as_posix(), ",".join(residual)))
    return findings


def _imported_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in getattr(tree, "body", ()):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.rsplit(".", 1)[-1])
        elif isinstance(node, ast.Import):
            names.update(alias.name.rsplit(".", 1)[-1] for alias in node.names)
    return names


def _cyclic_nodes(graph: Mapping[str, set[str]]) -> tuple[str, ...]:
    remaining = {node: set(dependencies) for node, dependencies in graph.items()}
    ready = sorted(node for node, dependencies in remaining.items() if not dependencies)
    while ready:
        resolved = ready.pop(0)
        remaining.pop(resolved, None)
        newly_ready: list[str] = []
        for node, dependencies in remaining.items():
            dependencies.discard(resolved)
            if not dependencies and node not in ready:
                newly_ready.append(node)
        ready.extend(sorted(newly_ready))
    return tuple(sorted(remaining))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0114 repository integration.")
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args(argv)
    findings = validate_repository_integration(args.repository_root)
    if findings:
        print(f"INTEGRATION FAILED ({len(findings)} finding(s))")
        for finding in findings:
            print(f"ERROR [{finding.code}] {finding.artifact} :: {finding.detail}")
        return 1
    print("INTEGRATION PASS")
    print("issue=ISSUE-0114 acceptance_criteria=4 dependencies=STORY-0002,STORY-0759")
    return 0


if __name__ == "__main__":
    sys.exit(main())
