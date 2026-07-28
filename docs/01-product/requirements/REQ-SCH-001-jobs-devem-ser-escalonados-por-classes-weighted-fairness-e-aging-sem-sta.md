# REQ-SCH-001 — Jobs devem ser escalonados por classes, weighted fairness e aging, sem starvation e sem ignorar budgets

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCH`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-012`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Operations`

## Requisito

Jobs devem ser escalonados por classes, weighted fairness e aging, sem starvation e sem ignorar budgets

## Rastreabilidade

- **Épicos:** `EPIC-019`, `EPIC-068`
- **Evidência ou teste canônico:** `test_class_aware_weighted_fair_scheduler_aging_and_no_starvation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
