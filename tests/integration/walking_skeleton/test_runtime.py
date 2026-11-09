from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from unittest.mock import Mock, call

from walking_skeleton_runtime import EXPECTED_TRACE, initialize_schema, load_job

RUNTIME_PATH = Path(__file__).with_name("walking_skeleton_runtime.py")
PROCESS_STOP_TIMEOUT_SECONDS = 5.0


def _terminate_and_reap(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=PROCESS_STOP_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=PROCESS_STOP_TIMEOUT_SECONDS)


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
    processes: list[subprocess.Popen[bytes]] = []
    body_failed = True
    try:
        worker = subprocess.Popen(
            [sys.executable, str(RUNTIME_PATH), "worker"], env=environment
        )
        processes.append(worker)
        api = subprocess.Popen(
            [sys.executable, str(RUNTIME_PATH), "api"], env=environment
        )
        processes.append(api)
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
        body_failed = False
    finally:
        cleanup_errors: list[Exception] = []
        for process in reversed(processes):
            try:
                _terminate_and_reap(process)
            except Exception as error:
                cleanup_errors.append(error)
        if cleanup_errors and not body_failed:
            raise cleanup_errors[0]


def test_process_cleanup_escalates_after_graceful_shutdown_timeout() -> None:
    process = Mock(spec=subprocess.Popen)
    process.poll.return_value = None
    process.wait.side_effect = [
        subprocess.TimeoutExpired(["worker"], PROCESS_STOP_TIMEOUT_SECONDS),
        -9,
    ]

    _terminate_and_reap(process)

    process.terminate.assert_called_once_with()
    process.kill.assert_called_once_with()
    assert process.wait.call_args_list == [
        call(timeout=PROCESS_STOP_TIMEOUT_SECONDS),
        call(timeout=PROCESS_STOP_TIMEOUT_SECONDS),
    ]


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
