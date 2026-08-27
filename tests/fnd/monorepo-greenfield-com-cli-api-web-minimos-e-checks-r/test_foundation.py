from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from functools import cache
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r"
)
FOUNDATION_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/foundation-plan.json"
)
CONTRACT_PATH = ROOT / (
    "contracts/contexts/engineering_governance/fnd/"
    "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/"
    "examples/monorepo-foundation.json"
)
TASK_PATH = ROOT / ".codex/tasks/TASK-0012.json"
VALIDATOR_PATH = MODULE_ROOT / "foundation_validation.py"
RUNTIME_PATH = MODULE_ROOT / "walking_skeleton_runtime.py"
MAKEFILE_PATH = ROOT / "Makefile"
CI_PATH = ROOT / ".github/workflows/ci.yml"
sys.path.insert(0, str(MODULE_ROOT))

from foundation_validation import validate_foundation, validate_paths  # noqa: E402
from walking_skeleton_runtime import EXPECTED_TRACE, initialize_schema, load_job  # noqa: E402


@cache
def _load(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _codes(plan: object, contract: object | None = None) -> set[str]:
    effective_contract = _load(CONTRACT_PATH) if contract is None else contract
    return {finding.code for finding in validate_foundation(plan, effective_contract)}


def test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done(
    tmp_path: Path,
) -> None:
    assert os.environ.get("FOUNDATION_INTEGRATION") == "1", (
        "FOUNDATION_INTEGRATION=1 and the pinned PostgreSQL/RabbitMQ services are required"
    )
    environment = {
        **os.environ,
        "FOUNDATION_ARTIFACT_DIR": str(tmp_path),
        "FOUNDATION_API_URL": "http://127.0.0.1:8765",
    }
    initialize_schema()
    worker = subprocess.Popen(
        [sys.executable, str(RUNTIME_PATH), "worker"], env=environment
    )
    api = subprocess.Popen(
        [sys.executable, str(RUNTIME_PATH), "api"], env=environment
    )
    try:
        _wait_for_api(api)
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNTIME_PATH),
                "cli",
                "--request-id",
                "sentinel-issue-0122",
            ],
            check=True,
            capture_output=True,
            env=environment,
            text=True,
        )
        report = json.loads(completed.stdout)
        job = load_job(report["job_id"])
        artifact_path = Path(job["artifact_path"])
        assert job["status"] == "COMPLETED"
        assert job["stage_trace"] == EXPECTED_TRACE
        assert artifact_path.is_file()
        assert hashlib.sha256(artifact_path.read_bytes()).hexdigest() == job["artifact_sha256"]
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        assert artifact["stage_trace"] == EXPECTED_TRACE
    finally:
        api.terminate()
        worker.terminate()
        api.wait(timeout=10)
        worker.wait(timeout=10)


def _wait_for_api(process: subprocess.Popen[bytes]) -> None:
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("foundation API exited before becoming ready")
        try:
            with urllib.request.urlopen("http://127.0.0.1:8765/health", timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.2)
    raise TimeoutError("foundation API did not become ready")


def test_host_container_ci_contract_and_no_implicit_downloads() -> None:
    policy = _load(FOUNDATION_PATH)["reproducibility"]
    assert policy["local_commands"] == policy["container_commands"] == policy["ci_commands"]
    assert policy["local_commands"] == ["make verify"]
    assert policy["dependency_resolution"] == "REPOSITORY_PINNED_ONLY"
    assert policy["implicit_downloads"] == "PROHIBITED"
    assert policy["network_required"] is False

    invalid = copy.deepcopy(_load(FOUNDATION_PATH))
    invalid["reproducibility"]["ci_commands"] = ["download-and-run-latest"]
    invalid["reproducibility"]["network_required"] = True
    invalid["reproducibility"]["download_url"] = "https://example.invalid/latest"
    assert {"COMMAND_PARITY_INVALID", "REPRODUCIBILITY_INVALID"} <= _codes(invalid)

    makefile = MAKEFILE_PATH.read_text(encoding="utf-8")
    workflow = CI_PATH.read_text(encoding="utf-8")
    assert VALIDATOR_PATH.relative_to(ROOT).as_posix() in makefile
    assert Path(__file__).relative_to(ROOT).as_posix() in makefile
    assert "run: make verify" in workflow
    assert 'FOUNDATION_INTEGRATION: "1"' in workflow


def test_epic_003_fundacao() -> None:
    plan = _load(FOUNDATION_PATH)
    contract = _load(CONTRACT_PATH)
    task = _load(TASK_PATH)
    assert validate_foundation(plan, contract) == []
    assert plan["requirement_evidence"] == {
        "REQ-DEL-001": "test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done",
        "REQ-DEV-001": "test_host_container_ci_contract_and_no_implicit_downloads",
    }
    assert set(plan["acceptance_evidence"]) == set(task["acceptance_criterion_ids"])
    assert set(task["tests"]) <= set(plan["requirement_evidence"].values()) | set(
        plan["acceptance_evidence"].values()
    )
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    assert {
        ".codex/tasks/TASK-0012.json",
        "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation.py",
        "evidence/implementation/epic-003/story-0012/**",
    } <= set(task["allow_paths"])


def test_foundation_rejects_contract_drift_and_silent_fallback() -> None:
    plan = copy.deepcopy(_load(FOUNDATION_PATH))
    plan["failure_policy"]["mode"] = "BEST_EFFORT"
    plan["failure_policy"]["silent_fallback"] = True
    plan["topology"]["semantic_authority"] = "CLI_LOCAL"
    plan["unexpected"] = "ignored-extension"
    assert {
        "FAILURE_POLICY_INVALID",
        "FOUNDATION_STRUCTURE_INVALID",
        "TOPOLOGY_INVALID",
    } <= _codes(plan)

    contract = copy.deepcopy(_load(CONTRACT_PATH))
    contract["contract_version"] = "2.0.0"
    drifted_plan = copy.deepcopy(_load(FOUNDATION_PATH))
    drifted_plan["contract_version"] = "2.0.0"
    assert {"CONTRACT_DRIFT", "FOUNDATION_IDENTITY_INVALID"} <= _codes(
        drifted_plan, contract
    )


def test_validator_cli_is_deterministic_and_fails_closed() -> None:
    command = [
        sys.executable,
        str(VALIDATOR_PATH),
        "--foundation",
        str(FOUNDATION_PATH),
        "--contract",
        str(CONTRACT_PATH),
    ]
    first = subprocess.run(command, check=False, capture_output=True, text=True)
    second = subprocess.run(command, check=False, capture_output=True, text=True)
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert json.loads(first.stdout)["status"] == "PASS"

    missing = FOUNDATION_PATH.with_name("missing-foundation.json")
    failed = subprocess.run(
        [*command[:2], "--foundation", str(missing), "--contract", str(CONTRACT_PATH)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert failed.returncode == 2
    report = json.loads(failed.stdout)
    assert report["status"] == "FAIL"
    assert report["findings"][0]["code"] == "FOUNDATION_UNREADABLE"
    assert validate_paths(missing, CONTRACT_PATH)[0].code == "FOUNDATION_UNREADABLE"
