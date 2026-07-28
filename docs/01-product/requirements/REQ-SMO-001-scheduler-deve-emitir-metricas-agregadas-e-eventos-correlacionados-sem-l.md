# REQ-SMO-001 — Scheduler deve emitir métricas agregadas e eventos correlacionados sem labels de alta cardinalidade

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SMO`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-039`
- **Estado:** `PENDING`
- **Gate:** `Operations/Jobs`

## Requisito

Scheduler deve emitir métricas agregadas e eventos correlacionados sem labels de alta cardinalidade

## Rastreabilidade

- **Épicos:** `EPIC-040`, `EPIC-069`
- **Evidência ou teste canônico:** `test_scheduler_low_cardinality_metrics_correlated_event_ledger_and_timeline`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
