# REQ-TOOL-004 — persistência usa SQLAlchemy 2/Alembic e permite SQL/PostGIS explícito

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `TOOL`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-018`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

persistência usa SQLAlchemy 2/Alembic e permite SQL/PostGIS explícito

## Rastreabilidade

- **Épicos:** `EPIC-012`, `EPIC-013`
- **Evidência ou teste canônico:** `test_sqlalchemy_alembic_postgis`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Contexts consumidores:** `BC-003/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
