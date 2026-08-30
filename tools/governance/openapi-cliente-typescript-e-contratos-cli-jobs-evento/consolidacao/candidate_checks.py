from __future__ import annotations

import ast
import csv
import hashlib
import io
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass

from candidate_repository import CandidateView


REVIEW_PATH = "docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv"
CONSOLIDATION_PATH = (
    "contracts/contexts/engineering_governance/fnd/"
    "openapi-cliente-typescript-e-contratos-cli-jobs-evento/"
    "consolidacao/examples/slice-consolidation.json"
)


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


def coverage_findings(
    view: CandidateView, tasks: tuple[Mapping[str, object], ...]
) -> tuple[tuple[str, ...], list[Finding]]:
    rows = {
        row["issue_id"]: row
        for row in csv.DictReader(io.StringIO(view.blob(REVIEW_PATH).decode("utf-8")))
    }
    findings: list[Finding] = []
    seen: set[str] = set()
    for task in tasks:
        issue_id = str(task.get("issue_id"))
        references = task.get("references")
        story_paths = [
            item
            for item in references or []
            if isinstance(item, str) and "/stories/STORY-" in item
        ]
        if len(story_paths) != 1:
            findings.append(
                Finding("REQUIREMENT_COVERAGE_INVALID", issue_id, "slice story is absent")
            )
            continue
        story = view.blob(story_paths[0]).decode("utf-8")
        section = re.search(r"## Requisitos\s+(.*?)\s+## ADRs", story, re.DOTALL)
        declared = tuple(
            sorted(set(re.findall(r"REQ-[A-Z0-9-]+", section.group(1) if section else "")))
        )
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
                Finding("REQUIREMENT_DUPLICATED", issue_id, ", ".join(sorted(duplicates)))
            )
        seen.update(declared)
    return tuple(sorted(seen)), findings


def integration_findings(
    view: CandidateView,
    tasks: tuple[Mapping[str, object], ...],
    scopes: tuple[tuple[str, ...], ...],
    paths: tuple[str, ...],
) -> list[Finding]:
    findings: list[Finding] = []
    source_digests: dict[str, str] = {}
    checkpoint_ids: dict[str, str] = {}
    control_owners: dict[str, str] = {}
    binding_digests: dict[str, str] = {}
    dependency_paths: set[str] = set()

    for task, group in zip(tasks, scopes, strict=True):
        group_paths = [
            path for path in paths if any(path.startswith(f"{scope}/") for scope in group)
        ]
        sources = [path for path in group_paths if path.endswith(".py")]
        checkpoints = [path for path in group_paths if path.endswith(".json")]
        documents = [path for path in group_paths if path.endswith(".md")]
        if len(sources) != 1 or len(checkpoints) != 1 or len(documents) != 1:
            findings.append(
                Finding(
                    "SLICE_OUTPUT_INVALID",
                    str(task.get("story_id")),
                    "one validator, checkpoint, and handoff document required",
                )
            )
            continue
        findings.extend(_source_findings(view, sources[0], source_digests))
        findings.extend(
            _checkpoint_findings(
                view,
                checkpoints[0],
                task,
                checkpoint_ids,
                control_owners,
                binding_digests,
                dependency_paths,
            )
        )
        if not view.blob(documents[0]).strip():
            findings.append(
                Finding("SLICE_OUTPUT_INVALID", documents[0], "handoff document is empty")
            )

    if dependency_paths != {CONSOLIDATION_PATH}:
        findings.append(
            Finding(
                "SLICE_INTEGRATION_MISSING",
                "dependency.consolidation",
                "all slices must consume the frozen consolidation contract",
            )
        )
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
        findings.append(Finding("REDUNDANT_IMPLEMENTATION", path, digests[digest]))
    digests[digest] = path
    return findings


def _checkpoint_findings(
    view: CandidateView,
    path: str,
    task: Mapping[str, object],
    checkpoint_ids: dict[str, str],
    control_owners: dict[str, str],
    binding_digests: dict[str, str],
    dependency_paths: set[str],
) -> list[Finding]:
    try:
        checkpoint = json.loads(view.blob(path))
    except json.JSONDecodeError as error:
        return [Finding("SLICE_OUTPUT_INVALID", path, str(error))]
    if not isinstance(checkpoint, Mapping):
        return [Finding("SLICE_OUTPUT_INVALID", path, "checkpoint object required")]

    findings = _identity_and_dependency_findings(
        view,
        checkpoint,
        task,
        path,
        checkpoint_ids,
        binding_digests,
        dependency_paths,
    )
    findings.extend(_requirement_findings(checkpoint, task, path))
    findings.extend(_control_findings(checkpoint, path, control_owners))
    findings.extend(_canonical_binding_findings(view, checkpoint, path, binding_digests))
    return findings


