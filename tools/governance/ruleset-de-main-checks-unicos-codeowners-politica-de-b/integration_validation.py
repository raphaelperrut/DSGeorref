from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any, cast

import yaml  # type: ignore[import-untyped]
from foundation_validation import validate_foundation

SLUG = "ruleset-de-main-checks-unicos-codeowners-politica-de-b"
ROOT = Path(__file__).resolve().parents[3]
CONTROL_ROOT = Path("docs/03-engineering/contexts/engineering_governance") / SLUG
TASK_PATH = Path(".codex/tasks/TASK-0563.json")
WORKFLOW_PATH = Path(f".github/workflows/{SLUG}.yaml")
CHECKPOINT_PATH = CONTROL_ROOT / "integration-checkpoint.json"
EVIDENCE_PATH = Path("evidence/implementation/epic-091/story-0563/validation.json")
TEST_PATH = Path(f"tests/fnd/{SLUG}/test_integration.py")
VALIDATOR_PATH = Path(f"tools/governance/{SLUG}/integration_validation.py")
REQUIRED_TEST = "test_epic_091_integracao"
REQUIRED_CHECKS = ["verify-foundation", "validate-main-ruleset-controls"]
REQUIREMENT_IDS = ["REQ-FRZ-003", "REQ-GOV-004", "REQ-ISS-003", "REQ-ISS-006", "REQ-PUB-002"]
ACCEPTANCE_EVIDENCE = {
    f"AC-ISSUE-0673-{index:02d}": REQUIRED_TEST for index in range(1, 5)
}
REQUIREMENT_EVIDENCE = dict.fromkeys(REQUIREMENT_IDS, REQUIRED_TEST)
VALIDATION_COMMAND = f"python -X utf8 {VALIDATOR_PATH.as_posix()}"
TEST_COMMAND = (
    "python -X utf8 -m pytest -q -p no:cacheprovider "
    f"{TEST_PATH.as_posix()}::{REQUIRED_TEST}"
)
EXPECTED_ALLOW_PATHS = [
    TASK_PATH.as_posix(),
    f"tools/governance/{SLUG}/**",
    f"tools/quality/contexts/engineering_governance/{SLUG}/**",
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
    f"tests/fnd/{SLUG}/**",
    WORKFLOW_PATH.as_posix(),
    "evidence/implementation/epic-091/story-0563/**",
]


