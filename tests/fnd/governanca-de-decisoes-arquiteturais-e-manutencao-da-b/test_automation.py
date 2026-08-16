from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_REL = Path(
    "tools/quality/contexts/engineering_governance/"
    "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/validator.py"
)
VALIDATOR_DIR_REL = VALIDATOR_REL.parent
CONTRACT_REL = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "governanca-de-decisoes-arquiteturais-e-manutencao-da-b"
)
OWNERSHIP_REL = Path("contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv")
SENTINEL_REL = Path("qa-unrelated-sentinel.bin")
SENTINEL_BYTES = b"ISSUE-0869 unrelated sentinel\x00\xff\n"
GOVERNED_SOURCE_RELS = (
    OWNERSHIP_REL,
    CONTRACT_REL / "contract-manifest.yaml",
    CONTRACT_REL / "examples/foundation-boundaries.json",
    CONTRACT_REL / "examples/issue-forecast.json",
    CONTRACT_REL / "examples/portfolio-snapshot.json",
    CONTRACT_REL / "foundation-boundaries.schema.json",
    CONTRACT_REL / "issue-forecast.schema.json",
    CONTRACT_REL / "portfolio-snapshot.schema.json",
    VALIDATOR_DIR_REL / "contract_definition.py",
    VALIDATOR_DIR_REL / "manifest_validation.py",
    VALIDATOR_DIR_REL / "semantic_invariants.py",
    VALIDATOR_DIR_REL / "validation_types.py",
    VALIDATOR_REL,
)


@dataclass(frozen=True)
class Execution:
    returncode: int
    stdout: bytes
    stderr: bytes
    filesystem_snapshot: tuple[tuple[str, str], ...]


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


def _snapshot_digest(snapshot: tuple[tuple[str, str], ...]) -> str:
    encoded = json.dumps(snapshot, ensure_ascii=True, separators=(",", ":")).encode()
    return _sha256(encoded)


def _assert_candidate_source_inventory() -> None:
    if not (ROOT / ".git").exists():
        return
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-files",
            "--",
            VALIDATOR_DIR_REL.as_posix(),
            CONTRACT_REL.as_posix(),
            OWNERSHIP_REL.as_posix(),
        ],
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    tracked = {Path(line) for line in completed.stdout.splitlines() if line}
    assert tracked == set(GOVERNED_SOURCE_RELS)
    unchanged = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "diff",
            "--quiet",
            "HEAD",
            "--",
            *(relative.as_posix() for relative in GOVERNED_SOURCE_RELS),
        ],
        check=False,
    )
    assert unchanged.returncode == 0


def _candidate_source_bytes(relative: Path) -> bytes:
    if not (ROOT / ".git").exists():
        return (ROOT / relative).read_bytes().replace(b"\r\n", b"\n")
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"HEAD:{relative.as_posix()}"],
        check=False,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout


def _prepare_sandbox(root: Path) -> None:
    _assert_candidate_source_inventory()
    for relative in GOVERNED_SOURCE_RELS:
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(_candidate_source_bytes(relative))
    (root / SENTINEL_REL).write_bytes(SENTINEL_BYTES)


def _execute(root: Path) -> Execution:
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "0",
            "PYTHONUTF8": "1",
        }
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(root / VALIDATOR_REL),
            "--repository-root",
            str(root),
        ],
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


def _read_json(root: Path, relative: Path) -> dict[str, Any]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def _write_json(root: Path, relative: Path, value: dict[str, Any]) -> None:
    (root / relative).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _json_mutation(relative: Path, change: Callable[[dict[str, Any]], None]) -> Mutation:
    def mutate(root: Path) -> None:
        value = _read_json(root, relative)
        change(value)
        _write_json(root, relative, value)

    return mutate


def _remove_portfolio_example(root: Path) -> None:
    (root / CONTRACT_REL / "examples/portfolio-snapshot.json").unlink()


def _truncate_forecast(root: Path) -> None:
    (root / CONTRACT_REL / "examples/issue-forecast.json").write_bytes(b'{"interval":')


