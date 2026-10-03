from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
SLUG = "license-citation-cff-contribuicao-dco-cla-e-gate-de-pu"
TOOL_PATH = ROOT / "tools/governance" / SLUG / "foundation_validation.py"
TASK_PATH = ROOT / ".codex/tasks/TASK-0032.json"


def _load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("issue_0142_foundation_validation", TOOL_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TOOL = _load_tool()


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def test_citation_cff_validation() -> None:
    result = TOOL.validate_citation(ROOT)
    assert result == {"artifact": "CITATION.cff", "version": "0.0.0", "status": "PASS"}

    invalid_citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    invalid_citation["license"] = "MIT"

    with pytest.raises(TOOL.FoundationValidationError, match="incompatible"):
        TOOL._validate_citation_document(
            invalid_citation,
            python_version="0.0.0",
            frontend_version="0.0.0",
        )


def test_layered_spdx_reuse_license_notices_dependency_and_asset_compatibility(
    tmp_path: Path,
) -> None:
    result = TOOL.validate_license_inventory(ROOT)
    assert result["license_classes"] == ["AGPL-3.0-or-later", "Apache-2.0", "CC-BY-4.0"]
    assert result["dep5_license_classes"] == 3
    assert result["license_text_digests"] == TOOL.EXPECTED_LICENSE_DIGESTS
    assert result["assigned_paths"] > 3_000

    inventory = _load_json(TOOL.LICENSE_INVENTORY_PATH)
    assignments = TOOL.classify_paths(
        inventory,
        ["src/backend/app.py", "contracts/example.schema.json", "docs/guide.md", "LICENSE"],
    )
    assert assignments == {
        "src/backend/app.py": "AGPL-3.0-or-later",
        "contracts/example.schema.json": "Apache-2.0",
        "docs/guide.md": "CC-BY-4.0",
        "LICENSE": "LICENSE-TEXT",
    }

    with pytest.raises(TOOL.FoundationValidationError, match="no license class"):
        TOOL.classify_paths(inventory, ["unclassified.xyz"])
    with pytest.raises(TOOL.FoundationValidationError, match="no explicit license record"):
        TOOL.classify_paths(inventory, ["assets/model.onnx"])

    unknown_license = copy.deepcopy(inventory)
    unknown_license["classes"][0]["license"] = "LicenseRef-Unknown"
    with pytest.raises(TOOL.FoundationValidationError, match="unknown file license expression"):
        TOOL.classify_paths(unknown_license, ["src/backend/app.py"])

    for relative_path in TOOL.EXPECTED_LICENSE_DIGESTS:
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative_path, target)
    adulterated = tmp_path / "LICENSES/AGPL-3.0-or-later.txt"
    adulterated.write_bytes(adulterated.read_bytes() + b"\nadulterated\n")
    with pytest.raises(TOOL.FoundationValidationError, match="license text digest mismatch"):
        TOOL.validate_license_texts(tmp_path)

    dep5_path = tmp_path / ".reuse/dep5"
    dep5_path.parent.mkdir(parents=True)
    dep5_path.write_text(
        (ROOT / ".reuse/dep5")
        .read_text(encoding="utf-8")
        .replace("Files: contracts/*", "Files: contracts/changed/*"),
        encoding="utf-8",
    )
    with pytest.raises(TOOL.FoundationValidationError, match="DEP5 patterns diverge"):
        TOOL.validate_dep5_inventory(tmp_path, inventory)


def test_license_and_dependency_inventory() -> None:
    result = TOOL.validate_dependency_inventory(ROOT)
    assert result == {"direct_dependencies": 23, "runtime_dependencies": 3, "status": "PASS"}

    inventory = _load_json(TOOL.DEPENDENCY_INVENTORY_PATH)
    records = inventory["runtime"] + inventory["development_and_validation"]
    assert len({(record["ecosystem"], record["name"]) for record in records}) == len(records)
    assert inventory["release_sbom"] == "REQUIRED_AT_RELEASE_CANDIDATE"
    assert inventory["unknown_or_unpinned_dependency"] == "REJECT"

    unknown_license = copy.deepcopy(records)
    unknown_license[0]["license"] = "LicenseRef-Unknown"
    with pytest.raises(TOOL.FoundationValidationError, match="unknown dependency license"):
        TOOL._index_dependency_records(unknown_license)

    mismatched_license = copy.deepcopy(records)
    mismatched_license[0]["license"] = "Apache-2.0"
    with pytest.raises(TOOL.FoundationValidationError, match="dependency license mismatch"):
        TOOL._index_dependency_records(mismatched_license)


