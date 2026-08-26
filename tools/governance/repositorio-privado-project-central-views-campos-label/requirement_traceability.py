from __future__ import annotations

import ast
import csv
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TASK_PATH = Path(".codex/tasks/TASK-0009.json")
STORY_PATH = Path(
    "docs/06-delivery/stories/"
    "STORY-0009-ISSUE-0119-integrar-a-capacidade-ao-fluxo-do-repositorio-"
    "repositorio-privado-project.md"
)
TRACE_PATH = Path("docs/06-delivery/TRACEABILITY_MATRIX.csv")
TEST_PATH = Path(
    "tests/fnd/repositorio-privado-project-central-views-campos-label/"
    "test_integration.py"
)
REQUIREMENT_TESTS = {
    "REQ-CLASSICPROFILE-006": ("ADR-044", "test_req_classicprofile_006"),
    "REQ-CLASSICPROFILE-008": ("ADR-045", "test_req_classicprofile_008"),
    "REQ-CLASSICPROFILE-010": ("ADR-044", "test_req_classicprofile_0010"),
    "REQ-NATIVE-001": ("ADR-042", "test_req_native_001"),
    "REQ-NATIVE-004": ("ADR-042", "test_req_native_004"),
}
REQUIREMENT_PATHS = {
    requirement: Path("docs/01-product/requirements") / filename
    for requirement, filename in {
        "REQ-CLASSICPROFILE-006": (
            "REQ-CLASSICPROFILE-006-ratio-reverse-matching-mutual-consistency-e-"
            "unicidade-sao-explicitos.md"
        ),
        "REQ-CLASSICPROFILE-008": (
            "REQ-CLASSICPROFILE-008-poda-pre-homografia-e-deterministica-e-preserva-"
            "coverage.md"
        ),
        "REQ-CLASSICPROFILE-010": (
            "REQ-CLASSICPROFILE-010-classicalmatchingprofile-e-imutavel-promovido-por-"
            "shadow-canary-e-revers.md"
        ),
        "REQ-NATIVE-001": "REQ-NATIVE-001-rasterio-e-boundary-principal-e-gdal-fica-isolado.md",
        "REQ-NATIVE-004": "REQ-NATIVE-004-rastertile-e-tipado-band-first-e-rastreavel.md",
    }.items()
}


@dataclass(frozen=True, order=True)
class TraceFinding:
    code: str
    artifact: str
    detail: str


def story_text(root: Path) -> tuple[str | None, list[TraceFinding]]:
    try:
        return (root / STORY_PATH).read_text(encoding="utf-8"), []
    except (OSError, UnicodeError) as error:
        return None, [TraceFinding("STORY_INVALID", STORY_PATH.as_posix(), str(error))]


def requirement_findings(
    root: Path, task: Mapping[str, Any], requirement_ids: Sequence[str]
) -> list[TraceFinding]:
    story, findings = story_text(root)
    try:
        with (root / TRACE_PATH).open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as error:
        return [*findings, TraceFinding("TRACE_MATRIX_INVALID", TRACE_PATH.as_posix(), str(error))]
    references = task.get("references")
    reference_values = references if isinstance(references, list) else []
    story_requirements = re.findall(r"REQ-[A-Z0-9-]+", story or "")
    for requirement_id in requirement_ids:
        owner, test_name = REQUIREMENT_TESTS[requirement_id]
        path = REQUIREMENT_PATHS[requirement_id]
        reference_count = reference_values.count(path.as_posix())
        if reference_count != 1 or story_requirements.count(requirement_id) < 1:
            code = (
                "REQUIREMENT_TRACE_DUPLICATED"
                if reference_count > 1
                else "REQUIREMENT_TRACE_MISSING"
            )
            findings.append(TraceFinding(code, requirement_id, "one task/story reference required"))
        try:
            document = (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(
                TraceFinding("REQUIREMENT_DOCUMENT_INVALID", path.as_posix(), str(error))
            )
            continue
        if any(token not in document for token in (requirement_id, owner, test_name, "`ACCEPTED`")):
            findings.append(
                TraceFinding("REQUIREMENT_DOCUMENT_DRIFT", path.as_posix(), "metadata differs")
            )
        matches = [row for row in rows if row.get("requirement_id") == requirement_id]
        valid = len(matches) == 1 and all(
            (
                matches[0].get("owner") == owner,
                matches[0].get("evidence_or_test") == test_name,
                matches[0].get("status") == "ACCEPTED",
                "STORY-0009" in matches[0].get("stories", "").split("/"),
                "EPIC-002" in matches[0].get("epics", "").split("/"),
            )
        )
        if not valid:
            findings.append(
                TraceFinding(
                    "REQUIREMENT_TRACE_DRIFT", TRACE_PATH.as_posix(), requirement_id
                )
            )
    return findings


def test_surface_findings(
    root: Path, expected: Sequence[str] | None = None
) -> list[TraceFinding]:
    names = tuple(expected or (value[1] for value in REQUIREMENT_TESTS.values()))
    if expected is None:
        names = (*names, "test_epic_002_integracao")
    try:
        tree = ast.parse((root / TEST_PATH).read_bytes(), filename=TEST_PATH.as_posix())
    except (OSError, SyntaxError) as error:
        return [TraceFinding("TEST_SURFACE_INVALID", TEST_PATH.as_posix(), str(error))]
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    missing = [name for name in names if functions.count(name) != 1]
    return [] if not missing else [
        TraceFinding("TEST_SURFACE_INVALID", TEST_PATH.as_posix(), ",".join(missing))
    ]


def validate_requirement_traceability(
    repository_root: Path, requirement_id: str
) -> tuple[TraceFinding, ...]:
    root = repository_root.resolve()
    if requirement_id not in REQUIREMENT_TESTS:
        return (TraceFinding("REQUIREMENT_UNKNOWN", requirement_id, "not governed by ISSUE-0119"),)
    try:
        task = json.loads((root / TASK_PATH).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return (TraceFinding("JSON_INVALID", TASK_PATH.as_posix(), str(error)),)
    findings = requirement_findings(root, task, (requirement_id,))
    findings.extend(test_surface_findings(root, (REQUIREMENT_TESTS[requirement_id][1],)))
    return tuple(sorted(set(findings)))
