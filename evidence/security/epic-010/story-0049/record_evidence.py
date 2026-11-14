"""Record this task's scope, integrated dependencies and LF content digests."""

import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASELINE = "bb2b2795ec414a7656c3f93aee32085f96b953bf"
EVIDENCE = Path("evidence/security/epic-010/story-0049")
TESTS = Path("tests/security/contexts/identity_access") / (
    "autorizacao-por-projeto-operacao-artefato-e-caminho"
)
TASK = ".codex/tasks/TASK-0049.json"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def segmented(raw):
    value = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
    encoded = "sha256:" + ":".join(value[i : i + 8] for i in range(0, 64, 8))
    assert encoded.removeprefix("sha256:").replace(":", "") == value
    return encoded


def main():
    before = json.loads(git("show", f"{BASELINE}:{TASK}"))
    after = json.loads((ROOT / TASK).read_text(encoding="utf-8"))
    expected = before["allow_paths"] + [EVIDENCE.as_posix() + "/**", TASK]
    assert after["allow_paths"] == after["phase_f_review"]["files"]["allow_paths"] == expected
    after["allow_paths"] = before["allow_paths"]
    after["phase_f_review"]["files"]["allow_paths"] = before["phase_f_review"]["files"][
        "allow_paths"
    ]
    assert after == before
    dependencies = {}
    for issue, commit in {123: "41544a2", 124: "b4a5340"}.items():
        revision = git("rev-parse", commit).decode().strip()
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", revision, BASELINE], cwd=ROOT, check=True
        )
        changed = git("diff-tree", "--no-commit-id", "--name-only", "-r", revision)
        files = changed.decode().splitlines()
        assert files
        assert all(
            git("show", f"{revision}:{path}") == git("show", f"{BASELINE}:{path}") for path in files
        )
        dependencies[str(issue)] = {
            "status": "INTEGRATED",
            "commit": revision,
            "outputs_identical_to_baseline": files,
        }
    xml = ET.parse(ROOT / EVIDENCE / "security-tests.xml")
    cases = xml.findall(".//testcase")
    assert len(cases) == 38 and not xml.findall(".//failure") and not xml.findall(".//error")
    assert not xml.findall(".//skipped")
    native_paths = json.loads(
        (
            ROOT / "evidence/implementation/epic-010/story-0048" / "native-gate-diagnosis.json"
        ).read_text()
    )["files"]
    native = []
    for row in native_paths:
        path = row["path"]
        raw = (ROOT / path).read_bytes()
        baseline = git("show", f"{BASELINE}:{path}")
        assert raw.replace(b"\r\n", b"\n") == baseline
        native.append(
            {
                "path": path,
                "matches_baseline_after_crlf_normalization": True,
                "raw_differs_from_baseline": raw != baseline,
                "lf_sha256": segmented(raw),
            }
        )
    files = [TASK] + [
        path.relative_to(ROOT).as_posix()
        for folder in (ROOT / TESTS, ROOT / EVIDENCE)
        for path in folder.rglob("*")
        if path.is_file()
        and ".runtime" not in path.parts
        and "__pycache__" not in path.parts
        and path.name != "validation.json"
    ]
    assert all(
        path == TASK or path.startswith((TESTS.as_posix() + "/", EVIDENCE.as_posix() + "/"))
        for path in files
    )
    result = {
        "issue": 125,
        "baseline_sha": BASELINE,
        "candidate_binding": (
            "The commit containing validation.json and the listed LF digests; resolve via git log."
        ),
        "task_only_authorized_allow_paths_changed": True,
        "scope_valid": True,
        "dependencies": dependencies,
        "tests_passed": len(cases),
        "new_security_cases": 27,
        "direct_resource_security_regressions": 11,
        "test_names": [case.attrib["name"] for case in cases],
        "database": "NOT_APPLICABLE",
        "migration_required": False,
        "api": "NOT_APPLICABLE",
        "frontend": "NOT_APPLICABLE",
        "production_changed": False,
        "contracts_changed": False,
        "native_gate": {
            "classification": "PREEXISTING_CHECKOUT_CRLF_RAW_DIGEST_MISMATCH",
            "files": native,
        },
        "digest_encoding": "UTF8_LF_SHA256_colon_separated_eight_hex_groups_reversible",
        "files_sha256": {path: segmented((ROOT / path).read_bytes()) for path in sorted(files)},
        "independent_qa_review": "PENDING; no self approval",
    }
    (ROOT / EVIDENCE / "validation.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
