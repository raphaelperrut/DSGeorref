# REQ-GOV-002 — Épicos representam outcomes encerráveis; histórias implementáveis possuem critérios, ADRs, riscos, testes, evidências, migration e rollback aplicáveis.

- **Tipo:** `GOVERNANCA`
- **Categoria:** `GOV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-006`
- **Estado:** `PENDING`
- **Gate:** `Governance/Foundation`

## Requisito

Épicos representam outcomes encerráveis; histórias implementáveis possuem critérios, ADRs, riscos, testes, evidências, migration e rollback aplicáveis.

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-090`
- **Evidência ou teste canônico:** `test_issue_form_required_acceptance_risk_test_rollback_fields`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
