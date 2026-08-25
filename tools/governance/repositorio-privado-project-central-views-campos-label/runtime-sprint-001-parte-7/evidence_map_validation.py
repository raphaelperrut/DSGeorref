from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


class EvidenceMapValidationError(ValueError):
    def __init__(self, findings: list[Finding] | tuple[Finding, ...]) -> None:
        self.findings = tuple(sorted(findings))
        message = "; ".join(
            f"{finding.code} at {finding.field}: {finding.detail}"
            for finding in self.findings
        )
        super().__init__(message)


EXPECTED_WRITE_SCOPE = (
    ".codex/tasks/TASK-0698.json",
    "tools/governance/repositorio-privado-project-central-views-campos-label/"
    "runtime-sprint-001-parte-7/**",
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "runtime-sprint-001-parte-7/**",
    "tests/fnd/repositorio-privado-project-central-views-campos-label/"
    "test_runtime_sprint_foundation.py",
    "evidence/implementation/repositorio-privado-project-central-views-campos-l/"
    "runtime-sprint-001-parte-7/**",
)
SPRINT_TEST_PATH = (
    "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "test_materialization.py"
)
LOCAL_TEST_PATH = (
    "tests/fnd/repositorio-privado-project-central-views-campos-label/"
    "test_runtime_sprint_foundation.py"
)
EXPECTED_REQUIREMENTS: dict[str, dict[str, str]] = {
    "REQ-RUNTIME-001": {
        "primitive_path": "contracts/contexts/engineering_governance/fnd/"
        "repositorio-privado-project-central-views-campos-label/"
        "classicprofile-iss-native-parte-1/examples/foundation-conformance.json",
        "checkpoint": "tests/fnd/repositorio-privado-project-central-views-campos-label/"
        "test_foundation_conformance.py::test_req_run_001",
        "test_path": LOCAL_TEST_PATH,
        "test_id": "test_runtime_decision_1",
    },
    "REQ-RUNTIME-002": {
        "primitive_path": "docs/03-engineering/contexts/engineering_governance/"
        "repositorio-privado-project-central-views-campos-label/"
        "prm-run-parte-6/foundation-policy.json",
        "checkpoint": "tests/fnd/repositorio-privado-project-central-views-campos-label/"
        "test_portfolio_runtime_foundation.py::test_req_run_002",
        "test_path": LOCAL_TEST_PATH,
        "test_id": "test_runtime_decision_2",
    },
    "REQ-SPRINT-001-001": {
        "primitive_path": "tools/governance/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "frz-gov-adr-gov-dec-parte-1/sprint_validation.py",
        "checkpoint": f"{SPRINT_TEST_PATH}::test_sprint_zero_baseline_decision_01",
        "test_path": SPRINT_TEST_PATH,
        "test_id": "test_sprint_zero_baseline_decision_01",
    },
    "REQ-SPRINT-001-002": {
        "primitive_path": "tools/governance/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "frz-gov-adr-gov-dec-parte-1/sprint_validation.py",
        "checkpoint": f"{SPRINT_TEST_PATH}::test_sprint_zero_baseline_decision_02",
        "test_path": SPRINT_TEST_PATH,
        "test_id": "test_sprint_zero_baseline_decision_02",
    },
    "REQ-SPRINT-001-003": {
        "primitive_path": "tools/governance/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "sprint-001-tool-parte-2/sprint_graph.py",
        "checkpoint": f"{SPRINT_TEST_PATH}::test_sprint_zero_baseline_decision_03",
        "test_path": SPRINT_TEST_PATH,
        "test_id": "test_sprint_zero_baseline_decision_03",
    },
    "REQ-SPRINT-001-005": {
        "primitive_path": "tools/governance/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "sprint-001-tool-parte-2/decision_evidence_validation.py",
        "checkpoint": f"{SPRINT_TEST_PATH}::test_sprint_zero_baseline_decision_05",
        "test_path": SPRINT_TEST_PATH,
        "test_id": "test_sprint_zero_baseline_decision_05",
    },
    "REQ-SPRINT-001-006": {
        "primitive_path": "tools/governance/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "sprint-001-tool-parte-2/decision_evidence_validation.py",
        "checkpoint": f"{SPRINT_TEST_PATH}::test_sprint_zero_baseline_decision_06",
        "test_path": SPRINT_TEST_PATH,
        "test_id": "test_sprint_zero_baseline_decision_06",
    },
    "REQ-SPRINT-001-007": {
        "primitive_path": "tools/governance/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "sprint-001-tool-parte-2/sprint_decisions.py",
        "checkpoint": f"{SPRINT_TEST_PATH}::test_sprint_zero_baseline_decision_07",
        "test_path": SPRINT_TEST_PATH,
        "test_id": "test_sprint_zero_baseline_decision_07",
    },
    "REQ-SPRINT-001-008": {
        "primitive_path": "tools/governance/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "sprint-001-tool-parte-2/sprint_evidence.py",
        "checkpoint": f"{SPRINT_TEST_PATH}::test_sprint_zero_baseline_decision_08",
        "test_path": SPRINT_TEST_PATH,
        "test_id": "test_sprint_zero_baseline_decision_08",
    },
    "REQ-SPRINT-001-009": {
        "primitive_path": "tools/governance/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "sprint-001-tool-parte-2/sprint_decisions.py",
        "checkpoint": f"{SPRINT_TEST_PATH}::test_sprint_zero_baseline_decision_09",
        "test_path": SPRINT_TEST_PATH,
        "test_id": "test_sprint_zero_baseline_decision_09",
    },
}
EXPECTED_MAP: dict[str, Any] = {
    "schema_version": "1.0.0",
    "map_id": "ENGINEERING-FOUNDATION-RUNTIME-SPRINT-EVIDENCE",
    "owner": "BC-001",
    "status": "CANDIDATE",
    "coverage": sorted(EXPECTED_REQUIREMENTS),
    "write_scope": list(EXPECTED_WRITE_SCOPE),
    "requirements": EXPECTED_REQUIREMENTS,
}


