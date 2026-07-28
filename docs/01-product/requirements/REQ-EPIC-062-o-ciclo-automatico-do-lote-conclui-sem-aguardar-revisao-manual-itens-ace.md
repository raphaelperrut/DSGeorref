# REQ-EPIC-062 — O ciclo automático do lote conclui sem aguardar revisão manual; itens aceitos são publicados e casos recuperáveis entram em fila opcional posterior

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-002`
- **Estado:** `PENDING`
- **Gate:** `Jobs/UX`

## Requisito

O ciclo automático do lote conclui sem aguardar revisão manual; itens aceitos são publicados e casos recuperáveis entram em fila opcional posterior

## Rastreabilidade

- **Épicos:** `EPIC-018`, `EPIC-034`, `EPIC-062`
- **Evidência ou teste canônico:** `test_batch_auto_completion_nonblocking_review_queue`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-016/BC-011`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
