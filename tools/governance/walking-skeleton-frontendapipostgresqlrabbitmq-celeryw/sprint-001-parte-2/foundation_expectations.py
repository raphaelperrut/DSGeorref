from __future__ import annotations

import re

CONTRACT_PATH = (
    "contracts/contexts/engineering_governance/fnd/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "examples/walking-skeleton.json"
)
POLICY_PATH = (
    "docs/03-engineering/contexts/engineering_governance/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "sprint-001-parte-2/foundation-policy.json"
)
EVIDENCE_PATH = (
    "evidence/implementation/walking-skeleton-frontendapipostgresqlrabbitmq-cel/"
    "sprint-001-parte-2/implementation-evidence.json"
)
LOCAL_TEST_PATH = (
    "tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_completion.py"
)
CENTRAL_TEST_PATH = (
    "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_materialization.py"
)
EXPECTED_REQUIREMENTS = ["REQ-SPRINT-001-009", "REQ-SPRINT-001-010"]
EXPECTED_TEST_TARGETS = {
    requirement: (CENTRAL_TEST_PATH, f"test_sprint_zero_baseline_decision_{number}")
    for requirement, number in zip(EXPECTED_REQUIREMENTS, ("09", "10"), strict=True)
}
EXPECTED_CAPABILITY_SCOPE = [
    ".codex/tasks/TASK-0753.json",
    "Makefile",
    "tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/sprint-001-parte-2/**",
    "docs/03-engineering/contexts/engineering_governance/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/sprint-001-parte-2/**",
    LOCAL_TEST_PATH,
    "evidence/implementation/walking-skeleton-frontendapipostgresqlrabbitmq-cel/"
    "sprint-001-parte-2/**",
]
EXPECTED_CLOSURE_POLICY = {
    "basis": "EVIDENCE",
    "calendar_fallback": False,
    "evidence_history": "REPOSITORY_BOUND_IMMUTABLE",
    "extension_basis": "DIRECT_BLOCKER_EVIDENCE",
    "extension_graph_revision_binding": True,
    "extension_authorization_role": "Product Owner",
}
EXPECTED_CUTOVER_POLICY = {
    "mode": "EXPLICIT",
    "foundation_gate": "G1_APPROVED_REQUIRED",
    "first_slice_authorization": "REQUIRED",
    "reviewed_candidate_lineage": "ANCESTOR_REQUIRED",
    "missing_proof": "DENY",
}
EXPECTED_FAILURE_POLICY = {
    "mode": "FAIL_CLOSED",
    "silent_fallback": False,
    "publication_on_error": "PROHIBITED",
}
ROOT_FIELDS = {
    "schema_version",
    "foundation_id",
    "owner",
    "status",
    "slice",
    "contract",
    "sprint_closure",
    "first_slice_cutover",
    "failure_policy",
    "requirement_evidence",
    "write_scope",
    "evidence_set",
}
TASK_PATH_PATTERN = re.compile(r"\.codex/tasks/TASK-[0-9]{4}\.json\Z")
TICKET_PATTERN = re.compile(r"\b(?:ISSUE|STORY|EPIC)-[0-9]{4}\b")
