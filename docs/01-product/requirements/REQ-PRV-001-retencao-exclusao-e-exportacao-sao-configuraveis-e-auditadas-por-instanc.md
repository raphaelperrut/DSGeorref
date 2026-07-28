# REQ-PRV-001 — Retenção, exclusão e exportação são configuráveis e auditadas por instância/projeto

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `PRV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-055`
- **Estado:** `PENDING`
- **Gate:** `Privacy`

## Requisito

Retenção, exclusão e exportação são configuráveis e auditadas por instância/projeto

## Rastreabilidade

- **Épicos:** `EPIC-012`, `EPIC-013`
- **Evidência ou teste canônico:** `retention_deletion_restore`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Contexts consumidores:** `BC-003/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
