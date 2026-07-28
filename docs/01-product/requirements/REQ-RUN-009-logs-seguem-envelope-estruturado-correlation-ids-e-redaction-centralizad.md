# REQ-RUN-009 — Logs seguem envelope estruturado, correlation IDs e redaction centralizada.

- **Tipo:** `CONTRATO`
- **Categoria:** `RUN`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-055`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Logs seguem envelope estruturado, correlation IDs e redaction centralizada.

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-004`, `EPIC-012`, `EPIC-031`
- **Evidência ou teste canônico:** `test_req_run_009`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-003/BC-016`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
