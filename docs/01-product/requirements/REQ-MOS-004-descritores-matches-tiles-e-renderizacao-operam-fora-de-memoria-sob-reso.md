# REQ-MOS-004 — Descritores, matches, tiles e renderização operam fora de memória sob Resource Governor e quotas de disco

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MOS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-044`
- **Estado:** `PENDING`
- **Gate:** `Geo/Platform`

## Requisito

Descritores, matches, tiles e renderização operam fora de memória sob Resource Governor e quotas de disco

## Rastreabilidade

- **Épicos:** `EPIC-019`, `EPIC-098`
- **Evidência ou teste canônico:** `test_out_of_core_pair_tile_rendering_ram_disk_quotas_and_resume`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
