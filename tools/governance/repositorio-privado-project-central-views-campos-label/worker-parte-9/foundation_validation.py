from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


class FoundationValidationError(ValueError):
    def __init__(self, findings: list[Finding] | tuple[Finding, ...]) -> None:
        self.findings = tuple(sorted(findings))
        message = "; ".join(
            f"{finding.code} at {finding.field}: {finding.detail}"
            for finding in self.findings
        )
        super().__init__(message)


EXPECTED_CAPABILITY_SCOPE = (
    "tools/governance/repositorio-privado-project-central-views-campos-label/"
    "worker-parte-9/**",
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/worker-parte-9/**",
    "tests/fnd/repositorio-privado-project-central-views-campos-label/"
    "test_worker_progress_cancellation_foundation.py",
    "evidence/implementation/repositorio-privado-project-central-views-campos-l/"
    "worker-parte-9/**",
)
TASK_ENVELOPE_PATH = re.compile(r"\.codex/tasks/TASK-[0-9]{4}\.json\Z")
EXPECTED_DENY_PATHS = ("src/**/epic-*", "src/**/issue-*")
LOCAL_TEST = EXPECTED_CAPABILITY_SCOPE[2]
REQUIREMENT_ROOT = "docs/01-product/requirements/"


def _evidence(
    requirement_file: str, authorities: tuple[str, ...], test_id: str
) -> dict[str, object]:
    return {
        "requirement_path": f"{REQUIREMENT_ROOT}{requirement_file}",
        "authority_paths": list(authorities),
        "checkpoint": f"{LOCAL_TEST}::{test_id}",
        "test_path": LOCAL_TEST,
        "test_id": test_id,
    }


EXPECTED_REQUIREMENTS = {
    "REQ-WORKER-008": _evidence(
        "REQ-WORKER-008-progresso-e-persistente-monotonico-e-reconciliavel-entre-sse-e-polling.md",
        (
            "docs/02-architecture/adrs/ADR-012-modelo-de-interacao-rest-sse-e-polling.md",
            "docs/02-architecture/adrs/ADR-018-postgresql-postgis-como-system-of-record.md",
            "docs/02-architecture/adrs/ADR-040-progresso-event-ledger-replay-e-eta.md",
            "docs/03-engineering/application-profiles/AP-007-worker-runtime-application-profile.md",
        ),
        "test_req_worker_008",
    ),
    "REQ-WORKER-009": _evidence(
        "REQ-WORKER-009-cancelamento-atua-somente-em-safe-points-e-preserva-consistencia-publica.md",
        (
            "docs/02-architecture/adrs/ADR-024-publicacao-atomica-checksums-e-content-addressing.md",
            "docs/02-architecture/adrs/ADR-037-workers-duraveis-leases-e-fencing.md",
            "docs/02-architecture/adrs/ADR-038-retry-quarantine-checkpoints-cancelamento-e-drain.md",
            "docs/03-engineering/application-profiles/AP-007-worker-runtime-application-profile.md",
        ),
        "test_req_worker_009",
    ),
}

EXPECTED_POLICY: dict[str, Any] = {
    "schema_version": "1.0.0",
    "policy_id": "ENGINEERING-FOUNDATION-WORKER-PROGRESS-CANCELLATION",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "coverage": list(EXPECTED_REQUIREMENTS),
    "controls": {
        "progress": {
            "authority": "PostgreSQL",
            "granularity": "WORK_UNIT",
            "typed": "REQUIRED",
            "monotonic": "REQUIRED",
            "regression": "REJECT",
            "sse": "PERSISTED_PROGRESS_ONLY",
            "polling": "RECONCILIATION_REQUIRED",
            "transport_state_authority": "REJECT",
        },
        "cancellation": {
            "request_token": "PERSISTED",
            "mode": "COOPERATIVE",
            "application": "SAFE_POINTS_ONLY",
            "lease_validation": "REQUIRED_BEFORE_COMMIT_CHECKPOINT_OR_PUBLICATION",
            "publication": "ATOMIC_ONLY",
            "partial_result_current": "REJECT",
        },
        "failure_handling": {
            "mode": "FAIL_CLOSED",
            "silent_fallback": "PROHIBITED",
            "incomplete_configuration": "REJECT",
        },
    },
    "requirements": EXPECTED_REQUIREMENTS,
}

AUTHORITY_MARKERS = {
    "docs/02-architecture/adrs/ADR-012-modelo-de-interacao-rest-sse-e-polling.md": (
        "SSE entrega progresso persistido e monotônico; polling é fallback obrigatório de reconciliação.",
        "Eventos de transporte não substituem o estado autoritativo no PostgreSQL.",
    ),
    "docs/02-architecture/adrs/ADR-018-postgresql-postgis-como-system-of-record.md": (
        "PostgreSQL/PostGIS é a fonte autoritativa",
        "Broker, logs, frontend e filesystem não substituem o estado relacional.",
    ),
    "docs/02-architecture/adrs/ADR-040-progresso-event-ledger-replay-e-eta.md": (
        "Progresso é persistido por work units, tipado e monotônico.",
        "Telemetria do Celery é derivada e não substitui o estado do produto.",
    ),
    "docs/02-architecture/adrs/ADR-024-publicacao-atomica-checksums-e-content-addressing.md": (
        "Publicação ocorre em staging no mesmo filesystem, seguida de fsync, validação e rename atômico.",
        "Falha antes do rename deixa apenas staging reconciliável e nunca um resultado vigente.",
    ),
    "docs/02-architecture/adrs/ADR-037-workers-duraveis-leases-e-fencing.md": (
        "Toda gravação, checkpoint e publicação valida lease, token e revision.",
        "Worker que perdeu lease não pode commitar efeito tardio.",
    ),
    "docs/02-architecture/adrs/ADR-038-retry-quarantine-checkpoints-cancelamento-e-drain.md": (
        "Pause/cancel usa token persistente e safe points",
    ),
    "docs/03-engineering/application-profiles/AP-007-worker-runtime-application-profile.md": (
        "progresso persistente e monotônico",
        "cancelamento por token persistente e safe points",
    ),
}


def _finding_code(field: str) -> str:
    mappings = {
        "$.coverage": "COVERAGE_INCOMPLETE",
        "$.write_scope": "WRITE_SCOPE_INVALID",
        "$.requirements": "REQUIREMENT_EVIDENCE_INVALID",
        "$.controls.progress": "PROGRESS_POLICY_INVALID",
        "$.controls.cancellation": "CANCELLATION_POLICY_INVALID",
        "$.controls.failure_handling": "FAIL_CLOSED_POLICY_INVALID",
    }
    return next(
        (code for prefix, code in mappings.items() if field.startswith(prefix)),
        "POLICY_STRUCTURE_INVALID",
    )


def _compare(actual: object, expected: object, field: str) -> list[Finding]:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [Finding(_finding_code(field), field, "expected object")]
        findings: list[Finding] = []
        for key in sorted(actual.keys() - expected.keys()):
            findings.append(
                Finding("POLICY_STRUCTURE_INVALID", f"{field}.{key}", "unknown field")
            )
        for key in sorted(expected.keys() - actual.keys()):
            target = f"{field}.{key}"
            findings.append(Finding(_finding_code(target), target, "missing field"))
        for key in sorted(actual.keys() & expected.keys()):
            findings.extend(_compare(actual[key], expected[key], f"{field}.{key}"))
        return findings
    if type(actual) is not type(expected) or actual != expected:
        return [Finding(_finding_code(field), field, f"expected {expected!r}")]
    return []


def _safe_file(repository_root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    if ".." in Path(value).parts or not value.startswith((".codex/", "docs/", "tests/")):
        return None
    candidate = (repository_root / value).resolve()
    try:
        candidate.relative_to(repository_root)
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def _reference_findings(
    policy: dict[str, Any], repository_root: Path
) -> list[Finding]:
    requirements = policy.get("requirements")
    if not isinstance(requirements, dict):
        return []
    findings: list[Finding] = []
    for requirement_id, evidence in requirements.items():
        field = f"$.requirements.{requirement_id}"
        if not isinstance(evidence, dict):
            continue
        references = [evidence.get("requirement_path"), evidence.get("test_path")]
        authorities = evidence.get("authority_paths")
        if not isinstance(authorities, list):
            findings.append(
                Finding("REFERENCE_INVALID", f"{field}.authority_paths", "expected path list")
            )
            authorities = []
        for index, reference in enumerate([*references, *authorities]):
            if _safe_file(repository_root, reference) is None:
                findings.append(
                    Finding("REFERENCE_INVALID", f"{field}.references[{index}]", "missing or unsafe file")
                )
        checkpoint = evidence.get("checkpoint")
        if not isinstance(checkpoint, str) or "::" not in checkpoint:
            findings.append(
                Finding("CHECKPOINT_INVALID", f"{field}.checkpoint", "invalid selector")
            )
            continue
        path_value, symbol = checkpoint.rsplit("::", 1)
        path = _safe_file(repository_root, path_value)
        if path is None or not symbol:
            findings.append(
                Finding("CHECKPOINT_INVALID", f"{field}.checkpoint", "missing selector target")
            )
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError) as error:
            findings.append(Finding("CHECKPOINT_INVALID", f"{field}.checkpoint", str(error)))
            continue
        functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
        if symbol not in functions:
            findings.append(
                Finding("CHECKPOINT_INVALID", f"{field}.checkpoint", "test symbol absent")
            )
    return findings


def _scope_findings(policy: dict[str, Any], repository_root: Path) -> list[Finding]:
    scope = policy.get("write_scope")
    if not isinstance(scope, list) or not all(isinstance(path, str) for path in scope):
        return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "expected path list")]
    valid_shape = (
        len(scope) == len(EXPECTED_CAPABILITY_SCOPE) + 1
        and TASK_ENVELOPE_PATH.fullmatch(scope[0]) is not None
        and scope[1:] == list(EXPECTED_CAPABILITY_SCOPE)
    )
    if not valid_shape:
        return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "capability scope mismatch")]
    roots = [path.removesuffix("/**").rstrip("/") for path in scope]
    if len(roots) != len(set(roots)) or any(
        left.startswith(f"{right}/") or right.startswith(f"{left}/")
        for index, left in enumerate(roots)
        for right in roots[index + 1 :]
    ):
        return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "overlapping paths")]
    try:
        task = json.loads((repository_root / scope[0]).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [Finding("TASK_ENVELOPE_INVALID", "$.write_scope", str(error))]
    findings: list[Finding] = []
    review_scope = task.get("phase_f_review", {}).get("files", {}).get("allow_paths")
    if task.get("allow_paths") != scope or review_scope != scope:
        findings.append(
            Finding("WRITE_SCOPE_INVALID", "$.write_scope", "TaskEnvelope scope mismatch")
        )
    if task.get("deny_paths") != list(EXPECTED_DENY_PATHS):
        findings.append(Finding("DENY_PATHS_INVALID", "$.deny_paths", "deny paths changed"))
    return findings


def _authority_findings(repository_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path_value, markers in AUTHORITY_MARKERS.items():
        path = _safe_file(repository_root, path_value)
        if path is None:
            findings.append(Finding("AUTHORITY_UNREADABLE", path_value, "missing or unsafe file"))
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(Finding("AUTHORITY_UNREADABLE", path_value, str(error)))
            continue
        for marker in markers:
            if marker not in content:
                findings.append(Finding("AUTHORITY_MISMATCH", path_value, marker))
    return findings


def validate_policy(policy: object, repository_root: Path) -> list[Finding]:
    if not isinstance(policy, dict):
        return sorted(_compare(policy, EXPECTED_POLICY, "$"))
    comparable = {key: value for key, value in policy.items() if key != "write_scope"}
    findings = _compare(comparable, EXPECTED_POLICY, "$")
    findings.extend(_reference_findings(policy, repository_root.resolve()))
    findings.extend(_scope_findings(policy, repository_root.resolve()))
    findings.extend(_authority_findings(repository_root.resolve()))
    return sorted(set(findings))


def load_policy(path: Path, repository_root: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise FoundationValidationError(
            [Finding("POLICY_UNREADABLE", "$", str(error))]
        ) from error
    findings = validate_policy(loaded, repository_root)
    if findings:
        raise FoundationValidationError(findings)
    return loaded
