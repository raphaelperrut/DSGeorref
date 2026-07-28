# REQ-RMV-002 — O sistema deve medir fechamento de ciclos e drift local/global com orçamento explícito e localização das piores inconsistências

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-050`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

O sistema deve medir fechamento de ciclos e drift local/global com orçamento explícito e localização das piores inconsistências

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-101`
- **Evidência ou teste canônico:** `test_cycle_basis_budgeted_long_cycle_sampling_drift_percentiles_and_localization`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
