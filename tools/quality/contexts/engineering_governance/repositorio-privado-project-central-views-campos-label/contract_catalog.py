from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


EXPECTED_VERSION = "1.0.0"
EXPECTED_OWNER = "BC-001"
CONTRACT_ROOT = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "repositorio-privado-project-central-views-campos-label"
)
OWNERSHIP_REL = Path("contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv")


@dataclass(frozen=True)
class ContractBundle:
    name: str
    directory: Path
    schema_name: str
    example_name: str
    contract_id: str
    identity: dict[str, str]

    @property
    def manifest(self) -> Path:
        return self.directory / "contract-manifest.yaml"

    @property
    def schema(self) -> Path:
        return self.directory / self.schema_name

    @property
    def example(self) -> Path:
        return self.directory / "examples" / self.example_name


BUNDLES = (
    ContractBundle(
        "foundation",
        CONTRACT_ROOT / "classicprofile-iss-native-parte-1",
        "foundation-conformance.schema.json",
        "foundation-conformance.json",
        "engineering-foundation-conformance",
        {
            "epic_id": "EPIC-002",
            "story_id": "STORY-0690",
            "issue_id": "ISSUE-0800",
            "task_id": "TASK-0690",
        },
    ),
    ContractBundle(
        "worker",
        CONTRACT_ROOT / "worker-parte-2",
        "worker-governance-conformance.schema.json",
        "worker-governance-conformance.json",
        "worker-governance-conformance",
        {
            "epic_id": "EPIC-002",
            "story_id": "STORY-0691",
            "issue_id": "ISSUE-0801",
            "task_id": "TASK-0691",
        },
    ),
    ContractBundle(
        "consolidation",
        CONTRACT_ROOT / "consolidacao",
        "slice-consolidation.schema.json",
        "slice-consolidation.json",
        "engineering-foundation-slice-consolidation",
        {
            "epic_id": "EPIC-002",
            "story_id": "STORY-0006",
            "issue_id": "ISSUE-0116",
            "task_id": "TASK-0006",
        },
    ),
)


def expected_artifacts() -> set[Path]:
    return {
        artifact
        for bundle in BUNDLES
        for artifact in (bundle.manifest, bundle.schema, bundle.example)
    }
