# REQ-RMR-001 — Relatórios do componente devem preservar snapshots imutáveis e oferecer visão consolidada vigente sem sobrescrever história

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMR`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-050`
- **Estado:** `PENDING`
- **Gate:** `Reporting/Data`

## Requisito

Relatórios do componente devem preservar snapshots imutáveis e oferecer visão consolidada vigente sem sobrescrever história

## Rastreabilidade

- **Épicos:** `EPIC-037`, `EPIC-102`
- **Evidência ou teste canônico:** `test_relative_mosaic_report_snapshots_current_view_and_history`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Contexts consumidores:** `BC-012/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
