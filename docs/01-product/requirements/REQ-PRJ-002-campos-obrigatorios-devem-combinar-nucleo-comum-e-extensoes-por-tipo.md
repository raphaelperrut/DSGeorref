# REQ-PRJ-002 — Campos obrigatórios devem combinar núcleo comum e extensões por tipo

- **Tipo:** `FUNCIONAL`
- **Categoria:** `PRJ`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-022`
- **Estado:** `PENDING`
- **Gate:** `Delivery/Governance`

## Requisito

Campos obrigatórios devem combinar núcleo comum e extensões por tipo

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-110`
- **Evidência ou teste canônico:** `test_mandatory_core_type_fields`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
