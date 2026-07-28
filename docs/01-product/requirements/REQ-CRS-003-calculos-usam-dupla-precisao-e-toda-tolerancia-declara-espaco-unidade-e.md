# REQ-CRS-003 — Cálculos usam dupla precisão e toda tolerância declara espaço, unidade e versão, sem arredondamento prematuro

- **Tipo:** `CONTRATO`
- **Categoria:** `CRS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-041`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

Cálculos usam dupla precisão e toda tolerância declara espaço, unidade e versão, sem arredondamento prematuro

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-093`
- **Evidência ou teste canônico:** `test_units_precision_tolerance_and_no_premature_rounding`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
