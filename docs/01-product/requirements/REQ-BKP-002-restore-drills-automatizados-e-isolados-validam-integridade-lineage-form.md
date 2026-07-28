# REQ-BKP-002 — Restore drills automatizados e isolados validam integridade, lineage, formatos geoespaciais, reconstrução de jobs, RPO e RTO

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `BKP`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-025`
- **Estado:** `PENDING`
- **Gate:** `Ops/Release`

## Requisito

Restore drills automatizados e isolados validam integridade, lineage, formatos geoespaciais, reconstrução de jobs, RPO e RTO

## Rastreabilidade

- **Épicos:** `EPIC-071`, `EPIC-072`
- **Evidência ou teste canônico:** `test_isolated_restore_drill_integrity_rpo_rto`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