def _identity_and_dependency_findings(
    view: CandidateView,
    checkpoint: Mapping[str, object],
    task: Mapping[str, object],
    path: str,
    checkpoint_ids: dict[str, str],
    binding_digests: dict[str, str],
    dependency_paths: set[str],
) -> list[Finding]:
    findings: list[Finding] = []
    checkpoint_id = checkpoint.get("checkpoint_id")
    compatible = (
        checkpoint.get("schema_version") == "1.0.0"
        and checkpoint.get("owner") == "BC-001"
        and isinstance(checkpoint_id, str)
        and bool(checkpoint_id)
    )
    if not compatible:
        findings.append(Finding("SLICE_OUTPUT_INVALID", path, "compatible BC-001 checkpoint required"))
    elif checkpoint_id in checkpoint_ids:
        findings.append(Finding("CONTRACT_COLLISION", path, checkpoint_ids[checkpoint_id]))
    else:
        checkpoint_ids[str(checkpoint_id)] = path

    dependency = checkpoint.get("dependency")
    if not isinstance(dependency, Mapping):
        return findings + [Finding("SLICE_OUTPUT_INVALID", path, "dependency object required")]
    consolidation = dependency.get("consolidation")
    dependency_path = (
        consolidation.get("path") if isinstance(consolidation, Mapping) else consolidation
    )
    if isinstance(dependency_path, str):
        dependency_paths.add(dependency_path)
    valid_dependency = (
        dependency_path == CONSOLIDATION_PATH
        and dependency.get("eligible_story") == task.get("story_id")
        and dependency.get("required_state") == "READY_FOR_INDEPENDENT_REVIEW"
    )
    if not valid_dependency:
        findings.append(Finding("SLICE_INTEGRATION_MISSING", path, "invalid consolidation binding"))
    if isinstance(consolidation, Mapping):
        findings.extend(_binding_findings(view, consolidation, binding_digests, path))
    return findings


def _requirement_findings(
    checkpoint: Mapping[str, object], task: Mapping[str, object], path: str
) -> list[Finding]:
    requirements = checkpoint.get("requirements")
    if not isinstance(requirements, list):
        return [Finding("SLICE_OUTPUT_INVALID", path, "checkpoint requirements are absent")]
    requirement_tests = {
        (item.get("id"), item.get("test"))
        for item in requirements
        if isinstance(item, Mapping)
    }
    task_tests = task.get("tests")
    references = task.get("references")
    expected_requirements = set(
        re.findall(
            r"REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*",
            " ".join(
                item
                for item in references or []
                if isinstance(item, str) and "/requirements/REQ-" in item
            ),
        )
    )
    valid = (
        isinstance(task_tests, list)
        and len(requirement_tests) == len(requirements)
        and {requirement for requirement, _test in requirement_tests}
        == expected_requirements
        and {test for _requirement, test in requirement_tests} == set(task_tests)
    )
    return [] if valid else [
        Finding("SLICE_OUTPUT_INVALID", path, "checkpoint tests differ from TaskEnvelope")
    ]


def _control_findings(
    checkpoint: Mapping[str, object], path: str, owners: dict[str, str]
) -> list[Finding]:
    controls = checkpoint.get("controls")
    if not isinstance(controls, Mapping) or not controls:
        return [Finding("SLICE_OUTPUT_INVALID", path, "controls are absent")]
    findings: list[Finding] = []
    for control in controls:
        name = str(control)
        if name in owners:
            findings.append(Finding("CONTRACT_COLLISION", path, f"control {name} in {owners[name]}"))
        else:
            owners[name] = path
    return findings


def _canonical_binding_findings(
    view: CandidateView,
    checkpoint: Mapping[str, object],
    path: str,
    binding_digests: dict[str, str],
) -> list[Finding]:
    bindings = checkpoint.get("canonical_bindings", checkpoint.get("canonical_contracts"))
    if not isinstance(bindings, Mapping) or not bindings:
        return [Finding("SLICE_OUTPUT_INVALID", path, "canonical bindings are absent")]
    findings: list[Finding] = []
    for binding in bindings.values():
        normalized = {"path": binding} if isinstance(binding, str) else binding
        if not isinstance(normalized, Mapping):
            findings.append(Finding("SLICE_OUTPUT_INVALID", path, "invalid canonical binding"))
        else:
            findings.extend(_binding_findings(view, normalized, binding_digests, path))
    return findings


def _binding_findings(
    view: CandidateView,
    binding: Mapping[str, object],
    binding_digests: dict[str, str],
    owner_path: str,
) -> list[Finding]:
    contract_path = binding.get("path")
    expected = binding.get("sha256")
    if not isinstance(contract_path, str) or not contract_path.startswith("contracts/"):
        return [Finding("CONTRACT_BINDING_INVALID", owner_path, "contract path required")]
    digest = hashlib.sha256(view.blob(contract_path)).hexdigest()
    if expected is not None and expected != digest:
        return [Finding("CONTRACT_BINDING_DRIFT", contract_path, owner_path)]
    previous = binding_digests.get(contract_path)
    if previous is not None and previous != digest:
        return [Finding("CONTRACT_BINDING_CONFLICT", contract_path, owner_path)]
    binding_digests[contract_path] = digest
    return []
