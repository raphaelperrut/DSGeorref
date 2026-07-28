# REQ-RMQ-003 — O mosaico virtual deve permanecer canônico e materializações devem ser tileadas, retomáveis e sob demanda

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMQ`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-036`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

O mosaico virtual deve permanecer canônico e materializações devem ser tileadas, retomáveis e sob demanda

## Rastreabilidade

- **Épicos:** `EPIC-098`, `EPIC-103`
- **Evidência ou teste canônico:** `test_virtual_canonical_preview_and_on_demand_tiled_materialization`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-008` — Mosaico Relativo.
- **Contexts consumidores:** `BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
