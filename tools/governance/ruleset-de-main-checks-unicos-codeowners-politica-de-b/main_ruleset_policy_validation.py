from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from typing import Any, cast

import yaml  # type: ignore[import-untyped]

SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
UTC_TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class FoundationValidationError(ValueError):
    """Raised when main-branch governance evidence cannot be accepted."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FoundationValidationError(message)


def require_exact_keys(value: Any, expected: set[str], subject: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{subject} must be an object")
    require(set(value) == expected, f"{subject} fields are incomplete or unknown")
    return cast(dict[str, Any], value)


def _safe_workflow_path(raw_path: Any) -> PurePosixPath:
    require(isinstance(raw_path, str) and bool(raw_path), "required check workflow is missing")
    path = PurePosixPath(raw_path)
    require(
        path.parts[:2] == (".github", "workflows")
        and len(path.parts) == 3
        and path.suffix in {".yml", ".yaml"},
        "required check workflow path is outside .github/workflows",
    )
    return path


def _workflow_jobs(root: Path) -> dict[str, list[tuple[str, str]]]:
    jobs: dict[str, list[tuple[str, str]]] = {}
    for path in sorted((root / ".github/workflows").glob("*.y*ml")):
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        require(isinstance(loaded, dict), f"workflow is invalid: {path.name}")
        workflow_jobs = loaded.get("jobs")
        require(isinstance(workflow_jobs, dict), f"workflow jobs are invalid: {path.name}")
        relative_path = path.relative_to(root).as_posix()
        for job_id in workflow_jobs:
            require(
                isinstance(job_id, str) and bool(job_id),
                f"workflow job id is invalid: {path.name}",
            )
            jobs.setdefault(job_id, []).append((relative_path, job_id))
    return jobs


def validate_required_check_registry(registry: Any, root: Path) -> list[str]:
    document = require_exact_keys(
        registry,
        {
            "schema_version",
            "registry_id",
            "protected_branch",
            "uniqueness_key",
            "duplicate_context",
            "required_checks",
        },
        "required check registry",
    )
    require(document["schema_version"] == "1.0.0", "unsupported registry version")
    require(document["registry_id"] == "MAIN-REQUIRED-CHECKS", "invalid registry identity")
    require(document["protected_branch"] == "main", "registry must protect main")
    require(document["uniqueness_key"] == "CHECK_CONTEXT", "invalid uniqueness key")
    require(document["duplicate_context"] == "REJECT", "duplicate contexts must reject")
    records = document["required_checks"]
    require(
        isinstance(records, list) and bool(records),
        "required check registry must not be empty",
    )
    workflow_jobs = _workflow_jobs(root)
    contexts: list[str] = []
    for raw_record in records:
        record = require_exact_keys(raw_record, {"context", "workflow", "job"}, "check record")
        context = record["context"]
        job = record["job"]
        require(isinstance(context, str) and bool(context), "required check context is missing")
        require(isinstance(job, str) and job == context, "check context must equal its job id")
        workflow = _safe_workflow_path(record["workflow"]).as_posix()
        require(
            (workflow, job) in workflow_jobs.get(context, []),
            "required check producer is missing",
        )
        require(len(workflow_jobs[context]) == 1, "required check context has ambiguous producers")
        contexts.append(context)
    require(len(contexts) == len(set(contexts)), "duplicate required check context")
    return contexts


def validate_codeowners(text: str) -> list[str]:
    entries: list[tuple[str, list[str]]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        require(len(fields) >= 2, "CODEOWNERS entry has no owner")
        owners = fields[1:]
        require(
            all(owner.startswith("@") and len(owner) > 1 for owner in owners),
            "unresolved owner",
        )
        entries.append((fields[0], owners))
    require(
        bool(entries) and any(pattern == "*" for pattern, _ in entries),
        "global CODEOWNERS coverage missing",
    )
    return sorted({owner for _, owners in entries for owner in owners})


def validate_ruleset(
    ruleset: Any,
    *,
    contract: dict[str, Any],
    required_contexts: list[str],
) -> None:
    document = require_exact_keys(
        ruleset,
        {
            "schema_version",
            "ruleset_id",
            "source_contract",
            "desired_enforcement",
            "live_enforcement_evidence",
            "branch_policy",
            "required_check_policy",
            "codeowners_policy",
            "bypass_policy",
            "authority",
            "failure_policy",
        },
        "main ruleset",
    )
    require(document["schema_version"] == "1.0.0", "unsupported ruleset version")
    require(document["ruleset_id"] == "DSGEOREF-MAIN", "invalid ruleset identity")
    require(
        document["source_contract"]
        == "contracts/contexts/engineering_governance/fnd/"
        "ruleset-de-main-checks-unicos-codeowners-politica-de-b/"
        "examples/main-ruleset-governance.json",
        "ruleset source contract diverges",
    )
    require(
        document["desired_enforcement"] == "ACTIVE",
        "main ruleset must target active enforcement",
    )
    require(
        document["live_enforcement_evidence"] == "NOT_ASSERTED_BY_FOUNDATION",
        "foundation must not assert live enforcement",
    )
    require(document["branch_policy"] == contract["branch_policy"], "branch policy diverges")
    expected_checks = dict(contract["required_check_policy"])
    expected_checks["required_contexts"] = required_contexts
    require(document["required_check_policy"] == expected_checks, "required check policy diverges")
    for field in ("codeowners_policy", "bypass_policy", "authority", "failure_policy"):
        require(document[field] == contract[field], f"{field} diverges from frozen contract")


def validate_bypass_record(
    record: Any,
    *,
    ruleset_id: str,
    candidate_sha: str,
    delivery_approval_verdict_ref: str,
) -> None:
    fields = {
        "event_id",
        "ruleset_id",
        "protected_branch",
        "candidate_sha",
        "actor_subject",
        "reason",
        "occurred_at",
        "delivery_approval_verdict_ref",
    }
    document = require_exact_keys(record, fields, "bypass record")
    require(SHA_PATTERN.fullmatch(candidate_sha) is not None, "candidate SHA must be exact")
    require(document["ruleset_id"] == ruleset_id, "bypass ruleset binding mismatch")
    require(document["protected_branch"] == "main", "bypass branch binding mismatch")
    require(document["candidate_sha"] == candidate_sha, "bypass candidate SHA is stale")
    require(
        document["delivery_approval_verdict_ref"] == delivery_approval_verdict_ref
        and bool(delivery_approval_verdict_ref),
        "bypass delivery approval evidence is missing or invalid",
    )
    for field in ("event_id", "actor_subject", "reason"):
        require(
            isinstance(document[field], str) and bool(document[field].strip()),
            f"{field} missing",
        )
    occurred_at = document["occurred_at"]
    require(
        isinstance(occurred_at, str) and UTC_TIMESTAMP_PATTERN.fullmatch(occurred_at) is not None,
        "bypass timestamp must be an explicit UTC instant",
    )
