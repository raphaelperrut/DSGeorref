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
    "del-ism-sprint-001-parte-1/foundation-policy.json"
)
EVIDENCE_PATH = (
    "evidence/implementation/walking-skeleton-frontendapipostgresqlrabbitmq-cel/"
    "del-ism-sprint-001-parte-1/sprint-evidence-set.json"
)
EXPECTED_CAPABILITY_SCOPE = [
    "Makefile",
    "tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "del-ism-sprint-001-parte-1/**",
    "docs/03-engineering/contexts/engineering_governance/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "del-ism-sprint-001-parte-1/**",
    "tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_implementation.py",
    "evidence/implementation/walking-skeleton-frontendapipostgresqlrabbitmq-cel/"
    "del-ism-sprint-001-parte-1/**",
]
EXPECTED_REQUIREMENTS = [
    "REQ-DEL-001",
    "REQ-DEL-002",
    "REQ-ISM-003",
    "REQ-SPRINT-001-001",
    "REQ-SPRINT-001-002",
    "REQ-SPRINT-001-003",
    "REQ-SPRINT-001-005",
    "REQ-SPRINT-001-006",
    "REQ-SPRINT-001-007",
    "REQ-SPRINT-001-008",
]
EXPECTED_FAILURE_POLICY = {
    "mode": "FAIL_CLOSED",
    "silent_fallback": False,
    "publication_on_error": "PROHIBITED",
}
CENTRAL_TEST_PATH = (
    "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_materialization.py"
)
LOCAL_TEST_PATH = (
    "tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_implementation.py"
)
EXPECTED_TEST_TARGETS = {
    "REQ-DEL-001": (
        "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation.py",
        "test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done",
    ),
    "REQ-DEL-002": (
        LOCAL_TEST_PATH,
        "test_private_operational_baseline_scope_cpu_only_clean_install",
    ),
    "REQ-ISM-003": (LOCAL_TEST_PATH, "test_thin_vertical_integrable_slices_and_pr_sequence"),
    **{
        f"REQ-SPRINT-001-{number}": (
            CENTRAL_TEST_PATH,
            f"test_sprint_zero_baseline_decision_{number[-2:]}",
        )
        for number in ("001", "002", "003", "005", "006", "007", "008")
    },
}
ROOT_FIELDS = {
    "schema_version",
    "foundation_id",
    "owner",
    "status",
    "slice",
    "contract",
    "private_baseline",
    "diagnostic_job",
    "ci_gate",
    "failure_policy",
    "requirement_evidence",
    "write_scope",
    "evidence_set",
}
TASK_PATH_PATTERN = re.compile(r"\.codex/tasks/TASK-[0-9]{4}\.json\Z")
