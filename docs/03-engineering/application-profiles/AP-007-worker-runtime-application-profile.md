# AP-007 — Worker runtime application profile

- **Status:** `Accepted`
- **Owner ADR:** ADR-036 para lease fencing
- **Tuning:** BP-004

## Aplicação das ADRs existentes

- TaskEnvelope mínimo e versionado por IDs/digests; schema em STORY-0136 / ISSUE-0246;
- poucas filas duráveis por classe de workload; PostgreSQL/outbox continua autoritativo;
- ack somente após commit/checkpoint durável; prefetch e concurrency promovidos pelo BP-004;
- processo worker isolado/reciclável conforme stack nativa e budgets;
- retry apenas para falha técnica classificada; quarantine registrada também no PostgreSQL;
- fan-out somente pelo scheduler/outbox;
- progresso persistente e monotônico; schema em STORY-0140 / ISSUE-0250;
- cancelamento por token persistente e safe points; terminate é contenção final;
- readiness por capability registration e drain governado em upgrades.

Nenhum item acima cria nova fonte de verdade; qualquer alteração material volta ao Owner ADR indicado.
