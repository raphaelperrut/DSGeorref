from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

SLUG = "fechamento-da-sprint-001-e-autorizacao-da-primeira-fat"
ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = ROOT / "contracts/contexts/engineering_governance/fnd" / SLUG
CONTRACT_PATH = CONTRACT_ROOT / "examples/sprint-001-closure-authorization.json"
SCHEMA_PATH = CONTRACT_ROOT / "sprint-001-closure-authorization.schema.json"
REGISTRY_PATH = (
    ROOT / "docs/03-engineering/contexts/engineering_governance" / SLUG
    / "foundation-evidence-registry.json"
)
CHECKPOINT_PATH = Path(__file__).with_name("foundation-checkpoint.json")
TASK_PATH = ROOT / ".codex/tasks/TASK-0566.json"
PORTABLE_COMMAND = f"python -X utf8 tools/governance/{SLUG}/foundation_validation.py"
MAKE_COMMAND = f"$(PYTHON) -X utf8 tools/governance/{SLUG}/foundation_validation.py"
MAKE_TEST_COMMAND = (
    "$(PYTHON) -X utf8 -m pytest -q -p no:cacheprovider "
    f"tests/fnd/{SLUG}/test_sprint_001_foundation.py"
)
FOUNDATION_TEST = f"tests/fnd/{SLUG}/test_sprint_001_foundation.py::test_epic_092_fundacao"
FAIL_CLOSED_TEST = (
    f"tests/fnd/{SLUG}/test_sprint_001_foundation.py::"
    "test_error_paths_are_fail_closed_without_silent_fallback"
)
EXPECTED_AC_EVIDENCE = {
    "AC-ISSUE-0676-01": FOUNDATION_TEST,
    "AC-ISSUE-0676-02": FOUNDATION_TEST,
    "AC-ISSUE-0676-03": FAIL_CLOSED_TEST,
    "AC-ISSUE-0676-04": FOUNDATION_TEST,
}
EXPECTED_REQUIREMENT_EVIDENCE = {
    "REQ-DEV-001": (
        "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/"
        "test_foundation.py::test_host_container_ci_contract_and_no_implicit_downloads"
    ),
    "REQ-FRZ-001": (
        "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "test_materialization.py::"
        "test_foundation_baseline_digest_controlled_change_and_adr_supersession"
    ),
    "REQ-FRZ-002": (
        "tests/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/"
        "test_bex_epic_frz_part_2.py::"
        "test_sprint_zero_authorization_and_functional_foundation_gate_blocking"
    ),
    "REQ-FRZ-003": (
        "tests/fnd/ruleset-de-main-checks-unicos-codeowners-politica-de-b/"
        "test_main_ruleset_foundation.py::"
        "test_issue_adr_decision_package_impact_boundary_and_no_silent_divergence"
    ),
    "REQ-FRZ-004": FOUNDATION_TEST,
    "REQ-GOV-005": FOUNDATION_TEST,
}
EXPECTED_REQUIRED_TESTS = list(dict.fromkeys(EXPECTED_REQUIREMENT_EVIDENCE.values()))
REGISTRY_FIELDS = {
    "schema_version", "registry_id", "issue_id", "story_id", "task_id",
    "source_contract", "requirement_evidence", "acceptance_evidence", "required_tests",
    "required_result", "evidence_policy", "failure_policy", "authorization_claim",
}
CHECKPOINT_FIELDS = {
    "schema_version", "issue_id", "story_id", "task_id", "source_contract",
    "evidence_registry", "reproducible_command", "local_command", "ci_command",
    "test_command", "reviewable_state", "authorization_claim", "migration", "rollback",
}


