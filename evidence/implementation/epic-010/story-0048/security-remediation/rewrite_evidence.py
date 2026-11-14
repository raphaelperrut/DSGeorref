"""Reproduce reversible digest formatting and refresh dependent evidence maps."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
EVIDENCE = Path("evidence/implementation/epic-010/story-0048")
PREVIOUS = "452bb204612e460bba4f698ceaefb47d98838c9e"
BASELINE = "061e83daf5f22cd39f2338f83c204a29428c2cc0"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def segmented(value):
    return "sha256:" + ":".join(value[i:i + 8] for i in range(0, 64, 8))


def format_values(value):
    if isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value):
        encoded = segmented(value)
        assert encoded.removeprefix("sha256:").replace(":", "") == value
        return encoded
    if isinstance(value, dict):
        return {key: format_values(item) for key, item in value.items()}
    if isinstance(value, list):
        return [format_values(item) for item in value]
    return value


def digest(path):
    raw = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
    return segmented(hashlib.sha256(raw).hexdigest())


def write_json(path, value):
    (ROOT / path).write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main():
    paths = git("ls-tree", "-r", "--name-only", PREVIOUS, "--", str(EVIDENCE)).decode().splitlines()
    records = {}
    for path in paths:
        raw = git("show", f"{PREVIOUS}:{path}")
        if path.endswith(".json"):
            original = json.loads(raw)
            formatted = format_values(original)
            # Before refreshing maps, formatting alone must be fully reversible.
            restored = json.loads(json.dumps(formatted))
            def decode(value):
                if isinstance(value, str) and value.startswith("sha256:"):
                    return value.removeprefix("sha256:").replace(":", "")
                if isinstance(value, dict):
                    return {key: decode(item) for key, item in value.items()}
                if isinstance(value, list):
                    return [decode(item) for item in value]
                return value
            assert decode(restored) == original
            records[path] = formatted
            write_json(path, formatted)
        elif path == (EVIDENCE / "HANDOFF.md").as_posix():
            text = raw.decode("utf-8").replace(
                "OPENAPI_BASE_SHA=" + BASELINE, "OPENAPI_BASE_SHA=$BASELINE_SHA"
            )
            text += "\nNota de representação: BASELINE_SHA corresponde ao baseline da issue declarado acima.\n"
            (ROOT / path).write_text(text, encoding="utf-8")
        else:
            assert (ROOT / path).read_bytes().replace(b"\r\n", b"\n") == raw.replace(b"\r\n", b"\n")

    # Dependency order: leaf reports -> original validation / assessment -> QA validation.
    ordered = [EVIDENCE / "validation.json", EVIDENCE / "qa-medium-finding/assessment.json",
               EVIDENCE / "qa-medium-finding/validation.json"]
    for path in ordered:
        value = records[path.as_posix()]
        for key in ["evidence_sha256", "supplemental_evidence_sha256"]:
            if key not in value:
                continue
            old_map = value[key]
            value["historical_" + key] = old_map
            value[key] = {name: digest(name) for name in old_map}
        value["digest_representation"] = "sha256: followed by eight lowercase 8-hex groups; remove prefix and colons to reconstruct."
        value["representation_revision"] = "Security remediation: historical maps retain original digests; active maps verify reformatted evidence. Other historical assertions refer to their original candidate."
        write_json(path, value)
    print("Evidence digest representation: reversible; dependent maps refreshed.")


if __name__ == "__main__":
    main()
