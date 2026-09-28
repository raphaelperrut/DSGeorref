from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[4]
CAPABILITY = "governanca-continua-do-backlog-e-decomposicao-de-epico"
TOOLS_ROOT = Path("tools/governance") / CAPABILITY
DOCS_ROOT = (
    Path("docs/03-engineering/contexts/engineering_governance") / CAPABILITY
)
EVIDENCE_ROOT = Path(
    "evidence/implementation/governanca-continua-do-backlog-e-decomposicao-de-e"
)
CONTRACT_PATH = Path(
    "contracts/contexts/engineering_governance/fnd"
) / CAPABILITY / "contract-manifest.yaml"
EPIC_PATH = Path("docs/06-delivery/epics") / (
    "EPIC-110-governanca-continua-do-backlog-e-decomposicao-de-epicos-em-"
    "historias-i.md"
)


@dataclass(frozen=True)
class Slice:
    story_id: str
    task_id: str
    package: str
    merge_commit: str
    outputs: tuple[Path, ...]


def _outputs(package: str, tool_files: tuple[str, ...], doc_files: tuple[str, ...],
             evidence_file: str | None = None) -> tuple[Path, ...]:
    paths = tuple(TOOLS_ROOT / package / name for name in tool_files)
    paths += tuple(DOCS_ROOT / package / name for name in doc_files)
    if evidence_file is not None:
        paths += (EVIDENCE_ROOT / package / evidence_file,)
    return paths


SLICES = (
    Slice(
        "STORY-0754",
        "TASK-0754",
        "ism-iss-parte-1",
        "af6fb2091a446cca6ec781003cc40a3528b881ca",
        _outputs(
            "ism-iss-parte-1",
            (
                "backlog_validation.py",
                "domain_taxonomy.py",
                "policy_validation.py",
                "test_backlog_governance.py",
            ),
            ("README.md", "domain-taxonomy.json", "foundation-policy.json"),
            "IMPLEMENTATION_EVIDENCE.yaml",
        ),
    ),
    Slice(
        "STORY-0755",
        "TASK-0755",
        "iss-pln-parte-2",
        "0686b168be5f1996972d60261a5da4afe110f0ca",
        _outputs(
            "iss-pln-parte-2",
            ("policy_validation.py", "test_policy_validation.py"),
            ("README.md", "foundation-policy.json"),
            "IMPLEMENTATION_EVIDENCE.yaml",
        ),
    ),
    Slice(
        "STORY-0756",
        "TASK-0756",
        "prj-prm-parte-3",
        "0415c9a880ebad159fdbb0b5aad5066c04052ab6",
        _outputs(
            "prj-prm-parte-3",
            ("policy_validation.py", "test_policy_validation.py"),
            ("HANDOFF.md", "foundation-policy.json"),
        ),
    ),
    Slice(
        "STORY-0757",
        "TASK-0757",
        "prm-sprint-001-parte-4",
        "97d6668c72b18cce5feca50ac3b0855afb47a357",
        _outputs(
            "prm-sprint-001-parte-4",
            ("policy_validation.py", "test_policy_validation.py"),
            ("HANDOFF.md", "foundation-policy.json"),
            "IMPLEMENTATION_EVIDENCE.md",
        ),
    ),
    Slice(
        "STORY-0758",
        "TASK-0758",
        "sprint-001-parte-5",
        "b40f0e9a94000eb0f5beb18a0813fcf11f6ba116",
        _outputs(
            "sprint-001-parte-5",
            ("policy_validation.py", "test_policy_validation.py"),
            ("HANDOFF.md", "foundation-policy.json"),
            "IMPLEMENTATION_EVIDENCE.md",
        ),
    ),
)


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads((ROOT / path).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), f"{path} must contain an object"
    return loaded


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), f"{path} must contain a mapping"
    return loaded


def _task_requirements(task: dict[str, Any]) -> set[str]:
    requirements: set[str] = set()
    for reference in task["references"]:
        match = re.match(r"(REQ-[A-Z]+(?:-\d+)+)-", Path(reference).name)
        if match is not None:
            requirements.add(match.group(1))
    return requirements


def _epic_requirements() -> set[str]:
    lines = (ROOT / EPIC_PATH).read_text(encoding="utf-8").splitlines()
    requirement_line = next(line for line in lines if line.startswith("- Requisitos:"))
    return set(re.findall(r"REQ-[A-Z]+(?:-\d+)+", requirement_line))


