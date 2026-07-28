# REQ-RMV-003 — Bridges, articulation points e arestas de leverage elevado devem passar por análise de sensibilidade e podem dividir o componente

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-050`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

Bridges, articulation points e arestas de leverage elevado devem passar por análise de sensibilidade e podem dividir o componente

## Rastreabilidade

- **Épicos:** `EPIC-056`, `EPIC-101`
- **Evidência ou teste canônico:** `test_bridge_articulation_leverage_removal_sensitivity_and_component_split`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