class IntegrationValidationError(ValueError):
    """Raised when repository-flow integration evidence cannot be accepted."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise IntegrationValidationError(message)


def _load_json(root: Path, relative: Path) -> dict[str, Any]:
    try:
        value = json.loads((root / relative).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise IntegrationValidationError(
            f"invalid JSON artifact: {relative.as_posix()}"
        ) from error
    _require(isinstance(value, dict), f"JSON artifact must be an object: {relative.as_posix()}")
    return cast(dict[str, Any], value)


def _validate_task(task: dict[str, Any]) -> None:
    expected = {
        "task_id": "TASK-0563",
        "issue_id": "ISSUE-0673",
        "story_id": "STORY-0563",
        "epic_id": "EPIC-091",
        "role": "Tech Lead",
        "dependencies": ["STORY-0561", "STORY-0562"],
        "tests": [REQUIRED_TEST],
        "acceptance_criterion_ids": list(ACCEPTANCE_EVIDENCE),
        "allow_paths": EXPECTED_ALLOW_PATHS,
    }
    drifted = [
        field for field, expected_value in expected.items() if task.get(field) != expected_value
    ]
    _require(not drifted, f"TaskEnvelope fields diverge: {', '.join(drifted)}")
    phase_f = task.get("phase_f_review")
    _require(isinstance(phase_f, dict), "TaskEnvelope phase-F review missing")
    phase_f_document = cast(dict[str, Any], phase_f)
    files = phase_f_document.get("files")
    _require(isinstance(files, dict), "TaskEnvelope phase-F file scope missing")
    files_document = cast(dict[str, Any], files)
    _require(
        files_document.get("allow_paths") == task["allow_paths"],
        "TaskEnvelope allow paths diverge",
    )


def _validate_workflow(root: Path) -> None:
    try:
        raw = (root / WORKFLOW_PATH).read_text(encoding="utf-8")
        workflow = yaml.safe_load(raw)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise IntegrationValidationError("integration workflow is unreadable") from error
    _require(isinstance(workflow, dict), "integration workflow must be an object")
    workflow_document = cast(dict[str, Any], workflow)
    _require(
        workflow_document.get("permissions") == {"contents": "read"},
        "workflow permissions diverge",
    )
    jobs = workflow_document.get("jobs")
    _require(isinstance(jobs, dict), "workflow jobs missing")
    jobs_document = cast(dict[str, Any], jobs)
    job = jobs_document.get("validate-main-ruleset-controls")
    _require(isinstance(job, dict), "required integration check producer missing")
    _require(
        "continue-on-error: true" not in raw,
        "integration workflow may not ignore failures",
    )
    job_document = cast(dict[str, Any], job)
    steps = job_document.get("steps")
    _require(isinstance(steps, list), "integration workflow steps missing")
    commands: list[str] = []
    for step in cast(list[Any], steps):
        if isinstance(step, dict) and isinstance(step.get("run"), str):
            commands.append(cast(str, step["run"]))
    _require(
        any(
            "tools/quality/contexts/engineering_governance" in command
            and "--dry-run" in command
            for command in commands
        ),
        "automation validator is not integrated",
    )
    _require(
        any(TEST_PATH.as_posix() in command and REQUIRED_TEST in command for command in commands),
        "required integration test is not integrated",
    )


def _local_imports(path: Path, local_modules: set[str]) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.as_posix())
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names if alias.name in local_modules)
        elif isinstance(node, ast.ImportFrom) and node.module in local_modules:
            imports.add(node.module)
    return imports


def _validate_dependency_direction(root: Path) -> None:
    modules = {
        "integration_validation": VALIDATOR_PATH,
        "foundation_validation": Path(f"tools/governance/{SLUG}/foundation_validation.py"),
        "main_ruleset_policy_validation": Path(
            f"tools/governance/{SLUG}/main_ruleset_policy_validation.py"
        ),
    }
    graph = {
        name: _local_imports(root / path, set(modules)) for name, path in modules.items()
    }
    _require(
        graph["integration_validation"] == {"foundation_validation"},
        "integration must reuse only the foundation validator",
    )
    _require(
        graph["foundation_validation"] == {"main_ruleset_policy_validation"},
        "foundation dependency direction diverges",
    )
    _require(
        not graph["main_ruleset_policy_validation"],
        "policy module creates a dependency cycle",
    )


def _validate_checkpoint(checkpoint: dict[str, Any]) -> None:
    expected = {
        "schema_version": "1.0.0",
        "issue_id": "ISSUE-0673",
        "story_id": "STORY-0563",
        "task_id": "TASK-0563",
        "source_ruleset": (CONTROL_ROOT / "main-ruleset.json").as_posix(),
        "required_check_contexts": REQUIRED_CHECKS,
        "workflow": WORKFLOW_PATH.as_posix(),
        "requirement_evidence": REQUIREMENT_EVIDENCE,
        "acceptance_evidence": ACCEPTANCE_EVIDENCE,
        "validation_command": VALIDATION_COMMAND,
        "test_command": TEST_COMMAND,
        "architecture_evidence": {
            "integration_reuses": "foundation_validation.validate_foundation",
            "local_policy_reimplementation": "NONE",
            "dependency_direction": (
                "integration_validation -> foundation_validation -> "
                "main_ruleset_policy_validation"
            ),
        },
        "live_ruleset_enforcement": "NOT_ASSERTED_BY_INTEGRATION",
        "migration": "NOT_APPLICABLE",
        "rollback": "REVERT_COMMIT_BEFORE_DOWNSTREAM_CONSUMPTION",
    }
    _require(checkpoint == expected, "integration checkpoint diverges")


def _validate_evidence(evidence: dict[str, Any]) -> None:
    expected = {
        "issue": "ISSUE-0673",
        "story": "STORY-0563",
        "status": "PASS",
        "required_test": REQUIRED_TEST,
        "requirement_evidence": REQUIREMENT_EVIDENCE,
        "acceptance_evidence": ACCEPTANCE_EVIDENCE,
        "validation_command": VALIDATION_COMMAND,
        "test_command": TEST_COMMAND,
        "required_check_contexts": REQUIRED_CHECKS,
        "contract_impact": "NONE; consumes the frozen ISSUE-0670 contract.",
        "migration": "NOT_APPLICABLE",
        "rollback": "Revert the ISSUE-0673 commit; no persistent state is changed.",
        "live_ruleset_enforcement": "NOT_ASSERTED_BY_INTEGRATION",
        "independent_review": "PENDING",
    }
    _require(evidence == expected, "candidate evidence diverges")


def validate_integration(root: Path = ROOT) -> dict[str, Any]:
    repository_root = root.resolve()
    foundation = validate_foundation(repository_root)
    _require(
        foundation["required_checks"] == REQUIRED_CHECKS,
        "required checks are not integrated",
    )
    _validate_task(_load_json(repository_root, TASK_PATH))
    _validate_workflow(repository_root)
    _validate_dependency_direction(repository_root)
    _validate_checkpoint(_load_json(repository_root, CHECKPOINT_PATH))
    _validate_evidence(_load_json(repository_root, EVIDENCE_PATH))
    test_source = (repository_root / TEST_PATH).read_text(encoding="utf-8")
    tests = {
        node.name for node in ast.walk(ast.parse(test_source)) if isinstance(node, ast.FunctionDef)
    }
    _require(REQUIRED_TEST in tests, "required integration test missing")
    return {
        "acceptance_evidence": ACCEPTANCE_EVIDENCE,
        "decision": "PASS",
        "issue_id": "ISSUE-0673",
        "live_ruleset_enforcement": "NOT_ASSERTED_BY_INTEGRATION",
        "required_checks": REQUIRED_CHECKS,
        "requirement_evidence": REQUIREMENT_EVIDENCE,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate EPIC-091 repository-flow integration")
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        report = validate_integration(args.repository_root)
    except Exception as error:  # CLI boundary is deliberately fail-closed.
        print(json.dumps({"decision": "FAIL", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
