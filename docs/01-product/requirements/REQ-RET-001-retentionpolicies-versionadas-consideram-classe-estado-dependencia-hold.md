# REQ-RET-001 — RetentionPolicies versionadas consideram classe, estado, dependência, hold e reprodução antes de tornar um objeto elegível à remoção

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `RET`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-012`
- **Estado:** `PENDING`
- **Gate:** `Data/Privacy`

## Requisito

RetentionPolicies versionadas consideram classe, estado, dependência, hold e reprodução antes de tornar um objeto elegível à remoção

## Rastreabilidade

- **Épicos:** `EPIC-049`, `EPIC-073`
- **Evidência ou teste canônico:** `test_retention_policy_protected_lineage_hold_dry_run`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
