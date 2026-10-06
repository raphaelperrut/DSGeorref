"""Stdlib-only structural/integrity checks; never resolve, install or write uv.lock."""
import argparse
import ast
import hashlib
import json
import re
import subprocess
import tomllib
from pathlib import Path
from urllib.parse import urlparse

D = Path("docs/02-architecture/design-reviews/python-workspace-dependency-graph")
E = Path("evidence/architecture/python-workspace-dependency-graph")
INDEX = "file:///opt/dsgeorref-python-inputs/simple"
BASE = "926a6a8c9a69a838b165cca9df6c4ebb9c03c8d6"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(lock_path=None, verify_digests=False):
    graph = json.loads((D / "approved-dependency-graph.yaml").read_text(encoding="utf-8"))
    snapshot = json.loads((E / "resolution-inputs.json").read_text(encoding="utf-8"))
    assert graph["base_sha"] == snapshot["base_sha"] == BASE
    assert graph["schema_version"] == graph["artifact_version"] == "1.0.0"
    assert not graph["review"]["approval_claimed"]
    direct = graph["direct_dependencies"]
    transitive = graph["transitive_dependencies"]
    expected = {p["name"]: p["version"] for p in direct + transitive}
    assert len(expected) == len(direct) + len(transitive) == 43
    assert expected == snapshot["selected"]
    assert len(direct) == 11 and len(transitive) == 32
    constraints = [line for line in (D / "constraints.txt").read_text(encoding="utf-8").splitlines() if line and not line.startswith("#")]
    assert len(constraints) == len(set(constraints)) == 31
    assert constraints == [p["name"] + "==" + p["version"] for p in transitive if p["constraint_file_entry"]]
    assert {p["name"] for p in transitive if not p["constraint_file_entry"]} == {"psycopg-binary"}
    assert expected["psycopg"] == expected["psycopg-binary"] == "3.3.6"
    assert expected["sqlalchemy"] == "2.1.2"
    assert expected["mako"] == "1.4.3" and expected["markupsafe"] == "3.0.3" and expected["typing-extensions"] == "4.16.0"
    proposed = tomllib.loads((E / "pyproject-proposed.toml").read_text(encoding="utf-8"))
    additions = tomllib.loads((E / "pyproject-additions.toml").read_text(encoding="utf-8"))
    assert proposed["project"]["dependencies"] == graph["groups"]["runtime"]
    assert proposed["project"]["requires-python"] == ">=3.12,<3.13"
    assert proposed["dependency-groups"] == {g: graph["groups"][g] for g in ("dev", "test")}
    assert proposed["tool"]["uv"] == additions["tool"]["uv"]
    assert proposed["tool"]["uv"]["constraint-dependencies"] == constraints
    assert proposed["tool"]["uv"]["environments"] == [graph["transitive_policy"]["markers"]]
    assert proposed["tool"]["uv"]["default-groups"] == []
    assert proposed["tool"]["uv"]["package"] is False
    config = tomllib.loads((E / "resolver-config.toml").read_text(encoding="utf-8"))
    assert config["required-version"] == "==0.12.19"
    assert config["index"] == [{"name": "approved-python-snapshot", "url": INDEX, "default": True}]
    assert config["no-build"] and config["python-downloads"] == "never" and config["prerelease"] == "disallow"
    static = {p["name"]: p for p in config["dependency-metadata"]}
    assert set(static) == set(expected)
    artifacts = {}
    for p in snapshot["packages"]:
        assert p["version"] == expected[p["name"]] == static[p["name"]]["version"]
        assert p["requires_dist"] == static[p["name"]]["requires-dist"]
        assert (p["requires_python"] or "") == static[p["name"]]["requires-python"]
        assert p["extras"] == static[p["name"]]["provides-extra"]
        assert p["files"]
        page = (E / "simple" / p["name"] / "index.html").read_text(encoding="utf-8")
        assert len(re.findall('<a href=', page)) == len(p["files"])
        for f in p["files"]:
            assert f["filename"].endswith(".whl")
            assert urlparse(f["url"]).hostname == "files.pythonhosted.org"
            assert re.fullmatch(r"[0-9a-f]{64}", f["digests"]["sha256"])
            assert f["digests"]["sha256"] in page and f["filename"] in page
            assert f["url"] not in artifacts
            artifacts[f["url"]] = "sha256:" + f["digests"]["sha256"]
    assert len(snapshot["active_edges"]) == 47
    reachable = {p["name"] for p in direct}
    while True:
        following = reachable | {edge["child"] for edge in snapshot["active_edges"] if edge["parent"] in reachable}
        if following == reachable:
            break
        reachable = following
    assert reachable == set(expected)
    for edge in snapshot["active_edges"]:
        assert edge["parent"] in expected and edge["child"] in expected
    for p in direct:
        assert p["requirement"] in graph["groups"][p["group"]]
        assert p["extras"] == (["binary"] if p["name"] == "psycopg" else [])
        assert all(Path(authority).is_file() for authority in p["authority"])
    for authority in snapshot["source_inputs"]:
        blob = subprocess.check_output(["git", "show", f"{BASE}:{authority['path']}"])
        assert hashlib.sha256(blob).hexdigest() == authority["git_blob_sha256"]
        if authority["path"] != "pyproject.toml" or not lock_path:
            assert Path(authority["path"]).read_text(encoding="utf-8-sig").replace("\r\n", "\n") == blob.decode("utf-8-sig").replace("\r\n", "\n")
    for package, hits in snapshot["import_evidence"].items():
        for hit in hits:
            path = Path(hit["path"])
            assert path.is_file() and 0 < hit["line"] <= len(path.read_text(encoding="utf-8-sig").splitlines())
    for document in ("rationale.md", "devops-handoff.md"):
        text = (D / document).read_text(encoding="utf-8")
        assert all(value in text for value in (BASE, "3.3.6", "3.2.9", "2.1.2", "2.0.x", "0.12.19", "digests.json")), document
    for path in list(D.iterdir()) + [p for p in E.rglob("*") if p.is_file()]:
        data = path.read_bytes()
        data.decode("utf-8")
        assert b"\r" not in data, path
        if path.suffix == ".py":
            ast.parse(data.decode("utf-8"), filename=str(path), feature_version=(3, 12))
    if verify_digests:
        manifest = json.loads((E / "digests.json").read_text(encoding="utf-8"))
        actual_paths = {p.as_posix() for p in list(D.iterdir()) + list(E.rglob("*")) if p.is_file() and p != E / "digests.json"}
        assert actual_paths == {item["path"] for item in manifest["files"]}
        for item in manifest["files"]:
            path = Path(item["path"])
            assert path.stat().st_size == item["bytes"] and digest(path) == item["sha256"], path
    if lock_path:
        lock = tomllib.loads(Path(lock_path).read_text(encoding="utf-8"))
        assert Path("pyproject.toml").read_bytes() == (E / "pyproject-proposed.toml").read_bytes()
        packages = lock["package"]
        root = [p for p in packages if p["name"] == "dsgeorref"]
        assert len(root) == 1 and root[0]["version"] == "0.0.0" and root[0]["source"] == {"virtual": "."}
        third_party = [p for p in packages if p["name"] != "dsgeorref"]
        assert len(third_party) == len(expected)
        assert {p["name"]: p["version"] for p in third_party} == expected
        for p in third_party:
            assert p["source"] == {"registry": INDEX}
            assert not p.get("sdist"), "source builds not approved"
            assert p.get("wheels"), p["name"]
            for wheel in p["wheels"]:
                assert artifacts.get(wheel["url"]) == wheel["hash"], wheel
    else:
        assert not Path("uv.lock").exists(), "uv.lock is forbidden in this author pass"
    return {"status": "PASS", "scope": "structural only", "direct_dependencies": 11, "transitive_dependencies": 32, "distributions": 43, "active_edges": 47, "constraints": 31, "admitted_wheels": len(artifacts), "digests_verified": verify_digests, "lock_checked": bool(lock_path), "runtime_or_abi_test": False, "make_verify": "NOT_RUN_USER_INSTRUCTION", "independent_approval": "NOT_CLAIMED"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-digests", action="store_true")
    parser.add_argument("--check-lock")
    args = parser.parse_args()
    print(json.dumps(check(args.check_lock, args.verify_digests), ensure_ascii=False))
