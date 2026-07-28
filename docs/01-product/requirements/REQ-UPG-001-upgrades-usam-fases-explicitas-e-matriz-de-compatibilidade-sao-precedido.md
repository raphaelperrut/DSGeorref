# REQ-UPG-001 — Upgrades usam fases explícitas e matriz de compatibilidade, são precedidos de preflight/BackupSet, executam migrations controladas, smoke tests e rollback/restore documentado

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `UPG`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-035`
- **Estado:** `PENDING`
- **Gate:** `Ops/Release`

## Requisito

Upgrades usam fases explícitas e matriz de compatibilidade, são precedidos de preflight/BackupSet, executam migrations controladas, smoke tests e rollback/restore documentado

## Rastreabilidade

- **Épicos:** `EPIC-071`, `EPIC-072`, `EPIC-081`
- **Evidência ou teste canônico:** `test_orchestrated_upgrade_preflight_migrations_rollback_restore`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-014/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
