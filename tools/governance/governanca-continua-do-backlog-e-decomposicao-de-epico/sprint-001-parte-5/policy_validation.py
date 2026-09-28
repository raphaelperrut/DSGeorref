from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


class PolicyValidationError(ValueError):
    def __init__(self, findings: list[Finding]) -> None:
        self.findings = tuple(sorted(findings))
        message = "; ".join(
            f"{finding.code} at {finding.field}: {finding.detail}"
            for finding in self.findings
        )
        super().__init__(message)


class _DuplicateKeyError(ValueError):
    pass


_POLICY_PATH = Path(__file__).resolve().parents[4] / (
    "docs/03-engineering/contexts/engineering_governance/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico/"
    "sprint-001-parte-5/foundation-policy.json"
)
_POLICY_SHA256 = "40cfa52aeba566014de3181c849e33da7206b302bee0bc8ec07037b7c9c95a9f"

_CONTROL_CODES = {
    "graph_selection": "GRAPH_SELECTION_INVALID",
    "vertical_waves": "VERTICAL_WAVES_INVALID",
    "essential_contracts": "ESSENTIAL_CONTRACTS_INVALID",
    "synthetic_diagnostic": "SYNTHETIC_DIAGNOSTIC_INVALID",
    "progressive_ci": "PROGRESSIVE_CI_INVALID",
    "sprint_evidence_set": "SPRINT_EVIDENCE_SET_INVALID",
    "sprint_closure": "SPRINT_CLOSURE_INVALID",
    "first_slice_cutover": "FIRST_SLICE_CUTOVER_INVALID",
}


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(key)
        result[key] = value
    return result


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object
        )
    except _DuplicateKeyError as error:
        raise PolicyValidationError(
            [Finding("POLICY_DUPLICATE_KEY", f"$.{error}", "duplicate key")]
        ) from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PolicyValidationError(
            [Finding("POLICY_UNREADABLE", "$", str(error))]
        ) from error
    if not isinstance(value, dict):
        raise PolicyValidationError(
            [Finding("POLICY_STRUCTURE_INVALID", "$", "expected object")]
        )
    return value


EXPECTED_POLICY = _read_json(_POLICY_PATH)
_canonical_policy = json.dumps(
    EXPECTED_POLICY, ensure_ascii=False, separators=(",", ":"), sort_keys=True
).encode("utf-8")
_policy_digest = sha256(_canonical_policy).hexdigest()
if _policy_digest != _POLICY_SHA256:
    raise PolicyValidationError(
        [Finding("POLICY_INTEGRITY_INVALID", "$", "unexpected policy digest")]
    )


def _finding_code(field: str) -> str:
    for control, code in _CONTROL_CODES.items():
        if field.startswith(f"$.controls.{control}"):
            return code
    if field.startswith("$.requirement_evidence"):
        return "REQUIREMENT_EVIDENCE_INVALID"
    return "POLICY_STRUCTURE_INVALID"


def _compare(actual: object, expected: object, field: str) -> list[Finding]:
    if not isinstance(expected, dict):
        if type(actual) is type(expected) and actual == expected:
            return []
        return [Finding(_finding_code(field), field, f"expected {expected!r}")]
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


def validate_policy(policy: object) -> list[Finding]:
    return sorted(_compare(policy, EXPECTED_POLICY, "$"))


def require_valid(policy: object) -> None:
    findings = validate_policy(policy)
    if findings:
        raise PolicyValidationError(findings)


def load_policy(path: Path) -> dict[str, Any]:
    loaded = _read_json(path)
    require_valid(loaded)
    return loaded
