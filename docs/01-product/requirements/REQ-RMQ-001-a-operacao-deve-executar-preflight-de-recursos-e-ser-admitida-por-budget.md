# REQ-RMQ-001 — A operação deve executar preflight de recursos e ser admitida por budgets explícitos sem relaxar gates geométricos

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMQ`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-036`
- **Estado:** `PENDING`
- **Gate:** `Geo/Operations`

## Requisito

A operação deve executar preflight de recursos e ser admitida por budgets explícitos sem relaxar gates geométricos

## Rastreabilidade

- **Épicos:** `EPIC-040`, `EPIC-103`
- **Evidência ou teste canônico:** `test_relative_mosaic_resource_preflight_budgets_admission_and_no_quality_relaxation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
