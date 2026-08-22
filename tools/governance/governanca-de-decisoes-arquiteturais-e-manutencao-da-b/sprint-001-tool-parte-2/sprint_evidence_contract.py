from __future__ import annotations


ZERO_DIGEST = "0" * 64
REQUIRED_DECISIONS = (3, 5, 6, 7, 8, 9, 10)
REQUIRED_REQUIREMENTS = tuple(
    sorted(
        {
            "REQ-SPRINT-001-003",
            "REQ-SPRINT-001-005",
            "REQ-SPRINT-001-006",
            "REQ-SPRINT-001-007",
            "REQ-SPRINT-001-008",
            "REQ-SPRINT-001-009",
            "REQ-SPRINT-001-010",
            "REQ-TOOL-001",
            "REQ-TOOL-002",
            "REQ-TOOL-010",
        }
    )
)
REQUIRED_TESTS = tuple(
    sorted(
        {
            "test_sprint_zero_baseline_decision_03",
            "test_sprint_zero_baseline_decision_05",
            "test_sprint_zero_baseline_decision_06",
            "test_sprint_zero_baseline_decision_07",
            "test_sprint_zero_baseline_decision_08",
            "test_sprint_zero_baseline_decision_09",
            "test_sprint_zero_baseline_decision_10",
            "test_python_312_primary_and_upgrade_gates",
            "test_uv_lock_frozen",
            "test_make_ci_parity",
        }
    )
)
REQUIRED_EVIDENCE_KINDS = tuple(
    sorted(
        {
            "AP008_DECISION_03_WAVE",
            "AP008_DECISION_05_CONTRACTS",
            "AP008_DECISION_06_DIAGNOSTIC",
            "AP008_DECISION_07_CI",
            "AP008_DECISION_08_EVIDENCE_SET",
            "AP008_DECISION_09_CLOSURE_EXTENSION",
            "AP008_DECISION_10_CUTOVER",
            "REQ_TOOL_MAKE_CI_PARITY",
            "REQ_TOOL_PYTHON_RUNTIME",
            "REQ_TOOL_UV_LOCK_FROZEN",
        }
    )
)
EVIDENCE_FIELDS = frozenset(
    {
        "schema_version",
        "record_type",
        "evidence_set_id",
        "sprint_id",
        "source_revision",
        "artifacts",
        "requirements",
        "tests",
        "decisions",
        "digest_algorithm",
        "evidence_set_digest",
    }
)
ARTIFACT_FIELDS = frozenset({"kind", "source_revision", "path", "sha256"})
TEST_FIELDS = frozenset({"test_id", "result", "artifact"})
VALIDATION_EVIDENCE_FIELDS = frozenset(
    {
        "record_type",
        "evidence_type",
        "subject",
        "validator",
        "finding_codes",
        "execution_report",
        "execution_authority",
        "authority_role",
        "task_id",
        "issue_id",
        "story_id",
        "reviewed_candidate_commit",
    }
)
TEST_EVIDENCE_FIELDS = frozenset(
    {
        "record_type",
        "test_id",
        "report",
        "execution_authority",
        "authority_role",
        "task_id",
        "issue_id",
        "story_id",
        "reviewed_candidate_commit",
    }
)
EVIDENCE_VALIDATOR_PATHS = {
    "AP008_DECISION_03_WAVE": "sprint_graph.py",
    "AP008_DECISION_05_CONTRACTS": "sprint_decisions.py",
    "AP008_DECISION_06_DIAGNOSTIC": "sprint_decisions.py",
    "AP008_DECISION_07_CI": "sprint_decisions.py",
    "AP008_DECISION_08_EVIDENCE_SET": "sprint_evidence.py",
    "AP008_DECISION_09_CLOSURE_EXTENSION": "sprint_decisions.py",
    "AP008_DECISION_10_CUTOVER": "sprint_decisions.py",
    "REQ_TOOL_MAKE_CI_PARITY": "toolchain_validation.py",
    "REQ_TOOL_PYTHON_RUNTIME": "toolchain_validation.py",
    "REQ_TOOL_UV_LOCK_FROZEN": "toolchain_validation.py",
}