class FoundationValidationError(ValueError):
    """Raised when foundation evidence cannot safely authorize review."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FoundationValidationError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FoundationValidationError(f"invalid JSON artifact: {path}") from exc
    require(isinstance(loaded, dict), f"JSON artifact must be an object: {path}")
    return cast(dict[str, Any], loaded)


def require_exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label} must be an object")
    document = cast(dict[str, Any], value)
    require(set(document) == expected, f"{label} fields diverge")
    return document


def validate_contract(root: Path = ROOT) -> dict[str, Any]:
    schema = load_json(root / SCHEMA_PATH.relative_to(ROOT))
    contract = load_json(root / CONTRACT_PATH.relative_to(ROOT))
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(contract))
    require(not errors, f"frozen contract is invalid: {errors[0].message if errors else ''}")
    return contract


def validate_task(root: Path = ROOT) -> dict[str, Any]:
    task = load_json(root / TASK_PATH.relative_to(ROOT))
    require(
        (task["issue_id"], task["story_id"], task["task_id"])
        == ("ISSUE-0676", "STORY-0566", "TASK-0566"),
        "TaskEnvelope identity diverges",
    )
    expected_names = [node_id.rsplit("::", 1)[1] for node_id in EXPECTED_REQUIRED_TESTS]
    require(task["tests"] == expected_names, "TaskEnvelope required tests diverge")
    expected_paths = {
        ".codex/tasks/TASK-0566.json",
        "Makefile",
        f"tools/governance/{SLUG}/**",
        f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
        f"tests/fnd/{SLUG}/test_sprint_001_foundation.py",
        "evidence/implementation/epic-092/story-0566/**",
    }
    require(expected_paths <= set(task["allow_paths"]), "TaskEnvelope omits required paths")
    require(
        task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"],
        "TaskEnvelope phase-F scope diverges",
    )
    return task


def _validate_registry_document(registry: Any, contract: dict[str, Any]) -> None:
    document = require_exact_keys(registry, REGISTRY_FIELDS, "foundation evidence registry")
    require(document["schema_version"] == "1.0.0", "unsupported registry version")
    require(document["registry_id"] == "SPRINT-001-FOUNDATION-EVIDENCE", "registry id diverges")
    require(
        (document["issue_id"], document["story_id"], document["task_id"])
        == ("ISSUE-0676", "STORY-0566", "TASK-0566"),
        "registry identity diverges",
    )
    require(
        document["source_contract"] == CONTRACT_PATH.relative_to(ROOT).as_posix(),
        "registry source contract diverges",
    )
    require(
        document["requirement_evidence"] == EXPECTED_REQUIREMENT_EVIDENCE,
        "requirement evidence diverges",
    )
    require(
        document["acceptance_evidence"] == EXPECTED_AC_EVIDENCE,
        "acceptance evidence diverges",
    )
    require(
        document["required_tests"] == EXPECTED_REQUIRED_TESTS,
        "required test registry diverges",
    )
    require(
        document["required_result"] == contract["foundation_evidence"]["required_result"],
        "required result diverges",
    )
    require(document["evidence_policy"] == contract["evidence_policy"], "evidence policy diverges")
    require(document["failure_policy"] == contract["failure_policy"], "failure policy diverges")
    require(
        document["authorization_claim"] == "NOT_ASSERTED_BY_FOUNDATION",
        "unsafe authorization claim",
    )


def validate_registered_tests(root: Path, registry: dict[str, Any]) -> None:
    for node_id in registry["required_tests"]:
        relative_path, function_name = node_id.rsplit("::", 1)
        test_path = root / relative_path
        try:
            tree = ast.parse(test_path.read_text(encoding="utf-8"), filename=str(test_path))
        except (OSError, SyntaxError) as exc:
            raise FoundationValidationError(f"registered test is unreadable: {node_id}") from exc
        functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        require(function_name in functions, f"registered test is missing: {node_id}")


def validate_registry(
    root: Path = ROOT,
    *,
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_contract = contract if contract is not None else validate_contract(root)
    registry = load_json(root / REGISTRY_PATH.relative_to(ROOT))
    _validate_registry_document(registry, resolved_contract)
    validate_registered_tests(root, registry)
    return registry


def _validate_checkpoint_document(checkpoint: Any, contract: dict[str, Any]) -> None:
    document = require_exact_keys(checkpoint, CHECKPOINT_FIELDS, "foundation checkpoint")
    require(document["schema_version"] == "1.0.0", "unsupported checkpoint version")
    require(
        (document["issue_id"], document["story_id"], document["task_id"])
        == ("ISSUE-0676", "STORY-0566", "TASK-0566"),
        "checkpoint identity diverges",
    )
    require(
        document["source_contract"] == CONTRACT_PATH.relative_to(ROOT).as_posix(),
        "checkpoint source contract diverges",
    )
    require(
        document["evidence_registry"] == REGISTRY_PATH.relative_to(ROOT).as_posix(),
        "checkpoint registry diverges",
    )
    command = document["reproducible_command"]
    require(
        command == document["local_command"] == document["ci_command"] == PORTABLE_COMMAND,
        "commands diverge",
    )
    require(
        document["test_command"] == MAKE_TEST_COMMAND.replace("$(PYTHON)", "python"),
        "test command diverges",
    )
    require(
        document["reviewable_state"] == contract["state_model"]["reviewable_state"],
        "reviewable state diverges",
    )
    require(
        document["authorization_claim"] == "NOT_ASSERTED_BY_FOUNDATION",
        "unsafe authorization claim",
    )
    require(document["migration"] == "NOT_APPLICABLE", "unexpected migration claim")
    require(
        document["rollback"] == contract["compatibility"]["rollback"],
        "rollback policy diverges",
    )


def validate_checkpoint(
    root: Path = ROOT,
    *,
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_contract = contract if contract is not None else validate_contract(root)
    checkpoint = load_json(root / CHECKPOINT_PATH.relative_to(ROOT))
    _validate_checkpoint_document(checkpoint, resolved_contract)
    return checkpoint


def validate_ci_integration(root: Path = ROOT) -> dict[str, str]:
    makefile = (root / "Makefile").read_text(encoding="utf-8")
    workflow = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    require(f"\t{MAKE_COMMAND}" in makefile, "make verify omits the foundation validator")
    require(f"\t{MAKE_TEST_COMMAND}" in makefile, "make verify omits the foundation tests")
    require("run: make verify" in workflow, "CI does not execute make verify")
    return {"ci_entrypoint": "make verify", "command": PORTABLE_COMMAND, "status": "PASS"}


def validate_foundation(root: Path = ROOT) -> dict[str, Any]:
    contract = validate_contract(root)
    task = validate_task(root)
    registry = validate_registry(root, contract=contract)
    checkpoint = validate_checkpoint(root, contract=contract)
    ci = validate_ci_integration(root)
    return {
        "acceptance_evidence": registry["acceptance_evidence"],
        "authorization_claim": checkpoint["authorization_claim"],
        "checks": dict.fromkeys(
            ["checkpoint", "ci_integration", "contract", "registry", "tests"],
            "PASS",
        ),
        "ci": ci,
        "decision": "PASS",
        "issue_id": task["issue_id"],
        "requirement_evidence": registry["requirement_evidence"],
        "reviewable_state": checkpoint["reviewable_state"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the EPIC-092 executable foundation")
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        report = validate_foundation(args.repository_root.resolve())
    except (FoundationValidationError, OSError) as exc:
        print(json.dumps({"decision": "FAIL", "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
