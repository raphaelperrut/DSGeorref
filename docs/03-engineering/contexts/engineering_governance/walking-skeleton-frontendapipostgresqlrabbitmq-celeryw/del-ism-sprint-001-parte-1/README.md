# Executable foundation materialization — slice 1/2

This package binds the ten requirements in the current slice to executable,
repository-local checkpoints. The validator rejects contract drift, incomplete
coverage, unsafe checkpoint paths, expanded scope, and silent fallback.

Run the focused materialization checks with:

```text
python -m pytest -q -p no:cacheprovider tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_implementation.py
```

The end-to-end checkpoint remains the already integrated PostgreSQL and
RabbitMQ/Celery sentinel. The current slice references it and the frozen walking
skeleton contract without duplicating runtime or changing application surfaces.

## Contract impact

No frozen contract was changed. The materialization binds to contract version
`1.0.0` and its SHA-256 digest, exercises only essential walking-skeleton
contracts, and fails closed if the version, digest, authority, or failure policy
drifts. No API, event, state, table, or migration was introduced.

## Risks and limitations

This is a private CPU-only foundation candidate. It makes no public claim about
cost, scale, latency, GPU capacity, recovery, or security. The synthetic job does
not perform functional georeferencing. Promotion still requires independent QA
and Reviewer evidence on the same candidate commit.

## Rollback

Revert the materialization commit before promotion. Because this slice changes
no frozen contract, database schema, runtime state, or published artifact, no
data migration or compensating operation is required.
