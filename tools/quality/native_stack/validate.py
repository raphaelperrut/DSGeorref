from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
ACTION_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s@]+)@([^\s#]+)", re.MULTILINE)


def _sha256(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"{path} must contain a YAML object")
    return value


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def _contains_value(value: Any, expected: str) -> bool:
    if value == expected:
        return True
    if isinstance(value, dict):
        return any(_contains_value(item, expected) for item in value.values())
    if isinstance(value, list):
        return any(_contains_value(item, expected) for item in value)
    return False


def _validate_contract(source_lock: dict[str, Any], contract: Path, review_dir: Path) -> None:
    policy_digest = _sha256(contract)
    policy = _load_yaml(contract)
    _require(policy.get("contract_version") == "1.0.2", "unexpected supply-chain contract version")
    _require(
        policy.get("signing", {}).get("trust_scope") == "DSGEOREF-NATIVE-RUNTIME-SUPPLY-CHAIN-V1",
        "unexpected supply-chain trust scope",
    )
    for filename, role in (
        ("architect-contract-review.json", "Architect/BC-015"),
        ("security-contract-review.json", "Security"),
    ):
        review = json.loads((review_dir / filename).read_text(encoding="utf-8"))
        _require(review.get("review_role") == role, f"unexpected review role in {filename}")
        _require(review.get("decision") == "APPROVE", f"{role} did not approve the contract")
        _require(
            f"sha256:{review.get('policy_sha256')}" == policy_digest,
            f"{role} reviewed a different policy digest",
        )
    _require(
        source_lock["immutable_inputs"]["target_platform"] == "linux/amd64", "wrong target platform"
    )


def _validate_conda_lock(source_lock: dict[str, Any], repository_root: Path) -> None:
    conda = source_lock["immutable_inputs"]["conda_environment"]
    lock_path = repository_root / conda["lock_file"]
    _require(_sha256(lock_path) == conda["lock_sha256"], "conda lock digest mismatch")
    lines = [
        line
        for line in lock_path.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#")
    ]
    _require(lines[0] == "@EXPLICIT", "conda lock must use explicit format")
    artifacts = lines[1:]
    _require(len(artifacts) == conda["artifact_count"], "conda artifact count mismatch")
    _require(len(set(artifacts)) == len(artifacts), "conda lock contains duplicate artifacts")
    for artifact in artifacts:
        url, separator, digest = artifact.partition("#")
        _require(
            separator == "#" and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
            "invalid conda artifact hash",
        )
        _require(
            url.startswith("https://conda.anaconda.org/conda-forge/linux-64/")
            or url.startswith("https://conda.anaconda.org/conda-forge/noarch/"),
            f"unapproved conda artifact URL: {url}",
        )
    expected_packages = {
        "python": source_lock["runtime"]["python"],
        "gdal": source_lock["native_stack"]["gdal"],
        "proj": source_lock["native_stack"]["proj"],
        "geos": source_lock["native_stack"]["geos"],
        "rasterio": source_lock["native_stack"]["rasterio"],
        "shapely": source_lock["native_stack"]["shapely"],
        "pydantic": source_lock["python_stack"]["pydantic"],
        "celery": source_lock["python_stack"]["celery"],
        "proj-data": conda["proj_data_version"],
        conda.get("smoke_driver_package", "psycopg"): source_lock["immutable_inputs"][
            "abi_smoke_service"
        ]["client_driver"]["version"],
    }
    filenames = [artifact.rsplit("/", 1)[-1].split("#", 1)[0] for artifact in artifacts]
    for package, version in expected_packages.items():
        prefix = f"{package}-{version}-"
        _require(
            sum(filename.startswith(prefix) for filename in filenames) == 1,
            f"expected one {package} {version} artifact",
        )


def _validate_source_lock(
    source_lock: dict[str, Any], source_lock_path: Path, repository_root: Path
) -> None:
    expected_versions = {
        ("runtime", "python"): "3.12.13",
        ("native_stack", "gdal"): "3.13.2",
        ("native_stack", "proj"): "9.8.1",
        ("native_stack", "geos"): "3.14.1",
        ("native_stack", "rasterio"): "1.5.0",
        ("native_stack", "shapely"): "2.1.2",
        ("native_stack", "postgresql"): "18.4",
        ("native_stack", "postgis"): "3.6.4",
        ("python_stack", "fastapi"): "0.140.2",
        ("python_stack", "pydantic"): "2.13.4",
        ("python_stack", "celery"): "5.6.3",
    }
    for (section, name), expected in expected_versions.items():
        _require(str(source_lock[section][name]) == expected, f"locked {name} version changed")
    immutable = source_lock["immutable_inputs"]
    _require(
        SHA256_RE.fullmatch(immutable["previous_source_lock_digest"]) is not None,
        "invalid source-lock lineage",
    )
    for image_key in ("base_image", "abi_smoke_service"):
        reference = immutable[image_key]["reference"]
        _require(
            re.search(r"@sha256:[0-9a-f]{64}$", reference) is not None,
            f"{image_key} is not digest pinned",
        )
    fastapi = immutable["pypi_artifacts"]["fastapi"]
    _require(
        str(fastapi["version"]) == str(source_lock["python_stack"]["fastapi"]),
        "FastAPI wheel version mismatch",
    )
    _require(SHA256_RE.fullmatch(fastapi["sha256"]) is not None, "FastAPI wheel lacks SHA-256")
    for action in immutable["workflow_actions"].values():
        _require(
            re.fullmatch(r"[^@]+@[0-9a-f]{40}", action) is not None,
            f"action is not commit pinned: {action}",
        )
    for name, tool in immutable["supply_chain_tools"].items():
        _require(tool.get("version") is not None, f"{name} version missing")
        _require(
            SHA256_RE.fullmatch(tool["linux_amd64_sha256"]) is not None, f"{name} checksum missing"
        )
    _validate_conda_lock(source_lock, repository_root)
    _require(
        _sha256(source_lock_path)
        == "sha256:16970dbaba6b1a5494a2003626a53bf0d6d9cfc5ed64471804bc888551d49a9e",
        "unexpected source-lock digest",
    )


def _validate_dockerfile(source_lock: dict[str, Any], dockerfile: Path) -> None:
    text = dockerfile.read_text(encoding="utf-8")
    immutable = source_lock["immutable_inputs"]
    _require(
        f"FROM {immutable['base_image']['reference']}" in text,
        "Dockerfile base differs from source lock",
    )
    wheel = immutable["pypi_artifacts"]["fastapi"]
    _require(wheel["url"] in text, "Dockerfile FastAPI URL differs from source lock")
    _require(
        wheel["sha256"].removeprefix("sha256:") in text,
        "Dockerfile FastAPI checksum differs from source lock",
    )
    _require("native-stack.conda-lock.txt" in text, "Dockerfile does not consume conda lock")
    _require(
        "pip install --no-deps" in text, "FastAPI install must not resolve floating dependencies"
    )


def _validate_workflow(source_lock: dict[str, Any], workflow: Path) -> None:
    text = workflow.read_text(encoding="utf-8")
    _require("pull_request_target" not in text, "pull_request_target is prohibited")
    _require("contents: read" in text, "global contents: read permission missing")
    _require(text.count("packages: write") == 1, "packages: write must exist only in publisher job")
    _require(text.count("id-token: write") == 1, "id-token: write must exist only in publisher job")
    _require(
        "refs/heads/codex/issue-973-native-runtime" in text,
        "authorized remediation ref guard missing",
    )
    _require("native-runtime-release" in text, "protected environment missing")
    _require(
        "github.repository == 'raphaelperrut/DSGeorref'" in text,
        "publisher repository guard missing",
    )
    action_values = set(source_lock["immutable_inputs"]["workflow_actions"].values())
    found_actions = {f"{name}@{revision}" for name, revision in ACTION_RE.findall(text)}
    _require(
        found_actions <= action_values,
        f"workflow contains unapproved actions: {sorted(found_actions - action_values)}",
    )
    _require(found_actions == action_values, "workflow does not use every source-locked action")
    for _, revision in ACTION_RE.findall(text):
        _require(
            re.fullmatch(r"[0-9a-f]{40}", revision) is not None,
            "workflow action is not commit pinned",
        )


def _validate_resolved_evidence(
    resolved: dict[str, Any], evidence_dir: Path, source_lock_digest: str
) -> None:
    summary = _load_json(evidence_dir / "publication-summary.json")
    abi = _load_json(evidence_dir / "abi-smoke.json")
    linkage = _load_json(evidence_dir / "linkage.json")
    provenance = _load_json(evidence_dir / "provenance.intoto.json")
    referrers = _load_json(evidence_dir / "image-referrers.json")
    revocations = _load_json(evidence_dir / "revocation-referrers.json")
    public_access = _load_json(evidence_dir / "registry-public-access.json")
    publication = _load_json(evidence_dir / "github-actions-publication.json")

    _require(summary.get("result") == "PASS", "publication summary is not PASS")
    _require(summary.get("source_lock_digest") == source_lock_digest, "wrong source-lock binding")
    resolved_to_summary = {
        "build_commit_sha": "build_commit_sha",
        "image_digest": "image_digest",
        "sbom_digest": "sbom_digest",
        "provenance_digest": "provenance_digest",
        "signature_reference": "signature_reference",
        "signature_bundle_digest": "signature_bundle_digest",
        "abi_smoke_evidence_digest": "abi_smoke_evidence_digest",
        "linkage_digest": "linkage_digest",
        "workflow_run_id": "workflow_run_id",
        "trust_scope": "trust_scope",
        "publisher_identity": "publisher_identity",
        "oidc_issuer": "oidc_issuer",
        "package": "package",
        "environment": "environment",
        "platform": "platform",
    }
    for resolved_field, summary_field in resolved_to_summary.items():
        _require(
            str(resolved.get(resolved_field)) == str(summary.get(summary_field)),
            f"resolved {resolved_field} diverges from publication evidence",
        )

    image_digest = resolved["image_digest"]
    _require(abi.get("result") == "PASS", "ABI smoke evidence is not PASS")
    _require(abi.get("candidate_image_digest") == image_digest, "ABI smoke image mismatch")
    _require(abi.get("source_lock_digest") == source_lock_digest, "ABI source-lock mismatch")
    _require(
        abi.get("components_verified") == resolved.get("abi_components_verified"),
        "ABI component list mismatch",
    )
    _require(
        _sha256(evidence_dir / "abi-smoke.json") == resolved["abi_smoke_evidence_digest"],
        "ABI evidence digest mismatch",
    )

    subjects = provenance.get("subject", [])
    _require(len(subjects) == 1, "provenance must have exactly one subject")
    _require(
        subjects[0].get("digest", {}).get("sha256") == image_digest.removeprefix("sha256:"),
        "provenance subject does not bind the image",
    )
    _require(
        provenance.get("predicateType") == "https://slsa.dev/provenance/v1",
        "provenance is not SLSA v1",
    )
    _require(linkage.get("sourceLockDigest") == source_lock_digest, "linkage source-lock mismatch")
    for field, key in (
        ("image_digest", "imageDigest"),
        ("sbom_digest", "sbomDigest"),
        ("provenance_digest", "provenanceDigest"),
        ("signature_reference", "signatureReference"),
        ("signature_bundle_digest", "signatureBundleDigest"),
        ("abi_smoke_evidence_digest", "abiSmokeEvidenceDigest"),
        ("build_commit_sha", "buildCommitSha"),
        ("trust_scope", "trustScope"),
    ):
        _require(linkage.get(key) == resolved.get(field), f"linkage {key} mismatch")

    for artifact, expected_type, field in (
        ("sbom", "application/spdx+json", "sbom_digest"),
        ("provenance", "application/vnd.in-toto+json", "provenance_digest"),
        (
            "linkage",
            "application/vnd.dsgeorref.native-runtime-linkage.v1+json",
            "linkage_digest",
        ),
    ):
        attached = _load_json(evidence_dir / f"{artifact}-attach.json")
        _require(
            attached.get("digest") == resolved[field],
            f"{artifact} attachment digest mismatch",
        )
        _require(attached.get("artifactType") == expected_type, f"{artifact} media type mismatch")
        _require(_contains_value(referrers, resolved[field]), f"{artifact} referrer is absent")

    for artifact, field in (
        ("image", "image_digest"),
        ("sbom", "sbom_digest"),
        ("provenance", "provenance_digest"),
        ("linkage", "linkage_digest"),
    ):
        verification = json.loads(
            (evidence_dir / f"{artifact}-signature-verification.json").read_text(encoding="utf-8")
        )
        _require(isinstance(verification, list) and verification, f"{artifact} signature absent")
        _require(
            _contains_value(verification, resolved[field]),
            f"{artifact} signature verifies a different digest",
        )

    _require(
        _sha256(evidence_dir / "image-signature.bundle.json")
        == resolved["signature_bundle_digest"],
        "signature bundle digest mismatch",
    )
    bundle = _load_json(evidence_dir / "image-signature.bundle.json")
    _require(
        _contains_value(bundle, resolved["transparency_log_reference"].split(":", 1)[1]),
        "transparency log index is absent from signature bundle",
    )
    _require(not revocations.get("referrers"), "a matching revocation referrer exists")
    _require(public_access.get("result") == "PASS", "public package check is not PASS")
    _require(public_access.get("anonymous_pull") is True, "package is not anonymously pullable")
    _require(
        public_access.get("docker_content_digest") == image_digest,
        "anonymous pull resolved a different digest",
    )
    _require(publication.get("result") == "PASS", "hosted publication is not PASS")
    _require(publication.get("deployment_status") == "success", "deployment is not successful")
    _require(
        publication.get("head_sha") == resolved["build_commit_sha"],
        "deployment build SHA mismatch",
    )


def _validate_resolved_lock(
    resolved: dict[str, Any], require_resolved: bool, evidence_dir: Path, source_lock_digest: str
) -> None:
    if resolved.get("status") == "NOT_BUILT":
        _require(not require_resolved, "resolved lock has not been promoted")
        forbidden = {"image_digest", "sbom_digest", "provenance_digest", "signature_reference"}
        _require(
            not (forbidden & resolved.keys()), "unbuilt resolved lock contains artifact values"
        )
        return
    _require(resolved.get("status") == "VERIFIED", "unknown resolved-lock status")
    for field in (
        "source_lock_digest",
        "image_digest",
        "sbom_digest",
        "provenance_digest",
        "signature_bundle_digest",
        "abi_smoke_evidence_digest",
    ):
        _require(
            SHA256_RE.fullmatch(resolved.get(field, "")) is not None, f"invalid resolved {field}"
        )
    _require(resolved.get("signature_verification") == "PASS", "signature verification is not PASS")
    _require(resolved.get("abi_smoke_result") == "PASS", "ABI smoke is not PASS")
    _require(resolved.get("artifact_linkage_verified") is True, "artifact linkage is not verified")
    _require(
        resolved.get("source_lock_digest") == source_lock_digest,
        "resolved source lock mismatch",
    )
    _require(resolved.get("package_visibility") == "public", "package is not recorded as public")
    _require(
        resolved.get("revocation_status") == "NO_MATCHING_REVOCATION_REFERRER",
        "revocation status is not clear",
    )
    _validate_resolved_evidence(resolved, evidence_dir, source_lock_digest)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Issue #973 native-stack inputs and promotion state"
    )
    parser.add_argument("--source-lock", type=Path, required=True)
    parser.add_argument("--resolved-lock", type=Path, required=True)
    parser.add_argument(
        "--dockerfile", type=Path, default=Path("infra/images/native-stack.Dockerfile")
    )
    parser.add_argument(
        "--workflow", type=Path, default=Path(".github/workflows/native-stack.yaml")
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path(
            "contracts/contexts/release_installation/native-stack-supply-chain/policy.yaml"
        ),
    )
    parser.add_argument(
        "--contract-review-dir", type=Path, default=Path("evidence/implementation/issue-0973")
    )
    parser.add_argument(
        "--evidence-dir", type=Path, default=Path("evidence/implementation/issue-0973")
    )
    parser.add_argument("--require-resolved", action="store_true")
    args = parser.parse_args()
    repository_root = Path.cwd()
    source_lock = _load_yaml(args.source_lock)
    _validate_source_lock(source_lock, args.source_lock, repository_root)
    _validate_contract(source_lock, args.contract, args.contract_review_dir)
    _validate_dockerfile(source_lock, args.dockerfile)
    _validate_workflow(source_lock, args.workflow)
    _validate_resolved_lock(
        _load_yaml(args.resolved_lock),
        args.require_resolved,
        args.evidence_dir,
        _sha256(args.source_lock),
    )
    print(
        json.dumps(
            {"result": "PASS", "source_lock_digest": _sha256(args.source_lock)}, sort_keys=True
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
