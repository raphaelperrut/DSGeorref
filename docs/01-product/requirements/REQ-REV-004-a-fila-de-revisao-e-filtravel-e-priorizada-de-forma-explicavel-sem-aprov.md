# REQ-REV-004 — A fila de revisão é filtrável e priorizada de forma explicável, sem aprovação, edição de GCPs ou override de hard gates em lote

- **Tipo:** `FUNCIONAL`
- **Categoria:** `REV`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-048`
- **Estado:** `PENDING`
- **Gate:** `UX/Quality`

## Requisito

A fila de revisão é filtrável e priorizada de forma explicável, sem aprovação, edição de GCPs ou override de hard gates em lote

## Rastreabilidade

- **Épicos:** `EPIC-062`, `EPIC-064`
- **Evidência ou teste canônico:** `test_review_queue_explainable_priority_no_bulk_approval`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-011` — Revisão e Correção.
- **Contexts consumidores:** `BC-011`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
