# REQ-DBSCHEMA-010 — migrations e compatibilidade seguem ADR-026

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `DBSCHEMA`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-026`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

migrations e compatibilidade seguem ADR-026

## Rastreabilidade

- **Épicos:** `EPIC-013`, `EPIC-107`
- **Evidência ou teste canônico:** `test_req_dbschema_0010`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
