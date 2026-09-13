from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from main_ruleset_policy_validation import (
    FoundationValidationError,
    require,
    require_exact_keys,
    validate_bypass_record,
    validate_codeowners,
    validate_required_check_registry,
    validate_ruleset,
)

SLUG = "ruleset-de-main-checks-unicos-codeowners-politica-de-b"
ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = ROOT / "contracts/contexts/engineering_governance/fnd" / SLUG
FOUNDATION_ROOT = ROOT / "docs/03-engineering/contexts/engineering_governance" / SLUG
CONTRACT_PATH = CONTRACT_ROOT / "examples/main-ruleset-governance.json"
SCHEMA_PATH = CONTRACT_ROOT / "main-ruleset-governance.schema.json"
RULESET_PATH = FOUNDATION_ROOT / "main-ruleset.json"
REGISTRY_PATH = FOUNDATION_ROOT / "required-check-registry.json"
CHECKPOINT_PATH = Path(__file__).with_name("foundation-checkpoint.json")
TASK_PATH = ROOT / ".codex/tasks/TASK-0561.json"
PORTABLE_COMMAND = f"python -X utf8 tools/governance/{SLUG}/foundation_validation.py"
MAKE_COMMAND = f"$(PYTHON) -X utf8 tools/governance/{SLUG}/foundation_validation.py"
MAKE_TEST_COMMAND = (
    f"$(PYTHON) -X utf8 -m pytest -q -p no:cacheprovider "
    f"tests/fnd/{SLUG}/test_main_ruleset_foundation.py"
)
EXPECTED_AC_IDS = [f"AC-ISSUE-0671-{index:02d}" for index in range(1, 5)]
EXPECTED_CONTROL_PLANE_ARTIFACTS = [
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/main-ruleset.json",
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/required-check-registry.json",
    ".github/CODEOWNERS",
]


def load_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FoundationValidationError(f"invalid JSON artifact: {path}") from exc
    require(isinstance(loaded, dict), f"JSON artifact must be an object: {path}")
    return cast(dict[str, Any], loaded)


def validate_contract(root: Path = ROOT) -> dict[str, Any]:
    schema = load_json(root / SCHEMA_PATH.relative_to(ROOT))
    contract = load_json(root / CONTRACT_PATH.relative_to(ROOT))
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(contract))
    require(not errors, f"frozen contract is invalid: {errors[0].message if errors else ''}")
    return contract


def _validate_checkpoint_document(
    checkpoint: Any,
    *,
    task: dict[str, Any],
    contract: dict[str, Any],
) -> None:
    document = require_exact_keys(
        checkpoint,
        {
            "schema_version",
            "issue_id",
            "story_id",
            "task_id",
            "source_contract",
            "control_plane_artifacts",
            "requirement_evidence",
            "acceptance_evidence",
            "reproducible_command",
            "local_command",
            "ci_command",
            "live_ruleset_enforcement",
            "migration",
            "rollback",
        },
        "foundation checkpoint",
    )
    require(document["schema_version"] == "1.0.0", "unsupported checkpoint version")
    require(
        (document["issue_id"], document["story_id"], document["task_id"])
        == ("ISSUE-0671", "STORY-0561", "TASK-0561")
        == (task["issue_id"], task["story_id"], task["task_id"]),
        "checkpoint identity diverges from TaskEnvelope",
    )
    require(
        document["source_contract"] == CONTRACT_PATH.relative_to(ROOT).as_posix(),
        "checkpoint source contract diverges",
    )
    require(
        document["control_plane_artifacts"] == EXPECTED_CONTROL_PLANE_ARTIFACTS,
        "checkpoint control plane artifacts diverge",
    )
    expected_requirements = {
        item["requirement_id"]: item["canonical_test"] for item in contract["requirement_evidence"]
    }
    require(
        document["requirement_evidence"] == expected_requirements,
        "requirement evidence diverges",
    )
    require(
        document["acceptance_evidence"] == dict.fromkeys(EXPECTED_AC_IDS, "test_epic_091_fundacao"),
        "acceptance evidence diverges",
    )
    command = document["reproducible_command"]
    require(command == document["local_command"] == document["ci_command"], "commands diverge")
    require(command == PORTABLE_COMMAND, "foundation command is not portable")
    require(document["live_ruleset_enforcement"] == "NOT_ASSERTED_BY_FOUNDATION", "unsafe claim")
    require(document["migration"] == "NOT_APPLICABLE", "unexpected migration claim")
    require(
        document["rollback"] == "REVERT_COMMIT_BEFORE_DOWNSTREAM_CONSUMPTION",
        "unexpected rollback policy",
    )