@pytest.fixture
def dependency_root(tmp_path: Path) -> Path:
    for relative in [
        TOOL.DEPENDENCY_INVENTORY_PATH.relative_to(ROOT),
        Path("requirements-validation.txt"),
        Path("pyproject.toml"),
        Path("src/frontend/package.json"),
        Path("pnpm-lock.yaml"),
        Path("THIRD_PARTY_NOTICES.md"),
    ]:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    return tmp_path


def test_dependency_review_baseline(dependency_root: Path) -> None:
    assert TOOL.validate_dependency_inventory(dependency_root) == {
        "direct_dependencies": 23,
        "runtime_dependencies": 3,
        "status": "PASS",
    }


@pytest.mark.parametrize("section", ["dependencies", "devDependencies"])
def test_unknown_manifest_dependency_fails(dependency_root: Path, section: str) -> None:
    path = dependency_root / "src/frontend/package.json"
    frontend = _load_json(path)
    frontend[section]["unreviewed-package"] = "1.0.0"
    path.write_text(json.dumps(frontend), encoding="utf-8")
    with pytest.raises(TOOL.FoundationValidationError, match="inventory diverges"):
        TOOL.validate_dependency_inventory(dependency_root)


@pytest.mark.parametrize("scope", ["runtime", "development_and_validation"])
def test_unknown_dependency_even_with_matching_manifest_and_lock_fails(
    dependency_root: Path, scope: str
) -> None:
    path = dependency_root / TOOL.DEPENDENCY_INVENTORY_PATH.relative_to(ROOT)
    inventory = _load_json(path)
    inventory[scope].append(
        {"ecosystem": "npm", "name": "unreviewed-package", "version": "1.0.0", "license": "MIT"}
    )
    path.write_text(json.dumps(inventory), encoding="utf-8")
    section = "dependencies" if scope == "runtime" else "devDependencies"
    manifest_path = dependency_root / "src/frontend/package.json"
    frontend = _load_json(manifest_path)
    frontend[section]["unreviewed-package"] = "1.0.0"
    manifest_path.write_text(json.dumps(frontend), encoding="utf-8")
    lock_path = dependency_root / "pnpm-lock.yaml"
    lock = yaml.safe_load(lock_path.read_text(encoding="utf-8"))
    lock["importers"]["src/frontend"][section]["unreviewed-package"] = {
        "specifier": "1.0.0",
        "version": "1.0.0",
    }
    lock_path.write_text(yaml.safe_dump(lock), encoding="utf-8")
    with pytest.raises(TOOL.FoundationValidationError, match="unknown dependency:"):
        TOOL.validate_dependency_inventory(dependency_root)


@pytest.mark.parametrize("section", ["optionalDependencies", "peerDependencies"])
def test_unreviewed_dependency_section_fails(dependency_root: Path, section: str) -> None:
    path = dependency_root / "src/frontend/package.json"
    frontend = _load_json(path)
    frontend[section] = {"unreviewed-package": "1.0.0"}
    path.write_text(json.dumps(frontend), encoding="utf-8")
    with pytest.raises(TOOL.FoundationValidationError, match="require release review"):
        TOOL.validate_dependency_inventory(dependency_root)


@pytest.mark.parametrize("scope", ["runtime", "development_and_validation"])
@pytest.mark.parametrize(
    "mutation", ["missing", "unknown", "version", "unpinned", "license", "swap"]
)
def test_dependency_inventory_rejects_drift(
    dependency_root: Path, scope: str, mutation: str
) -> None:
    path = dependency_root / TOOL.DEPENDENCY_INVENTORY_PATH.relative_to(ROOT)
    inventory = _load_json(path)
    records = inventory[scope]
    record = next(item for item in records if item["ecosystem"] == "npm")
    expected_error = {
        "missing": "inventory is incomplete",
        "unknown": "unknown dependency:",
        "version": "inventory diverges",
        "unpinned": "not exactly pinned",
        "license": "dependency license mismatch",
        "swap": "classification diverges",
    }[mutation]
    if mutation == "missing":
        records.remove(record)
    elif mutation == "unknown":
        records.append({**record, "name": "unreviewed-package"})
    elif mutation == "version":
        record["version"] = "0.0.1"
    elif mutation == "unpinned":
        record["version"] = "^" + record["version"]
    elif mutation == "license":
        record["license"] = "Apache-2.0" if record["license"] == "MIT" else "MIT"
    else:
        other_scope = (
            "runtime" if scope == "development_and_validation" else "development_and_validation"
        )
        records.remove(record)
        inventory[other_scope].append(record)
    path.write_text(json.dumps(inventory), encoding="utf-8")
    with pytest.raises(TOOL.FoundationValidationError, match=expected_error):
        TOOL.validate_dependency_inventory(dependency_root)


