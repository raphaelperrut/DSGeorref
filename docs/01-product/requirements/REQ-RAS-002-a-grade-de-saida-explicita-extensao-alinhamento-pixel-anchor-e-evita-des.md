# REQ-RAS-002 — A grade de saída explicita extensão, alinhamento, pixel anchor e evita deslocamento de meio pixel.

- **Tipo:** `CONTRATO`
- **Categoria:** `RAS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-049`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

A grade de saída explicita extensão, alinhamento, pixel anchor e evita deslocamento de meio pixel.

## Rastreabilidade

- **Épicos:** `EPIC-044`, `EPIC-097`
- **Evidência ou teste canônico:** `test_output_grid_extent_alignment_pixel_anchor_and_no_half_pixel_shift`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
