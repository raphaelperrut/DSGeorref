# REQ-CIT-001 — Releases públicas fornecem metadados e instruções de citação

- **Tipo:** `GOVERNANCA`
- **Categoria:** `CIT`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-037`
- **Estado:** `PENDING`
- **Gate:** `Governance`

## Requisito

Releases públicas fornecem metadados e instruções de citação

## Rastreabilidade

- **Épicos:** `EPIC-007`, `EPIC-042`
- **Evidência ou teste canônico:** `citation_cff_validation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
