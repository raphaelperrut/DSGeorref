# REQ-RMR-004 — Provenance de sobreposição deve explicar fontes e seamlines de forma escalável, com detalhe por pixel apenas sob demanda

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMR`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-050`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

Provenance de sobreposição deve explicar fontes e seamlines de forma escalável, com detalhe por pixel apenas sob demanda

## Rastreabilidade

- **Épicos:** `EPIC-098`, `EPIC-102`
- **Evidência ou teste canônico:** `test_hierarchical_tile_region_provenance_and_dense_on_demand_limits`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-008` — Mosaico Relativo.
- **Contexts consumidores:** `BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
