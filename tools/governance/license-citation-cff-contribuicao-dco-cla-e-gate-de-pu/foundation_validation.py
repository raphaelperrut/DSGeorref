from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

import yaml

SLUG = "license-citation-cff-contribuicao-dco-cla-e-gate-de-pu"
ROOT = Path(__file__).resolve().parents[3]
FOUNDATION_ROOT = ROOT / "docs/03-engineering/contexts/engineering_governance" / SLUG
CHECKPOINT_PATH = Path(__file__).with_name("foundation-checkpoint.json")
LICENSE_INVENTORY_PATH = FOUNDATION_ROOT / "license-inventory.json"
DEPENDENCY_INVENTORY_PATH = FOUNDATION_ROOT / "dependency-inventory.json"

EXPECTED_REQUIREMENTS = [
    "REQ-CIT-001",
    "REQ-EPIC-042",
    "REQ-OSS-001",
    "REQ-PUB-002",
]
EXPECTED_LICENSES = {
    "AGPL-3.0-or-later": (
        "LICENSES/AGPL-3.0-or-later.txt",
        "GNU AFFERO GENERAL PUBLIC LICENSE",
    ),
    "Apache-2.0": ("LICENSES/Apache-2.0.txt", "Apache License"),
    "CC-BY-4.0": (
        "LICENSES/CC-BY-4.0.txt",
        "Creative Commons Attribution 4.0 International",
    ),
}
SIGNOFF_PATTERN = re.compile(
    r"^Signed-off-by:\s+[^<>\r\n]+\s+<[^<>\s]+@[^<>\s]+>\s*$",
    re.IGNORECASE | re.MULTILINE,
)
SAFE_REVISION_RANGE = re.compile(r"^[A-Za-z0-9_./@{}~^+\-]+\.\.[A-Za-z0-9_./@{}~^+\-]+$")


