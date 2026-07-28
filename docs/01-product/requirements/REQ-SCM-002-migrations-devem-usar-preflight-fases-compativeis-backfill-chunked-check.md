# REQ-SCM-002 — Migrations devem usar preflight, fases compatíveis, backfill chunked, checkpoints e validação de invariantes

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCM`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-026`
- **Estado:** `PENDING`
- **Gate:** `Data/Operations`

## Requisito

Migrations devem usar preflight, fases compatíveis, backfill chunked, checkpoints e validação de invariantes

## Rastreabilidade

- **Épicos:** `EPIC-012`, `EPIC-106`
- **Evidência ou teste canônico:** `test_expand_migrate_contract_chunked_backfill_resume_invariants_and_irreversibility`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Contexts consumidores:** `BC-003/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
