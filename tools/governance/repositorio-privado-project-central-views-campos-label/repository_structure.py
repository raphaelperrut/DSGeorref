from __future__ import annotations

import ast
import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, order=True)
class StructureFinding:
    code: str
    artifact: str
    detail: str


def module_findings(repository_root: Path, tool_root: Path) -> tuple[StructureFinding, ...]:
    files = sorted((repository_root / tool_root).rglob("*.py"))
    graph: dict[str, set[str]] = {}
    digests: dict[str, str] = {}
    findings: list[StructureFinding] = []
    for path in files:
        relative = path.relative_to(repository_root).as_posix()
        node = path.relative_to(repository_root / tool_root).with_suffix("").as_posix()
        try:
            content = path.read_bytes()
            tree = ast.parse(content, filename=relative)
        except (OSError, SyntaxError) as error:
            findings.append(StructureFinding("PYTHON_MODULE_INVALID", relative, str(error)))
            continue
        digest = hashlib.sha256(content).hexdigest()
        if len(content) > 200 and digest in digests:
            findings.append(StructureFinding("RULE_DUPLICATED", relative, digests[digest]))
        digests[digest] = relative
        siblings = {item.stem for item in path.parent.glob("*.py")}
        graph[node] = {
            f"{path.parent.relative_to(repository_root / tool_root).as_posix()}/{name}".lstrip(
                "./"
            )
            for name in _imported_names(tree).intersection(siblings)
        }
    cyclic = cyclic_nodes(graph)
    if cyclic:
        findings.append(
            StructureFinding("PYTHON_IMPORT_CYCLE", tool_root.as_posix(), ",".join(cyclic))
        )
    return tuple(sorted(findings))


def cyclic_nodes(
    graph: Mapping[str, set[str]], edges: Sequence[tuple[str, str]] = ()
) -> tuple[str, ...]:
    remaining = {node: set(dependencies) for node, dependencies in graph.items()}
    for source, target in edges:
        remaining.setdefault(source, set())
        remaining.setdefault(target, set()).add(source)
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


def _imported_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in getattr(tree, "body", ()):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.rsplit(".", 1)[-1])
        elif isinstance(node, ast.Import):
            names.update(alias.name.rsplit(".", 1)[-1] for alias in node.names)
    return names
