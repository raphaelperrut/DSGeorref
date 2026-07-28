# REQ-RMV-001 — O componente relativo deve possuir gates independentes e versionados; hard gates não podem ser compensados por score agregado

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-050`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

O componente relativo deve possuir gates independentes e versionados; hard gates não podem ser compensados por score agregado

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-101`
- **Evidência ou teste canônico:** `test_relative_mosaic_quality_profile_independent_hard_and_reviewable_gates`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
