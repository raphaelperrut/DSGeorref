from __future__ import annotations

import ast
import json
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


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
    "sprint-001-tool-worker-parte-8/**",
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "sprint-001-tool-worker-parte-8/**",
    "tests/fnd/repositorio-privado-project-central-views-campos-label/"
    "test_tool_worker_foundation.py",
    "evidence/implementation/repositorio-privado-project-central-views-campos-l/"
    "sprint-001-tool-worker-parte-8/**",
)
TASK_ENVELOPE_PATH = re.compile(r"\.codex/tasks/TASK-[0-9]{4}\.json\Z")
EXPECTED_DENY_PATHS = ("src/**/epic-*", "src/**/issue-*")
CENTRAL_TEST = (
    "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "test_materialization.py"
)
LOCAL_TEST = EXPECTED_CAPABILITY_SCOPE[2]
REQUIREMENT_ROOT = "docs/01-product/requirements/"


def _evidence(
    requirement_file: str, authority: str, test_path: str, test_id: str
) -> dict[str, str]:
    return {
        "requirement_path": f"{REQUIREMENT_ROOT}{requirement_file}",
        "authority_path": authority,
        "checkpoint": f"{test_path}::{test_id}",
        "test_path": test_path,
        "test_id": test_id,
    }


EXPECTED_REQUIREMENTS = {
    "REQ-SPRINT-001-010": _evidence(
        "REQ-SPRINT-001-010-liberar-primeira-fatia-funcional-somente-por-cutover-explicito-apos-foun.md",
        "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "sprint-001-tool-parte-2/sprint_decisions.py",
        CENTRAL_TEST,
        "test_sprint_zero_baseline_decision_10",
    ),
    "REQ-TOOL-001": _evidence(
        "REQ-TOOL-001-python-3-12-runtime-primario-com-upgrade-controlado-para-3-13-e-3-14.md",
        "docs/03-engineering/PYTHON_312_RUNTIME_POLICY.md",
        CENTRAL_TEST,
        "test_python_312_primary_and_upgrade_gates",
    ),
    "REQ-TOOL-002": _evidence(
        "REQ-TOOL-002-dependencias-python-usam-uv-workspace-e-lock-frozen.md",
        "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "sprint-001-tool-parte-2/uv_validation.py",
        CENTRAL_TEST,
        "test_uv_lock_frozen",
    ),
    "REQ-TOOL-005": _evidence(
        "REQ-TOOL-005-dominio-transporte-e-persistencia-possuem-modelos-separados.md",
        "contracts/architecture/python-module-boundaries.yaml",
        LOCAL_TEST,
        "test_model_boundary_architecture",
    ),
    "REQ-WORKER-002": _evidence(
        "REQ-WORKER-002-existem-poucas-filas-duraveis-por-classe-de-workload-sem-fila-dinamica-p.md",
        "contracts/operations/lock-and-queue-policy.yaml",
        LOCAL_TEST,
        "test_req_worker_002",
    ),
    "REQ-WORKER-003": _evidence(
        "REQ-WORKER-003-ack-ocorre-somente-apos-commit-autoritativo-e-prefetch-e-calibrado-por-w.md",
        "contracts/operations/lock-and-queue-policy.yaml",
        LOCAL_TEST,
        "test_req_worker_003",
    ),
    "REQ-WORKER-004": _evidence(
        "REQ-WORKER-004-workers-usam-prefork-reciclavel-e-isolamento-explicito-de-processos-subp.md",
        "docs/03-engineering/application-profiles/AP-007-worker-runtime-application-profile.md",
        LOCAL_TEST,
        "test_req_worker_004",
    ),
    "REQ-WORKER-005": _evidence(
        "REQ-WORKER-005-leases-persistem-em-postgresql-com-fencing-token-e-expiracao-verificavel.md",
        "contracts/operations/lock-and-queue-policy.yaml",
        LOCAL_TEST,
        "test_req_worker_005",
    ),
    "REQ-WORKER-006": _evidence(
        "REQ-WORKER-006-retry-segue-taxonomia-de-dominio-poison-messages-entram-em-quarantine-au.md",
        "contracts/operations/lock-and-queue-policy.yaml",
        LOCAL_TEST,
        "test_req_worker_006",
    ),
    "REQ-WORKER-007": _evidence(
        "REQ-WORKER-007-scheduler-e-outbox-sao-autoritativos-para-dag-despacho-e-redelivery.md",
        "docs/03-engineering/application-profiles/AP-007-worker-runtime-application-profile.md",
        LOCAL_TEST,
        "test_req_worker_007",
    ),
}

