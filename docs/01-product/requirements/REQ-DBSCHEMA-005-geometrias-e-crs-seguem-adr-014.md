# REQ-DBSCHEMA-005 — geometrias e CRS seguem ADR-041

- **Tipo:** `CONTRATO`
- **Categoria:** `DBSCHEMA`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-041`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Toda geometria persistida deve declarar SRID compatível com o registry de CRS, aplicar normalização de axis order nas boundaries e obedecer ao contrato de precisão e validade definido pela ADR-041.

## Rastreabilidade

- **Épicos:** `EPIC-012`, `EPIC-021`
- **Evidência ou teste canônico:** `test_req_dbschema_005`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Contexts consumidores:** `BC-003/BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
