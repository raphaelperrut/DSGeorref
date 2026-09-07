from __future__ import annotations

import argparse
import fnmatch
import hashlib
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
EXPECTED_FILE_CLASSES = {
    "application-code": ("AGPL-3.0-or-later", "LICENSES/AGPL-3.0-or-later.txt"),
    "reusable-contracts": ("Apache-2.0", "LICENSES/Apache-2.0.txt"),
    "original-documentation": ("CC-BY-4.0", "LICENSES/CC-BY-4.0.txt"),
}
EXPECTED_LICENSE_DIGESTS = {
    "LICENSES/AGPL-3.0-or-later.txt": (
        "d8a6cc31abc16b6748c7a21f21611f5a1ec33f67d22ca23d7da1c19b95496bee"
    ),
    "LICENSES/Apache-2.0.txt": ("074e6e32c86a4c0ef8b3ed25b721ca23aca83df277cd88106ef7177c354615ff"),
    "LICENSES/CC-BY-4.0.txt": ("d557539df68e771cc1eedcc91d13f70fca930e508d11eedcafa4b15db49e3744"),
}
EXPECTED_DEPENDENCY_LICENSES = {
    ("pypi", "PyYAML"): "MIT",
    ("pypi", "jsonschema"): "MIT",
    ("pypi", "cryptography"): "Apache-2.0 OR BSD-3-Clause",
    ("pypi", "celery"): "BSD-3-Clause",
    ("pypi", "psycopg[binary]"): "LGPL-3.0-only",
    ("pypi", "pytest"): "MIT",
    ("pypi", "ruff"): "MIT",
    ("pypi", "mypy"): "MIT",
    ("npm", "@playwright/test"): "Apache-2.0",
    ("npm", "@testing-library/dom"): "MIT",
    ("npm", "@types/node"): "MIT",
    ("npm", "jsdom"): "MIT",
    ("npm", "typescript"): "Apache-2.0",
    ("npm", "vitest"): "MIT",
}
ALLOWED_DEPENDENCY_LICENSES = frozenset(EXPECTED_DEPENDENCY_LICENSES.values())
EXPECTED_ASSET_EXTENSIONS = frozenset(
    {
        ".bin",
        ".dat",
        ".dbf",
        ".gif",
        ".gpkg",
        ".jpeg",
        ".jpg",
        ".onnx",
        ".pdf",
        ".png",
        ".pt",
        ".pth",
        ".shp",
        ".shx",
        ".tif",
        ".tiff",
        ".webp",
        ".zip",
    }
)
EXPECTED_CANDIDATE_EVIDENCE = {
    "DEPENDENCY_INVENTORY_AND_SBOM": frozenset({"REQUIRED_AT_RELEASE_CANDIDATE", "PASS"}),
    "DCO_AUTOMATED_CHECK": frozenset({"REQUIRES_CANDIDATE_COMMIT_RANGE", "PASS"}),
    "LEGAL_REVIEW_BEFORE_G6": frozenset({"NOT_PROVIDED", "PASS"}),
    "SECURITY_LICENSE_RESTORE_COMPATIBILITY_SCIENTIFIC_GATES": frozenset({"NOT_PROVIDED", "PASS"}),
}
PORTABLE_COMMAND = f"python -X utf8 tools/governance/{SLUG}/foundation_validation.py"
MAKE_VALIDATION_COMMAND = f"$(PYTHON) -X utf8 tools/governance/{SLUG}/foundation_validation.py"
MAKE_TEST_COMMAND = (
    f"$(PYTHON) -X utf8 -m pytest -q -p no:cacheprovider tests/fnd/{SLUG}/test_foundation.py"
)
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


