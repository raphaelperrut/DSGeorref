from __future__ import annotations

import ast
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

SLUG = "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca"
TASK_REL = Path(".codex/tasks/TASK-0028.json")
TASK_SCHEMA_REL = Path(".codex/tasks/TASK_ENVELOPE.schema.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
TEST_REL = Path(f"tests/fnd/{SLUG}/test_automation.py")
QUALITY_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}")
CONTRACT_ROOT_REL = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
DOC_ROOT_REL = Path(f"docs/03-engineering/contexts/engineering_governance/{SLUG}")
CHECKPOINT_REL = Path(f"tools/governance/{SLUG}/foundation-checkpoint.json")
MANIFEST_REL = CONTRACT_ROOT_REL / "contract-manifest.yaml"
CONTRACT_SCHEMA_REL = CONTRACT_ROOT_REL / "capability-catalog-foundation.schema.json"
CONTRACT_EXAMPLE_REL = CONTRACT_ROOT_REL / "examples/capability-catalog-foundation.json"
CATALOG_REL = DOC_ROOT_REL / "capability-catalog.json"
CATALOG_SCHEMA_REL = DOC_ROOT_REL / "capability-catalog.schema.json"
CORPUS_REL = DOC_ROOT_REL / "test-corpus-manifest.json"
CORPUS_SCHEMA_REL = DOC_ROOT_REL / "test-corpus-manifest.schema.json"

REQUIREMENT_EVIDENCE = {
    "REQ-AI-007": "test_epic_006_automacao",
    "REQ-TST-001": "test_epic_006_automacao",
}
ACCEPTANCE_EVIDENCE = {
    f"AC-ISSUE-0138-{index:02d}": "test_epic_006_automacao" for index in range(1, 5)
}
EXPECTED_ALLOW_PATHS = [
    TASK_REL.as_posix(),
    f"tests/fnd/{SLUG}/**",
    f"tools/quality/contexts/engineering_governance/{SLUG}/**",
    WORKFLOW_REL.as_posix(),
    "evidence/operations/epic-006/story-0028/**",
]
EXPECTED_SOURCES = {
    "contract": MANIFEST_REL.as_posix(),
    "catalog": CATALOG_REL.as_posix(),
    "catalog_schema": CATALOG_SCHEMA_REL.as_posix(),
    "corpus": CORPUS_REL.as_posix(),
    "corpus_schema": CORPUS_SCHEMA_REL.as_posix(),
}
CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"
EXPECTED_MANIFEST_SHA256 = "472092ed06c8e9ce07b5af85be23af67a4aaa019a3171d646ab843fd06792495"
EXPECTED_CORPUS_POLICY = {"access_integrity": "FAIL_CLOSED", "split_overlap": "REJECT"}
EXPECTED_ACCESS_BY_SPLIT = {
    "DEVELOPMENT": "DEVELOPMENT",
    "VALIDATION_PROTECTED": "QA_PROTECTED",
    "HOLDOUT_BLIND": "INDEPENDENT_QA_BLIND",
}


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"artifact": self.artifact, "code": self.code, "detail": self.detail}


def _finding(code: str, artifact: Path, detail: str) -> Finding:
    return Finding(code, artifact.as_posix(), detail)


