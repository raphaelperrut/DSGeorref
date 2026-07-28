# REQ-ARTLAYOUT-001 — roots internos são separados por função e durabilidade

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `ARTLAYOUT`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-009`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

roots internos são separados por função e durabilidade

## Rastreabilidade

- **Épicos:** `EPIC-026`, `EPIC-039`
- **Evidência ou teste canônico:** `test_req_artlayout_001`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