EXPECTED_POLICY: dict[str, Any] = {
    "schema_version": "1.0.0",
    "policy_id": "ENGINEERING-FOUNDATION-TOOL-WORKER",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "coverage": list(EXPECTED_REQUIREMENTS),
    "controls": {
        "cutover": {
            "mode": "EXPLICIT",
            "foundation_gate": "APPROVED_REQUIRED",
            "missing_authorization": "REJECT",
        },
        "python_runtime": {
            "primary": "3.12.13",
            "requires_python": ">=3.12,<3.13",
            "future_versions": "GATED_NON_BLOCKING",
        },
        "python_dependencies": {
            "manager": "uv",
            "workspace": "REQUIRED",
            "lock": "FROZEN_REQUIRED",
        },
        "model_boundaries": {
            "domain": "SEPARATE",
            "transport": "SEPARATE",
            "persistence": "SEPARATE",
            "cross_layer_model_reuse": "REJECT",
        },
        "worker": {
            "queue": {
                "classes": ["interactive", "batch", "ai-gpu", "maintenance"],
                "dynamic_per_job": "REJECT",
            },
            "ack_prefetch": {
                "ack": "AFTER_AUTHORITATIVE_COMMIT",
                "initial_prefetch": 1,
                "promotion_owner": "BP-004",
                "premature_ack": "REJECT",
            },
            "isolation": {
                "pool": "PREFORK",
                "process_isolation": "REQUIRED",
                "recycling": "REQUIRED",
                "missing_isolation_or_recycling": "REJECT",
            },
            "leases": {
                "authority": "PostgreSQL",
                "fencing_token": "REQUIRED",
                "expiration": "VERIFIABLE",
                "stale_owner_commit_or_publish": "REJECT",
            },
            "retry": {
                "taxonomy": "CLASSIFIED_TECHNICAL_ONLY",
                "poison_message": "AUDITABLE_QUARANTINE",
                "unclassified_or_unquarantined": "REJECT",
            },
            "dispatch": {
                "authority": "SCHEDULER_AND_OUTBOX",
                "direct_fanout": "REJECT",
                "redelivery": "OUTBOX_RECONCILED",
            },
        },
        "failure_handling": {
            "mode": "FAIL_CLOSED",
            "silent_fallback": "PROHIBITED",
            "incomplete_configuration": "REJECT",
        },
    },
    "requirements": EXPECTED_REQUIREMENTS,
}


def _finding_code(field: str) -> str:
    mappings = {
        "$.coverage": "COVERAGE_INCOMPLETE",
        "$.write_scope": "WRITE_SCOPE_INVALID",
        "$.requirements": "REQUIREMENT_EVIDENCE_INVALID",
        "$.controls.model_boundaries": "MODEL_BOUNDARY_INVALID",
        "$.controls.worker.queue": "QUEUE_POLICY_INVALID",
        "$.controls.worker.ack_prefetch": "ACK_PREFETCH_POLICY_INVALID",
        "$.controls.worker.isolation": "WORKER_ISOLATION_INVALID",
        "$.controls.worker.leases": "FENCING_POLICY_INVALID",
        "$.controls.worker.retry": "RETRY_POLICY_INVALID",
        "$.controls.worker.dispatch": "DISPATCH_POLICY_INVALID",
        "$.controls.failure_handling": "FAIL_CLOSED_POLICY_INVALID",
    }
    for prefix, code in mappings.items():
        if field.startswith(prefix):
            return code
    return "POLICY_STRUCTURE_INVALID"


