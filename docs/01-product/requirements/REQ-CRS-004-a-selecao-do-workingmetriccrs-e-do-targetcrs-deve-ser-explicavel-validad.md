# REQ-CRS-004 — A seleção do WorkingMetricCRS e do TargetCRS deve ser explicável, validada contra AOI/área de uso/distorção e não pode presumir EPSG:3857 apenas por sua unidade ser metro

- **Tipo:** `CONTRATO`
- **Categoria:** `CRS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-041`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

A seleção do WorkingMetricCRS e do TargetCRS deve ser explicável, validada contra AOI/área de uso/distorção e não pode presumir EPSG:3857 apenas por sua unidade ser metro

## Rastreabilidade

- **Épicos:** `EPIC-093`, `EPIC-096`
- **Evidência ou teste canônico:** `test_aoi_aware_working_crs_selection_distortion_and_explanation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