def _claim(unique: dict[str, str], key: str, owner: str, kind: str) -> None:
    assert key not in unique, (
        f"duplicate {kind} {key}: {unique.get(key)} and {owner}"
    )
    unique[key] = owner


def _assert_merge_is_ancestor(commit: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"dependency merge {commit} is not in candidate HEAD: {result.stderr}"
    )


def _assert_scopes_are_disjoint(scopes: list[tuple[str, str]]) -> None:
    for index, (owner, raw_path) in enumerate(scopes):
        path = raw_path.removesuffix("/**").rstrip("/")
        for other_owner, other_raw_path in scopes[index + 1 :]:
            other = other_raw_path.removesuffix("/**").rstrip("/")
            overlaps = (
                path == other
                or path.startswith(f"{other}/")
                or other.startswith(f"{path}/")
            )
            assert not overlaps, (
                f"write-scope collision: {owner}:{raw_path} and "
                f"{other_owner}:{other_raw_path}"
            )


def _path_is_allowed(path: Path, allow_paths: list[str]) -> bool:
    value = path.as_posix()
    for raw_path in allow_paths:
        root = raw_path.removesuffix("/**").rstrip("/")
        if value == root or (raw_path.endswith("/**") and value.startswith(f"{root}/")):
            return True
    return False


def test_story_0684_slice_consolidation() -> None:
    integration_task = _load_json(Path(".codex/tasks/TASK-0684.json"))
    expected_dependencies = [slice_.story_id for slice_ in SLICES]
    assert integration_task["dependencies"] == expected_dependencies

    contract = _load_yaml(CONTRACT_PATH)
    assert contract["owner"] == "BC-001"
    assert contract["status"] == "FROZEN"
    assert contract["schema_version"] == contract["contract_version"] == "1.0.0"

    requirement_owners: dict[str, str] = {}
    test_owners: dict[str, str] = {}
    control_owners: dict[str, str] = {}
    output_owners: dict[str, str] = {}
    policy_ids: dict[str, str] = {}
    scopes: list[tuple[str, str]] = []

    for entry in contract["requirements"]:
        _claim(requirement_owners, entry["id"], contract["identity"]["story_id"], "requirement")
        _claim(test_owners, entry["test"], contract["identity"]["story_id"], "test")
        _claim(
            control_owners,
            entry["control"].rsplit("/", 1)[-1],
            contract["identity"]["story_id"],
            "control",
        )
    for control in contract["contract"]["example"], contract["contract"]["schema"]:
        assert (ROOT / control).is_file(), f"missing frozen contract output: {control}"

    for slice_ in SLICES:
        task = _load_json(Path(f".codex/tasks/{slice_.task_id}.json"))
        assert task["story_id"] == slice_.story_id
        _assert_merge_is_ancestor(slice_.merge_commit)

        for output in slice_.outputs:
            assert (ROOT / output).is_file(), f"missing {slice_.story_id} output: {output}"
            assert _path_is_allowed(output, task["allow_paths"]), (
                f"{slice_.story_id} output is outside its write scope: {output}"
            )
            _claim(output_owners, output.as_posix(), slice_.story_id, "output")

        policy = _load_json(DOCS_ROOT / slice_.package / "foundation-policy.json")
        assert policy["schema_version"] == "1.0.0"
        assert policy["owner"] == contract["owner"]
        _claim(policy_ids, policy["policy_id"], slice_.story_id, "policy id")

        requirement_evidence = policy["requirement_evidence"]
        assert set(requirement_evidence) == _task_requirements(task)
        assert set(requirement_evidence.values()) == set(task["tests"])
        for requirement, test_name in requirement_evidence.items():
            _claim(requirement_owners, requirement, slice_.story_id, "requirement")
            _claim(test_owners, test_name, slice_.story_id, "test")
        for control in policy["controls"]:
            _claim(control_owners, control, slice_.story_id, "control")
        scopes.extend((slice_.story_id, path) for path in task["allow_paths"])

    binding = _load_json(DOCS_ROOT / SLICES[0].package / "foundation-policy.json")[
        "contract_binding"
    ]
    assert binding == {
        "source": CONTRACT_PATH.as_posix(),
        "contract_version": contract["contract_version"],
        "status": contract["status"],
    }

    assert set(requirement_owners) == _epic_requirements()
    assert len(requirement_owners) == len(test_owners) == len(control_owners) == 53
    assert len(requirement_owners) - len(contract["requirements"]) == 48
    _assert_scopes_are_disjoint(scopes)
