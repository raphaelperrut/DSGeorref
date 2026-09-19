from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW_ROOT = ROOT / ".github/workflows"
REQUIRED_CHECK_REGISTRY = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "ruleset-de-main-checks-unicos-codeowners-politica-de-b/"
    "required-check-registry.json"
)
TASK_ENVELOPE = ROOT / ".codex/tasks/operations/TASK-0762.json"
TASK_SCHEMA = ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json"

ALWAYS_ON_PULL_REQUEST = {
    "epic-091-main-ruleset-controls",
    "foundation-ci",
    "foundation-security",
}

MANUAL_ONLY = {
    "epic-003-foundation-controls",
    "engineering-foundation-contract-validation",
    "epic-092-sprint-001-closure-controls",
}


def _workflows() -> dict[str, tuple[Path, dict[str, object], str]]:
    workflows: dict[str, tuple[Path, dict[str, object], str]] = {}
    for path in sorted(WORKFLOW_ROOT.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        document = yaml.load(text, Loader=yaml.BaseLoader)
        assert isinstance(document, dict), path
        name = document.get("name")
        assert isinstance(name, str) and name not in workflows, path
        workflows[name] = (path, document, text)
    return workflows


def test_common_pull_request_fan_out_is_bounded() -> None:
    workflows = _workflows()
    assert len(workflows) == 14

    unfiltered: set[str] = set()
    path_scoped: set[str] = set()
    for name, (_, document, _) in workflows.items():
        triggers = document.get("on")
        assert isinstance(triggers, dict), name
        if "pull_request" not in triggers:
            continue
        pull_request = triggers["pull_request"]
        if pull_request == "":
            unfiltered.add(name)
            continue
        assert isinstance(pull_request, dict), name
        paths = pull_request.get("paths")
        if paths is None:
            unfiltered.add(name)
        else:
            assert isinstance(paths, list) and paths, name
            path_scoped.add(name)

    assert unfiltered == ALWAYS_ON_PULL_REQUEST
    assert len(path_scoped) == 8


def test_functional_and_security_gates_remain_reachable() -> None:
    workflows = _workflows()

    _, ci, _ = workflows["foundation-ci"]
    ci_triggers = ci["on"]
    assert isinstance(ci_triggers, dict)
    assert "pull_request" in ci_triggers
    assert "workflow_dispatch" in ci_triggers
    assert ci_triggers["push"] == {"branches": ["main"]}
    assert ci["permissions"] == {"contents": "read"}

    _, security, _ = workflows["foundation-security"]
    security_triggers = security["on"]
    assert isinstance(security_triggers, dict)
    assert set(security_triggers) == {"pull_request", "workflow_dispatch"}
    assert security["permissions"] == {"contents": "read"}

    registry = json.loads(REQUIRED_CHECK_REGISTRY.read_text(encoding="utf-8"))
    required_contexts = {
        item["context"] for item in registry["required_checks"]
    }
    unfiltered_jobs: set[str] = set()
    for _, document, _ in workflows.values():
        triggers = document["on"]
        assert isinstance(triggers, dict)
        if triggers.get("pull_request") != "":
            continue
        jobs = document.get("jobs")
        assert isinstance(jobs, dict)
        unfiltered_jobs.update(jobs)
    assert required_contexts <= unfiltered_jobs
    assert "secret-pattern-review" in unfiltered_jobs


def test_historical_controls_are_manual_and_scoped_controls_cover_themselves() -> None:
    workflows = _workflows()

    for name in MANUAL_ONLY:
        _, document, _ = workflows[name]
        assert document["on"] == {"workflow_dispatch": ""}

    for name, (path, document, _) in workflows.items():
        triggers = document["on"]
        assert isinstance(triggers, dict)
        pull_request = triggers.get("pull_request")
        if not isinstance(pull_request, dict) or "paths" not in pull_request:
            continue
        paths = pull_request["paths"]
        assert isinstance(paths, list)
        own_path = path.relative_to(ROOT).as_posix()
        assert own_path in paths, name
        assert any(item != own_path for item in paths), name
        assert "push" not in triggers, name
        assert "workflow_dispatch" in triggers, name


def test_concurrency_and_unprivileged_trigger_sentinels() -> None:
    forbidden_text = ("pull_request_target:", "DSGEO_PROJECT_TOKEN")
    workflows = _workflows()

    for name, (_, document, text) in workflows.items():
        concurrency = document.get("concurrency")
        assert isinstance(concurrency, dict), name
        assert concurrency.get("cancel-in-progress") == "true", name
        assert "github.workflow" in str(concurrency.get("group")), name

        triggers = document.get("on")
        assert isinstance(triggers, dict), name
        assert "issues" not in triggers, name
        assert all(value not in text for value in forbidden_text), name


def test_operational_task_envelope_is_typed_and_strictly_scoped() -> None:
    schema = json.loads(TASK_SCHEMA.read_text(encoding="utf-8"))
    task = json.loads(TASK_ENVELOPE.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(task)
    assert task["issue_id"] == "ISSUE-0872"
    assert task["allow_paths"] == [
        ".github/workflows/**",
        "tests/fnd/github-actions-usage/**",
        "evidence/operations/github-actions-usage/**",
        ".codex/tasks/operations/TASK-0762.json",
    ]
    assert task["domain_model_impact"] == "NONE"
