# REQ-MAT-001 — Matching utiliza pirâmide coarse-to-fine e tiles adaptativos com transformação de coordenadas testada entre níveis

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MAT`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-044`
- **Estado:** `PENDING`
- **Gate:** `Geo/Scale`

## Requisito

Matching utiliza pirâmide coarse-to-fine e tiles adaptativos com transformação de coordenadas testada entre níveis

## Rastreabilidade

- **Épicos:** `EPIC-019`, `EPIC-047`
- **Evidência ou teste canônico:** `test_pyramid_tile_coordinate_roundtrip_refinement`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
