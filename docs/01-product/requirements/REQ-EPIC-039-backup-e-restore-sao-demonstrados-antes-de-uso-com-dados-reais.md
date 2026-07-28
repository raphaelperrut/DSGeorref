# REQ-EPIC-039 — Backup e restore são demonstrados antes de uso com dados reais

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-027`
- **Estado:** `PENDING`
- **Gate:** `Ops`

## Requisito

Backup e restore são demonstrados antes de uso com dados reais

## Rastreabilidade

- **Épicos:** `EPIC-013`, `EPIC-072`
- **Evidência ou teste canônico:** `test_req_epic_039`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
