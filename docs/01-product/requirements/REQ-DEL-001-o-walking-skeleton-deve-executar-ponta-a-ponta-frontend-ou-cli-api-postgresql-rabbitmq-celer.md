# REQ-DEL-001 — O walking skeleton deve executar ponta a ponta frontend ou CLI → API → PostgreSQL → RabbitMQ/Celery → worker → artifact diagnóstico, com Definition of Done e teste automatizado.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `DEL`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-014`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

O walking skeleton deve executar ponta a ponta frontend ou CLI → API → PostgreSQL → RabbitMQ/Celery → worker → artifact diagnóstico, com Definition of Done e teste automatizado.

## Rastreabilidade

- **Épicos:** `EPIC-003`, `EPIC-086`
- **Evidência ou teste canônico:** `test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
