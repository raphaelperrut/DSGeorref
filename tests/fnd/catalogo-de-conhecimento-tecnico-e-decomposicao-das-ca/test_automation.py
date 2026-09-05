from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
SLUG = "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca"
VALIDATOR_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py")
QUALITY_REL = VALIDATOR_REL.parent
CONTRACT_ROOT_REL = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
DOC_ROOT_REL = Path(f"docs/03-engineering/contexts/engineering_governance/{SLUG}")
FOUNDATION_ROOT_REL = Path(f"tools/governance/{SLUG}")
TASK_REL = Path(".codex/tasks/TASK-0028.json")
TASK_SCHEMA_REL = Path(".codex/tasks/TASK_ENVELOPE.schema.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
CATALOG_REL = DOC_ROOT_REL / "capability-catalog.json"
CORPUS_REL = DOC_ROOT_REL / "test-corpus-manifest.json"
CHECKPOINT_REL = FOUNDATION_ROOT_REL / "foundation-checkpoint.json"
MANIFEST_REL = CONTRACT_ROOT_REL / "contract-manifest.yaml"
CONTRACT_EXAMPLE_REL = CONTRACT_ROOT_REL / "examples/capability-catalog-foundation.json"
SENTINEL_REL = Path("unrelated-sentinel.bin")
SENTINEL_BYTES = b"ISSUE-0138 unrelated sentinel\x00\xff\n"


@dataclass(frozen=True)
class Execution:
    returncode: int
    stdout: bytes
    stderr: bytes
    snapshot: tuple[tuple[str, str], ...]


Mutation = Callable[[Path], None]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _snapshot(root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            (path.relative_to(root).as_posix(), _sha256(path.read_bytes()))
            for path in root.rglob("*")
            if path.is_file()
        )
    )


def _catalog_sources() -> list[Path]:
    catalog = json.loads((ROOT / CATALOG_REL).read_text(encoding="utf-8"))
    paths: list[Path] = []
    for capability in catalog["capabilities"]:
        paths.extend(
            Path(value)
            for value in [capability["contract"], *capability["knowledge_sources"]]
        )
    return paths


def _copy_sources(root: Path) -> None:
    sources = [
        *(ROOT / QUALITY_REL).glob("*.py"),
        *(ROOT / CONTRACT_ROOT_REL).rglob("*"),
        *(ROOT / DOC_ROOT_REL).rglob("*"),
        *(ROOT / relative for relative in _catalog_sources()),
        ROOT / CHECKPOINT_REL,
        ROOT / TASK_REL,
        ROOT / TASK_SCHEMA_REL,
        ROOT / WORKFLOW_REL,
        ROOT / Path(__file__).relative_to(ROOT),
    ]
    for source in sources:
        if not source.is_file():
            continue
        destination = root / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    (root / SENTINEL_REL).write_bytes(SENTINEL_BYTES)


def _execute(root: Path, *, dry_run: bool = False) -> Execution:
    command = [
        sys.executable,
        "-B",
        str(root / VALIDATOR_REL),
        "--repository-root",
        str(root),
    ]
    if dry_run:
        command.append("--dry-run")
    environment = os.environ.copy()
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"})
    completed = subprocess.run(
        command,
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
    )
    return Execution(
        completed.returncode,
        completed.stdout,
        completed.stderr,
        _snapshot(root),
    )


