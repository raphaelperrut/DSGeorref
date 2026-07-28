# REQ-SRP-002 — Decisões de admissão, fairness, leases, backpressure e breakers devem poder ser simuladas offline sem executar imagens

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SRP`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-037`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Quality`

## Requisito

Decisões de admissão, fairness, leases, backpressure e breakers devem poder ser simuladas offline sem executar imagens

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-104`
- **Evidência ou teste canônico:** `test_offline_scheduler_decision_replay_without_scientific_workload_or_providers`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
