# ISSUE-0678 integration evidence

The integration consumes the read-only, fail-closed ISSUE-0677 validator report for
the exact candidate SHA. That report already validates the ISSUE-0676 executable
foundation. The integration does not import or duplicate either dependency's domain
rules and does not assert authorization for the first functional slice.

Acceptance evidence:

- `AC-ISSUE-0678-01`: `test_epic_092_integracao` proves the versioned registry,
  checkpoint, and observable integration report.
- `AC-ISSUE-0678-02`: `test_epic_092_integracao` proves the linked requirement
  evidence is preserved from the validated dependency report.
- `AC-ISSUE-0678-03`: `test_epic_092_integracao` covers missing candidate SHA,
  malformed or failed dependency reports, and drifted control artifacts.
- `AC-ISSUE-0678-04`: `test_epic_092_integracao` proves a read-only subprocess
  boundary and unchanged repository snapshots across repeated executions.

Focused validation command:

`python -X utf8 -m pytest -q -p no:cacheprovider tests/fnd/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/test_integration.py::test_epic_092_integracao`

Migration is not applicable. Rollback is a revert of the integration commit.
