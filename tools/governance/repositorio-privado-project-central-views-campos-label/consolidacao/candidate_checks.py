from __future__ import annotations

import ast
import csv
import hashlib
import io
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from candidate_repository import CandidateView


REVIEW_PATH = "docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv"


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


def coverage_findings(
    view: CandidateView, tasks: tuple[Mapping[str, Any], ...]
) -> tuple[tuple[str, ...], list[Finding]]:
    rows = {
        row["issue_id"]: row
        for row in csv.DictReader(
            io.StringIO(view.blob(REVIEW_PATH).decode("utf-8"))
        )
    }
    findings: list[Finding] = []
    seen: set[str] = set()
    for task in tasks:
        issue_id = str(task.get("issue_id"))
        references = task.get("references")
        stories = [
            item
            for item in references or []
            if isinstance(item, str) and "/stories/STORY-" in item
        ]
        if len(stories) != 1:
            findings.append(
                Finding("REQUIREMENT_COVERAGE_INVALID", issue_id, "slice story is absent")
            )
            continue
        story = view.blob(stories[0]).decode("utf-8")
        section = re.search(r"## Requisitos\s+(.*?)\s+## ADRs", story, re.DOTALL)
        section_text = section.group(1) if section else ""
        declared = tuple(sorted(set(re.findall(r"REQ-[A-Z0-9-]+", section_text))))
        row = rows.get(issue_id)
        reviewed = tuple(sorted(row["requirements"].split("/"))) if row else ()
        if row is None or row.get("status") != "PASS" or declared != reviewed:
            findings.append(
                Finding(
                    "REQUIREMENT_COVERAGE_INVALID",
                    issue_id,
                    "story and review matrix differ",
                )
            )
        duplicates = seen.intersection(declared)
        if duplicates:
            findings.append(
                Finding(
                    "REQUIREMENT_DUPLICATED",
                    issue_id,
                    ", ".join(sorted(duplicates)),
                )
            )
        seen.update(declared)
    return tuple(sorted(seen)), findings


def integration_findings(
    view: CandidateView,
    scopes: tuple[tuple[str, ...], ...],
    paths: tuple[str, ...],
) -> list[Finding]:
    findings: list[Finding] = []
    source_digests: dict[str, str] = {}
    artifact_ids: dict[str, str] = {}
    for group in scopes:
        group_paths = [
            path
            for path in paths
            if any(path.startswith(f"{scope}/") for scope in group)
        ]
        sources = [path for path in group_paths if path.endswith(".py")]
        artifacts = [path for path in group_paths if path.endswith(".json")]
        if len(sources) != 1 or len(artifacts) != 1:
            findings.append(
                Finding(
                    "SLICE_OUTPUT_INVALID",
                    "outputs",
                    "each slice requires one validator and one policy/map",
                )
            )
        for path in sources:
            findings.extend(_source_findings(view, path, source_digests))
        for path in artifacts:
            findings.extend(_artifact_findings(view, path, artifact_ids))
    return findings


def _source_findings(
    view: CandidateView, path: str, digests: dict[str, str]
) -> list[Finding]:
    content = view.blob(path)
    findings: list[Finding] = []
    try:
        ast.parse(content, filename=path)
    except SyntaxError as error:
        findings.append(Finding("SLICE_OUTPUT_INVALID", path, str(error)))
    digest = hashlib.sha256(content).hexdigest()
    if digest in digests:
        findings.append(
            Finding("REDUNDANT_IMPLEMENTATION", path, f"duplicates {digests[digest]}")
        )
    digests[digest] = path
    return findings


def _artifact_findings(
    view: CandidateView, path: str, identities: dict[str, str]
) -> list[Finding]:
    try:
        payload = json.loads(view.blob(path))
    except json.JSONDecodeError as error:
        return [Finding("SLICE_OUTPUT_INVALID", path, str(error))]
    if not isinstance(payload, Mapping):
        return [Finding("SLICE_OUTPUT_INVALID", path, "JSON object required")]
    artifact_id = payload.get("policy_id") or payload.get("map_id")
    compatible = (
        payload.get("schema_version") == "1.0.0"
        and payload.get("owner") == "BC-001"
        and payload.get("status") == "CANDIDATE"
    )
    if not isinstance(artifact_id, str) or not artifact_id or not compatible:
        return [
            Finding(
                "SLICE_OUTPUT_INVALID",
                path,
                "compatible BC-001 candidate policy/map identity required",
            )
        ]
    if artifact_id in identities:
        return [
            Finding("CONTRACT_COLLISION", path, f"duplicates {identities[artifact_id]}")
        ]
    identities[artifact_id] = path
    return []