@pytest.mark.parametrize("section", ["dependencies", "devDependencies"])
@pytest.mark.parametrize("mutation", ["removed", "version", "unpinned", "swap"])
def test_manifest_classification_and_pins_fail_closed(
    dependency_root: Path, section: str, mutation: str
) -> None:
    path = dependency_root / "src/frontend/package.json"
    frontend = _load_json(path)
    name = next(iter(frontend[section]))
    version = frontend[section][name]
    if mutation == "removed":
        del frontend[section][name]
    elif mutation == "version":
        frontend[section][name] = "0.0.1"
    elif mutation == "unpinned":
        frontend[section][name] = "^" + version
    else:
        other_section = "dependencies" if section == "devDependencies" else "devDependencies"
        frontend[other_section][name] = frontend[section].pop(name)
    path.write_text(json.dumps(frontend), encoding="utf-8")
    with pytest.raises(TOOL.FoundationValidationError, match="inventory diverges"):
        TOOL.validate_dependency_inventory(dependency_root)


@pytest.mark.parametrize("section", ["dependencies", "devDependencies"])
@pytest.mark.parametrize("mutation", ["specifier", "version", "missing", "extra", "swap"])
def test_lockfile_scope_and_resolved_pin_fail_closed(
    dependency_root: Path, section: str, mutation: str
) -> None:
    path = dependency_root / "pnpm-lock.yaml"
    lock = yaml.safe_load(path.read_text(encoding="utf-8"))
    importer = lock["importers"]["src/frontend"]
    name = next(iter(importer[section]))
    if mutation in {"specifier", "version"}:
        importer[section][name][mutation] = "0.0.1"
    elif mutation == "missing":
        del importer[section][name]
    elif mutation == "extra":
        importer[section]["unreviewed-package"] = {"specifier": "1.0.0", "version": "1.0.0"}
    else:
        other_section = "dependencies" if section == "devDependencies" else "devDependencies"
        importer[other_section][name] = importer[section].pop(name)
    path.write_text(yaml.safe_dump(lock), encoding="utf-8")
    with pytest.raises(TOOL.FoundationValidationError, match=r"not locked|lockfile dependency set"):
        TOOL.validate_dependency_inventory(dependency_root)


@pytest.mark.parametrize(
    "mutation", ["missing_file", "missing_row", "version", "license", "scope", "extra"]
)
def test_notices_fail_closed(dependency_root: Path, mutation: str) -> None:
    path = dependency_root / "THIRD_PARTY_NOTICES.md"
    text = path.read_text(encoding="utf-8")
    row = "| npm | react | 19.2.4 | MIT | runtime |"
    if mutation == "missing_file":
        path.unlink()
    else:
        replacements = {
            "missing_row": "",
            "version": row.replace("19.2.4", "0.0.1"),
            "license": row.replace("MIT", "ISC"),
            "scope": row.replace("runtime", "development"),
            "extra": row + "\n" + row,
        }
        path.write_text(text.replace(row, replacements[mutation]), encoding="utf-8")
    with pytest.raises(TOOL.FoundationValidationError, match="third-party notices"):
        TOOL.validate_dependency_inventory(dependency_root)


def test_contribution_origin_dco_signoff_and_inbound_outbound_policy() -> None:
    result = TOOL.validate_contribution_policy(ROOT)
    assert result == {"origin_certification": "DCO-1.1", "cla": "NOT_REQUIRED", "status": "PASS"}

    signed_message = (
        "feat: materialize governance foundation\n\n"
        "Signed-off-by: External Contributor <contributor@example.com>"
    )
    assert TOOL.validate_dco_messages([("abc123", signed_message)]) == {
        "commits_checked": 1,
        "status": "PASS",
    }
    with pytest.raises(TOOL.FoundationValidationError, match="unsigned external commits: deadbeef"):
        TOOL.validate_dco_messages([("deadbeef", "feat: unsigned")])
    with pytest.raises(TOOL.FoundationValidationError, match="unsigned external commits: badc0de"):
        TOOL.validate_dco_messages([("badc0de", "Signed-off-by: Missing Email")])
    with pytest.raises(TOOL.FoundationValidationError, match="unsafe or invalid"):
        TOOL.validate_dco_commit_range("main;echo unsafe", ROOT)


