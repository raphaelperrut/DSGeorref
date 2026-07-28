# REQ-ART-002 — O original permanece imutável e todo raster operacional aceito é COG validado por policy versionada

- **Tipo:** `CONTRATO`
- **Categoria:** `ART`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-042`
- **Estado:** `PENDING`
- **Gate:** `Data/Geo`

## Requisito

O original permanece imutável e todo raster operacional aceito é COG validado por policy versionada

## Rastreabilidade

- **Épicos:** `EPIC-044`, `EPIC-046`
- **Evidência ou teste canônico:** `test_original_immutable_cog_validation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