def _compare(actual: object, expected: object, field: str) -> list[Finding]:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [Finding(_finding_code(field), field, "expected object")]
        findings: list[Finding] = []
        for key in sorted(actual.keys() - expected.keys()):
            findings.append(Finding("POLICY_STRUCTURE_INVALID", f"{field}.{key}", "unknown field"))
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
    if not isinstance(value, str) or not value or "\\" in value or ".." in Path(value).parts:
        return None
    permitted_roots = (".codex/", "contracts/", "docs/", "tests/", "tools/")
    permitted_files = {".python-version", "pyproject.toml", "uv.lock"}
    if value not in permitted_files and not value.startswith(permitted_roots):
        return None
    candidate = (repository_root / value).resolve()
    try:
        candidate.relative_to(repository_root)
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def _reference_findings(policy: dict[str, Any], repository_root: Path) -> list[Finding]:
    requirements = policy.get("requirements")
    if not isinstance(requirements, dict):
        return []
    findings: list[Finding] = []
    for requirement_id, evidence in requirements.items():
        field = f"$.requirements.{requirement_id}"
        if not isinstance(evidence, dict):
            continue
        for key in ("requirement_path", "authority_path", "test_path"):
            if _safe_file(repository_root, evidence.get(key)) is None:
                findings.append(Finding("REFERENCE_INVALID", f"{field}.{key}", "missing or unsafe file"))
        checkpoint = evidence.get("checkpoint")
        if not isinstance(checkpoint, str) or "::" not in checkpoint:
            findings.append(Finding("CHECKPOINT_INVALID", f"{field}.checkpoint", "invalid selector"))
            continue
        path_value, symbol = checkpoint.rsplit("::", 1)
        path = _safe_file(repository_root, path_value)
        if path is None or not symbol:
            findings.append(Finding("CHECKPOINT_INVALID", f"{field}.checkpoint", "missing selector target"))
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError) as error:
            findings.append(Finding("CHECKPOINT_INVALID", f"{field}.checkpoint", str(error)))
            continue
        functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
        if symbol not in functions:
            findings.append(Finding("CHECKPOINT_INVALID", f"{field}.checkpoint", "test symbol absent"))
    return findings


def _task_findings(
    repository_root: Path, task_path: str, expected_scope: list[str]
) -> list[Finding]:
    try:
        task = json.loads((repository_root / task_path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [Finding("TASK_ENVELOPE_INVALID", "$.write_scope", str(error))]
    allow_paths = task.get("allow_paths")
    review_paths = task.get("phase_f_review", {}).get("files", {}).get("allow_paths")
    findings: list[Finding] = []
    if allow_paths != expected_scope or review_paths != allow_paths:
        findings.append(Finding("WRITE_SCOPE_INVALID", "$.write_scope", "TaskEnvelope scope mismatch"))
    if task.get("deny_paths") != list(EXPECTED_DENY_PATHS):
        findings.append(Finding("DENY_PATHS_INVALID", "$.deny_paths", "deny paths changed"))
    return findings


def _scope_findings(policy: dict[str, Any], repository_root: Path) -> list[Finding]:
    scope = policy.get("write_scope")
    if not isinstance(scope, list) or not all(isinstance(path, str) for path in scope):
        return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "expected path list")]
    if (
        len(scope) != len(EXPECTED_CAPABILITY_SCOPE) + 1
        or TASK_ENVELOPE_PATH.fullmatch(scope[0]) is None
        or scope[1:] != list(EXPECTED_CAPABILITY_SCOPE)
    ):
        return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "capability scope mismatch")]
    roots = [path.removesuffix("/**").rstrip("/") for path in scope]
    if len(roots) != len(set(roots)) or any(
        left.startswith(f"{right}/") or right.startswith(f"{left}/")
        for index, left in enumerate(roots)
        for right in roots[index + 1 :]
    ):
        return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "overlapping paths")]
    if _safe_file(repository_root, scope[0]) is None:
        return [Finding("TASK_ENVELOPE_INVALID", "$.write_scope[0]", "missing or unsafe envelope")]
    return _task_findings(repository_root, scope[0], scope)


