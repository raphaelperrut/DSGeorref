# REQ-RMR-002 — A visualização deve sincronizar raster, grafo, fontes e heatmaps com level-of-detail e carregamento sob demanda

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMR`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-042`
- **Estado:** `PENDING`
- **Gate:** `Web/Geo`

## Requisito

A visualização deve sincronizar raster, grafo, fontes e heatmaps com level-of-detail e carregamento sob demanda

## Rastreabilidade

- **Épicos:** `EPIC-032`, `EPIC-102`
- **Evidência ou teste canônico:** `test_multiscale_graph_raster_source_heatmap_lod_and_incremental_loading`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
