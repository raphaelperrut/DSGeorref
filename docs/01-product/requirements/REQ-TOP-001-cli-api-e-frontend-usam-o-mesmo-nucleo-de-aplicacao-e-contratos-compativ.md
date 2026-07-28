# REQ-TOP-001 — CLI, API e frontend usam o mesmo núcleo de aplicação e contratos compatíveis

- **Tipo:** `FUNCIONAL`
- **Categoria:** `TOP`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-014`
- **Estado:** `PENDING`
- **Gate:** `Foundation`

## Requisito

CLI, API e frontend usam o mesmo núcleo de aplicação e contratos compatíveis

## Rastreabilidade

- **Épicos:** `EPIC-003`, `EPIC-004`, `EPIC-015`
- **Evidência ou teste canônico:** `cli_api_semantic_contract`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
