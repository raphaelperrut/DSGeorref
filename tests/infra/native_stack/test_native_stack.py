from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from contextlib import nullcontext
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
SOURCE_LOCK = ROOT / "infra/images/native-stack.lock.yaml"
CONDA_LOCK = ROOT / "infra/images/native-stack.conda-lock.txt"
RESOLVED_LOCK = ROOT / "infra/images/native-stack.resolved.yaml"
WORKFLOW = ROOT / ".github/workflows/native-stack.yaml"
DOCKERFILE = ROOT / "infra/images/native-stack.Dockerfile"
TASK_ENVELOPE = ROOT / ".codex/tasks/operations/TASK-0763.json"
POLICY = ROOT / "contracts/contexts/release_installation/native-stack-supply-chain/policy.yaml"
POLICY_SCHEMA = (
    ROOT / "contracts/contexts/release_installation/native-stack-supply-chain/policy.schema.json"
)
EVIDENCE = ROOT / "evidence/implementation/issue-0973"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_smoke_module() -> ModuleType:
    path = ROOT / "tools/quality/native_stack/abi_smoke.py"
    spec = importlib.util.spec_from_file_location("native_stack_abi_smoke", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_validator_module() -> ModuleType:
    path = ROOT / "tools/quality/native_stack/validate.py"
    spec = importlib.util.spec_from_file_location("native_stack_validator", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_source_lock_preserves_versions_and_has_immutable_lineage() -> None:
    source = yaml.safe_load(SOURCE_LOCK.read_text(encoding="utf-8"))
    assert (
        _sha256(SOURCE_LOCK) == "16970dbaba6b1a5494a2003626a53bf0d6d9cfc5ed64471804bc888551d49a9e"
    )
    assert source["immutable_inputs"]["previous_source_lock_digest"] == (
        "sha256:61197932f5cd5d4eed96c4a6c9d24185cfe9761e81094c6fd3a378c7eaa13d50"
    )
    assert source["runtime"]["python"] == "3.12.13"
    assert source["native_stack"] == {
        "gdal": "3.13.2",
        "proj": "9.8.1",
        "geos": "3.14.1",
        "rasterio": "1.5.0",
        "shapely": "2.1.2",
        "postgresql": "18.4",
        "postgis": "3.6.4",
        "rabbitmq": "4.3.4",
    }
    assert source["python_stack"] == {
        "fastapi": "0.140.2",
        "pydantic": "2.13.4",
        "celery": "5.6.3",
    }
    assert source["immutable_inputs"]["target_platform"] == "linux/amd64"


def test_conda_lock_is_explicit_hash_complete_and_version_exact() -> None:
    source = yaml.safe_load(SOURCE_LOCK.read_text(encoding="utf-8"))
    conda = source["immutable_inputs"]["conda_environment"]
    assert f"sha256:{_sha256(CONDA_LOCK)}" == conda["lock_sha256"]
    lines = [
        line
        for line in CONDA_LOCK.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#")
    ]
    assert lines[0] == "@EXPLICIT"
    assert len(lines[1:]) == conda["artifact_count"] == 136
    assert all(
        re.fullmatch(
            r"https://conda\.anaconda\.org/conda-forge/(linux-64|noarch)/[^#]+#[0-9a-f]{64}", line
        )
        for line in lines[1:]
    )
    for expected in (
        "python-3.12.13-",
        "gdal-3.13.2-",
        "proj-9.8.1-",
        "proj-data-1.25-",
        "geos-3.14.1-",
        "rasterio-1.5.0-",
        "shapely-2.1.2-",
        "pydantic-2.13.4-",
        "celery-5.6.3-",
        "psycopg-3.2.9-",
    ):
        assert sum(expected in line for line in lines[1:]) == 1


def test_contract_has_two_independent_approvals_for_exact_bytes() -> None:
    policy = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    assert policy["contract_version"] == "1.0.2"
    assert policy["scope"]["dependency_720_resolution"] == "OWNER_APPROVED_B"
    assert policy["scope"]["epic_080_satisfied"] is False
    assert policy["scope"]["issue_974_authorized"] is False
    assert policy["revocation_and_recovery"]["selectors"] == ["IMAGE_DIGEST"]
    policy_digest = _sha256(POLICY)
    schema_digest = _sha256(POLICY_SCHEMA)
    assert policy_digest == "756dd9e682c844e942a24a12c82db462179ad7e3ec6bf800cb8e21f34a77d1eb"
    assert schema_digest == "53ee536a0cf745c5f192b98787a395a7bb89ac4ee3ece2c42da6800696faada8"
    for filename, role in (
        ("architect-contract-review.json", "Architect/BC-015"),
        ("security-contract-review.json", "Security"),
    ):
        review = json.loads((EVIDENCE / filename).read_text(encoding="utf-8"))
        assert review["review_role"] == role
        assert review["decision"] == "APPROVE"
        assert review["policy_sha256"] == policy_digest
        assert review["schema_sha256"] == schema_digest


def test_task_envelope_authorizes_only_required_issue_973_paths() -> None:
    envelope = json.loads(TASK_ENVELOPE.read_text(encoding="utf-8"))
    assert envelope["task_id"] == "TASK-0763"
    assert envelope["issue_id"] == "ISSUE-0973"
    assert envelope["phase_f_review"]["dependencies"] == {
        "status": "PASS",
        "count": 1,
        "items": ["ISSUE-0080: OWNER_APPROVED_B_RUNTIME_EQUIVALENT_CONTRACT"],
    }
    assert envelope["phase_f_review"]["artifacts"]["contract"] == (
        "contracts/contexts/release_installation/native-stack-supply-chain/policy.yaml"
    )
    allow = set(envelope["allow_paths"])
    assert ".github/workflows/native-stack.yaml" in allow
    assert "infra/images/native-stack.lock.yaml" in allow
    assert "infra/images/native-stack.resolved.yaml" in allow
    assert "tools/quality/native_stack/abi_smoke.py" in allow
    assert all("ISSUE-0874" not in path and "EPIC-110" not in path for path in allow)


def test_workflow_separates_untrusted_validation_from_publisher_permissions() -> None:
    workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert set(workflow["on"]) == {"pull_request", "push"}
    assert workflow["permissions"] == {"contents": "read"}
    publish = workflow["jobs"]["publish"]
    assert publish["environment"] == "native-runtime-release"
    assert publish["permissions"] == {
        "contents": "read",
        "packages": "write",
        "id-token": "write",
    }
    assert "github.event_name == 'push'" in publish["if"]
    assert "github.repository == 'raphaelperrut/DSGeorref'" in publish["if"]
    assert "github.ref == 'refs/heads/codex/issue-973-native-runtime'" in publish["if"]
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "pull_request_target" not in text
    assert text.count("packages: write") == 1
    assert text.count("id-token: write") == 1
    assert "(.manifests // [])" not in text
    assert '--revocation-check-operation promotion' in text
    action_revisions = re.findall(r"^\s*uses:\s*[^@\s]+@([^\s#]+)", text, flags=re.MULTILINE)
    assert action_revisions
    assert all(re.fullmatch(r"[0-9a-f]{40}", revision) for revision in action_revisions)


def test_dockerfile_consumes_only_digest_and_hash_pinned_runtime_inputs() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "FROM docker.io/mambaorg/micromamba@sha256:e583f8e" in text
    assert "native-stack.conda-lock.txt" in text
    assert (
        "--checksum=sha256:944336ef298148dfd97478638567b223d929aba8717ad8be73ae962a62ecd61d" in text
    )
    assert "pip install --no-deps" in text
    assert "apt-get" not in text


def test_smoke_reads_required_versions_and_rejects_non_digest_candidate() -> None:
    smoke = _load_smoke_module()
    versions = smoke._locked_versions(SOURCE_LOCK)
    assert versions["runtime.python"] == "3.12.13"
    assert versions["native_stack.postgresql"] == "18.4"
    assert versions["native_stack.postgis"] == "3.6.4"
    assert smoke.SHA256_RE.fullmatch("sha256:" + "a" * 64)
    assert smoke.SHA256_RE.fullmatch("latest") is None


def test_smoke_retries_only_transient_database_connection_errors(monkeypatch) -> None:
    smoke = _load_smoke_module()

    class OperationalError(Exception):
        pass

    class FakePsycopg:
        attempts = 0

        @classmethod
        def connect(cls, dsn, **kwargs):
            assert dsn == "postgresql://smoke"
            assert kwargs == {"autocommit": False, "connect_timeout": 5}
            cls.attempts += 1
            if cls.attempts == 1:
                raise OperationalError("database is still starting")
            return nullcontext("connection")

    FakePsycopg.OperationalError = OperationalError
    ticks = iter((0.0, 0.1, 2.1))
    monkeypatch.setattr(smoke.time, "monotonic", lambda: next(ticks))
    monkeypatch.setattr(smoke.time, "sleep", lambda seconds: None)

    connection = smoke._connect_database(FakePsycopg, "postgresql://smoke", 120)
    assert connection is not None
    assert FakePsycopg.attempts == 2


def _oras_response(image_reference: str, referrers: object) -> dict[str, object]:
    return {
        "reference": image_reference,
        "mediaType": "application/vnd.oci.image.manifest.v1+json",
        "digest": image_reference.rsplit("@", 1)[1],
        "size": 2947,
        "referrers": referrers,
    }


def _completed_oras(response: object, returncode: int = 0) -> subprocess.CompletedProcess[str]:
    stdout = response if isinstance(response, str) else json.dumps(response)
    return subprocess.CompletedProcess(["oras"], returncode, stdout=stdout, stderr="")


def test_revocation_guard_accepts_valid_empty_referrers() -> None:
    validator = _load_validator_module()
    image = "ghcr.io/raphaelperrut/dsgeorref-native-stack@sha256:" + "a" * 64
    calls = []

    def runner(command, **kwargs):
        calls.append((command, kwargs))
        return _completed_oras(_oras_response(image, []))

    output = Mock()
    response = validator._query_fresh_revocation_state(image, "promotion", output, runner)
    assert response["referrers"] == []
    written = output.write_text.call_args.args[0]
    assert json.loads(written)["referrers"] == []
    assert len(calls) == 1
    assert "--artifact-type" in calls[0][0]
    assert validator.SHA256_RE.fullmatch(response["digest"])


def test_revocation_guard_rejects_applicable_revocation() -> None:
    validator = _load_validator_module()
    image = "ghcr.io/raphaelperrut/dsgeorref-native-stack@sha256:" + "b" * 64
    revocation = {
        "digest": "sha256:" + "c" * 64,
        "artifactType": validator.REVOCATION_ARTIFACT_TYPE,
    }

    with pytest.raises(RuntimeError, match="candidate image is revoked"):
        validator._query_fresh_revocation_state(
            image,
            "promotion",
            runner=lambda *args, **kwargs: _completed_oras(
                _oras_response(image, [revocation])
            ),
        )


def test_revocation_guard_rejects_missing_referrers_field() -> None:
    validator = _load_validator_module()
    image = "ghcr.io/raphaelperrut/dsgeorref-native-stack@sha256:" + "2" * 64
    response = _oras_response(image, [])
    del response["referrers"]
    with pytest.raises(RuntimeError, match="field referrers is missing or invalid"):
        validator._query_fresh_revocation_state(
            image,
            "promotion",
            runner=lambda *args, **kwargs: _completed_oras(response),
        )


@pytest.mark.parametrize(
    ("response", "message"),
    [
        ({"reference": "unused"}, "field mediaType is missing or invalid"),
        ({"referrers": None}, "field referrers is missing or invalid"),
        ({"referrers": {}}, "field referrers is missing or invalid"),
        ([], "response is not an object"),
        ("", "empty response"),
        ("not-json", "invalid JSON"),
    ],
)
def test_revocation_guard_rejects_malformed_responses(response, message) -> None:
    validator = _load_validator_module()
    image = "ghcr.io/raphaelperrut/dsgeorref-native-stack@sha256:" + "d" * 64
    if isinstance(response, dict) and set(response) == {"referrers"}:
        response = _oras_response(image, response["referrers"])
    with pytest.raises(RuntimeError, match=message):
        validator._query_fresh_revocation_state(
            image,
            "promotion",
            runner=lambda *args, **kwargs: _completed_oras(response),
        )


def test_revocation_guard_rejects_oras_failure_and_unavailability() -> None:
    validator = _load_validator_module()
    image = "ghcr.io/raphaelperrut/dsgeorref-native-stack@sha256:" + "e" * 64
    with pytest.raises(RuntimeError, match="exit code 1"):
        validator._query_fresh_revocation_state(
            image,
            "promotion",
            runner=lambda *args, **kwargs: _completed_oras("", returncode=1),
        )

    def unavailable(*args, **kwargs):
        raise OSError("registry unavailable")

    with pytest.raises(RuntimeError, match="query unavailable"):
        validator._query_fresh_revocation_state(image, "recovery", runner=unavailable)


def test_revocation_guard_queries_again_and_rejects_new_revocation() -> None:
    validator = _load_validator_module()
    image = "ghcr.io/raphaelperrut/dsgeorref-native-stack@sha256:" + "f" * 64
    responses = [
        _completed_oras(_oras_response(image, [])),
        _completed_oras(
            _oras_response(
                image,
                [
                    {
                        "digest": "sha256:" + "1" * 64,
                        "artifactType": validator.REVOCATION_ARTIFACT_TYPE,
                    }
                ],
            )
        ),
    ]
    calls = []

    def runner(*args, **kwargs):
        calls.append((args, kwargs))
        return responses.pop(0)

    validator._query_fresh_revocation_state(image, "promotion", runner=runner)
    with pytest.raises(RuntimeError, match="candidate image is revoked"):
        validator._query_fresh_revocation_state(image, "recovery", runner=runner)
    assert len(calls) == 2


def test_validator_accepts_only_the_current_fail_closed_promotion_state() -> None:
    resolved = yaml.safe_load(RESOLVED_LOCK.read_text(encoding="utf-8"))
    command = [
        sys.executable,
        str(ROOT / "tools/quality/native_stack/validate.py"),
        "--source-lock",
        str(SOURCE_LOCK.relative_to(ROOT)),
        "--resolved-lock",
        str(RESOLVED_LOCK.relative_to(ROOT)),
    ]
    if resolved["status"] == "VERIFIED":
        command.append("--require-resolved")
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["result"] == "PASS"
    if resolved["status"] == "NOT_BUILT":
        assert "image_digest" not in resolved
        return
    summary = json.loads((EVIDENCE / "publication-summary.json").read_text(encoding="utf-8"))
    assert resolved["status"] == "VERIFIED"
    assert resolved["source_lock_digest"] == summary["source_lock_digest"]
    assert resolved["build_commit_sha"] == summary["build_commit_sha"]
    assert resolved["image_digest"] == summary["image_digest"]
    assert resolved["sbom_digest"] == summary["sbom_digest"]
    assert resolved["provenance_digest"] == summary["provenance_digest"]
    assert resolved["signature_reference"] == summary["signature_reference"]
    assert resolved["abi_smoke_result"] == "PASS"
    assert resolved["artifact_linkage_verified"] is True
