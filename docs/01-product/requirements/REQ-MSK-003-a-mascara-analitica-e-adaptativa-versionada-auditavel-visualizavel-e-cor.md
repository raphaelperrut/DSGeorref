# REQ-MSK-003 — A máscara analítica é adaptativa, versionada, auditável, visualizável e corrigível sem modificar o raster original

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MSK`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-055`
- **Estado:** `PENDING`
- **Gate:** `Geo/UX`

## Requisito

A máscara analítica é adaptativa, versionada, auditável, visualizável e corrigível sem modificar o raster original

## Rastreabilidade

- **Épicos:** `EPIC-032`, `EPIC-045`
- **Evidência ou teste canônico:** `test_adaptive_mask_preview_correction_versioning`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