def validate_checkpoint(
    root: Path = ROOT,
    *,
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_contract = contract if contract is not None else validate_contract(root)
    checkpoint = load_json(root / CHECKPOINT_PATH.relative_to(ROOT))
    task = load_json(root / TASK_PATH.relative_to(ROOT))
    _validate_checkpoint_document(checkpoint, task=task, contract=resolved_contract)
    expected_paths = {
        ".codex/tasks/TASK-0561.json",
        "Makefile",
        f"tools/governance/{SLUG}/**",
        f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
        f"tests/fnd/{SLUG}/test_main_ruleset_foundation.py",
        "evidence/implementation/epic-091/story-0561/**",
    }
    require(
        expected_paths <= set(task["allow_paths"]),
        "TaskEnvelope omits required foundation paths",
    )
    require(
        task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"],
        "TaskEnvelope phase-F scope diverges",
    )
    return checkpoint


def validate_ci_integration(root: Path = ROOT) -> dict[str, str]:
    makefile = (root / "Makefile").read_text(encoding="utf-8")
    ci_workflow = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    require(f"\t{MAKE_COMMAND}" in makefile, "make verify omits the foundation validator")
    require(f"\t{MAKE_TEST_COMMAND}" in makefile, "make verify omits the foundation tests")
    require("run: make verify" in ci_workflow, "CI does not execute make verify")
    return {"ci_entrypoint": "make verify", "command": PORTABLE_COMMAND, "status": "PASS"}


def validate_foundation(root: Path = ROOT) -> dict[str, Any]:
    contract = validate_contract(root)
    registry = load_json(root / REGISTRY_PATH.relative_to(ROOT))
    required_contexts = validate_required_check_registry(registry, root)
    ruleset = load_json(root / RULESET_PATH.relative_to(ROOT))
    validate_ruleset(ruleset, contract=contract, required_contexts=required_contexts)
    owners = validate_codeowners(
        (root / contract["codeowners_policy"]["source"]).read_text(encoding="utf-8")
    )
    checkpoint = validate_checkpoint(root, contract=contract)
    ci = validate_ci_integration(root)
    return {
        "acceptance_evidence": checkpoint["acceptance_evidence"],
        "checks": dict.fromkeys(
            ["checkpoint", "ci_integration", "codeowners", "contract", "registry", "ruleset"],
            "PASS",
        ),
        "ci": ci,
        "decision": "PASS",
        "issue_id": "ISSUE-0671",
        "live_ruleset_enforcement": "NOT_ASSERTED_BY_FOUNDATION",
        "owners": owners,
        "required_checks": required_contexts,
        "requirement_evidence": checkpoint["requirement_evidence"],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the EPIC-091 main-ruleset foundation")
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--bypass-record", type=Path)
    parser.add_argument("--candidate-sha")
    parser.add_argument("--delivery-approval-verdict-ref")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        report = validate_foundation(args.repository_root)
        bypass_arguments = (
            args.bypass_record,
            args.candidate_sha,
            args.delivery_approval_verdict_ref,
        )
        require(
            all(value is None for value in bypass_arguments) or all(bypass_arguments),
            "incomplete bypass evidence",
        )
        if args.bypass_record is not None:
            require(isinstance(args.candidate_sha, str), "candidate SHA missing")
            require(
                isinstance(args.delivery_approval_verdict_ref, str),
                "delivery approval verdict reference missing",
            )
            ruleset = load_json(args.repository_root / RULESET_PATH.relative_to(ROOT))
            validate_bypass_record(
                load_json(args.bypass_record),
                ruleset_id=ruleset["ruleset_id"],
                candidate_sha=args.candidate_sha,
                delivery_approval_verdict_ref=args.delivery_approval_verdict_ref,
            )
            report["bypass_evidence"] = "PASS"
    except (FoundationValidationError, OSError) as exc:
        print(json.dumps({"decision": "FAIL", "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
