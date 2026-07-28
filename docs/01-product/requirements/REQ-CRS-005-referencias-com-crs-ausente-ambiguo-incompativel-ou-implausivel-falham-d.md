# REQ-CRS-005 — Referências com CRS ausente, ambíguo, incompatível ou implausível falham de modo fechado até atribuição ou correção auditável

- **Tipo:** `CONTRATO`
- **Categoria:** `CRS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-041`
- **Estado:** `PENDING`
- **Gate:** `Geo/Providers`

## Requisito

Referências com CRS ausente, ambíguo, incompatível ou implausível falham de modo fechado até atribuição ou correção auditável

## Rastreabilidade

- **Épicos:** `EPIC-058`, `EPIC-096`
- **Evidência ou teste canônico:** `test_reference_crs_fail_closed_metadata_area_operation_roundtrip`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
