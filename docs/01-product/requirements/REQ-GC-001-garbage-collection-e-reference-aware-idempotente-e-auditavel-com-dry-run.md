# REQ-GC-001 — Garbage collection é reference-aware, idempotente e auditável, com dry-run, tombstone, quarentena, período de graça e revalidação

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `GC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-016`
- **Estado:** `PENDING`
- **Gate:** `Data/Ops`

## Requisito

Garbage collection é reference-aware, idempotente e auditável, com dry-run, tombstone, quarentena, período de graça e revalidação

## Rastreabilidade

- **Épicos:** `EPIC-073`, `EPIC-074`
- **Evidência ou teste canônico:** `test_reference_aware_gc_tombstone_quarantine_race_idempotency`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
