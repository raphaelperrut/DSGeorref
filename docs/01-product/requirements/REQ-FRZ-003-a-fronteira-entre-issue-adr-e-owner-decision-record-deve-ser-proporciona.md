# REQ-FRZ-003 — A fronteira entre issue, ADR e owner decision record deve ser proporcional, auditável e impedir divergência silenciosa

- **Tipo:** `GOVERNANCA`
- **Categoria:** `FRZ`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-057`
- **Estado:** `PENDING`
- **Gate:** `Governance/Engineering`

## Requisito

A fronteira entre issue, ADR e owner decision record deve ser proporcional, auditável e impedir divergência silenciosa

## Rastreabilidade

- **Épicos:** `EPIC-091`, `EPIC-092`
- **Evidência ou teste canônico:** `test_issue_adr_decision_package_impact_boundary_and_no_silent_divergence`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
