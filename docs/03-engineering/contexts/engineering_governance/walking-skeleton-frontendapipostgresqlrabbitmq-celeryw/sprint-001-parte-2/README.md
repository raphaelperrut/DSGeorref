# Foundation completion policy

This slice binds the executable walking-skeleton foundation to the canonical
SPRINT-001 closure and first-slice cutover checkpoints. Sprint closure is based
only on repository-bound evidence; an extension requires evidence of a direct
blocker in the bound dependency graph. First-slice cutover requires both an
approved G1 Foundation Gate and explicit authorization, with candidate lineage
preserved.

Run the focused sentinel:

```text
python -X utf8 tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/sprint-001-parte-2/foundation_validation.py --policy docs/03-engineering/contexts/engineering_governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/sprint-001-parte-2/foundation-policy.json --repository-root .
python -X utf8 -m pytest -q -p no:cacheprovider tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_completion.py tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_materialization.py::test_sprint_zero_baseline_decision_09 tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_materialization.py::test_sprint_zero_baseline_decision_10
```

## Contract impact

No frozen contract was changed. The policy binds version `1.0.0` of the
published walking-skeleton example by canonical JSON SHA-256. No API, event,
database state, migration, frontend, worker, or product runtime changed.

## Risks and limitations

This artifact materializes governance checkpoints; it does not grant a real
cutover authorization or claim production readiness. Invalid, missing, stale,
or reconstructed evidence is rejected without silent fallback. Independent QA
and Reviewer approval remain required on the same candidate commit.

## Rollback

Revert the candidate commit. There is no database migration, runtime state, or
external side effect to compensate. The previous frozen walking-skeleton
contract and slice-1 evidence remain authoritative.
