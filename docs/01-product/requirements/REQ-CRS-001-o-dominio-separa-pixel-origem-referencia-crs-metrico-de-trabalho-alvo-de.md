# REQ-CRS-001 — O domínio separa pixel, origem, referência, CRS métrico de trabalho, alvo, descoberta WGS84 e visualização EPSG:3857, preservando a cadeia de transformações no lineage

- **Tipo:** `CONTRATO`
- **Categoria:** `CRS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-041`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

O domínio separa pixel, origem, referência, CRS métrico de trabalho, alvo, descoberta WGS84 e visualização EPSG:3857, preservando a cadeia de transformações no lineage

## Rastreabilidade

- **Épicos:** `EPIC-063`, `EPIC-093`
- **Evidência ou teste canônico:** `test_pixel_reference_target_discovery_coordinate_roundtrip`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-011` — Revisão e Correção.
- **Contexts consumidores:** `BC-011/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
