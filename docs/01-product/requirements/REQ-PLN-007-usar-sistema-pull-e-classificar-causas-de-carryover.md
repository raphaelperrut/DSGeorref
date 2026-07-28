# REQ-PLN-007 — usar sistema pull e classificar causas de carryover

- **Tipo:** `FUNCIONAL`
- **Categoria:** `PLN`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-016`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

usar sistema pull e classificar causas de carryover

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-110`
- **Evidência ou teste canônico:** `test_pull_iteration_objective_and_carryover_reason_classification`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
