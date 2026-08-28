from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


TASK_PATH = Path(".codex/tasks/TASK-0014.json")
STORY_PATH = Path(
    "docs/06-delivery/stories/"
    "STORY-0014-ISSUE-0124-integrar-a-capacidade-ao-fluxo-do-repositorio-"
    "monorepo-greenfield-com-cli.md"
)
GRAPH_PATH = Path("docs/06-delivery/STORY_DEPENDENCY_GRAPH.json")
WORKFLOW_PATH = Path(
    ".github/workflows/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r.yaml"
)
TOOL_ROOT = Path(
    "tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r"
)
QUALITY_VALIDATOR = Path(
    "tools/quality/contexts/engineering_governance/"
    "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/validator.py"
)
TEST_PATH = Path(
    "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/"
    "test_integration.py"
)
EVIDENCE_PATH = Path(
    "evidence/implementation/epic-003/story-0014/implementation-report.md"
)
EXPECTED_ALLOW_PATHS = (
    f"{TOOL_ROOT.as_posix()}/**",
    "docs/03-engineering/contexts/engineering_governance/"
    "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**",
    TEST_PATH.as_posix(),
    WORKFLOW_PATH.as_posix(),
    "evidence/implementation/epic-003/story-0014/**",
)
EXPECTED_DENY_PATHS = ("src/**/epic-*", "src/**/issue-*")
EXPECTED_AC_IDS = tuple(f"AC-ISSUE-0124-{number:02d}" for number in range(1, 5))
EXPECTED_DEPENDENCIES = ("STORY-0012", "STORY-0013")
EXPECTED_REQUIREMENTS = ("REQ-DEL-001", "REQ-DEV-001", "REQ-TOP-001")
EXPECTED_UPSTREAM_AC_IDS = tuple(
    f"AC-ISSUE-0123-{number:02d}" for number in range(1, 5)
)
WORKFLOW_TOKENS = (
    QUALITY_VALIDATOR.as_posix(),
    f"{TOOL_ROOT.as_posix()}/repository_integration.py",
    TEST_PATH.as_posix(),
    "test_epic_003_automacao",
    "test_epic_003_integracao",
)


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str


