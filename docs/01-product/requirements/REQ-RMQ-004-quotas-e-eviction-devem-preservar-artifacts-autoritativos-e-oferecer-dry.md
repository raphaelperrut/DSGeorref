# REQ-RMQ-004 — Quotas e eviction devem preservar artifacts autoritativos e oferecer dry-run e plano de recomputação

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMQ`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-039`
- **Estado:** `PENDING`
- **Gate:** `Operations/Data`

## Requisito

Quotas e eviction devem preservar artifacts autoritativos e oferecer dry-run e plano de recomputação

## Rastreabilidade

- **Épicos:** `EPIC-075`, `EPIC-103`
- **Evidência ou teste canônico:** `test_quota_pinning_dependency_aware_eviction_dry_run_and_recompute_plan`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
