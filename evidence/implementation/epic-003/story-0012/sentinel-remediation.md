# STORY-0012 sentinel remediation evidence

- Scope: remediation of the two HIGH findings from Sentinel QA on
  `1da2bb440cf10183a51dc38db5aa62d5e58c3682`.
- Requirement path: CLI → HTTP API → PostgreSQL → RabbitMQ/Celery → worker →
  deterministic diagnostic artifact.
- State authority: PostgreSQL; RabbitMQ carries only the job UUID used by the
  issue-specific Celery task.
- CI path: `make verify` invokes the frozen-contract validator and the focused
  ISSUE-0122 tests; the integration case runs when `FOUNDATION_INTEGRATION=1`.
- Service versions: PostgreSQL 18.4, RabbitMQ 4.3.4, and Celery 5.6.3, matching
  `infra/images/native-stack.lock.yaml`.
- Product impact: none; the probe publishes no shared API, job model, queue
  primitive, migration, or runtime package.

Validation commands:

```text
make verify
py -3.12 -m pytest -q -p no:cacheprovider tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation_contract.py
git diff --check
```
