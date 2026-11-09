"""Compatible entry point for frozen scope and authenticated composition."""

from __future__ import annotations

from pathlib import Path

from foundation_validation_types import Finding
from scope_authority import validate_legacy_scope
from scope_composition import validate_composed_scope
from scope_integration import GitHubIntegrationAuthority, IntegrationProof


def validate_effective_task_scope(
    repository_root: Path,
    *,
    base_revision: str,
    authority_checkpoint: str,
    candidate_revision: str,
    task_envelope_path: str,
    integration_revision: str | None = None,
    integration_proofs: tuple[IntegrationProof, ...] = (),
    integration_authority: GitHubIntegrationAuthority | None = None,
) -> list[Finding]:
    if integration_revision is None:
        if integration_proofs or integration_authority is not None:
            return [Finding("COMPOSITION_INVALID", "$", "integration revision is required")]
        return validate_legacy_scope(
            repository_root,
            base_revision=base_revision,
            authority_checkpoint=authority_checkpoint,
            candidate_revision=candidate_revision,
            task_envelope_path=task_envelope_path,
        )
    return validate_composed_scope(
        repository_root,
        base_revision=base_revision,
        authority_checkpoint=authority_checkpoint,
        candidate_revision=candidate_revision,
        task_envelope_path=task_envelope_path,
        integration_revision=integration_revision,
        integration_proofs=integration_proofs,
        integration_authority=integration_authority,
    )
