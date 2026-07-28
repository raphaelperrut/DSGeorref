# REQ-RUN-006 — Erros de domínio são tipados e mapeados de forma versionada para Problem Details.

- **Tipo:** `CONTRATO`
- **Categoria:** `RUN`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-040`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Erros de domínio são tipados e mapeados de forma versionada para Problem Details.

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-004`, `EPIC-012`, `EPIC-031`
- **Evidência ou teste canônico:** `test_req_run_006`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-003/BC-016`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
