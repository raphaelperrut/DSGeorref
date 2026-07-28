# REQ-SCM-004 — Upgrade, rollback e downgrade devem avaliar compatibilidade e bloquear operações irreversíveis sem restore seguro

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SCM`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-035`
- **Estado:** `PENDING`
- **Gate:** `Release/Operations/Data`

## Requisito

Upgrade, rollback e downgrade devem avaliar compatibilidade e bloquear operações irreversíveis sem restore seguro

## Rastreabilidade

- **Épicos:** `EPIC-071`, `EPIC-072`, `EPIC-106`
- **Evidência ou teste canônico:** `test_upgrade_rollback_compatibility_matrix_downgrade_blockers_forward_fix_and_restore`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-014/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
