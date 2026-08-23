# Engineering-governance repository integration

`STORY-0004` integrates the already governed `EPIC-001` slices into the
repository validation flow. It does not define a second contract, persistence
authority, decision model, or approval authority.

The read-only entry point is
`tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/repository_integration.py`.
It derives the integration state from `TASK-0004`, the canonical story graph,
the story traceability, the existing dependency surfaces, and the dedicated
GitHub Actions workflow.

Validation fails closed when:

- the TaskEnvelope identity, exact allow/deny scope, AC IDs, dependencies, or
  mandatory test drift;
- story traceability or graph dependencies are missing;
- the workflow stops invoking the integration entry point or canonical test;
- a required consolidated/automation surface is absent;
- the owned Python capability contains an exact duplicated implementation,
  ambiguous module name, syntax error, or import cycle.

Findings are sorted and deterministic. The validator is read-only and does not
create evidence, approve the candidate, mutate GitHub, or replace independent QA
and Review. Rollback is a revert of the candidate commit.
