from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SLUG = "migrations-ci-secret-dependency-scan-e-telemetria-mini"
TASK_PATH = Path(".codex/tasks/TASK-0024.json")
FOUNDATION_PATH = Path(
    "contracts/contexts/engineering_governance/fnd/"
    f"{SLUG}/aie-bex-epic-parte-1/examples/contract-foundation.json"
)
JOB_PATH = Path("contracts/domain/job.schema.json")
ATTEMPT_PATH = Path("contracts/domain/attempt.schema.json")
TASK_ENVELOPE_PATH = Path("contracts/events/task-envelope.schema.json")
NATIVE_POLICY_PATH = Path(
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "native-pln-parte-3/foundation-policy.json"
)
TECHNOLOGY_BASELINE_PATH = Path("docs/03-engineering/TECHNOLOGY_BASELINE.yaml")
BATCH_REPORTING_PATH = Path(
    "docs/04-quality/STRONG_GEOMETRIC_VERIFIER_AND_BATCH_REPORTING.md"
)
DATABASE_MIGRATIONS_PATH = Path("docs/03-engineering/DATABASE_MIGRATIONS.md")
ROLLBACK_MATRIX_PATH = Path("contracts/operations/version-and-rollback-matrix.yaml")
QUALITY_VALIDATOR_PATH = Path(
    f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py"
)
EXPECTED_ALLOW_PATHS = (
    ".codex/tasks/TASK-0024.json",
    f"tools/governance/{SLUG}/**",
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
    "evidence/implementation/epic-005/story-0024/**",
)
EXPECTED_TESTS = (
    "test_batch_execution_decision_01",
    "test_batch_execution_decision_06",
    "test_first_functional_slice_decision_06",
    "test_epic_005_integracao",
)
EXPECTED_AC_IDS = tuple(f"AC-ISSUE-0134-{index:02d}" for index in range(1, 5))
EXPECTED_QUALITY_AC_IDS = tuple(
    f"AC-ISSUE-0133-{index:02d}" for index in range(1, 5)
)
EXPECTED_QUALITY_REQUIREMENT_COUNT = 51
REQUIREMENTS = {
    "REQ-BEX-001": (
        Path(
            "docs/01-product/requirements/"
            "REQ-BEX-001-representar-lote-imagem-tentativa-e-work-units-em-hierarquia-explicita.md"
        ),
        "representar lote, imagem, tentativa e work units em hierarquia explícita",
        "test_batch_execution_decision_01",
        "ADR-039",
    ),
    "REQ-BEX-006": (
        Path(
            "docs/01-product/requirements/"
            "REQ-BEX-006-persistir-checkpoints-canonicos-por-estagio-imagem-e-tentativa.md"
        ),
        "persistir checkpoints canônicos por estágio, imagem e tentativa",
        "test_batch_execution_decision_06",
        "ADR-038",
    ),
    "REQ-FS1-006": (
        Path(
            "docs/01-product/requirements/"
            "REQ-FS1-006-usar-homografia-canonica-e-usac-magsac-sem-fallback-silencioso.md"
        ),
        "usar homografia canônica e USAC_MAGSAC sem fallback silencioso",
        "test_first_functional_slice_decision_06",
        "ADR-045",
    ),
}


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"artifact": self.artifact, "code": self.code, "detail": self.detail}


