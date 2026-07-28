# REQ-ARTLAYOUT-002 — objetos internos são content-addressed e vinculados a IDs lógicos

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `ARTLAYOUT`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-012`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

objetos internos são content-addressed e vinculados a IDs lógicos

## Rastreabilidade

- **Épicos:** `EPIC-012`, `EPIC-026`
- **Evidência ou teste canônico:** `test_req_artlayout_002`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Contexts consumidores:** `BC-003/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
