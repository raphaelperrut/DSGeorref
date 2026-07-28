# REQ-GOV-ADR-003 — Refinements, profiles, benchmarks e detalhes locais não podem ser promovidos artificialmente a ADR.

- **Tipo:** `GOVERNANCA`
- **Categoria:** `GOV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-040`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Refinements, profiles, benchmarks e detalhes locais não podem ser promovidos artificialmente a ADR.

## Rastreabilidade

- **Épicos:** `EPIC-001`, `EPIC-002`
- **Evidência ou teste canônico:** `test_adr_governance_overlap`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