def _load_json(root: Path, path: Path) -> tuple[Mapping[str, Any] | None, list[Finding]]:
    try:
        loaded = json.loads((root / path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [Finding("DOCUMENT_INVALID", path.as_posix(), str(error))]
    if not isinstance(loaded, Mapping):
        return None, [Finding("DOCUMENT_INVALID", path.as_posix(), "object required")]
    return loaded, []


def _load_text(root: Path, path: Path) -> tuple[str, list[Finding]]:
    try:
        return (root / path).read_text(encoding="utf-8"), []
    except (OSError, UnicodeError) as error:
        return "", [Finding("DOCUMENT_INVALID", path.as_posix(), str(error))]


def _nested(document: Mapping[str, Any], *keys: str) -> object:
    current: object = document
    for key in keys:
        if not isinstance(current, Mapping):
            return None
        current = current.get(key)
    return current


def _task_findings(task: Mapping[str, Any]) -> list[Finding]:
    expected = {
        "task_id": "TASK-0024",
        "issue_id": "ISSUE-0134",
        "story_id": "STORY-0024",
        "epic_id": "EPIC-005",
        "role": "Tech Lead",
        "bounded_context": "BC-001",
    }
    findings = [
        Finding("TASK_IDENTITY_INVALID", field, f"expected {value}")
        for field, value in expected.items()
        if task.get(field) != value
    ]
    exact_lists = {
        "allow_paths": EXPECTED_ALLOW_PATHS,
        "deny_paths": ("src/**/epic-*", "src/**/issue-*"),
        "tests": EXPECTED_TESTS,
        "dependencies": ("STORY-0022", "STORY-0023"),
        "acceptance_criterion_ids": EXPECTED_AC_IDS,
    }
    for field, expected_values in exact_lists.items():
        actual = task.get(field)
        if not isinstance(actual, list) or tuple(actual) != expected_values:
            findings.append(
                Finding("TASK_SCOPE_INVALID", field, "governed values drifted")
            )
    phase_files = _nested(task, "phase_f_review", "files", "allow_paths")
    if not isinstance(phase_files, list) or tuple(phase_files) != EXPECTED_ALLOW_PATHS:
        findings.append(
            Finding("TASK_SCOPE_INVALID", "phase_f_review.files", "scope drift")
        )
    database = _nested(task, "phase_f_review", "database")
    database_valid = bool(
        isinstance(database, Mapping)
        and database.get("applicability") == "APPLICABLE"
        and database.get("migration_required") is True
        and database.get("rollback_required") is True
    )
    if not database_valid:
        findings.append(
            Finding(
                "MIGRATION_DECLARATION_INVALID",
                TASK_PATH.as_posix(),
                "migration and rollback must remain required",
            )
        )
    return findings


def _requirement_document_findings(
    task: Mapping[str, Any], requirement_id: str, text: str
) -> list[Finding]:
    path, statement, test_name, owner = REQUIREMENTS[requirement_id]
    references = task.get("references")
    tokens = (
        f"# {requirement_id}",
        statement,
        f"`{test_name}`",
        f"Owner normativo:** `{owner}`",
    )
    findings: list[Finding] = []
    if not isinstance(references, list) or path.as_posix() not in references:
        findings.append(
            Finding("REQUIREMENT_UNBOUND", TASK_PATH.as_posix(), path.as_posix())
        )
    if any(token not in text for token in tokens):
        findings.append(
            Finding("REQUIREMENT_UNBOUND", path.as_posix(), "canonical text drift")
        )
    return findings


def _batch_hierarchy_findings(
    foundation: Mapping[str, Any],
    job: Mapping[str, Any],
    attempt: Mapping[str, Any],
    envelope: Mapping[str, Any],
    reporting_text: str,
) -> list[Finding]:
    batch = _nested(foundation, "controls", "batch_execution")
    retry = _nested(foundation, "controls", "retry_boundary")
    job_required = job.get("required")
    attempt_required = attempt.get("required")
    envelope_required = envelope.get("required")
    valid = bool(
        isinstance(batch, Mapping)
        and batch.get("job_contract") == JOB_PATH.as_posix()
        and batch.get("image_verdicts") == "PRESERVE_EACH_IMAGE"
        and batch.get("missing_image_verdict") == "REJECT"
        and isinstance(retry, Mapping)
        and retry.get("attempt_contract") == ATTEMPT_PATH.as_posix()
        and retry.get("ambiguous_retry") == "REJECT"
        and isinstance(job_required, list)
        and "id" in job_required
        and isinstance(attempt_required, list)
        and {"id", "job_id"}.issubset(attempt_required)
        and isinstance(envelope_required, list)
        and {"job_id", "work_unit_id", "attempt_id"}.issubset(envelope_required)
        and all(
            token in reporting_text
            for token in (
                "image_id",
                "batch_id / project_id / job_id / attempt_id",
                "batch pai com unidades de trabalho",
            )
        )
    )
    return [] if valid else [
        Finding(
            "REQ_BEX_001_HIERARCHY_INVALID",
            FOUNDATION_PATH.as_posix(),
            "batch, image, attempt, and work-unit lineage must stay explicit",
        )
    ]


def _checkpoint_findings(
    foundation: Mapping[str, Any], migration_text: str, rollback_text: str
) -> list[Finding]:
    reuse = _nested(foundation, "controls", "canonical_reuse")
    migration = _nested(foundation, "controls", "schema_migrations")
    valid = bool(
        isinstance(reuse, Mapping)
        and reuse.get("checkpoints") == "CANONICAL_ONLY"
        and reuse.get("digest_verification") == "REQUIRED"
        and reuse.get("incompatible_reuse") == "REJECT"
        and isinstance(migration, Mapping)
        and migration.get("authority") == "POSTGRESQL"
        and migration.get("evolution") == "VERSIONED_MIGRATIONS_ONLY"
        and migration.get("flow") == "EXPAND_MIGRATE_CONTRACT"
        and migration.get("preflight") == "REQUIRED"
        and migration.get("failed_cutover") == "REJECT"
        and migration.get("version_matrix") == ROLLBACK_MATRIX_PATH.as_posix()
        and "checkpoints e estado persistido" in migration_text
        and "forward fix ou restore" in migration_text
        and "expand then migrate then contract" in rollback_text
        and "rollback decision before contract phase" in rollback_text
    )
    return [] if valid else [
        Finding(
            "REQ_BEX_006_CHECKPOINT_INVALID",
            FOUNDATION_PATH.as_posix(),
            "canonical persisted checkpoints and fail-closed rollback are required",
        )
    ]


def _scientific_control_findings(
    native_policy: Mapping[str, Any], technology_text: str
) -> list[Finding]:
    estimator = _nested(native_policy, "controls", "robust_estimator")
    valid = bool(
        isinstance(estimator, Mapping)
        and estimator.get("library") == "OPENCV"
        and estimator.get("estimator") == "USAC_MAGSAC"
        and estimator.get("boundary") == "ENCAPSULATED"
        and estimator.get("silent_fallback") == "PROHIBITED"
        and "technology: projective homography + USAC_MAGSAC" in technology_text
        and "decision: canonical final model/robust estimator" in technology_text
    )
    return [] if valid else [
        Finding(
            "REQ_FS1_006_FAIL_CLOSED_INVALID",
            NATIVE_POLICY_PATH.as_posix(),
            "projective homography and USAC_MAGSAC must remain canonical without fallback",
        )
    ]


def validate_requirement_evidence(
    repository_root: Path, requirement_id: str
) -> tuple[Finding, ...]:
    if requirement_id not in REQUIREMENTS:
        return (Finding("REQUIREMENT_UNKNOWN", requirement_id, "unsupported requirement"),)
    root = repository_root.resolve()
    task, findings = _load_json(root, TASK_PATH)
    requirement_path = REQUIREMENTS[requirement_id][0]
    requirement_text, text_findings = _load_text(root, requirement_path)
    findings.extend(text_findings)
    if task is not None:
        findings.extend(
            _requirement_document_findings(task, requirement_id, requirement_text)
        )

    if requirement_id == "REQ-BEX-001":
        documents = [
            _load_json(root, path)
            for path in (FOUNDATION_PATH, JOB_PATH, ATTEMPT_PATH, TASK_ENVELOPE_PATH)
        ]
        for _, document_findings in documents:
            findings.extend(document_findings)
        reporting_text, reporting_findings = _load_text(root, BATCH_REPORTING_PATH)
        findings.extend(reporting_findings)
        loaded = [document for document, _ in documents]
        if all(document is not None for document in loaded):
            foundation, job, attempt, envelope = loaded
            assert foundation is not None and job is not None
            assert attempt is not None and envelope is not None
            findings.extend(
                _batch_hierarchy_findings(
                    foundation, job, attempt, envelope, reporting_text
                )
            )
    elif requirement_id == "REQ-BEX-006":
        foundation, foundation_findings = _load_json(root, FOUNDATION_PATH)
        migration_text, migration_findings = _load_text(root, DATABASE_MIGRATIONS_PATH)
        rollback_text, rollback_findings = _load_text(root, ROLLBACK_MATRIX_PATH)
        findings.extend(foundation_findings + migration_findings + rollback_findings)
        if foundation is not None:
            findings.extend(
                _checkpoint_findings(foundation, migration_text, rollback_text)
            )
    else:
        native_policy, policy_findings = _load_json(root, NATIVE_POLICY_PATH)
        technology_text, technology_findings = _load_text(
            root, TECHNOLOGY_BASELINE_PATH
        )
        findings.extend(policy_findings + technology_findings)
        if native_policy is not None:
            findings.extend(
                _scientific_control_findings(native_policy, technology_text)
            )
    return tuple(sorted(set(findings)))


def _quality_report_findings(report: object, returncode: int) -> list[Finding]:
    if not isinstance(report, Mapping):
        return [
            Finding(
                "QUALITY_VALIDATOR_INVALID",
                QUALITY_VALIDATOR_PATH.as_posix(),
                "object required",
            )
        ]
    requirements = report.get("requirements")
    valid = bool(
        returncode == 0
        and report.get("status") == "PASS"
        and report.get("mode") == "DRY_RUN"
        and report.get("destructive_actions") == 0
        and report.get("findings") == []
        and report.get("automation")
        == "EPIC-005_MIGRATIONS_CI_SCANS_TELEMETRY_CONTROLS"
        and report.get("acceptance_criteria") == list(EXPECTED_QUALITY_AC_IDS)
        and isinstance(requirements, list)
        and len(requirements) == EXPECTED_QUALITY_REQUIREMENT_COUNT
        and requirements == sorted(set(requirements))
    )
    return [] if valid else [
        Finding(
            "QUALITY_VALIDATION_FAILED",
            QUALITY_VALIDATOR_PATH.as_posix(),
            f"returncode={returncode} status={report.get('status')}",
        )
    ]


def _quality_findings(root: Path) -> list[Finding]:
    environment = os.environ.copy()
    environment.update(
        {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"}
    )
    command = [
        sys.executable,
        "-B",
        str(root / QUALITY_VALIDATOR_PATH),
        "--repository-root",
        str(root),
        "--dry-run",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        report = json.loads(completed.stdout)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [
            Finding(
                "QUALITY_VALIDATOR_INVALID",
                QUALITY_VALIDATOR_PATH.as_posix(),
                str(error),
            )
        ]
    return _quality_report_findings(report, completed.returncode)


def validate_repository_integration(repository_root: Path) -> tuple[Finding, ...]:
    root = repository_root.resolve()
    task, findings = _load_json(root, TASK_PATH)
    if task is not None:
        findings.extend(_task_findings(task))
    for requirement_id in REQUIREMENTS:
        findings.extend(validate_requirement_evidence(root, requirement_id))
    findings.extend(_quality_findings(root))
    return tuple(sorted(set(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate ISSUE-0134 repository integration"
    )
    parser.add_argument(
        "--repository-root", type=Path, default=Path(__file__).resolve().parents[3]
    )
    args = parser.parse_args(argv)
    findings = validate_repository_integration(args.repository_root)
    report = {
        "acceptance_criteria": list(EXPECTED_AC_IDS),
        "control_plane": "SUBPROCESS_READ_ONLY",
        "findings": [finding.as_dict() for finding in findings],
        "issue": "ISSUE-0134",
        "migration_policy": "EXPAND_MIGRATE_CONTRACT_WITH_ROLLBACK",
        "requirements": list(REQUIREMENTS),
        "status": "FAIL" if findings else "PASS",
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
