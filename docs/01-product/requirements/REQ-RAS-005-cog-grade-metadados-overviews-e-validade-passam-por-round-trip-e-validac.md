# REQ-RAS-005 — COG, grade, metadados, overviews e validade passam por round-trip e validação independente antes da publicação atômica.

- **Tipo:** `CONTRATO`
- **Categoria:** `RAS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-040`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

COG, grade, metadados, overviews e validade passam por round-trip e validação independente antes da publicação atômica.

## Rastreabilidade

- **Épicos:** `EPIC-046`, `EPIC-097`
- **Evidência ou teste canônico:** `test_cog_grid_metadata_overviews_validity_roundtrip_and_atomic_publication`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