class FoundationValidationError(ValueError):
    """Raised when foundation evidence cannot be accepted."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FoundationValidationError(f"invalid JSON artifact: {path}") from exc
    if not isinstance(value, dict):
        raise FoundationValidationError(f"JSON artifact must be an object: {path}")
    return value


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise FoundationValidationError(message)


def _validate_citation_document(
    citation: Any,
    *,
    python_version: str,
    frontend_version: str,
) -> dict[str, Any]:
    _require(isinstance(citation, dict), "CITATION.cff must contain a mapping")
    allowed_fields = {
        "cff-version",
        "message",
        "title",
        "type",
        "authors",
        "repository-code",
        "version",
        "license",
    }
    _require(set(citation) == allowed_fields, "CITATION.cff fields are incomplete or unverified")
    _require(citation["cff-version"] == "1.2.0", "unsupported CFF version")
    _require(citation["title"] == "DSGeorref", "citation title does not identify DSGeorref")
    _require(citation["type"] == "software", "citation type must be software")
    _require(
        citation["repository-code"] == "https://github.com/raphaelperrut/DSGeorref",
        "citation repository does not match the canonical repository",
    )
    _require(citation["license"] == "AGPL-3.0-or-later", "citation license is incompatible")
    _require(
        isinstance(citation["message"], str) and citation["message"].strip(), "missing message"
    )

    authors = citation["authors"]
    _require(isinstance(authors, list) and len(authors) > 0, "citation must name an author")
    for author in authors:
        _require(isinstance(author, dict), "citation author must be a mapping")
        _require(
            isinstance(author.get("given-names"), str)
            and isinstance(author.get("family-names"), str),
            "citation author must have given-names and family-names",
        )

    _require(
        citation["version"] == python_version == frontend_version,
        "citation version diverges from package metadata",
    )
    return {"artifact": "CITATION.cff", "version": citation["version"], "status": "PASS"}


def validate_citation(root: Path = ROOT) -> dict[str, Any]:
    citation_path = root / "CITATION.cff"
    try:
        citation = yaml.safe_load(citation_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise FoundationValidationError("CITATION.cff is missing or invalid YAML") from exc

    with (root / "pyproject.toml").open("rb") as pyproject_file:
        python_version = tomllib.load(pyproject_file)["project"]["version"]
    frontend_version = json.loads((root / "src/frontend/package.json").read_text(encoding="utf-8"))[
        "version"
    ]
    return _validate_citation_document(
        citation,
        python_version=python_version,
        frontend_version=frontend_version,
    )


def _matches(path: str, pattern: str) -> bool:
    if "/" not in pattern and "/" in path:
        return False
    return fnmatch.fnmatchcase(path, pattern)


def classify_paths(inventory: dict[str, Any], paths: list[str]) -> dict[str, str]:
    classes = inventory.get("classes")
    _require(isinstance(classes, list) and classes, "license classes are missing")
    license_patterns = inventory.get("license_file_patterns")
    _require(isinstance(license_patterns, list), "license file patterns are missing")
    asset_extensions = set(inventory.get("asset_extensions", []))
    asset_records = {
        record["path"]: record
        for record in inventory.get("asset_records", [])
        if isinstance(record, dict) and isinstance(record.get("path"), str)
    }

    assignments: dict[str, str] = {}
    for path in paths:
        suffix = Path(path).suffix.lower()
        if suffix in asset_extensions:
            record = asset_records.get(path)
            _require(record is not None, f"asset has no explicit license record: {path}")
            license_id = record.get("license")
            _require(
                isinstance(license_id, str) and license_id, f"asset license is missing: {path}"
            )
            assignments[path] = license_id
            continue

        if any(_matches(path, pattern) for pattern in license_patterns):
            assignments[path] = "LICENSE-TEXT"
            continue

        matching_classes = [
            item
            for item in classes
            if any(_matches(path, pattern) for pattern in item.get("patterns", []))
        ]
        _require(matching_classes, f"tracked path has no license class: {path}")
        license_ids = {item.get("license") for item in matching_classes}
        _require(len(license_ids) == 1, f"tracked path has ambiguous license classes: {path}")
        license_id = next(iter(license_ids))
        _require(isinstance(license_id, str), f"invalid license class for path: {path}")
        assignments[path] = license_id
    return assignments


def _tracked_files(root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    _require(completed.returncode == 0, "unable to enumerate tracked repository files")
    return [line.strip().replace("\\", "/") for line in completed.stdout.splitlines() if line]


def validate_license_inventory(
    root: Path = ROOT,
    *,
    tracked_files: list[str] | None = None,
) -> dict[str, Any]:
    inventory_path = root / LICENSE_INVENTORY_PATH.relative_to(ROOT)
    inventory = _load_json(inventory_path)
    _require(inventory.get("unknown_or_ambiguous") == "REJECT", "license fallback must reject")

    class_map = {item.get("license"): item for item in inventory.get("classes", [])}
    _require(set(class_map) == set(EXPECTED_LICENSES), "layered license classes are incomplete")
    for license_id, (relative_path, marker) in EXPECTED_LICENSES.items():
        item = class_map[license_id]
        _require(item.get("license_text") == relative_path, f"wrong license text for {license_id}")
        license_path = root / relative_path
        try:
            license_text = license_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise FoundationValidationError(f"missing license text: {relative_path}") from exc
        _require(
            len(license_text) > 5_000 and marker in license_text,
            f"invalid license text: {relative_path}",
        )

    assignments = classify_paths(inventory, tracked_files or _tracked_files(root))
    reuse_text = (root / ".reuse/dep5").read_text(encoding="utf-8")
    for license_id in EXPECTED_LICENSES:
        _require(f"License: {license_id}" in reuse_text, f"REUSE metadata misses {license_id}")

    notice = (root / "NOTICE").read_text(encoding="utf-8")
    third_party = (root / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    _require("Copyright 2026 Raphael Perrut" in notice, "project NOTICE is incomplete")
    _require("complete SBOM" in third_party, "third-party notice omits release SBOM policy")
    return {
        "assigned_paths": len(assignments),
        "license_classes": sorted(class_map),
        "status": "PASS",
    }


def _parse_pinned_requirements(path: Path) -> dict[str, str]:
    dependencies: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        _require(line.count("==") == 1, f"dependency is not exactly pinned: {line}")
        name, version = line.split("==")
        _require(name not in dependencies, f"duplicate dependency: {name}")
        dependencies[name] = version
    return dependencies


def validate_dependency_inventory(root: Path = ROOT) -> dict[str, Any]:
    inventory_path = root / DEPENDENCY_INVENTORY_PATH.relative_to(ROOT)
    inventory = _load_json(inventory_path)
    _require(inventory.get("requirement") == "REQ-OSS-001", "dependency requirement is missing")
    _require(inventory.get("unknown_or_unpinned_dependency") == "REJECT", "dependency fallback")
    _require(inventory.get("runtime") == [], "foundation declares unexpected runtime dependencies")

    records = inventory.get("development_and_validation")
    _require(isinstance(records, list), "dependency records are missing")
    keyed: dict[tuple[str, str], dict[str, Any]] = {}
    for record in records:
        _require(isinstance(record, dict), "dependency record must be an object")
        key = (record.get("ecosystem"), record.get("name"))
        _require(all(isinstance(value, str) and value for value in key), "invalid dependency key")
        _require(key not in keyed, f"duplicate inventory dependency: {key}")
        _require(isinstance(record.get("version"), str), f"missing dependency version: {key}")
        _require(isinstance(record.get("license"), str), f"missing dependency license: {key}")
        keyed[key] = record

    expected_python = _parse_pinned_requirements(root / "requirements-validation.txt")
    with (root / "pyproject.toml").open("rb") as pyproject_file:
        runtime_python = tomllib.load(pyproject_file)["project"]["dependencies"]
    _require(
        runtime_python == [], "runtime Python dependencies require release compatibility review"
    )
    inventoried_python = {
        name: record["version"]
        for (ecosystem, name), record in keyed.items()
        if ecosystem == "pypi"
    }
    _require(
        inventoried_python == expected_python, "Python dependency inventory diverges from pins"
    )

    frontend = json.loads((root / "src/frontend/package.json").read_text(encoding="utf-8"))
    _require(not frontend.get("dependencies"), "runtime npm dependencies require release review")
    expected_node = frontend.get("devDependencies", {})
    inventoried_node = {
        name: record["version"] for (ecosystem, name), record in keyed.items() if ecosystem == "npm"
    }
    _require(
        inventoried_node == expected_node, "npm dependency inventory diverges from package.json"
    )

    pnpm_lock = yaml.safe_load((root / "pnpm-lock.yaml").read_text(encoding="utf-8"))
    locked_node = pnpm_lock["importers"]["src/frontend"]["devDependencies"]
    for name, version in expected_node.items():
        _require(
            str(locked_node[name]["specifier"]) == version, f"npm dependency is not locked: {name}"
        )

    notices = (root / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    for record in records:
        marker = f"| {record['name']} | {record['version']} | {record['license']} |"
        _require(marker in notices, f"third-party notice missing dependency: {record['name']}")
    return {"direct_dependencies": len(records), "runtime_dependencies": 0, "status": "PASS"}


def validate_contribution_policy(root: Path = ROOT) -> dict[str, Any]:
    contributing = (root / "CONTRIBUTING.md").read_text(encoding="utf-8")
    required_markers = [
        "Developer Certificate of Origin 1.1",
        "Signed-off-by: Nome do Contribuidor <email@example.com>",
        "git commit -s",
        "inbound=outbound",
        "CLA não é exigido",
        "fallback para DCO ausente",
    ]
    for marker in required_markers:
        _require(marker in contributing, f"contribution policy is missing: {marker}")
    return {"origin_certification": "DCO-1.1", "cla": "NOT_REQUIRED", "status": "PASS"}


def validate_dco_messages(messages: list[tuple[str, str]]) -> dict[str, Any]:
    unsigned = [
        commit_sha for commit_sha, message in messages if not SIGNOFF_PATTERN.search(message)
    ]
    _require(not unsigned, f"unsigned external commits: {', '.join(unsigned)}")
    return {"commits_checked": len(messages), "status": "PASS"}


def validate_dco_commit_range(commit_range: str, root: Path = ROOT) -> dict[str, Any]:
    _require(bool(SAFE_REVISION_RANGE.fullmatch(commit_range)), "unsafe or invalid commit range")
    completed = subprocess.run(
        ["git", "log", "--no-merges", "--format=%H%x00%B%x00", commit_range, "--"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    _require(completed.returncode == 0, "commit range cannot be resolved")
    parts = completed.stdout.split("\x00")
    messages = [
        (parts[index].strip(), parts[index + 1].strip())
        for index in range(0, len(parts) - 1, 2)
        if parts[index].strip()
    ]
    return validate_dco_messages(messages)


def validate_checkpoint(root: Path = ROOT) -> dict[str, Any]:
    checkpoint_path = root / CHECKPOINT_PATH.relative_to(ROOT)
    checkpoint = _load_json(checkpoint_path)
    _require(
        checkpoint.get("requirements") == EXPECTED_REQUIREMENTS, "checkpoint requirements diverge"
    )
    _require(checkpoint.get("foundation_state") == "MATERIALIZED", "foundation is not materialized")
    _require(
        checkpoint.get("local_command")
        == checkpoint.get("ci_command")
        == checkpoint.get("reproducible_command"),
        "local and CI commands diverge",
    )
    for artifact in checkpoint.get("artifacts", []):
        _require((root / artifact).is_file(), f"checkpoint artifact is missing: {artifact}")
    publication_gate = checkpoint.get("publication_gate", {})
    _require(
        publication_gate.get("failure_mode") == "FAIL_CLOSED", "publication gate is not fail-closed"
    )
    _require(
        publication_gate.get("decision") == "BLOCK_UNLESS_ALL_APPLICABLE_EVIDENCE_PASSES",
        "publication gate has a permissive decision",
    )
    _require(
        publication_gate.get("current_decision") == "BLOCKED", "publication readiness is unproven"
    )
    return checkpoint


def evaluate_publication_gate(
    checkpoint: dict[str, Any],
    *,
    dco_verified: bool,
) -> dict[str, Any]:
    candidate_evidence = checkpoint["publication_gate"]["candidate_evidence"]
    blockers = [
        name
        for name, status in candidate_evidence.items()
        if status != "PASS" and not (name == "DCO_AUTOMATED_CHECK" and dco_verified)
    ]
    if blockers:
        return {"decision": "BLOCKED", "blockers": sorted(blockers), "status": "PASS"}
    return {"decision": "PASS", "blockers": [], "status": "PASS"}


def validate_foundation(
    root: Path = ROOT,
    *,
    commit_range: str | None = None,
) -> dict[str, Any]:
    checkpoint = validate_checkpoint(root)
    checks: dict[str, Any] = {
        "checkpoint": {"status": "PASS"},
        "citation": validate_citation(root),
        "licensing": validate_license_inventory(root),
        "dependencies": validate_dependency_inventory(root),
        "contribution": validate_contribution_policy(root),
    }
    if commit_range is not None:
        checks["dco"] = validate_dco_commit_range(commit_range, root)
    else:
        checks["dco"] = {"status": "NOT_REQUESTED", "reason": "no external commit range"}
    return {
        "schema_version": "1.0.0",
        "issue_id": checkpoint["identity"]["issue_id"],
        "decision": "PASS",
        "checks": checks,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the ISSUE-0142 governance foundation")
    parser.add_argument("--commit-range", help="External contribution range in base..head form")
    parser.add_argument(
        "--publication-gate",
        action="store_true",
        help="Evaluate release evidence and fail closed while any evidence is absent",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        report = validate_foundation(commit_range=args.commit_range)
        if args.publication_gate:
            checkpoint = validate_checkpoint()
            gate = evaluate_publication_gate(checkpoint, dco_verified=args.commit_range is not None)
            report["publication_gate"] = gate
            report["decision"] = gate["decision"]
            print(json.dumps(report, indent=2, sort_keys=True))
            return 0 if gate["decision"] == "PASS" else 1
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except FoundationValidationError as exc:
        print(
            json.dumps(
                {
                    "schema_version": "1.0.0",
                    "issue_id": "ISSUE-0142",
                    "decision": "ERROR",
                    "error": str(exc),
                },
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
