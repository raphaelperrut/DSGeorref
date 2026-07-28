# REQ-SCM-003 — Artifacts históricos devem permanecer imutáveis e qualquer rematerialização deve criar novo lineage e checksums

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCM`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Data/Reporting/Geo`

## Requisito

Artifacts históricos devem permanecer imutáveis e qualquer rematerialização deve criar novo lineage e checksums

## Rastreabilidade

- **Épicos:** `EPIC-037`, `EPIC-105`
- **Evidência ou teste canônico:** `test_immutable_artifact_read_adapters_lineage_preserving_rematerialization_and_supersession`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Contexts consumidores:** `BC-012/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
