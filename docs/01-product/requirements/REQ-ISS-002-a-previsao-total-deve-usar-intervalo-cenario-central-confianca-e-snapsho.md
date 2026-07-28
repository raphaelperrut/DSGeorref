# REQ-ISS-002 — A previsão total deve usar intervalo, cenário central, confiança e snapshots versionados

- **Tipo:** `GOVERNANCA`
- **Categoria:** `ISS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-008`
- **Estado:** `PENDING`
- **Gate:** `Delivery/Governance`

## Requisito

A previsão total deve usar intervalo, cenário central, confiança e snapshots versionados

## Rastreabilidade

- **Épicos:** `EPIC-001`, `EPIC-110`
- **Evidência ou teste canônico:** `test_issue_forecast_min_mode_max_confidence_and_snapshot_variance`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
