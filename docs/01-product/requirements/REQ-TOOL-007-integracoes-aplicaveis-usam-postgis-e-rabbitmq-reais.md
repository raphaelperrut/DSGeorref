# REQ-TOOL-007 — integrações aplicáveis usam PostGIS e RabbitMQ reais

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `TOOL`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-018`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

integrações aplicáveis usam PostGIS e RabbitMQ reais

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-028`
- **Evidência ou teste canônico:** `test_pytest_real_services`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
