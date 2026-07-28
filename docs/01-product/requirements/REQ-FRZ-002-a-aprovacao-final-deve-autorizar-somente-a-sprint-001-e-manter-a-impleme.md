# REQ-FRZ-002 — A aprovação final deve autorizar somente a SPRINT-001 e manter a implementação funcional bloqueada pelo executable Foundation Gate

- **Tipo:** `GOVERNANCA`
- **Categoria:** `FRZ`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-057`
- **Estado:** `PENDING`
- **Gate:** `Delivery/Quality`

## Requisito

A aprovação final deve autorizar somente a SPRINT-001 e manter a implementação funcional bloqueada pelo executable Foundation Gate

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-092`
- **Evidência ou teste canônico:** `test_sprint_zero_authorization_and_functional_foundation_gate_blocking`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