def _authority_findings(repository_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        pyproject = tomllib.loads((repository_root / "pyproject.toml").read_text(encoding="utf-8"))
        python_pin = (repository_root / ".python-version").read_text(encoding="utf-8").strip()
        boundaries = yaml.safe_load(
            (repository_root / "contracts/architecture/python-module-boundaries.yaml").read_text(encoding="utf-8")
        )
        queue_policy = yaml.safe_load(
            (repository_root / "contracts/operations/lock-and-queue-policy.yaml").read_text(encoding="utf-8")
        )
        worker_profile = (
            repository_root / "docs/03-engineering/application-profiles/AP-007-worker-runtime-application-profile.md"
        ).read_text(encoding="utf-8")
    except (OSError, UnicodeError, tomllib.TOMLDecodeError, yaml.YAMLError) as error:
        return [Finding("AUTHORITY_UNREADABLE", "$.controls", str(error))]
    runtime = boundaries.get("runtime", {})
    if python_pin != "3.12.13" or pyproject.get("project", {}).get("requires-python") != ">=3.12,<3.13" or runtime.get("primary") != "3.12":
        findings.append(Finding("PYTHON_RUNTIME_AUTHORITY_MISMATCH", "$.controls.python_runtime", "Python 3.12 baseline mismatch"))
    broker = queue_policy.get("broker", {})
    leases = queue_policy.get("leases", {})
    expected_broker = EXPECTED_POLICY["controls"]["worker"]
    if broker.get("durable_queue_classes") != expected_broker["queue"]["classes"] or broker.get("ack") != "after authoritative commit" or broker.get("initial_prefetch") != 1 or broker.get("prefetch_promotion_owner") != "BP-004":
        findings.append(Finding("WORKER_AUTHORITY_MISMATCH", "$.controls.worker", "queue/ack/prefetch mismatch"))
    if leases.get("heartbeat_authority") != "PostgreSQL" or leases.get("require_fencing_token") is not True or leases.get("stale_owner_cannot_publish") is not True:
        findings.append(Finding("WORKER_AUTHORITY_MISMATCH", "$.controls.worker.leases", "lease authority mismatch"))
    if "processo worker isolado/reciclável" not in worker_profile or "fan-out somente pelo scheduler/outbox" not in worker_profile:
        findings.append(Finding("WORKER_AUTHORITY_MISMATCH", "$.controls.worker", "worker profile mismatch"))
    return findings


def validate_policy(policy: object, repository_root: Path) -> list[Finding]:
    if not isinstance(policy, dict):
        return sorted(_compare(policy, EXPECTED_POLICY, "$"))
    comparable_policy = {key: value for key, value in policy.items() if key != "write_scope"}
    findings = _compare(comparable_policy, EXPECTED_POLICY, "$")
    findings.extend(_reference_findings(policy, repository_root.resolve()))
    findings.extend(_scope_findings(policy, repository_root.resolve()))
    findings.extend(_authority_findings(repository_root.resolve()))
    return sorted(set(findings))


def load_policy(path: Path, repository_root: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise FoundationValidationError([Finding("POLICY_UNREADABLE", "$", str(error))]) from error
    findings = validate_policy(loaded, repository_root)
    if findings:
        raise FoundationValidationError(findings)
    return loaded
