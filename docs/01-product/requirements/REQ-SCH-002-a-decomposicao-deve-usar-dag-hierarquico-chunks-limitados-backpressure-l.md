# REQ-SCH-002 — A decomposição deve usar DAG hierárquico, chunks limitados, backpressure, leases e safe boundaries

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCH`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-039`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Platform`

## Requisito

A decomposição deve usar DAG hierárquico, chunks limitados, backpressure, leases e safe boundaries

## Rastreabilidade

- **Épicos:** `EPIC-018`, `EPIC-068`
- **Evidência ou teste canônico:** `test_hierarchical_dag_chunk_limits_backpressure_leases_and_safe_boundaries`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
