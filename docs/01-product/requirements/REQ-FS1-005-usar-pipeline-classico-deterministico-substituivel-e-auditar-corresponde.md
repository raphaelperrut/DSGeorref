# REQ-FS1-005 — usar pipeline clássico determinístico, substituível e auditar correspondências

- **Tipo:** `FUNCIONAL`
- **Categoria:** `FS1`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-055`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

usar pipeline clássico determinístico, substituível e auditar correspondências

## Rastreabilidade

- **Épicos:** `EPIC-004`, `EPIC-005`, `EPIC-014`, `EPIC-020`, `EPIC-021`, `EPIC-022`, `EPIC-023`, `EPIC-024`, `EPIC-026`, `EPIC-031`
- **Evidência ou teste canônico:** `test_first_functional_slice_decision_05`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-010/BC-016/BC-007/BC-005/BC-006/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
