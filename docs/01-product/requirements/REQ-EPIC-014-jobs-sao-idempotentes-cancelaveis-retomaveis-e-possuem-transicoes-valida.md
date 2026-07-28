# REQ-EPIC-014 — Jobs são idempotentes, canceláveis, retomáveis e possuem transições válidas

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-016`
- **Estado:** `PENDING`
- **Gate:** `Core`

## Requisito

Jobs são idempotentes, canceláveis, retomáveis e possuem transições válidas

## Rastreabilidade

- **Épicos:** `EPIC-014`, `EPIC-016`
- **Evidência ou teste canônico:** `job_state_idempotency_cancel_resume`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