def _read_json(root: Path, relative: Path) -> dict[str, object]:
    value = json.loads((root / relative).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _write_json(root: Path, relative: Path, value: dict[str, object]) -> None:
    (root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _missing_contract(root: Path) -> None:
    (root / MANIFEST_REL).unlink()


def _invalid_requirement_evidence(root: Path) -> None:
    manifest = yaml.safe_load((root / MANIFEST_REL).read_text(encoding="utf-8"))
    manifest["requirements"] = ["REQ-AI-007"]
    (root / MANIFEST_REL).write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")


def _allowed_self_approval(root: Path) -> None:
    manifest = yaml.safe_load((root / MANIFEST_REL).read_text(encoding="utf-8"))
    manifest["review"]["self_approval"] = "ALLOWED"
    (root / MANIFEST_REL).write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")


def _permissive_corpus_policy(root: Path) -> None:
    contract = _read_json(root, CONTRACT_EXAMPLE_REL)
    corpus = contract["corpus_contract"]
    assert isinstance(corpus, dict)
    corpus["split_overlap"] = "ALLOW"
    corpus["access_integrity"] = "WARN"
    _write_json(root, CONTRACT_EXAMPLE_REL, contract)


def _invalid_catalog(root: Path) -> None:
    catalog = _read_json(root, CATALOG_REL)
    catalog["source_policy"] = {"runtime_import": "ALLOWED"}
    _write_json(root, CATALOG_REL, catalog)


def _tampered_corpus(root: Path) -> None:
    corpus = _read_json(root, CORPUS_REL)
    fixtures = corpus["fixtures"]
    assert isinstance(fixtures, list) and isinstance(fixtures[0], dict)
    fixtures[0]["sha256"] = "0" * 64
    _write_json(root, CORPUS_REL, corpus)


def _duplicate_fixture_id(root: Path) -> None:
    corpus = _read_json(root, CORPUS_REL)
    fixtures = corpus["fixtures"]
    assert isinstance(fixtures, list) and all(isinstance(item, dict) for item in fixtures)
    fixtures[2]["fixture_id"] = fixtures[0]["fixture_id"]
    _write_json(root, CORPUS_REL, corpus)


def _duplicate_fixture_path(root: Path) -> None:
    corpus = _read_json(root, CORPUS_REL)
    fixtures = corpus["fixtures"]
    assert isinstance(fixtures, list) and all(isinstance(item, dict) for item in fixtures)
    fixtures[2]["path"] = fixtures[0]["path"]
    _write_json(root, CORPUS_REL, corpus)


def _invalid_split_access(root: Path) -> None:
    corpus = _read_json(root, CORPUS_REL)
    fixtures = corpus["fixtures"]
    assert isinstance(fixtures, list) and isinstance(fixtures[3], dict)
    fixtures[3]["access"] = "QA_PROTECTED"
    _write_json(root, CORPUS_REL, corpus)


def _silent_fallback(root: Path) -> None:
    checkpoint = _read_json(root, CHECKPOINT_REL)
    failure_policy = checkpoint["failure_policy"]
    assert isinstance(failure_policy, dict)
    failure_policy["silent_fallback"] = True
    _write_json(root, CHECKPOINT_REL, checkpoint)


def _unsafe_source(root: Path) -> None:
    catalog = _read_json(root, CATALOG_REL)
    capabilities = catalog["capabilities"]
    assert isinstance(capabilities, list) and isinstance(capabilities[0], dict)
    capabilities[0]["contract"] = "../outside.md"
    _write_json(root, CATALOG_REL, catalog)


def _invalid_task(root: Path) -> None:
    task = _read_json(root, TASK_REL)
    task["tests"] = ["untracked_test"]
    _write_json(root, TASK_REL, task)


def _invalid_workflow(root: Path) -> None:
    path = root / WORKFLOW_REL
    changed = path.read_text(encoding="utf-8").replace("--dry-run", "--write")
    path.write_text(changed, encoding="utf-8")


def _assert_failure(execution: Execution, code: str) -> None:
    report = json.loads(execution.stdout)
    assert execution.returncode == 1
    assert execution.stderr == b""
    assert report["status"] == "FAIL"
    assert report["destructive_actions"] == 0
    assert code in {finding["code"] for finding in report["findings"]}


def test_epic_006_automacao() -> None:
    with tempfile.TemporaryDirectory(prefix="issue-0138-valid-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        before = _snapshot(sandbox)
        first = _execute(sandbox)
        second = _execute(sandbox)
        dry_first = _execute(sandbox, dry_run=True)
        dry_second = _execute(sandbox, dry_run=True)

        returncodes = {
            first.returncode,
            second.returncode,
            dry_first.returncode,
            dry_second.returncode,
        }
        assert returncodes == {0}, json.loads(first.stdout)["findings"]
        assert first == second
        assert dry_first == dry_second
        assert before == first.snapshot == dry_first.snapshot
        report = json.loads(first.stdout)
        assert report["status"] == "PASS"
        assert report["mode"] == "READ_ONLY"
        assert json.loads(dry_first.stdout)["mode"] == "DRY_RUN"
        assert set(report["requirement_evidence"]) == {"REQ-AI-007", "REQ-TST-001"}
        assert set(report["acceptance_evidence"]) == {
            "AC-ISSUE-0138-01",
            "AC-ISSUE-0138-02",
            "AC-ISSUE-0138-03",
            "AC-ISSUE-0138-04",
        }
        assert dict(first.snapshot)[SENTINEL_REL.as_posix()] == _sha256(SENTINEL_BYTES)

    cases: tuple[tuple[str, str, Mutation], ...] = (
        ("missing_contract", "CONTRACT_UNREADABLE", _missing_contract),
        ("requirement_drift", "CONTRACT_MANIFEST_INVALID", _invalid_requirement_evidence),
        ("self_approval", "SELF_APPROVAL_INVALID", _allowed_self_approval),
        ("corpus_policy", "CORPUS_POLICY_INVALID", _permissive_corpus_policy),
        ("invalid_catalog", "CATALOG_SCHEMA_INVALID", _invalid_catalog),
        ("tampered_corpus", "CORPUS_HASH_MISMATCH", _tampered_corpus),
        ("duplicate_fixture_id", "CORPUS_SPLIT_OVERLAP", _duplicate_fixture_id),
        ("duplicate_fixture_path", "CORPUS_SPLIT_OVERLAP", _duplicate_fixture_path),
        ("split_access", "CORPUS_ACCESS_INVALID", _invalid_split_access),
        ("silent_fallback", "FAILURE_POLICY_INVALID", _silent_fallback),
        ("unsafe_source", "SOURCE_PATH_INVALID", _unsafe_source),
        ("invalid_task", "TASK_CONTROL_INVALID", _invalid_task),
        ("invalid_workflow", "WORKFLOW_INVALID", _invalid_workflow),
    )
    for name, code, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0138-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            mutate(sandbox)
            before = _snapshot(sandbox)
            first = _execute(sandbox, dry_run=True)
            second = _execute(sandbox, dry_run=True)
            _assert_failure(first, code)
            assert first == second
            assert before == first.snapshot
