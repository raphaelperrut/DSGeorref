# REQ-CRS-002 — Toda coordenada fora de espaço fechado possui CRS e convenção de eixos explícitos; APIs e adapters normalizam axis order nas fronteiras

- **Tipo:** `CONTRATO`
- **Categoria:** `CRS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-041`
- **Estado:** `PENDING`
- **Gate:** `Geo/API`

## Requisito

Toda coordenada fora de espaço fechado possui CRS e convenção de eixos explícitos; APIs e adapters normalizam axis order nas fronteiras

## Rastreabilidade

- **Épicos:** `EPIC-004`, `EPIC-093`
- **Evidência ou teste canônico:** `test_explicit_axis_order_and_adapter_normalization`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
