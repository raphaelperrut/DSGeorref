from __future__ import annotations

import copy
import csv
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r"
)
SCHEMA_PATH = CONTRACT_ROOT / "monorepo-foundation.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/monorepo-foundation.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0011.json"
GRAPH_PATH = ROOT / "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
OPENAPI_PATH = ROOT / "contracts/http/openapi.yaml"
OPERATION_CATALOG_PATH = ROOT / "contracts/http/OPERATION_CATALOG.json"
DESIGN_REVIEW_PATH = (
    ROOT
    / "docs/02-architecture/design-reviews"
    / "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/DESIGN-REVIEW.md"
)


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _graph_edges(*, source: str | None = None, target: str | None = None) -> set[str]:
    graph = _load_json(GRAPH_PATH)
    values: set[str] = set()
    for edge in graph["edges"]:
        if edge["relation"] != "blocks":
            continue
        if source is not None and edge["from"] == source:
            values.add(edge["to"])
        if target is not None and edge["to"] == target:
            values.add(edge["from"])
    return values


def test_cli_api_semantic_contract() -> None:
    schema = _load_json(SCHEMA_PATH)
    contract = _load_json(EXAMPLE_PATH)
    openapi = _load_yaml(OPENAPI_PATH)
    operation_catalog = _load_json(OPERATION_CATALOG_PATH)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)

    surfaces = contract["architecture"]["interface_flow"]
    assert [surface["surface"] for surface in surfaces] == ["CLI", "HTTP_API", "WEB"]
    assert {surface["semantic_authority"] for surface in surfaces} == {
        "APPLICATION_SERVICES"
    }
    assert all(surface["direct_authoritative_store"] is False for surface in surfaces)
    assert surfaces[0]["invocation"] == surfaces[1]["invocation"] == (
        "APPLICATION_SERVICE_PORT"
    )
    assert surfaces[2]["invocation"] == "HTTP_API_OPENAPI_CLIENT"

    http_source = contract["contract_sources"]["http"]
    assert openapi["openapi"] == "3.1.0"
    assert openapi["info"]["version"] == http_source["version"] == "2.6.0"
    assert operation_catalog["schema_version"] == (
        contract["contract_sources"]["operation_catalog"]["schema_version"]
    )
    assert all(operation["contract_status"] == "FROZEN" for operation in operation_catalog["operations"])


def test_epic_003_contrato() -> None:
    contract = _load_json(EXAMPLE_PATH)
    manifest = _load_yaml(MANIFEST_PATH)
    task = _load_json(TASK_PATH)

    assert manifest["identity"] == {
        "epic_id": "EPIC-003",
        "story_id": "STORY-0011",
        "issue_id": "ISSUE-0121",
        "task_id": "TASK-0011",
    }
    assert manifest["requirements"] == contract["requirement_ids"] == ["REQ-TOP-001"]
    assert manifest["acceptance_criteria"] == task["acceptance_criterion_ids"]
    assert manifest["proof"]["required_tests"] == task["tests"]
    assert manifest["review"]["self_approval"] == "PROHIBITED"
    assert _graph_edges(target="STORY-0011") == {"STORY-0005"}
    assert _graph_edges(source="STORY-0011") == set(
        contract["review_gate"]["eligible_dependents"]
    )
    assert contract["review_gate"]["released_dependents"] == []

    required_allow_paths = {
        ".codex/tasks/TASK-0011.json",
        "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv",
        "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation_contract.py",
        "evidence/implementation/epic-003/story-0011/**",
    }
    assert required_allow_paths <= set(task["allow_paths"])
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]

    expected_contracts = {
        path.relative_to(ROOT).as_posix()
        for path in (MANIFEST_PATH, SCHEMA_PATH, EXAMPLE_PATH)
    }
    with OWNERSHIP_PATH.open(encoding="utf-8", newline="") as ownership_file:
        registered = {
            row["contract"]
            for row in csv.DictReader(ownership_file)
            if row["owner_context"] == "BC-001" and row["status"] == "VERSIONED"
        }
    assert expected_contracts <= registered

    design_review = DESIGN_REVIEW_PATH.read_text(encoding="utf-8")
    for criterion_id in task["acceptance_criterion_ids"]:
        assert criterion_id in design_review


def test_foundation_contract_rejects_silent_fallback_and_duplicate_authority() -> None:
    schema = _load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    invalid = copy.deepcopy(_load_json(EXAMPLE_PATH))
    invalid["failure_policy"]["mode"] = "BEST_EFFORT"
    invalid["failure_policy"]["silent_fallback"] = True
    invalid["architecture"]["interface_flow"][0]["semantic_authority"] = "CLI_LOCAL"
    invalid["unexpected"] = "implicit-contract-extension"

    errors = list(validator.iter_errors(invalid))
    assert {error.validator for error in errors} == {"additionalProperties", "const"}
    assert len(errors) == 4
