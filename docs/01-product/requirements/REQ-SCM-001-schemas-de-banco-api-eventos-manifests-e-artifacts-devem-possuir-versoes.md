# REQ-SCM-001 — Schemas de banco, API, eventos, manifests e artifacts devem possuir versões e matriz explícita de readers/writers

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCM`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Platform/Data/API`

## Requisito

Schemas de banco, API, eventos, manifests e artifacts devem possuir versões e matriz explícita de readers/writers

## Rastreabilidade

- **Épicos:** `EPIC-004`, `EPIC-105`
- **Evidência ou teste canônico:** `test_versioned_schema_registry_reader_writer_compatibility_window_and_unknown_major_rejection`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
