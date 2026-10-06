"""Capture architectural dependency inputs; never install packages or create uv.lock."""
import ast
import hashlib
import html
import json
import subprocess
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.tags import compatible_tags, cpython_tags
from packaging.utils import canonicalize_name, parse_wheel_filename
from packaging.version import Version

BASE = "926a6a8c9a69a838b165cca9df6c4ebb9c03c8d6"
CUTOFF = datetime.fromisoformat("2026-10-06T22:27:26+00:00")
OUT = Path("evidence/architecture/python-workspace-dependency-graph")
ENV = {
    "python_version": "3.12", "python_full_version": "3.12.13",
    "implementation_name": "cpython", "implementation_version": "3.12.13",
    "platform_python_implementation": "CPython", "os_name": "posix",
    "sys_platform": "linux", "platform_system": "Linux", "platform_machine": "x86_64",
    "extra": "", "platform_release": "", "platform_version": "",
}
platforms = [f"manylinux_2_{n}_x86_64" for n in range(28, 4, -1)]
platforms += ["manylinux2014_x86_64", "manylinux2010_x86_64", "manylinux1_x86_64", "linux_x86_64"]
TAGS = set(cpython_tags((3, 12), abis=["cp312"], platforms=platforms)) | set(compatible_tags((3, 12), interpreter="cp312", platforms=platforms))
manifest_paths = ["requirements-validation.txt", "src/backend/dsgeorref/contexts/identity_access/adapters/local_identity/requirements.txt"]
pins = {}
for path in manifest_paths:
    for text in Path(path).read_text(encoding="utf-8-sig").splitlines():
        req = Requirement(text)
        pin = next(iter(req.specifier)).version
        name = canonicalize_name(req.name)
        assert name not in pins or pins[name] == pin
        pins[name] = pin
extras = defaultdict(set, {"psycopg": {"binary"}})
cache = {}

def fetch(name, version=None):
    url = f"https://pypi.org/pypi/{name}/" + (f"{version}/" if version else "") + "json"
    if url not in cache:
        with urllib.request.urlopen(url, timeout=30) as response:
            cache[url] = json.load(response)
    return cache[url]

def eligible(file):
    return not file.get("yanked", False) and datetime.fromisoformat(file["upload_time_iso_8601"].replace("Z", "+00:00")) <= CUTOFF

def wheel_ok(file):
    if file["packagetype"] != "bdist_wheel" or not eligible(file):
        return False
    if file.get("requires_python") and Version("3.12.13") not in SpecifierSet(file["requires_python"]):
        return False
    return bool(parse_wheel_filename(file["filename"])[3] & TAGS)

def select(name, specs):
    if name in pins:
        candidates = [pins[name]]
    else:
        project = fetch(name)
        candidates = []
        for version, files in project["releases"].items():
            value = Version(version)
            if not value.is_prerelease and not value.is_devrelease and any(wheel_ok(f) for f in files):
                candidates.append(version)
        candidates.sort(key=Version, reverse=True)
    for version in candidates:
        if all(Version(version) in spec for spec in specs):
            metadata = fetch(name, version)
            if (not metadata["info"]["requires_python"] or Version("3.12.13") in SpecifierSet(metadata["info"]["requires_python"])) and any(wheel_ok(f) for f in metadata["urls"]):
                return version
    raise RuntimeError(f"No authorized compatible candidate for {name}: {specs}")

selected = dict(pins)
for iteration in range(30):
    requirements = defaultdict(list)
    next_extras = defaultdict(set, {"psycopg": {"binary"}})
    for name, version in sorted(selected.items()):
        for text in fetch(name, version)["info"]["requires_dist"] or []:
            req = Requirement(text)
            if req.marker and not any(req.marker.evaluate(ENV | {"extra": extra}) for extra in {""} | extras.get(name, set())):
                continue
            child = canonicalize_name(req.name)
            requirements[child].append(req.specifier)
            next_extras[child].update(req.extras)
    names = set(pins) | set(requirements)
    following = {name: select(name, requirements[name]) for name in sorted(names)}
    if following == selected and {k: v for k, v in next_extras.items() if v} == {k: v for k, v in extras.items() if v}:
        break
    selected, extras = following, next_extras
else:
    raise RuntimeError("Dependency metadata closure did not converge; no outputs approved")

