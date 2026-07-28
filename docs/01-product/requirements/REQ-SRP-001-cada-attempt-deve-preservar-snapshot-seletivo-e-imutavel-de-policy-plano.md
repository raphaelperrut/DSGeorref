# REQ-SRP-001 — Cada attempt deve preservar snapshot seletivo e imutável de policy, plano, capacidade, prioridade e runners sem secrets

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SRP`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Operations/Security`

## Requisito

Cada attempt deve preservar snapshot seletivo e imutável de policy, plano, capacidade, prioridade e runners sem secrets

## Rastreabilidade

- **Épicos:** `EPIC-040`, `EPIC-104`
- **Evidência ou teste canônico:** `test_scheduler_execution_snapshot_selective_immutable_redacted_and_versioned`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
