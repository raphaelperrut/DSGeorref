from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import psycopg
from celery import Celery


DATABASE_URL = os.environ.get("FOUNDATION_DATABASE_URL", "")
BROKER_URL = os.environ.get("FOUNDATION_BROKER_URL", "")
ARTIFACT_DIR = Path(os.environ.get("FOUNDATION_ARTIFACT_DIR", ".foundation-artifacts"))
API_URL = os.environ.get("FOUNDATION_API_URL", "http://127.0.0.1:8765")
QUEUE = "issue_0122_foundation"
EXPECTED_TRACE = [
    "CLI_OR_WEB_INPUT",
    "HTTP_API",
    "POSTGRESQL_POSTGIS",
    "RABBITMQ_CELERY",
    "WORKER",
    "DIAGNOSTIC_ARTIFACT",
]

celery_app = Celery("issue_0122_foundation", broker=BROKER_URL or "memory://")
celery_app.conf.update(
    accept_content=["json"],
    broker_connection_retry_on_startup=True,
    task_default_queue=QUEUE,
    task_ignore_result=True,
    task_serializer="json",
)


def _connection() -> psycopg.Connection[Any]:
    if not DATABASE_URL:
        raise RuntimeError("FOUNDATION_DATABASE_URL is required")
    return psycopg.connect(DATABASE_URL)


def initialize_schema() -> None:
    with _connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS issue_0122_foundation_jobs (
                job_id UUID PRIMARY KEY,
                request_id TEXT NOT NULL,
                status TEXT NOT NULL,
                stage_trace JSONB NOT NULL,
                artifact_path TEXT,
                artifact_sha256 TEXT
            )
            """
        )


def load_job(job_id: str) -> dict[str, Any]:
    with _connection() as connection:
        row = connection.execute(
            """
            SELECT job_id, request_id, status, stage_trace,
                   artifact_path, artifact_sha256
            FROM issue_0122_foundation_jobs WHERE job_id = %s
            """,
            (job_id,),
        ).fetchone()
    if row is None:
        raise KeyError(job_id)
    return {
        "job_id": str(row[0]),
        "request_id": row[1],
        "status": row[2],
        "stage_trace": row[3],
        "artifact_path": row[4],
        "artifact_sha256": row[5],
    }


def _update_failed(job_id: str) -> None:
    with _connection() as connection:
        connection.execute(
            "UPDATE issue_0122_foundation_jobs SET status = 'FAILED' WHERE job_id = %s",
            (job_id,),
        )


def submit_job(request_id: str) -> str:
    job_id = str(uuid.uuid4())
    with _connection() as connection:
        connection.execute(
            """
            INSERT INTO issue_0122_foundation_jobs
                (job_id, request_id, status, stage_trace)
            VALUES (%s, %s, 'PENDING', %s)
            """,
            (job_id, request_id, json.dumps(EXPECTED_TRACE[:3])),
        )
    try:
        with _connection() as connection:
            connection.execute(
                """
                UPDATE issue_0122_foundation_jobs
                SET status = 'DISPATCHING', stage_trace = %s
                WHERE job_id = %s
                """,
                (json.dumps(EXPECTED_TRACE[:4]), job_id),
            )
        process_diagnostic.apply_async(args=[job_id], task_id=job_id, queue=QUEUE)
    except Exception:
        _update_failed(job_id)
        raise
    return job_id


@celery_app.task(name="issue_0122.process_diagnostic")
def process_diagnostic(job_id: str) -> None:
    job = load_job(job_id)
    trace = list(job["stage_trace"])
    if trace != EXPECTED_TRACE[:4]:
        _update_failed(job_id)
        raise RuntimeError("required pre-worker stages are absent or reordered")
    trace.append("WORKER")
    with _connection() as connection:
        connection.execute(
            "UPDATE issue_0122_foundation_jobs SET status = 'RUNNING', stage_trace = %s "
            "WHERE job_id = %s",
            (json.dumps(trace), job_id),
        )

    artifact = {
        "artifact_kind": "FOUNDATION_DIAGNOSTIC",
        "job_id": job_id,
        "request_id": job["request_id"],
        "stage_trace": [*trace, "DIAGNOSTIC_ARTIFACT"],
    }
    encoded = json.dumps(artifact, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path = ARTIFACT_DIR / f"{job_id}.json"
    temporary_path = artifact_path.with_suffix(".tmp")
    temporary_path.write_bytes(encoded)
    temporary_path.replace(artifact_path)

    with _connection() as connection:
        connection.execute(
            """
            UPDATE issue_0122_foundation_jobs
            SET status = 'COMPLETED', stage_trace = %s,
                artifact_path = %s, artifact_sha256 = %s
            WHERE job_id = %s
            """,
            (json.dumps(artifact["stage_trace"]), str(artifact_path), digest, job_id),
        )


class FoundationHandler(BaseHTTPRequestHandler):
    def _respond(self, status: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._respond(200, {"status": "ready"})
            return
        if self.path.startswith("/jobs/"):
            try:
                self._respond(200, load_job(self.path.removeprefix("/jobs/")))
            except KeyError:
                self._respond(404, {"error": "job_not_found"})
            return
        self._respond(404, {"error": "route_not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/jobs":
            self._respond(404, {"error": "route_not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            request_id = payload["request_id"]
            if not isinstance(request_id, str) or not request_id:
                raise ValueError("request_id must be a non-empty string")
            self._respond(202, {"job_id": submit_job(request_id)})
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            self._respond(400, {"error": str(error)})

    def log_message(self, _format: str, *_args: object) -> None:
        return


def run_api(host: str, port: int) -> None:
    ThreadingHTTPServer((host, port), FoundationHandler).serve_forever()


def _request_json(request: urllib.request.Request) -> dict[str, Any]:
    with urllib.request.urlopen(request, timeout=5) as response:
        loaded = json.loads(response.read())
    if not isinstance(loaded, dict):
        raise RuntimeError("API response must be an object")
    return loaded


def run_cli(request_id: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{API_URL}/jobs",
        data=json.dumps({"request_id": request_id}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    job_id = str(_request_json(request)["job_id"])
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status = _request_json(urllib.request.Request(f"{API_URL}/jobs/{job_id}"))
        if status["status"] == "COMPLETED":
            return status
        if status["status"] == "FAILED":
            raise RuntimeError("walking skeleton failed closed")
        time.sleep(0.2)
    raise TimeoutError("walking skeleton did not complete")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ISSUE-0122 executable foundation probe")
    subparsers = parser.add_subparsers(dest="command", required=True)
    api = subparsers.add_parser("api")
    api.add_argument("--host", default="127.0.0.1")
    api.add_argument("--port", default=8765, type=int)
    cli = subparsers.add_parser("cli")
    cli.add_argument("--request-id", required=True)
    cli.add_argument("--timeout", default=45.0, type=float)
    subparsers.add_parser("worker")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "api":
        run_api(args.host, args.port)
    elif args.command == "worker":
        celery_app.worker_main(
            ["worker", "--pool=solo", "--concurrency=1", "--loglevel=WARNING", f"--queues={QUEUE}"]
        )
    else:
        print(json.dumps(run_cli(args.request_id, args.timeout), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