metadata_records = []
edges = []
for name, version in sorted(selected.items()):
    data = fetch(name, version)
    files = [{k: f[k] for k in ("filename", "url", "digests", "requires_python", "upload_time_iso_8601")} for f in data["urls"] if wheel_ok(f)]
    record = {
        "name": name, "version": version, "requires_python": data["info"]["requires_python"],
        "requires_dist": data["info"]["requires_dist"] or [],
        "license_expression": data["info"].get("license_expression"),
        "license": data["info"].get("license"),
        "metadata_origin": f"https://pypi.org/pypi/{name}/{version}/json",
        "extras": sorted(extras.get(name, set())), "files": sorted(files, key=lambda f: f["filename"]),
    }
    for text in record["requires_dist"]:
        req = Requirement(text)
        if req.marker and not any(req.marker.evaluate(ENV | {"extra": extra}) for extra in {""} | extras.get(name, set())):
            continue
        child = canonicalize_name(req.name)
        assert child in selected and Version(selected[child]) in req.specifier, (name, text)
        edges.append({"parent": name, "child": child, "requirement": text})
    metadata_records.append(record)

imports = defaultdict(list)
for directory in ("src", "tools", "tests"):
    for path in Path(directory).rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig"))):
            names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module else []
            for imported in names:
                imports[imported.split(".")[0]].append({"path": path.as_posix(), "line": node.lineno})

sources = manifest_paths + ["pyproject.toml", ".python-version", "docs/03-engineering/TECHNOLOGY_BASELINE.yaml", "docs/03-engineering/TECHNOLOGY_BASELINE.md", "infra/images/native-stack.lock.yaml", "infra/images/native-stack.conda-lock.txt", "infra/images/native-stack.Dockerfile", "docs/03-engineering/contexts/engineering_governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/dependency-inventory.json", "evidence/implementation/contas-locais-bootstrap-unico-sessoes-tokens-e-ada/id-parte-2/VALIDATION-REPORT.json", "evidence/implementation/contas-locais-bootstrap-unico-sessoes-tokens-e-ada/auth-impl-dbschema-parte-1/VALIDATION-REPORT.json"]
source_records = []
for path in sources:
    blob = subprocess.check_output(["git", "show", f"{BASE}:{path}"])
    source_records.append({"path": path, "git_blob_sha256": hashlib.sha256(blob).hexdigest(), "worktree_bytes_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()})

snapshot = {
    "schema_version": "1.0.0", "artifact_version": "1.0.0", "base_sha": BASE,
    "selection_policy": "Preserve manifest pins; for newly required transitives select highest stable wheel-compatible release uploaded no later than source BASE commit timestamp; recompute all active metadata constraints to a fixed point. No package installation, runtime check or uv lock was performed.",
    "cutoff_utc": CUTOFF.isoformat(), "environment": ENV,
    "selected": selected, "packages": metadata_records, "active_edges": edges,
    "source_inputs": source_records,
    "import_evidence": {name: imports[name] for name in ("alembic", "sqlalchemy", "cryptography", "jwt", "psycopg", "yaml", "jsonschema", "celery", "pytest", "fastapi", "pydantic", "numpy", "rasterio", "shapely")},
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "resolution-inputs.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
for record in metadata_records:
    directory = OUT / "simple" / record["name"]
    directory.mkdir(parents=True, exist_ok=True)
    links = []
    for file in record["files"]:
        href = html.escape(file["url"] + "#sha256=" + file["digests"]["sha256"], quote=True)
        requires = html.escape(file["requires_python"] or "", quote=True)
        links.append(f'<a href="{href}" data-requires-python="{requires}">{html.escape(file["filename"])}</a><br>')
    (directory / "index.html").write_text('<!DOCTYPE html>\n<html><body>\n' + '\n'.join(links) + '\n</body></html>\n', encoding="utf-8", newline="\n")
(OUT / "simple" / "index.html").write_text('<!DOCTYPE html>\n<html><body>\n' + '\n'.join(f'<a href="{name}/">{name}</a><br>' for name in sorted(selected)) + '\n</body></html>\n', encoding="utf-8", newline="\n")
print(json.dumps({"packages": len(selected), "active_edges": len(edges), "selected": selected}))