def _invalidate_owner_registry(root: Path) -> None:
    path = root / OWNERSHIP_REL
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    target = (CONTRACT_REL / "contract-manifest.yaml").as_posix()
    match = next(row for row in rows if row["contract"] == target)
    match["owner_context"] = "BC-999"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _case_mutations() -> tuple[tuple[str, str, Mutation], ...]:
    portfolio_example = CONTRACT_REL / "examples/portfolio-snapshot.json"
    forecast_example = CONTRACT_REL / "examples/issue-forecast.json"
    portfolio_schema = CONTRACT_REL / "portfolio-snapshot.schema.json"
    return (
        ("required_artifact_missing", "ARTIFACT_MISSING", _remove_portfolio_example),
        ("invalid_truncated_json", "JSON_INVALID", _truncate_forecast),
        (
            "unresolvable_reference",
            "SCHEMA_REFERENCE_UNRESOLVABLE",
            _json_mutation(
                portfolio_schema,
                lambda value: value.update(
                    {"$ref": "https://example.invalid/missing-contract/1.0.0"}
                ),
            ),
        ),
        ("invalid_owner_metadata", "OWNER_INVALID", _invalidate_owner_registry),
        (
            "prohibited_unknown_property",
            "EXAMPLE_SCHEMA_INVALID",
            _json_mutation(
                portfolio_example, lambda value: value.update({"fallback": "accept"})
            ),
        ),
        (
            "violated_semantic_invariant",
            "INVALID_INTERVAL_ORDER",
            _json_mutation(
                forecast_example,
                lambda value: value["interval"].update({"minimum": 9, "mode": 8}),
            ),
        ),
        (
            "unsupported_schema_dialect",
            "SCHEMA_DIALECT_INVALID",
            _json_mutation(
                portfolio_schema,
                lambda value: value.update(
                    {"$schema": "https://example.invalid/unknown-dialect"}
                ),
            ),
        ),
        (
            "invalid_unannounced_leap_second",
            "EXAMPLE_SCHEMA_INVALID",
            _json_mutation(
                portfolio_example,
                lambda value: value.update({"captured_at": "2025-01-31T23:59:60Z"}),
            ),
        ),
    )


def _assert_controlled_failure(execution: Execution, code: str) -> None:
    combined = execution.stdout + execution.stderr
    assert execution.returncode != 0
    assert b"VALIDATION FAILED" in execution.stdout
    assert f"ERROR [{code}]".encode() in execution.stdout
    assert b"VALIDATION PASS" not in combined
    assert b"Traceback" not in combined


def collect_validation_evidence() -> dict[str, Any]:
    assert sys.version_info[:2] == (3, 12), platform.python_version()
    sentinel_hash = _sha256(SENTINEL_BYTES)
    with tempfile.TemporaryDirectory(prefix=".issue-0869-valid-", dir=ROOT) as temporary:
        valid_root = Path(temporary)
        _prepare_sandbox(valid_root)
        before = _snapshot(valid_root)
        first = _execute(valid_root)
        between = _snapshot(valid_root)
        second = _execute(valid_root)
        after = _snapshot(valid_root)
        assert first.returncode == second.returncode == 0
        assert first == second
        assert before == between == after == first.filesystem_snapshot
        assert dict(after)[SENTINEL_REL.as_posix()] == sentinel_hash
        valid_report = {
            "first_returncode": first.returncode,
            "second_returncode": second.returncode,
            "stdout_sha256": _sha256(first.stdout),
            "stderr_sha256": _sha256(first.stderr),
            "filesystem_snapshot_sha256": _snapshot_digest(after),
            "filesystem_file_count": len(after),
            "filesystem_paths": [path for path, _digest in after],
            "sentinel_sha256": sentinel_hash,
        }

    case_reports: list[dict[str, Any]] = []
    for name, code, mutate in _case_mutations():
        with tempfile.TemporaryDirectory(
            prefix=f".issue-0869-{name}-", dir=ROOT
        ) as temporary:
            invalid_root = Path(temporary)
            _prepare_sandbox(invalid_root)
            mutate(invalid_root)
            before = _snapshot(invalid_root)
            first = _execute(invalid_root)
            after = _snapshot(invalid_root)
            _assert_controlled_failure(first, code)
            assert before == after == first.filesystem_snapshot
            assert dict(after)[SENTINEL_REL.as_posix()] == sentinel_hash
            repeated = None
            if name == "required_artifact_missing":
                repeated = _execute(invalid_root)
                _assert_controlled_failure(repeated, code)
                assert repeated == first
            case_reports.append(
                {
                    "case": name,
                    "expected_finding": code,
                    "returncode": first.returncode,
                    "stdout_sha256": _sha256(first.stdout),
                    "stderr_sha256": _sha256(first.stderr),
                    "filesystem_snapshot_sha256": _snapshot_digest(after),
                    "repeated_identically": repeated == first if repeated else False,
                }
            )
    return {
        "cpython": platform.python_version(),
        "valid": valid_report,
        "fail_closed": case_reports,
    }


def test_epic_001_automacao() -> None:
    report = collect_validation_evidence()
    assert len(report["fail_closed"]) == 8
