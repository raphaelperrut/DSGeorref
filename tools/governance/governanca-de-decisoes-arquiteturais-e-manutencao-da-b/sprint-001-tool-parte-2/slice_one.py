from __future__ import annotations

import sys
from pathlib import Path


SLICE_ONE_ROOT = (
    Path(__file__).resolve().parent.parent / "frz-gov-adr-gov-dec-parte-1"
)
if str(SLICE_ONE_ROOT) not in sys.path:
    sys.path.insert(0, str(SLICE_ONE_ROOT))

from canonical_json import canonical_json_bytes, load_json_bytes  # noqa: E402
from foundation_validation_types import Finding, require_valid  # noqa: E402
from governed_artifacts import (  # noqa: E402
    COMMIT_PATTERN,
    git_blob,
    resolve_governed_artifact,
    revision_first_parent,
    revision_is_ancestor,
    role_authorizes_path,
    task_authorizes_artifact,
)
from lifecycle_records import AppendOnlyRecordLedger  # noqa: E402
from lifecycle_evidence import (  # noqa: E402
    validate_closure as validate_foundation_closure,
    validate_evidence_set as validate_foundation_evidence_set,
)
from sprint_validation import derive_canonical_sprint_selection  # noqa: E402


__all__ = [
    "AppendOnlyRecordLedger",
    "COMMIT_PATTERN",
    "Finding",
    "canonical_json_bytes",
    "derive_canonical_sprint_selection",
    "git_blob",
    "load_json_bytes",
    "require_valid",
    "resolve_governed_artifact",
    "revision_first_parent",
    "revision_is_ancestor",
    "role_authorizes_path",
    "task_authorizes_artifact",
    "validate_foundation_closure",
    "validate_foundation_evidence_set",
]
