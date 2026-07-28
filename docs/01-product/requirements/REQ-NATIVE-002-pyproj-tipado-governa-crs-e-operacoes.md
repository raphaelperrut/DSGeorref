# REQ-NATIVE-002 — pyproj tipado governa CRS e operações

- **Tipo:** `FUNCIONAL`
- **Categoria:** `NATIVE`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-041`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

pyproj tipado governa CRS e operações

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-021`, `EPIC-022`, `EPIC-026`
- **Evidência ou teste canônico:** `test_req_native_002`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-007/BC-005/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
