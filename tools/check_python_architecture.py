from __future__ import annotations

import ast
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "contracts/architecture/python-module-boundaries.yaml"
EXCEPTION_PATH = ROOT / "docs/02-architecture/design-reviews/PYTHON_ARCHITECTURE_EXCEPTIONS.yaml"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def module_name(path: Path) -> str:
    rel = path.relative_to(ROOT).with_suffix("")
    parts = list(rel.parts)
    if parts[:3] == ["src", "backend", "dsgeorref"]:
        parts = parts[2:]
    elif parts[:3] == ["src", "geo", "dsgeorref_geo"]:
        parts = parts[2:]
    elif parts[:3] == ["src", "ai", "dsgeorref_ai"]:
        parts = parts[2:]
    else:
        parts = parts[1:]
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def resolve_relative(current: str, level: int, imported: str | None) -> str:
    base = current.split(".")[:-1]
    keep = max(0, len(base) - level + 1)
    prefix = base[:keep]
    if imported:
        prefix.extend(imported.split("."))
    return ".".join(prefix)


def branch_points(node: ast.AST) -> int:
    points = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.IfExp, ast.comprehension)):
            points += 1
        elif isinstance(child, ast.Try):
            points += len(child.handlers) + bool(child.orelse) + bool(child.finalbody)
        elif isinstance(child, ast.Match):
            points += len(child.cases)
        elif isinstance(child, ast.BoolOp):
            points += max(0, len(child.values) - 1)
    return points


def exception_keys() -> set[str]:
    if not EXCEPTION_PATH.exists():
        return set()
    data = load_yaml(EXCEPTION_PATH)
    keys = set()
    for item in data.get("exceptions", []):
        path = item.get("path")
        symbol = item.get("symbol")
        if path:
            keys.add(path if not symbol else f"{path}::{symbol}")
    return keys