class EvidenceMapValidator:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve()

    def validate(self, evidence_map: object) -> list[Finding]:
        findings = self._compare(evidence_map, EXPECTED_MAP, "$")
        if not isinstance(evidence_map, dict):
            return sorted(findings)
        findings.extend(self._scope_findings(evidence_map.get("write_scope")))
        findings.extend(self._task_findings())
        findings.extend(self._reference_findings(evidence_map.get("requirements")))
        return sorted(set(findings))

    def _compare(self, actual: object, expected: object, field: str) -> list[Finding]:
        if isinstance(expected, dict):
            if not isinstance(actual, dict):
                return [Finding(self._finding_code(field), field, "expected object")]
            findings: list[Finding] = []
            for key in sorted(actual.keys() - expected.keys()):
                findings.append(Finding("MAP_STRUCTURE_INVALID", f"{field}.{key}", "unknown field"))
            for key in sorted(expected.keys() - actual.keys()):
                target = f"{field}.{key}"
                findings.append(Finding(self._finding_code(target), target, "missing field"))
            for key in sorted(actual.keys() & expected.keys()):
                findings.extend(self._compare(actual[key], expected[key], f"{field}.{key}"))
            return findings
        if type(actual) is not type(expected) or actual != expected:
            return [Finding(self._finding_code(field), field, f"expected {expected!r}")]
        return []

    @staticmethod
    def _finding_code(field: str) -> str:
        if field.startswith("$.coverage"):
            return "COVERAGE_INCOMPLETE"
        if field.startswith("$.write_scope"):
            return "WRITE_SCOPE_INVALID"
        if any(field.endswith(suffix) for suffix in (".primitive_path", ".checkpoint", ".test_path")):
            return "REFERENCE_INVALID"
        if field.startswith("$.requirements"):
            return "REQUIREMENT_EVIDENCE_INVALID"
        return "MAP_STRUCTURE_INVALID"

    def _scope_findings(self, scope: object) -> list[Finding]:
        if not isinstance(scope, list) or not all(isinstance(path, str) for path in scope):
            return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "expected path list")]
        roots = [path.removesuffix("/**").rstrip("/") for path in scope]
        if len(roots) != len(set(roots)):
            return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "duplicate path")]
        for index, root in enumerate(roots):
            for other in roots[index + 1 :]:
                if root.startswith(f"{other}/") or other.startswith(f"{root}/"):
                    return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "overlapping paths")]
        return []

    def _task_findings(self) -> list[Finding]:
        task_path = self.repository_root / ".codex/tasks/TASK-0698.json"
        try:
            task = json.loads(task_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", str(error))]
        expected = list(EXPECTED_WRITE_SCOPE)
        phase_f_scope = task.get("phase_f_review", {}).get("files", {}).get("allow_paths")
        if task.get("allow_paths") != expected or phase_f_scope != expected:
            return [Finding("WRITE_SCOPE_INVALID", "$.write_scope", "TaskEnvelope scope mismatch")]
        return []

    def _reference_findings(self, requirements: object) -> list[Finding]:
        if not isinstance(requirements, dict):
            return []
        findings: list[Finding] = []
        for requirement_id, evidence in requirements.items():
            field = f"$.requirements.{requirement_id}"
            if not isinstance(evidence, dict):
                continue
            for key in ("primitive_path", "test_path"):
                reference = evidence.get(key)
                if self._resolve_reference(reference) is None:
                    findings.append(Finding("REFERENCE_INVALID", f"{field}.{key}", "missing or unsafe path"))
            checkpoint = evidence.get("checkpoint")
            if not isinstance(checkpoint, str) or "::" not in checkpoint:
                findings.append(Finding("REFERENCE_INVALID", f"{field}.checkpoint", "invalid selector"))
                continue
            path_value, symbol = checkpoint.rsplit("::", 1)
            path = self._resolve_reference(path_value)
            if path is None or not symbol:
                findings.append(Finding("REFERENCE_INVALID", f"{field}.checkpoint", "missing selector target"))
                continue
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, SyntaxError) as error:
                findings.append(Finding("REFERENCE_INVALID", f"{field}.checkpoint", str(error)))
                continue
            functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
            if symbol not in functions:
                findings.append(Finding("REFERENCE_INVALID", f"{field}.checkpoint", "test symbol absent"))
        return findings

    def _resolve_reference(self, value: object) -> Path | None:
        if not isinstance(value, str) or not value or "\\" in value:
            return None
        candidate = (self.repository_root / value).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError:
            return None
        return candidate if candidate.is_file() else None


def validate_evidence_map(evidence_map: object, repository_root: Path) -> list[Finding]:
    return EvidenceMapValidator(repository_root).validate(evidence_map)


def load_evidence_map(path: Path, repository_root: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EvidenceMapValidationError(
            [Finding("MAP_UNREADABLE", "$", str(error))]
        ) from error
    findings = validate_evidence_map(loaded, repository_root)
    if findings:
        raise EvidenceMapValidationError(findings)
    return loaded