def _validated_inventory_classes(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    classes = inventory.get("classes")
    _require(isinstance(classes, list) and classes, "license classes are missing")
    validated: list[dict[str, Any]] = []
    for item in classes:
        _require(isinstance(item, dict), "license class must be an object")
        _require(
            set(item) == {"id", "license", "license_text", "patterns"},
            "license class fields are incomplete or unknown",
        )
        class_id = item["id"]
        _require(
            isinstance(class_id, str) and class_id in EXPECTED_FILE_CLASSES,
            f"unknown license class: {class_id}",
        )
        expected_license, expected_text = EXPECTED_FILE_CLASSES[class_id]
        license_id = item["license"]
        _require(
            isinstance(license_id, str)
            and license_id in {item[0] for item in EXPECTED_FILE_CLASSES.values()},
            f"unknown file license expression: {license_id}",
        )
        _require(license_id == expected_license, f"license class mismatch: {class_id}")
        _require(item["license_text"] == expected_text, f"license text mismatch: {class_id}")
        patterns = item["patterns"]
        _require(
            isinstance(patterns, list)
            and bool(patterns)
            and all(isinstance(pattern, str) and pattern for pattern in patterns),
            f"invalid license patterns: {class_id}",
        )
        _require(len(patterns) == len(set(patterns)), f"duplicate license pattern: {class_id}")
        validated.append(item)
    _require(
        {item["id"] for item in validated} == set(EXPECTED_FILE_CLASSES),
        "layered license classes are incomplete",
    )
    return validated


def _validated_asset_records(inventory: dict[str, Any]) -> dict[str, dict[str, str]]:
    extensions = inventory.get("asset_extensions")
    _require(
        isinstance(extensions, list)
        and all(isinstance(extension, str) for extension in extensions)
        and set(extensions) == EXPECTED_ASSET_EXTENSIONS,
        "asset extension set is incomplete or unknown",
    )
    raw_records = inventory.get("asset_records")
    _require(isinstance(raw_records, list), "asset records must be a list")
    records: dict[str, dict[str, str]] = {}
    for record in raw_records:
        _require(isinstance(record, dict), "asset record must be an object")
        _require(set(record) == {"path", "license"}, "asset record fields are invalid")
        path = record["path"]
        license_id = record["license"]
        _require(
            isinstance(path, str)
            and bool(path)
            and "\\" not in path
            and not path.startswith("/")
            and ".." not in Path(path).parts,
            "asset record path is invalid",
        )
        _require(
            isinstance(license_id, str)
            and license_id in {item[0] for item in EXPECTED_FILE_CLASSES.values()},
            f"unknown asset license expression: {license_id}",
        )
        _require(path not in records, f"duplicate asset record: {path}")
        records[path] = record
    return records


def classify_paths(inventory: dict[str, Any], paths: list[str]) -> dict[str, str]:
    classes = _validated_inventory_classes(inventory)
    license_patterns = inventory.get("license_file_patterns")
    _require(
        license_patterns == ["LICENSE", "LICENSES/**"],
        "license file patterns are incomplete or unknown",
    )
    asset_records = _validated_asset_records(inventory)

    assignments: dict[str, str] = {}
    for path in paths:
        suffix = Path(path).suffix.lower()
        if suffix in EXPECTED_ASSET_EXTENSIONS:
            record = asset_records.get(path)
            _require(record is not None, f"asset has no explicit license record: {path}")
            assignments[path] = record["license"]
            continue

        if any(_matches(path, pattern) for pattern in license_patterns):
            assignments[path] = "LICENSE-TEXT"
            continue

        matching_classes = [
            item for item in classes if any(_matches(path, pattern) for pattern in item["patterns"])
        ]
        _require(matching_classes, f"tracked path has no license class: {path}")
        license_ids = {item["license"] for item in matching_classes}
        _require(len(license_ids) == 1, f"tracked path has ambiguous license classes: {path}")
        assignments[path] = next(iter(license_ids))
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


def _normalized_sha256(path: Path) -> str:
    try:
        content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    except OSError as exc:
        raise FoundationValidationError(f"missing license text: {path.as_posix()}") from exc
    return hashlib.sha256(content).hexdigest()


def validate_license_texts(root: Path = ROOT) -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative_path, expected_digest in EXPECTED_LICENSE_DIGESTS.items():
        digest = _normalized_sha256(root / relative_path)
        _require(digest == expected_digest, f"license text digest mismatch: {relative_path}")
        observed[relative_path] = digest
    return observed


def _parse_dep5(path: Path) -> list[dict[str, str]]:
    try:
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    except OSError as exc:
        raise FoundationValidationError(".reuse/dep5 is missing") from exc
    paragraphs: list[dict[str, str]] = []
    for raw_paragraph in text.split("\n\n"):
        if not raw_paragraph.strip():
            continue
        fields: dict[str, str] = {}
        previous_field: str | None = None
        for line in raw_paragraph.splitlines():
            if line.startswith((" ", "\t")):
                _require(previous_field is not None, "DEP5 continuation has no field")
                fields[previous_field] = f"{fields[previous_field]} {line.strip()}"
                continue
            _require(":" in line, f"malformed DEP5 line: {line}")
            name, value = line.split(":", 1)
            _require(name not in fields, f"duplicate DEP5 field: {name}")
            _require(bool(name) and bool(value.strip()), f"empty DEP5 field: {name}")
            fields[name] = value.strip()
            previous_field = name
        paragraphs.append(fields)
    return paragraphs


def validate_dep5_inventory(root: Path, inventory: dict[str, Any]) -> dict[str, list[str]]:
    classes = _validated_inventory_classes(inventory)
    dep5_by_license: dict[str, list[str]] = {}
    for paragraph in _parse_dep5(root / ".reuse/dep5"):
        if "Files" not in paragraph:
            continue
        _require(
            set(paragraph) == {"Files", "Copyright", "License"},
            "DEP5 license paragraph fields are invalid",
        )
        license_id = paragraph["License"]
        _require(
            license_id in {item[0] for item in EXPECTED_FILE_CLASSES.values()},
            f"unknown DEP5 license expression: {license_id}",
        )
        _require(license_id not in dep5_by_license, f"duplicate DEP5 license: {license_id}")
        _require(
            paragraph["Copyright"] == "2026 Raphael Perrut",
            f"DEP5 copyright mismatch: {license_id}",
        )
        patterns = paragraph["Files"].split()
        _require(len(patterns) == len(set(patterns)), f"duplicate DEP5 pattern: {license_id}")
        dep5_by_license[license_id] = patterns

    inventory_by_license = {item["license"]: item["patterns"] for item in classes}
    _require(
        set(dep5_by_license) == set(inventory_by_license),
        "DEP5 and license inventory cover different license expressions",
    )
    for license_id, patterns in inventory_by_license.items():
        _require(
            set(dep5_by_license[license_id]) == set(patterns),
            f"DEP5 patterns diverge from license inventory: {license_id}",
        )
    return dep5_by_license


def validate_license_inventory(
    root: Path = ROOT,
    *,
    tracked_files: list[str] | None = None,
) -> dict[str, Any]:
    inventory_path = root / LICENSE_INVENTORY_PATH.relative_to(ROOT)
    inventory = _load_json(inventory_path)
    _require(inventory.get("schema_version") == "1.0.0", "invalid license inventory version")
    _require(
        inventory.get("requirements") == ["REQ-EPIC-042", "REQ-OSS-001"],
        "license inventory requirements diverge",
    )
    _require(inventory.get("unknown_or_ambiguous") == "REJECT", "license fallback must reject")

    classes = _validated_inventory_classes(inventory)
    license_digests = validate_license_texts(root)
    dep5_assignments = validate_dep5_inventory(root, inventory)
    repository_paths = tracked_files if tracked_files is not None else _tracked_files(root)
    assignments = classify_paths(inventory, repository_paths)
    recorded_assets = set(_validated_asset_records(inventory))
    tracked_assets = {
        path for path in repository_paths if Path(path).suffix.lower() in EXPECTED_ASSET_EXTENSIONS
    }
    _require(recorded_assets == tracked_assets, "asset records diverge from tracked assets")

    notice = (root / "NOTICE").read_text(encoding="utf-8")
    third_party = (root / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    _require("Copyright 2026 Raphael Perrut" in notice, "project NOTICE is incomplete")
    _require("complete SBOM" in third_party, "third-party notice omits release SBOM policy")
    return {
        "assigned_paths": len(assignments),
        "dep5_license_classes": len(dep5_assignments),
        "license_classes": sorted(item["license"] for item in classes),
        "license_text_digests": license_digests,
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


def _index_dependency_records(records: Any) -> dict[tuple[str, str], dict[str, Any]]:
    _require(isinstance(records, list) and records, "dependency records are missing")
    keyed: dict[tuple[str, str], dict[str, Any]] = {}
    for record in records:
        _require(isinstance(record, dict), "dependency record must be an object")
        _require(
            set(record) == {"ecosystem", "name", "version", "license"},
            "dependency record fields are incomplete or unknown",
        )
        ecosystem = record.get("ecosystem")
        name = record.get("name")
        _require(
            isinstance(ecosystem, str) and ecosystem and isinstance(name, str) and name,
            "invalid dependency key",
        )
        key = (ecosystem, name)
        _require(key not in keyed, f"duplicate inventory dependency: {key}")
        _require(key in EXPECTED_DEPENDENCY_LICENSES, f"unknown dependency: {key}")
        _require(
            isinstance(record.get("version"), str) and bool(record["version"]),
            f"missing dependency version: {key}",
        )
        license_expression = record.get("license")
        _require(
            isinstance(license_expression, str)
            and license_expression in ALLOWED_DEPENDENCY_LICENSES,
            f"unknown dependency license expression: {license_expression}",
        )
        _require(
            license_expression == EXPECTED_DEPENDENCY_LICENSES[key],
            f"dependency license mismatch: {key}",
        )
        keyed[key] = record
    _require(
        set(keyed) == set(EXPECTED_DEPENDENCY_LICENSES),
        "dependency license inventory is incomplete",
    )
    return keyed


def validate_dependency_inventory(root: Path = ROOT) -> dict[str, Any]:
    inventory_path = root / DEPENDENCY_INVENTORY_PATH.relative_to(ROOT)
    inventory = _load_json(inventory_path)
    _require(
        set(inventory)
        == {
            "schema_version",
            "requirement",
            "inventory_scope",
            "source_manifests",
            "runtime",
            "development_and_validation",
            "redistribution",
            "release_sbom",
            "unknown_or_unpinned_dependency",
        },
        "dependency inventory fields are incomplete or unknown",
    )
    _require(inventory.get("schema_version") == "1.0.0", "invalid dependency inventory version")
    _require(inventory.get("requirement") == "REQ-OSS-001", "dependency requirement is missing")
    _require(
        inventory.get("inventory_scope") == "DIRECT_DECLARED_DEPENDENCIES",
        "dependency inventory scope diverges",
    )
    _require(
        inventory.get("source_manifests")
        == [
            "pyproject.toml",
            "requirements-validation.txt",
            "src/frontend/package.json",
            "pnpm-lock.yaml",
        ],
        "dependency source manifests diverge",
    )
    _require(inventory.get("unknown_or_unpinned_dependency") == "REJECT", "dependency fallback")
    _require(inventory.get("runtime") == [], "foundation declares unexpected runtime dependencies")
    _require(
        inventory.get("redistribution") == "NONE_IN_FOUNDATION_0.0.0",
        "dependency redistribution policy diverges",
    )
    _require(
        inventory.get("release_sbom") == "REQUIRED_AT_RELEASE_CANDIDATE",
        "release SBOM policy diverges",
    )

    records = inventory.get("development_and_validation")
    keyed = _index_dependency_records(records)

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


def _validated_candidate_evidence(checkpoint: dict[str, Any]) -> dict[str, str]:
    publication_gate = checkpoint.get("publication_gate")
    _require(isinstance(publication_gate, dict), "publication gate must be an object")
    candidate_evidence = publication_gate.get("candidate_evidence")
    _require(
        isinstance(candidate_evidence, dict) and bool(candidate_evidence),
        "candidate evidence must be a non-empty object",
    )
    missing = set(EXPECTED_CANDIDATE_EVIDENCE) - set(candidate_evidence)
    unknown = set(candidate_evidence) - set(EXPECTED_CANDIDATE_EVIDENCE)
    _require(not missing, f"candidate evidence is missing: {', '.join(sorted(missing))}")
    _require(not unknown, f"candidate evidence is unknown: {', '.join(sorted(unknown))}")
    for evidence_name, allowed_statuses in EXPECTED_CANDIDATE_EVIDENCE.items():
        status = candidate_evidence[evidence_name]
        _require(
            isinstance(status, str) and status in allowed_statuses,
            f"candidate evidence is malformed: {evidence_name}",
        )
    return candidate_evidence


def validate_ci_integration(root: Path = ROOT) -> dict[str, Any]:
    makefile_lines = (root / "Makefile").read_text(encoding="utf-8").splitlines()
    validation_line = f"\t{MAKE_VALIDATION_COMMAND}"
    test_line = f"\t{MAKE_TEST_COMMAND}"
    _require(validation_line in makefile_lines, "make verify omits ISSUE-0142 validator")
    _require(test_line in makefile_lines, "make verify omits ISSUE-0142 tests")
    legacy_integration = next(
        (
            index
            for index, line in enumerate(makefile_lines)
            if "monorepo-greenfield" in line and "foundation_validation.py" in line
        ),
        None,
    )
    _require(legacy_integration is not None, "canonical integration gate is missing")
    _require(
        makefile_lines.index(validation_line) < legacy_integration
        and makefile_lines.index(test_line) < legacy_integration,
        "ISSUE-0142 gate must run before service-dependent integration",
    )
    return {"mechanism": "make verify", "python": "$(PYTHON)", "status": "PASS"}


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
        == checkpoint.get("reproducible_command")
        == PORTABLE_COMMAND,
        "local and CI commands diverge",
    )
    artifacts = checkpoint.get("artifacts")
    _require(
        isinstance(artifacts, list)
        and bool(artifacts)
        and all(isinstance(artifact, str) and artifact for artifact in artifacts),
        "checkpoint artifacts must be a non-empty string list",
    )
    for artifact in artifacts:
        _require((root / artifact).is_file(), f"checkpoint artifact is missing: {artifact}")
    publication_gate = checkpoint.get("publication_gate")
    _require(isinstance(publication_gate, dict), "publication gate must be an object")
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
    _validated_candidate_evidence(checkpoint)
    return checkpoint


def evaluate_publication_gate(
    checkpoint: dict[str, Any],
    *,
    dco_verified: bool,
) -> dict[str, Any]:
    _require(isinstance(dco_verified, bool), "DCO verification state must be boolean")
    candidate_evidence = _validated_candidate_evidence(checkpoint)
    blockers = [
        name
        for name, status in candidate_evidence.items()
        if (name == "DCO_AUTOMATED_CHECK" and not dco_verified)
        or (name != "DCO_AUTOMATED_CHECK" and status != "PASS")
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
        "ci_integration": validate_ci_integration(root),
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
