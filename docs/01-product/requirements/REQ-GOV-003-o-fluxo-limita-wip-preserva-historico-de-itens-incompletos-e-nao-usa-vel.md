# REQ-GOV-003 — O fluxo limita WIP, preserva histórico de itens incompletos e não usa velocidade como meta de produtividade

- **Tipo:** `GOVERNANCA`
- **Categoria:** `GOV`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-006`
- **Estado:** `PENDING`
- **Gate:** `Governance`

## Requisito

O fluxo limita WIP, preserva histórico de itens incompletos e não usa velocidade como meta de produtividade

## Rastreabilidade

- **Épicos:** `EPIC-002`
- **Evidência ou teste canônico:** `test_iteration_wip_limits_and_incomplete_item_history`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