def _load_json(root: Path, relative: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return json.loads((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [_finding(code, relative, str(error))]


def _load_yaml(root: Path, relative: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return yaml.safe_load((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return None, [_finding(code, relative, str(error))]


def _schema_findings(
    instance: object, schema: object, artifact: Path, code: str
) -> list[Finding]:
    if not isinstance(schema, dict):
        return [_finding(code, artifact, "schema object required")]
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        return [_finding(code, artifact, error.message)]
    return [
        _finding(code, artifact, f"{error.json_path}: {error.message}")
        for error in Draft202012Validator(schema).iter_errors(instance)
    ]


def _safe_path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str):
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    try:
        resolved = (root / relative).resolve()
    except OSError:
        return None
    return resolved if resolved.is_relative_to(root.resolve()) else None


def _canonical_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _semantic_sha256(value: object) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _defined_tests(root: Path) -> tuple[set[str], list[Finding]]:
    try:
        tree = ast.parse((root / TEST_REL).read_text(encoding="utf-8"), TEST_REL.as_posix())
    except (OSError, UnicodeError, SyntaxError) as error:
        return set(), [_finding("TEST_SOURCE_INVALID", TEST_REL, str(error))]
    names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    return names, []


def _contract_findings(root: Path) -> list[Finding]:
    manifest, findings = _load_yaml(root, MANIFEST_REL, "CONTRACT_UNREADABLE")
    contract_schema, errors = _load_json(root, CONTRACT_SCHEMA_REL, "CONTRACT_UNREADABLE")
    contract_example, example_errors = _load_json(
        root, CONTRACT_EXAMPLE_REL, "CONTRACT_UNREADABLE"
    )
    findings.extend(errors + example_errors)
    if contract_schema is not None and contract_example is not None:
        findings.extend(
            _schema_findings(
                contract_example,
                contract_schema,
                CONTRACT_EXAMPLE_REL,
                "CONTRACT_SCHEMA_INVALID",
            )
        )
        corpus_policy = (
            contract_example.get("corpus_contract")
            if isinstance(contract_example, dict)
            else None
        )
        if not isinstance(corpus_policy, dict) or {
            key: corpus_policy.get(key) for key in EXPECTED_CORPUS_POLICY
        } != EXPECTED_CORPUS_POLICY:
            findings.append(
                _finding(
                    "CORPUS_POLICY_INVALID",
                    CONTRACT_EXAMPLE_REL,
                    "split_overlap=REJECT and access_integrity=FAIL_CLOSED required",
                )
            )
    if not isinstance(manifest, dict):
        return findings
    review = manifest.get("review")
    if not isinstance(review, dict) or review.get("self_approval") != "PROHIBITED":
        findings.append(
            _finding("SELF_APPROVAL_INVALID", MANIFEST_REL, "self_approval must be PROHIBITED")
        )
    # Pin every semantic key/value while allowing harmless YAML formatting and key ordering.
    if _semantic_sha256(manifest) != EXPECTED_MANIFEST_SHA256:
        findings.append(
            _finding("CONTRACT_MANIFEST_INVALID", MANIFEST_REL, "frozen manifest drift")
        )
    return findings


def _document_findings(root: Path) -> tuple[dict[str, Any], list[Finding]]:
    loaded: dict[str, Any] = {}
    findings: list[Finding] = []
    paths = {
        "catalog": CATALOG_REL,
        "catalog_schema": CATALOG_SCHEMA_REL,
        "corpus": CORPUS_REL,
        "corpus_schema": CORPUS_SCHEMA_REL,
        "checkpoint": CHECKPOINT_REL,
    }
    for label, relative in paths.items():
        value, errors = _load_json(root, relative, f"{label.upper()}_UNREADABLE")
        findings.extend(errors)
        if value is not None:
            loaded[label] = value
    if "catalog" in loaded and "catalog_schema" in loaded:
        findings.extend(
            _schema_findings(
                loaded["catalog"], loaded["catalog_schema"], CATALOG_REL, "CATALOG_SCHEMA_INVALID"
            )
        )
    if "corpus" in loaded and "corpus_schema" in loaded:
        findings.extend(
            _schema_findings(
                loaded["corpus"], loaded["corpus_schema"], CORPUS_REL, "CORPUS_SCHEMA_INVALID"
            )
        )
    return loaded, findings


def _source_and_corpus_findings(root: Path, loaded: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    catalog = loaded.get("catalog")
    capabilities = catalog.get("capabilities") if isinstance(catalog, dict) else None
    if isinstance(capabilities, list):
        for index, capability in enumerate(capabilities):
            if not isinstance(capability, dict):
                continue
            sources = [capability.get("contract"), *capability.get("knowledge_sources", [])]
            for value in sources:
                path = _safe_path(root, value)
                if path is None:
                    findings.append(
                        _finding(
                            "SOURCE_PATH_INVALID",
                            CATALOG_REL,
                            f"capabilities.{index}: {value!r}",
                        )
                    )
                elif not path.is_file():
                    findings.append(_finding("SOURCE_MISSING", CATALOG_REL, str(value)))
                elif path.suffix.lower() in {".py", ".pyc", ".pyd", ".so", ".dll"}:
                    findings.append(_finding("LEGACY_RUNTIME_IMPORT", CATALOG_REL, str(value)))
    corpus = loaded.get("corpus")
    fixtures = corpus.get("fixtures") if isinstance(corpus, dict) else None
    if isinstance(fixtures, list):
        seen_fixture_ids: set[str] = set()
        seen_paths: set[str] = set()
        for index, fixture in enumerate(fixtures):
            if not isinstance(fixture, dict):
                continue
            fixture_id = fixture.get("fixture_id")
            path_value = fixture.get("path")
            split = fixture.get("split")
            access = fixture.get("access")
            if isinstance(fixture_id, str):
                if fixture_id in seen_fixture_ids:
                    findings.append(
                        _finding(
                            "CORPUS_SPLIT_OVERLAP",
                            CORPUS_REL,
                            f"duplicate fixture_id: {fixture_id}",
                        )
                    )
                seen_fixture_ids.add(fixture_id)
            if isinstance(path_value, str):
                if path_value in seen_paths:
                    findings.append(
                        _finding(
                            "CORPUS_SPLIT_OVERLAP",
                            CORPUS_REL,
                            f"duplicate path: {path_value}",
                        )
                    )
                seen_paths.add(path_value)
            if EXPECTED_ACCESS_BY_SPLIT.get(split) != access:
                findings.append(
                    _finding(
                        "CORPUS_ACCESS_INVALID",
                        CORPUS_REL,
                        f"fixtures.{index}: split/access mismatch",
                    )
                )
            path = _safe_path(root, path_value)
            if path is None:
                findings.append(
                    _finding("CORPUS_PATH_INVALID", CORPUS_REL, f"fixtures.{index}.path")
                )
                continue
            if isinstance(fixture_id, str) and path.stem != fixture_id:
                findings.append(
                    _finding(
                        "CORPUS_ASSOCIATION_INVALID",
                        CORPUS_REL,
                        f"fixtures.{index}: fixture_id/path mismatch",
                    )
                )
            try:
                digest = _canonical_sha256(path)
            except OSError as error:
                findings.append(_finding("CORPUS_FIXTURE_UNREADABLE", CORPUS_REL, str(error)))
                continue
            if digest != fixture.get("sha256"):
                findings.append(
                    _finding("CORPUS_HASH_MISMATCH", CORPUS_REL, f"fixtures.{index}.sha256")
                )
    return findings


def _checkpoint_findings(loaded: dict[str, Any]) -> list[Finding]:
    checkpoint = loaded.get("checkpoint")
    if not isinstance(checkpoint, dict):
        return []
    failure = checkpoint.get("failure_policy")
    commands = checkpoint.get("commands")
    valid = (
        checkpoint.get("checkpoint_id") == "EPIC-006-CAPABILITY-CATALOG-FOUNDATION"
        and checkpoint.get("contract_version") == "1.0.0"
        and checkpoint.get("sources") == EXPECTED_SOURCES
        and isinstance(commands, dict)
        and commands.get("local") == commands.get("ci")
        and isinstance(failure, dict)
        and failure.get("mode") == "FAIL_CLOSED"
        and failure.get("silent_fallback") is False
        and all(failure.get(key) == "REJECT" for key in (
            "invalid_descriptor",
            "missing_corpus_evidence",
            "legacy_runtime_detected",
        ))
    )
    return [] if valid else [_finding("FAILURE_POLICY_INVALID", CHECKPOINT_REL, "checkpoint drift")]


def _task_findings(root: Path) -> list[Finding]:
    task, findings = _load_json(root, TASK_REL, "TASK_UNREADABLE")
    schema, errors = _load_json(root, TASK_SCHEMA_REL, "TASK_SCHEMA_UNREADABLE")
    findings.extend(errors)
    if task is not None and schema is not None:
        findings.extend(_schema_findings(task, schema, TASK_REL, "TASK_SCHEMA_INVALID"))
    if not isinstance(task, dict):
        return findings
    expected = {
        "task_id": "TASK-0028",
        "issue_id": "ISSUE-0138",
        "story_id": "STORY-0028",
        "epic_id": "EPIC-006",
        "role": "DevOps",
        "dependencies": ["STORY-0026"],
        "tests": ["test_epic_006_automacao"],
        "acceptance_criterion_ids": list(ACCEPTANCE_EVIDENCE),
        "allow_paths": EXPECTED_ALLOW_PATHS,
    }
    if any(task.get(key) != value for key, value in expected.items()):
        findings.append(
            _finding("TASK_CONTROL_INVALID", TASK_REL, "identity, test, AC, or scope drift")
        )
    phase_f = task.get("phase_f_review")
    files = phase_f.get("files") if isinstance(phase_f, dict) else None
    if not isinstance(files, dict) or files.get("allow_paths") != task.get("allow_paths"):
        findings.append(_finding("TASK_SCOPE_DRIFT", TASK_REL, "Phase F allow_paths differ"))
    tests, test_errors = _defined_tests(root)
    findings.extend(test_errors)
    expected_tests = set(REQUIREMENT_EVIDENCE.values()) | set(ACCEPTANCE_EVIDENCE.values())
    if expected_tests - tests:
        findings.append(_finding("REQUIRED_TEST_MISSING", TEST_REL, "test_epic_006_automacao"))
    return findings


def _workflow_findings(root: Path) -> list[Finding]:
    workflow, findings = _load_yaml(root, WORKFLOW_REL, "WORKFLOW_INVALID")
    if not isinstance(workflow, dict):
        return findings
    jobs = workflow.get("jobs")
    steps = [
        step
        for job in (jobs or {}).values()
        if isinstance(job, dict)
        for step in job.get("steps", [])
        if isinstance(step, dict)
    ]
    commands = [step["run"] for step in steps if isinstance(step.get("run"), str)]
    uses = [step["uses"] for step in steps if isinstance(step.get("uses"), str)]
    text = (root / WORKFLOW_REL).read_text(encoding="utf-8")
    checks = {
        "read-only permissions": workflow.get("permissions") == {"contents": "read"},
        "pinned checkout": f"actions/checkout@{CHECKOUT_SHA}" in uses,
        "pinned Python": f"actions/setup-python@{SETUP_PYTHON_SHA}" in uses,
        "Python 3.12.13": "python-version: '3.12.13'" in text,
        "validator dry-run": any(
            (QUALITY_REL / "validator.py").as_posix() in command and "--dry-run" in command
            for command in commands
        ),
        "focused acceptance test": any(
            TEST_REL.as_posix() in command and "test_epic_006_automacao" in command
            for command in commands
        ),
        "fail closed": "continue-on-error: true" not in text,
    }
    findings.extend(
        _finding("WORKFLOW_INVALID", WORKFLOW_REL, f"missing {name}")
        for name, passed in checks.items()
        if not passed
    )
    return findings


def validate(root: Path) -> list[Finding]:
    resolved = root.resolve()
    loaded, findings = _document_findings(resolved)
    findings.extend(_contract_findings(resolved))
    findings.extend(_source_and_corpus_findings(resolved, loaded))
    findings.extend(_checkpoint_findings(loaded))
    findings.extend(_task_findings(resolved))
    findings.extend(_workflow_findings(resolved))
    return sorted(set(findings))
