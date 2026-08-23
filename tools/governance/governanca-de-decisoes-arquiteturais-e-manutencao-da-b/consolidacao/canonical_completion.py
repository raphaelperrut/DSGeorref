from __future__ import annotations

import sys
from pathlib import Path


CANONICAL_TOOL_ROOT = Path(__file__).resolve().parent.parent / "sprint-001-tool-parte-2"
if str(CANONICAL_TOOL_ROOT) not in sys.path:
    sys.path.insert(0, str(CANONICAL_TOOL_ROOT))

from delivery_approval import DeliveryApprovalGate  # noqa: E402
from slice_one import Finding  # noqa: E402
from sprint_graph_evidence import completion_story_ids  # noqa: E402


def validate_governed_completion(
    repository_root: Path, references: object
) -> tuple[list[str], list[Finding]]:
    """Delegate completion authority to the existing governed contract."""
    return completion_story_ids(
        repository_root,
        references,
        delivery_gate=DeliveryApprovalGate(),
    )
