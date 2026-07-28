# REQ-ISS-004 — O portfólio deve possuir skeleton completo e detalhamento progressivo das próximas fases

- **Tipo:** `GOVERNANCA`
- **Categoria:** `ISS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-040`
- **Estado:** `PENDING`
- **Gate:** `Delivery/Planning`

## Requisito

O portfólio deve possuir skeleton completo e detalhamento progressivo das próximas fases

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-110`
- **Evidência ou teste canônico:** `test_complete_portfolio_skeleton_and_progressive_detailing_rules`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
