# REQ-GOV-001 — Um único GitHub Project central oferece views de roadmap, backlog, sprint, riscos, ADRs, releases e Geo/IA sem duplicar itens

- **Tipo:** `GOVERNANCA`
- **Categoria:** `GOV`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-043`
- **Estado:** `PENDING`
- **Gate:** `Governance`

## Requisito

Um único GitHub Project central oferece views de roadmap, backlog, sprint, riscos, ADRs, releases e Geo/IA sem duplicar itens

## Rastreabilidade

- **Épicos:** `EPIC-002`
- **Evidência ou teste canônico:** `test_single_project_views_fields_and_no_duplicate_backlog`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
