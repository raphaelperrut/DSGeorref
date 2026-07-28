# REQ-RUNTIME-004 — Unit of Work, transactions curtas, erros e idempotência seguem AP-002 e ADR-018

- **Tipo:** `CONTRATO`
- **Categoria:** `RUNTIME`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-045`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Unit of Work, transactions curtas, erros e idempotência seguem AP-002 e ADR-018

## Rastreabilidade

- **Épicos:** `EPIC-004`, `EPIC-078`
- **Evidência ou teste canônico:** `test_runtime_decision_4`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