def _load_json(root: Path, relative: Path) -> tuple[Mapping[str, Any] | None, list[Finding]]:
    try:
        value = json.loads((root / relative).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [Finding("JSON_INVALID", relative.as_posix(), str(error))]
    if not isinstance(value, Mapping):
        return None, [Finding("JSON_INVALID", relative.as_posix(), "object required")]
    return value, []


def _task_findings(task: Mapping[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    identity = tuple(task.get(key) for key in ("task_id", "issue_id", "story_id"))
    if identity != ("TASK-0014", "ISSUE-0124", "STORY-0014"):
        findings.append(Finding("TASK_IDENTITY_INVALID", TASK_PATH.as_posix(), str(identity)))
    expected = {
        "allow_paths": EXPECTED_ALLOW_PATHS,
        "deny_paths": EXPECTED_DENY_PATHS,
        "acceptance_criterion_ids": EXPECTED_AC_IDS,
        "dependencies": EXPECTED_DEPENDENCIES,
        "tests": ("test_epic_003_integracao",),
        "applicable_specifications": ("SPEC-001", "SPEC-004"),
        "evidence": (
            "evidence/implementation/epic-003/story-0014/",
            "commit candidato e relatório de testes",
        ),
    }
    for field, required in expected.items():
        actual = task.get(field)
        if not isinstance(actual, list) or tuple(actual) != required:
            findings.append(Finding("TASK_SCOPE_INVALID", field, "exact governed values required"))
    phase_review = task.get("phase_f_review")
    phase_files = phase_review.get("files") if isinstance(phase_review, Mapping) else None
    phase_dependencies = (
        phase_review.get("dependencies") if isinstance(phase_review, Mapping) else None
    )
    if not isinstance(phase_files, Mapping) or tuple(
        phase_files.get("allow_paths", ())
    ) != EXPECTED_ALLOW_PATHS or tuple(
        phase_files.get("deny_paths", ())
    ) != EXPECTED_DENY_PATHS:
        findings.append(Finding("TASK_SCOPE_INVALID", "phase_f_review.files", "scope drift"))
    if not isinstance(phase_dependencies, Mapping) or tuple(
        phase_dependencies.get("items", ())
    ) != EXPECTED_DEPENDENCIES:
        findings.append(
            Finding("TASK_DEPENDENCY_INVALID", "phase_f_review.dependencies", "dependency drift")
        )
    if (
        task.get("bounded_context") != "BC-001"
        or task.get("requirement_basis") != "DERIVED_CONTROL"
    ):
        findings.append(
            Finding(
                "TASK_IDENTITY_INVALID",
                TASK_PATH.as_posix(),
                "BC-001 derived control required",
            )
        )
    return findings


def _story_findings(root: Path) -> list[Finding]:
    try:
        text = (root / STORY_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [Finding("STORY_INVALID", STORY_PATH.as_posix(), str(error))]
    missing = [
        token for token in (*EXPECTED_AC_IDS, "test_epic_003_integracao") if token not in text
    ]
    return [] if not missing else [
        Finding("STORY_TRACEABILITY_INVALID", STORY_PATH.as_posix(), ",".join(missing))
    ]


def _cyclic_nodes(graph: Mapping[str, set[str]]) -> tuple[str, ...]:
    remaining = {node: set(dependencies) for node, dependencies in graph.items()}
    ready = sorted(node for node, dependencies in remaining.items() if not dependencies)
    while ready:
        resolved = ready.pop(0)
        remaining.pop(resolved, None)
        for node, dependencies in remaining.items():
            dependencies.discard(resolved)
            if not dependencies and node not in ready:
                ready.append(node)
        ready.sort()
    return tuple(sorted(remaining))


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
    node_ids = [str(node.get("id")) for node in nodes if isinstance(node, Mapping)]
    pairs = [
        (str(edge.get("from")), str(edge.get("to")))
        for edge in edges
        if isinstance(edge, Mapping) and edge.get("relation") == "blocks"
    ]
    incoming = tuple(sorted(source for source, target in pairs if target == "STORY-0014"))
    findings: list[Finding] = []
    if len(node_ids) != len(set(node_ids)) or not set(EXPECTED_DEPENDENCIES).issubset(node_ids):
        findings.append(Finding("DEPENDENCY_GRAPH_INVALID", GRAPH_PATH.as_posix(), "node drift"))
    if incoming != EXPECTED_DEPENDENCIES:
        findings.append(Finding("DEPENDENCY_GRAPH_MISMATCH", "STORY-0014", str(incoming)))
    dependency_graph = {node: set() for node in node_ids}
    for source, target in pairs:
        dependency_graph.setdefault(target, set()).add(source)
        dependency_graph.setdefault(source, set())
    cyclic = _cyclic_nodes(dependency_graph)
    if cyclic:
        findings.append(Finding("DEPENDENCY_CYCLE", GRAPH_PATH.as_posix(), ",".join(cyclic)))
    return findings


def _workflow_findings(root: Path) -> list[Finding]:
    try:
        document = yaml.safe_load((root / WORKFLOW_PATH).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return [Finding("CONTROL_PLANE_INVALID", WORKFLOW_PATH.as_posix(), str(error))]
    if not isinstance(document, Mapping):
        return [Finding("CONTROL_PLANE_INVALID", WORKFLOW_PATH.as_posix(), "mapping required")]
    pending: list[object] = [document]
    commands: list[str] = []
    while pending:
        value = pending.pop()
        if isinstance(value, Mapping):
            commands.extend(
                item for key, item in value.items() if key == "run" and isinstance(item, str)
            )
            pending.extend(item for key, item in value.items() if key != "run")
        elif isinstance(value, list):
            pending.extend(value)
    missing = [token for token in WORKFLOW_TOKENS if token not in "\n".join(commands)]
    permissions = document.get("permissions")
    read_only = isinstance(permissions, Mapping) and permissions.get("contents") == "read"
    return [] if not missing and read_only else [
        Finding(
            "CONTROL_PLANE_INVALID",
            WORKFLOW_PATH.as_posix(),
            ",".join(missing) or "read-only required",
        )
    ]


def _test_surface_findings(root: Path) -> list[Finding]:
    try:
        tree = ast.parse((root / TEST_PATH).read_bytes(), filename=TEST_PATH.as_posix())
    except (OSError, SyntaxError) as error:
        return [Finding("TEST_SURFACE_INVALID", TEST_PATH.as_posix(), str(error))]
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    return [] if functions.count("test_epic_003_integracao") == 1 else [
        Finding("TEST_SURFACE_INVALID", TEST_PATH.as_posix(), "one canonical test required")
    ]


def _module_findings(root: Path) -> list[Finding]:
    files = sorted((root / TOOL_ROOT).glob("*.py"))
    stems = {path.stem for path in files}
    graph: dict[str, set[str]] = {}
    digests: dict[str, str] = {}
    findings: list[Finding] = []
    for path in files:
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
        imported = {
            node.module.rsplit(".", 1)[-1]
            for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module
        }
        imported.update(
            alias.name.rsplit(".", 1)[-1]
            for node in tree.body
            if isinstance(node, ast.Import)
            for alias in node.names
        )
        graph[path.stem] = imported.intersection(stems)
    cyclic = _cyclic_nodes(graph)
    if cyclic:
        findings.append(Finding("PYTHON_IMPORT_CYCLE", TOOL_ROOT.as_posix(), ",".join(cyclic)))
    return findings


def _automation_findings(root: Path) -> list[Finding]:
    environment = os.environ.copy()
    environment.update(
        {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"}
    )
    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(root / QUALITY_VALIDATOR),
                "--repository-root",
                str(root),
                "--dry-run",
            ],
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        report = json.loads(completed.stdout)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [Finding("UPSTREAM_VALIDATOR_INVALID", QUALITY_VALIDATOR.as_posix(), str(error))]
    expected = {
        "status": "PASS",
        "mode": "DRY_RUN",
        "destructive_actions": 0,
        "requirements": list(EXPECTED_REQUIREMENTS),
        "acceptance_criteria": list(EXPECTED_UPSTREAM_AC_IDS),
        "findings": [],
    }
    if completed.returncode == 0 and isinstance(report, Mapping) and all(
        report.get(key) == value for key, value in expected.items()
    ):
        return []
    upstream = report.get("findings") if isinstance(report, Mapping) else None
    if isinstance(upstream, list) and upstream:
        return [
            Finding(
                str(item.get("code", "UPSTREAM_VALIDATION_FAILED")),
                str(item.get("artifact", QUALITY_VALIDATOR)),
                str(item.get("detail", "validation failed")),
            )
            for item in upstream
            if isinstance(item, Mapping)
        ]
    return [
        Finding(
            "UPSTREAM_VALIDATION_FAILED",
            QUALITY_VALIDATOR.as_posix(),
            f"exit={completed.returncode}",
        )
    ]


def validate_repository_integration(repository_root: Path) -> tuple[Finding, ...]:
    root = repository_root.resolve()
    task, task_load = _load_json(root, TASK_PATH)
    graph, graph_load = _load_json(root, GRAPH_PATH)
    findings = [*task_load, *graph_load]
    if task is not None:
        findings.extend(_task_findings(task))
    if graph is not None:
        findings.extend(_graph_findings(graph))
    findings.extend(_story_findings(root))
    findings.extend(_workflow_findings(root))
    findings.extend(_test_surface_findings(root))
    findings.extend(_module_findings(root))
    findings.extend(_automation_findings(root))
    for path in (TEST_PATH, EVIDENCE_PATH):
        if not (root / path).is_file():
            findings.append(
                Finding(
                    "INTEGRATION_SURFACE_MISSING",
                    path.as_posix(),
                    "required artifact absent",
                )
            )
    return tuple(sorted(set(findings)))


def _report(findings: tuple[Finding, ...]) -> dict[str, object]:
    return {
        "acceptance_criteria": list(EXPECTED_AC_IDS),
        "dependencies": list(EXPECTED_DEPENDENCIES),
        "findings": [asdict(finding) for finding in findings],
        "issue": "ISSUE-0124",
        "requirements": list(EXPECTED_REQUIREMENTS),
        "status": "FAIL" if findings else "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0124 repository integration.")
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args(argv)
    try:
        findings = validate_repository_integration(args.repository_root)
    except Exception as error:  # CLI boundary must fail closed without a traceback.
        findings = (Finding("INTEGRATION_INTERNAL_ERROR", ".", str(error)),)
    print(json.dumps(_report(findings), ensure_ascii=False, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
