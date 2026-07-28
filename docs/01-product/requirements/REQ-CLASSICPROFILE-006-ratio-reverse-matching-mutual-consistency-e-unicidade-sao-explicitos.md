# REQ-CLASSICPROFILE-006 — ratio, reverse matching, mutual consistency e unicidade são explícitos

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `CLASSICPROFILE`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-044`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

ratio, reverse matching, mutual consistency e unicidade são explícitos

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-022`, `EPIC-028`
- **Evidência ou teste canônico:** `test_req_classicprofile_006`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-005/BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
