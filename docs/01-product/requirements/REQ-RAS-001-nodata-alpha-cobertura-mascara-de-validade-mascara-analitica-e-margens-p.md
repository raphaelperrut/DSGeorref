# REQ-RAS-001 — Nodata, alpha, cobertura, máscara de validade, máscara analítica e margens preservadas são semanticamente separados e validados no OutputProfile

- **Tipo:** `CONTRATO`
- **Categoria:** `RAS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-042`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

Nodata, alpha, cobertura, máscara de validade, máscara analítica e margens preservadas são semanticamente separados e validados no OutputProfile

## Rastreabilidade

- **Épicos:** `EPIC-044`, `EPIC-045`, `EPIC-093`
- **Evidência ou teste canônico:** `test_nodata_alpha_coverage_analysis_mask_separation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