def main() -> int:
    policy = load_yaml(POLICY_PATH)
    limits = policy["limits"]
    exceptions = exception_keys()
    errors: list[str] = []
    notices: list[str] = []
    python_files = sorted((ROOT / "src").rglob("*.py"))
    parsed: dict[Path, ast.Module] = {}
    modules: dict[str, Path] = {}
    imports: dict[str, set[str]] = defaultdict(set)
    function_hashes: dict[str, list[str]] = defaultdict(list)

    generic_names = set(policy.get("prohibited_generic_modules", []))

    for path in python_files:
        rel = path.relative_to(ROOT).as_posix()
        if re_search := ("/epic-" in f"/{rel}" or "/issue-" in f"/{rel}"):
            errors.append(f"path orientado a backlog: {rel}")
        if path.name in generic_names:
            errors.append(f"módulo genérico proibido: {rel}")

        lines = path.read_text(encoding="utf-8").splitlines()
        file_review = limits["file_lines"]["review"]
        file_hard = limits["file_lines"]["hard"]
        if len(lines) > file_hard:
            errors.append(f"arquivo acima do limite hard ({len(lines)}>{file_hard}): {rel}")
        elif len(lines) > file_review and rel not in exceptions:
            errors.append(f"arquivo exige Design Review ({len(lines)}>{file_review}): {rel}")

        try:
            tree = ast.parse("\n".join(lines) + "\n", filename=rel, feature_version=(3, 12))
        except SyntaxError as exc:
            errors.append(f"sintaxe incompatível com Python 3.12 em {rel}:{exc.lineno}: {exc.msg}")
            continue
        parsed[path] = tree
        mod = module_name(path)
        modules[mod] = path

        top_defs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        top_review = limits["top_level_definitions"]["review"]
        top_hard = limits["top_level_definitions"]["hard"]
        if len(top_defs) > top_hard:
            errors.append(f"definições top-level acima do limite hard ({len(top_defs)}>{top_hard}): {rel}")
        elif len(top_defs) > top_review and rel not in exceptions:
            errors.append(f"definições top-level exigem Design Review ({len(top_defs)}>{top_review}): {rel}")

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and any(a.name == "*" for a in node.names):
                errors.append(f"import * proibido em {rel}:{node.lineno}")
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                length = (node.end_lineno or node.lineno) - node.lineno + 1
                key = f"{rel}::{node.name}"
                review = limits["function_lines"]["review"]
                hard = limits["function_lines"]["hard"]
                if length > hard:
                    errors.append(f"função acima do limite hard ({length}>{hard}): {key}")
                elif length > review and key not in exceptions:
                    errors.append(f"função exige Design Review ({length}>{review}): {key}")
                branches = branch_points(node)
                branch_review = limits["approximate_branch_points"]["review"]
                branch_hard = limits["approximate_branch_points"]["hard"]
                if branches > branch_hard:
                    errors.append(f"branch points acima do limite hard ({branches}>{branch_hard}): {key}")
                elif branches > branch_review and key not in exceptions:
                    errors.append(f"branch points exigem Design Review ({branches}>{branch_review}): {key}")
                if length >= 12 and len(node.body) >= 4:
                    normalized = ast.dump(ast.Module(body=node.body, type_ignores=[]), include_attributes=False)
                    digest = hashlib.sha256(normalized.encode()).hexdigest()
                    function_hashes[digest].append(key)
            elif isinstance(node, ast.ClassDef):
                public = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("_")]
                key = f"{rel}::{node.name}"
                review = limits["public_methods_per_class"]["review"]
                hard = limits["public_methods_per_class"]["hard"]
                if len(public) > hard:
                    errors.append(f"classe acima do limite hard de métodos públicos ({len(public)}>{hard}): {key}")
                elif len(public) > review and key not in exceptions:
                    errors.append(f"classe exige Design Review ({len(public)}>{review}): {key}")

        for node in tree.body:
            if isinstance(node, ast.Import):
                imports[mod].update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                target = resolve_relative(mod, node.level, node.module) if node.level else (node.module or "")
                if target:
                    imports[mod].add(target)

    # Layer rules and internal graph.
    external_forbidden = {
        "dsgeorref.domain": {"fastapi", "starlette", "sqlalchemy", "alembic", "celery", "kombu", "rasterio", "pyproj", "shapely", "cv2"},
        "dsgeorref.application": {"fastapi", "starlette", "sqlalchemy", "alembic", "celery", "kombu"},
        "dsgeorref_geo": {"fastapi", "starlette", "celery", "sqlalchemy"},
        "dsgeorref_ai": {"fastapi", "starlette", "celery", "sqlalchemy"},
    }
    internal_graph: dict[str, set[str]] = {m: set() for m in modules}
    for mod, targets in imports.items():
        for prefix, forbidden in external_forbidden.items():
            if mod == prefix or mod.startswith(prefix + "."):
                for target in targets:
                    root = target.split(".")[0]
                    if root in forbidden:
                        errors.append(f"dependência de camada proibida: {mod} -> {target}")
        for target in targets:
            match = target if target in modules else next((m for m in modules if target.startswith(m + ".")), None)
            if match:
                internal_graph[mod].add(match)

    state = {m: 0 for m in modules}
    stack: list[str] = []

    def visit(mod: str) -> bool:
        state[mod] = 1
        stack.append(mod)
        for target in internal_graph[mod]:
            if state[target] == 0:
                if not visit(target):
                    return False
            elif state[target] == 1:
                cycle = stack[stack.index(target):] + [target]
                errors.append("ciclo de imports: " + " -> ".join(cycle))
                return False
        stack.pop()
        state[mod] = 2
        return True

    for mod in modules:
        if state[mod] == 0 and not visit(mod):
            break

    for locations in function_hashes.values():
        if len(locations) > 1:
            errors.append("implementação duplicada: " + " | ".join(sorted(locations)))

    if not python_files:
        notices.append("nenhum arquivo Python de produção criado; fitness functions preparadas para a SPRINT-001")

    if errors:
        print("PYTHON ARCHITECTURE FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("PYTHON ARCHITECTURE PASS")
    print(f"python_files: {len(python_files)}")
    print(f"modules: {len(modules)}")
    for notice in notices:
        print("notice:", notice)
    return 0


if __name__ == "__main__":
    sys.exit(main())
