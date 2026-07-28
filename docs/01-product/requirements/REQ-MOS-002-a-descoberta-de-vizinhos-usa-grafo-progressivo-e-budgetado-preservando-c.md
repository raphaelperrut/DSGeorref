# REQ-MOS-002 — A descoberta de vizinhos usa grafo progressivo e budgetado, preservando componentes disjuntos e imagens isoladas

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MOS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-040`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

A descoberta de vizinhos usa grafo progressivo e budgetado, preservando componentes disjuntos e imagens isoladas

## Rastreabilidade

- **Épicos:** `EPIC-055`, `EPIC-098`
- **Evidência ou teste canônico:** `test_budgeted_neighbor_graph_disconnected_components_and_singletons`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