def test_candidate_evidence_set_is_closed_and_fail_closed() -> None:
    checkpoint = TOOL.validate_checkpoint(ROOT)

    empty = copy.deepcopy(checkpoint)
    empty["publication_gate"]["candidate_evidence"] = {}
    with pytest.raises(TOOL.FoundationValidationError, match="non-empty object"):
        TOOL.evaluate_publication_gate(empty, dco_verified=False)

    for evidence_name in TOOL.EXPECTED_CANDIDATE_EVIDENCE:
        missing = copy.deepcopy(checkpoint)
        del missing["publication_gate"]["candidate_evidence"][evidence_name]
        with pytest.raises(TOOL.FoundationValidationError, match=evidence_name):
            TOOL.evaluate_publication_gate(missing, dco_verified=False)

    malformed = copy.deepcopy(checkpoint)
    malformed["publication_gate"]["candidate_evidence"]["LEGAL_REVIEW_BEFORE_G6"] = {
        "status": "PASS"
    }
    with pytest.raises(TOOL.FoundationValidationError, match="candidate evidence is malformed"):
        TOOL.evaluate_publication_gate(malformed, dco_verified=False)


def test_epic_007_fundacao() -> None:
    report = TOOL.validate_foundation(ROOT)
    assert report["decision"] == "PASS"
    assert {name: check["status"] for name, check in report["checks"].items()} == {
        "checkpoint": "PASS",
        "ci_integration": "PASS",
        "citation": "PASS",
        "licensing": "PASS",
        "dependencies": "PASS",
        "contribution": "PASS",
        "dco": "NOT_REQUESTED",
    }

    checkpoint = TOOL.validate_checkpoint(ROOT)
    gate = TOOL.evaluate_publication_gate(checkpoint, dco_verified=False)
    assert gate["decision"] == "BLOCKED"
    assert gate["blockers"] == [
        "DCO_AUTOMATED_CHECK",
        "DEPENDENCY_INVENTORY_AND_SBOM",
        "LEGAL_REVIEW_BEFORE_G6",
        "SECURITY_LICENSE_RESTORE_COMPATIBILITY_SCIENTIFIC_GATES",
    ]

    permissive_checkpoint = copy.deepcopy(checkpoint)
    permissive_checkpoint["publication_gate"]["candidate_evidence"] = dict.fromkeys(
        checkpoint["publication_gate"]["candidate_evidence"], "PASS"
    )
    assert TOOL.evaluate_publication_gate(permissive_checkpoint, dco_verified=True) == {
        "decision": "PASS",
        "blockers": [],
        "status": "PASS",
    }
    assert TOOL.evaluate_publication_gate(permissive_checkpoint, dco_verified=False) == {
        "decision": "BLOCKED",
        "blockers": ["DCO_AUTOMATED_CHECK"],
        "status": "PASS",
    }

    task = _load_json(TASK_PATH)
    required_allow_paths = {
        ".codex/tasks/TASK-0032.json",
        ".reuse/dep5",
        "CITATION.cff",
        "CONTRIBUTING.md",
        "LICENSE",
        "LICENSES/**",
        "Makefile",
        "NOTICE",
        "THIRD_PARTY_NOTICES.md",
        f"tests/fnd/{SLUG}/test_foundation.py",
        "evidence/implementation/epic-007/story-0032/**",
    }
    assert required_allow_paths <= set(task["allow_paths"])
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    assert task["acceptance_criterion_ids"] == [
        "AC-ISSUE-0142-01",
        "AC-ISSUE-0142-02",
        "AC-ISSUE-0142-03",
        "AC-ISSUE-0142-04",
    ]

    checkpoint_command = checkpoint["reproducible_command"]
    assert checkpoint_command == checkpoint["local_command"] == checkpoint["ci_command"]
    assert checkpoint_command == TOOL.PORTABLE_COMMAND
    assert "py -3.12" not in checkpoint_command
    assert TOOL.validate_ci_integration(ROOT) == {
        "mechanism": "make verify",
        "python": "$(PYTHON)",
        "status": "PASS",
    }

    readme = (TOOL.FOUNDATION_ROOT / "README.md").read_text(encoding="utf-8")
    assert "ISSUE-0141" not in readme
    assert "ISSUE-0142" in readme

    completed = subprocess.run(
        [sys.executable, "-X", "utf8", str(TOOL_PATH)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["decision"] == "PASS"

    blocked = subprocess.run(
        [sys.executable, "-X", "utf8", str(TOOL_PATH), "--publication-gate"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert blocked.returncode == 1, blocked.stderr
    assert json.loads(blocked.stdout)["decision"] == "BLOCKED"
