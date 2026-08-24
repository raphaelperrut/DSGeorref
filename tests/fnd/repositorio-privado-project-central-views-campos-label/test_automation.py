from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_REL = Path(
    "tools/quality/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/validator.py"
)
VALIDATOR_DIR = VALIDATOR_REL.parent
CONTRACT_REL = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "repositorio-privado-project-central-views-campos-label"
)
OWNERSHIP_REL = Path("contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv")
EXTERNAL_REFS = (
    Path(".codex/tasks/TASK_ENVELOPE.schema.json"),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "foundation-boundaries.schema.json"
    ),
)
SENTINEL_REL = Path("unrelated-sentinel.bin")
SENTINEL_BYTES = b"ISSUE-0118 unrelated sentinel\x00\xff\n"


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


def _copy_sources(root: Path) -> None:
    sources = [
        *(ROOT / VALIDATOR_DIR).glob("*.py"),
        *(ROOT / CONTRACT_REL).rglob("*"),
        ROOT / OWNERSHIP_REL,
        *(ROOT / reference for reference in EXTERNAL_REFS),
    ]
    for source in sources:
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT)
        destination = root / relative
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
    return Execution(completed.returncode, completed.stdout, completed.stderr, _snapshot(root))


def _read_json(root: Path, relative: Path) -> dict[str, object]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def _write_json(root: Path, relative: Path, value: dict[str, object]) -> None:
    (root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _missing_manifest(root: Path) -> None:
    (root / CONTRACT_REL / "worker-parte-2/contract-manifest.yaml").unlink()


def _truncated_json(root: Path) -> None:
    path = root / CONTRACT_REL / "consolidacao/examples/slice-consolidation.json"
    path.write_bytes(b'{"slices":')


def _invalid_example(root: Path) -> None:
    relative = (
        CONTRACT_REL
        / "classicprofile-iss-native-parte-1/examples/foundation-conformance.json"
    )
    value = _read_json(root, relative)
    value["status"] = "OPEN"
    _write_json(root, relative, value)


def _invalid_owner(root: Path) -> None:
    path = root / OWNERSHIP_REL
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    row = next(item for item in rows if item["contract"].startswith(CONTRACT_REL.as_posix()))
    row["owner_context"] = "BC-999"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _invalid_lineage(root: Path) -> None:
    relative = CONTRACT_REL / "consolidacao/examples/slice-consolidation.json"
    value = _read_json(root, relative)
    slices = value["slices"]
    assert isinstance(slices, list)
    slices[0]["artifacts"][0]["sha256"] = "0" * 64
    _write_json(root, relative, value)


def _missing_reference(root: Path) -> None:
    (root / EXTERNAL_REFS[0]).unlink()


def _unknown_manifest_field(root: Path) -> None:
    path = root / CONTRACT_REL / "worker-parte-2/contract-manifest.yaml"
    path.write_text(path.read_text(encoding="utf-8") + "fallback: accept\n", encoding="utf-8")


def _assert_failure(execution: Execution, code: str) -> None:
    combined = execution.stdout + execution.stderr
    assert execution.returncode != 0
    assert b"VALIDATION FAILED" in execution.stdout
    assert f"ERROR [{code}]".encode() in execution.stdout
    assert b"VALIDATION PASS" not in combined
    assert b"Traceback" not in combined


def test_epic_002_automacao() -> None:
    with tempfile.TemporaryDirectory(prefix="issue-0118-valid-") as temporary:
        sandbox = Path(temporary)
        _copy_sources(sandbox)
        before = _snapshot(sandbox)
        first = _execute(sandbox)
        second = _execute(sandbox)
        dry_first = _execute(sandbox, dry_run=True)
        dry_second = _execute(sandbox, dry_run=True)
        assert {
            first.returncode,
            second.returncode,
            dry_first.returncode,
            dry_second.returncode,
        } == {0}
        assert first == second
        assert dry_first == dry_second
        assert before == first.snapshot == dry_first.snapshot
        assert b"mode=READ_ONLY destructive_actions=0" in first.stdout
        assert b"mode=DRY_RUN destructive_actions=0" in dry_first.stdout
        assert b"requirements=12" in first.stdout
        assert dict(first.snapshot)[SENTINEL_REL.as_posix()] == _sha256(SENTINEL_BYTES)

    cases: tuple[tuple[str, str, Mutation], ...] = (
        ("missing_manifest", "ARTIFACT_MISSING", _missing_manifest),
        ("truncated_json", "JSON_INVALID", _truncated_json),
        ("invalid_example", "EXAMPLE_SCHEMA_INVALID", _invalid_example),
        ("invalid_owner", "OWNER_INVALID", _invalid_owner),
        ("invalid_lineage", "LINEAGE_DIGEST_MISMATCH", _invalid_lineage),
        ("missing_reference", "REFERENCE_MISSING", _missing_reference),
        ("unknown_manifest_field", "MANIFEST_SHAPE_INVALID", _unknown_manifest_field),
    )
    for name, code, mutate in cases:
        with tempfile.TemporaryDirectory(prefix=f"issue-0118-{name}-") as temporary:
            sandbox = Path(temporary)
            _copy_sources(sandbox)
            mutate(sandbox)
            before = _snapshot(sandbox)
            first = _execute(sandbox, dry_run=True)
            second = _execute(sandbox, dry_run=True)
            _assert_failure(first, code)
            assert first == second
            assert before == first.snapshot
