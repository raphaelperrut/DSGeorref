from __future__ import annotations

import argparse
import json
import runpy
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from requirement_traceability import (
    REQUIREMENT_PATHS,
    REQUIREMENT_TESTS,
    STORY_PATH,
    TASK_PATH,
    TEST_PATH,
    TRACE_PATH,
    requirement_findings,
    story_text,
    test_surface_findings,
    validate_requirement_traceability as validate_traceability,
)
from repository_structure import cyclic_nodes, module_findings


GRAPH_PATH = Path("docs/06-delivery/STORY_DEPENDENCY_GRAPH.json")
WORKFLOW_PATH = Path(
    ".github/workflows/repositorio-privado-project-central-views-campos-label.yaml"
)
TOOL_ROOT = Path(
    "tools/governance/repositorio-privado-project-central-views-campos-label"
)
QUALITY_ROOT = Path(
    "tools/quality/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label"
)
CONTRACT_ROOT = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "repositorio-privado-project-central-views-campos-label"
)
EXPECTED_ALLOW_PATHS = (
    f"{TOOL_ROOT.as_posix()}/**",
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/**",
    TEST_PATH.as_posix(),
    WORKFLOW_PATH.as_posix(),
    "evidence/implementation/epic-002/story-0009/**",
)
EXPECTED_DENY_PATHS = ("src/**/epic-*", "src/**/issue-*")
EXPECTED_AC_IDS = tuple(f"AC-ISSUE-0119-{number:02d}" for number in range(1, 5))
EXPECTED_DEPENDENCIES = ("STORY-0007", "STORY-0008")
EXPECTED_TASK_TESTS = (
    "test_req_classicprofile_006",
    "test_req_classicprofile_008",
    "test_req_classicprofile_0010",
    "test_req_native_001",
    "test_epic_002_integracao",
)
REQUIRED_SURFACES = (
    TOOL_ROOT / "consolidacao/slice_consolidation.py",
    QUALITY_ROOT / "validator.py",
    Path(
        "tests/fnd/repositorio-privado-project-central-views-campos-label/"
        "test_automation.py"
    ),
)
WORKFLOW_TOKENS = (
    f"{TOOL_ROOT.as_posix()}/repository_integration.py",
    TEST_PATH.as_posix(),
    *tuple(value[1] for value in REQUIREMENT_TESTS.values()),
    "test_epic_002_integracao",
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
        findings.extend(
            Finding(item.code, item.artifact, item.detail)
            for item in requirement_findings(root, task, tuple(REQUIREMENT_TESTS))
        )
    findings.extend(_story_findings(root))
    findings.extend(
        Finding(item.code, item.artifact, item.detail)
        for item in test_surface_findings(root)
    )
    if graph is not None:
        findings.extend(_graph_findings(graph))
    findings.extend(_workflow_findings(root))
    findings.extend(_contract_findings(root))
    findings.extend(
        Finding("SURFACE_MISSING", path.as_posix(), "required dependency is absent")
        for path in REQUIRED_SURFACES
        if not (root / path).is_file()
    )
    findings.extend(
        Finding(item.code, item.artifact, item.detail)
        for item in module_findings(root, TOOL_ROOT)
    )
    return tuple(sorted(set(findings)))


def validate_requirement_traceability(
    repository_root: Path, requirement_id: str
) -> tuple[Finding, ...]:
    return tuple(
        Finding(item.code, item.artifact, item.detail)
        for item in validate_traceability(repository_root, requirement_id)
    )


def _task_findings(task: Mapping[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    identity = tuple(task.get(key) for key in ("task_id", "issue_id", "story_id"))
    if identity != ("TASK-0009", "ISSUE-0119", "STORY-0009"):
        findings.append(Finding("TASK_IDENTITY_INVALID", TASK_PATH.as_posix(), str(identity)))
    expected = {
        "allow_paths": EXPECTED_ALLOW_PATHS,
        "deny_paths": EXPECTED_DENY_PATHS,
        "acceptance_criterion_ids": EXPECTED_AC_IDS,
        "dependencies": EXPECTED_DEPENDENCIES,
        "tests": EXPECTED_TASK_TESTS,
        "governing_adrs": (
            "ADR-003", "ADR-004", "ADR-005", "ADR-006", "ADR-007",
            "ADR-008", "ADR-042", "ADR-044", "ADR-045",
        ),
        "applicable_specifications": ("SPEC-001", "SPEC-004"),
        "evidence": (
            "evidence/implementation/epic-002/story-0009/",
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
    if not isinstance(phase_files, Mapping) or (
        tuple(phase_files.get("allow_paths", ())) != EXPECTED_ALLOW_PATHS
        or tuple(phase_files.get("deny_paths", ())) != EXPECTED_DENY_PATHS
    ):
        findings.append(Finding("TASK_SCOPE_INVALID", "phase_f_review.files", "scope drift"))
    if not isinstance(phase_dependencies, Mapping) or tuple(
        phase_dependencies.get("items", ())
    ) != EXPECTED_DEPENDENCIES:
        findings.append(
            Finding("TASK_DEPENDENCY_INVALID", "phase_f_review.dependencies", "dependency drift")
        )
    if task.get("bounded_context") != "BC-001":
        findings.append(Finding("TASK_IDENTITY_INVALID", "bounded_context", "BC-001 required"))
    return findings


def _story_findings(root: Path) -> list[Finding]:
    text, trace_findings = story_text(root)
    findings = [Finding(item.code, item.artifact, item.detail) for item in trace_findings]
    if text is None:
        return findings
    identifiers = (*EXPECTED_AC_IDS, *EXPECTED_TASK_TESTS)
    missing = [identifier for identifier in identifiers if identifier not in text]
    if missing:
        findings.append(
            Finding("STORY_TRACEABILITY_INVALID", STORY_PATH.as_posix(), ",".join(missing))
        )
    return findings


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
        and edge.get("to") == "STORY-0009"
    )
    findings: list[Finding] = []
    if len(node_ids) != len(set(node_ids)) or not set(EXPECTED_DEPENDENCIES).issubset(node_ids):
        findings.append(Finding("DEPENDENCY_GRAPH_INVALID", GRAPH_PATH.as_posix(), "node drift"))
    if tuple(incoming) != EXPECTED_DEPENDENCIES:
        findings.append(Finding("DEPENDENCY_GRAPH_MISMATCH", "STORY-0009", str(incoming)))
    edge_pairs = [
        (str(edge.get("from")), str(edge.get("to")))
        for edge in edges
        if isinstance(edge, Mapping) and edge.get("relation") == "blocks"
    ]
    cyclic = cyclic_nodes({str(node): set() for node in node_ids}, edge_pairs)
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
    values: list[object] = [document]
    commands: list[str] = []
    while values:
        value = values.pop()
        if isinstance(value, Mapping):
            commands.extend(
                item for key, item in value.items() if key == "run" and isinstance(item, str)
            )
            values.extend(item for key, item in value.items() if key != "run")
        elif isinstance(value, list):
            values.extend(value)
    command_surface = "\n".join(commands)
    missing = [token for token in WORKFLOW_TOKENS if token not in command_surface]
    permissions = document.get("permissions")
    if missing or not isinstance(permissions, Mapping) or permissions.get("contents") != "read":
        return [
            Finding(
                "CONTROL_PLANE_INVALID",
                WORKFLOW_PATH.as_posix(),
                ",".join(missing) or "read-only required",
            )
        ]
    return []


def _contract_findings(root: Path) -> list[Finding]:
    quality_path = root / QUALITY_ROOT
    if not quality_path.is_dir():
        return [Finding("SURFACE_MISSING", QUALITY_ROOT.as_posix(), "contract validator absent")]
    original_path = tuple(sys.path)
    modules = {name: sys.modules.get(name) for name in (
        "artifact_validation", "contract_catalog", "semantic_validation",
        "validation_types", "validator",
    )}
    try:
        sys.path.insert(0, str(quality_path))
        namespace = runpy.run_path(
            str(quality_path / "validator.py"),
            run_name="issue_0119_contract_validator",
        )
        contract_findings = namespace["validate"](root)
    except (OSError, UnicodeError, TypeError, ValueError, KeyError) as error:
        return [Finding("CONTRACT_VALIDATION_FAILED", CONTRACT_ROOT.as_posix(), str(error))]
    finally:
        sys.path[:] = original_path
        for name, module in modules.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module
    return [Finding(item.code, item.artifact, item.detail) for item in contract_findings]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0119 repository integration.")
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args(argv)
    findings = validate_repository_integration(args.repository_root)
    if findings:
        print(f"INTEGRATION FAILED ({len(findings)} finding(s))")
        for finding in findings:
            print(f"ERROR [{finding.code}] {finding.artifact} :: {finding.detail}")
        return 1
    print("INTEGRATION PASS")
    print("issue=ISSUE-0119 requirements=5 dependencies=STORY-0007,STORY-0008")
    return 0


if __name__ == "__main__":
    sys.exit(main())
