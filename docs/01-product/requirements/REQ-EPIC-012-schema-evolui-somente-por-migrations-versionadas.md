# REQ-EPIC-012 — Schema evolui somente por migrations versionadas

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-026`
- **Estado:** `PENDING`
- **Gate:** `Data`

## Requisito

Schema evolui somente por migrations versionadas

## Rastreabilidade

- **Épicos:** `EPIC-005`
- **Evidência ou teste canônico:** `migration_upgrade_rollback`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
