# REQ-EPIC-016 — Retry automático é permitido apenas para falhas técnicas transitórias classificadas; mudança algorítmica cria nova tentativa versionada e nunca relaxa o SGV

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-038`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Quality`

## Requisito

Retry automático é permitido apenas para falhas técnicas transitórias classificadas; mudança algorítmica cria nova tentativa versionada e nunca relaxa o SGV

## Rastreabilidade

- **Épicos:** `EPIC-016`, `EPIC-030`
- **Evidência ou teste canônico:** `test_retry_classification_budget_idempotency_no_quality_relaxation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-012`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
