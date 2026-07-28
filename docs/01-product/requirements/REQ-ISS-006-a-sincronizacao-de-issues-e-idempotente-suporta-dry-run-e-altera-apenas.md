# REQ-ISS-006 — A sincronização de issues é idempotente, suporta dry-run e altera apenas campos sob autoridade do repositório.

- **Tipo:** `GOVERNANCA`
- **Categoria:** `ISS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-016`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

A sincronização de issues é idempotente, suporta dry-run e altera apenas campos sob autoridade do repositório.

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-091`
- **Evidência ou teste canônico:** `test_idempotent_dry_run_managed_field_issue_sync`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
