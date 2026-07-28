# REQ-GCP-002 — GCPs possuem lifecycle tipado, versão, proveniência e exports GeoPackage/GeoJSON/CSV/manifesto com schema versionado

- **Tipo:** `FUNCIONAL`
- **Categoria:** `GCP`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-048`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

GCPs possuem lifecycle tipado, versão, proveniência e exports GeoPackage/GeoJSON/CSV/manifesto com schema versionado

## Rastreabilidade

- **Épicos:** `EPIC-037`, `EPIC-063`
- **Evidência ou teste canônico:** `test_gcp_lifecycle_roundtrip_exports_provenance`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Contexts consumidores:** `BC-012/BC-011`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
