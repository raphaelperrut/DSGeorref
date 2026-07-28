# REQ-SCL-002 — Consulta e exportação de lotes usam paginação, filtros e streaming server-side sem carregar todo o lote no navegador

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCL`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `UX/Scale`

## Requisito

Consulta e exportação de lotes usam paginação, filtros e streaming server-side sem carregar todo o lote no navegador

## Rastreabilidade

- **Épicos:** `EPIC-034`, `EPIC-037`
- **Evidência ou teste canônico:** `test_server_pagination_filter_stream_export`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-012`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
