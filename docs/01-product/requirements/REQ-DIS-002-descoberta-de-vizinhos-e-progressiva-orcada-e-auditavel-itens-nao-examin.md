# REQ-DIS-002 — Descoberta de vizinhos é progressiva, orçada e auditável; itens não examinados por limite de recurso são distinguíveis de incompatíveis

- **Tipo:** `FUNCIONAL`
- **Categoria:** `DIS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-047`
- **Estado:** `PENDING`
- **Gate:** `Geo/Scale`

## Requisito

Descoberta de vizinhos é progressiva, orçada e auditável; itens não examinados por limite de recurso são distinguíveis de incompatíveis

## Rastreabilidade

- **Épicos:** `EPIC-019`, `EPIC-055`
- **Evidência ou teste canônico:** `test_budgeted_neighbor_retrieval_recall_and_unexamined_state`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-005`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
