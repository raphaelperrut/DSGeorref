# REQ-ISM-003 — decompor outcomes em fatias verticais finas e integráveis

- **Tipo:** `GOVERNANCA`
- **Categoria:** `ISM`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-006`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

decompor outcomes em fatias verticais finas e integráveis

## Rastreabilidade

- **Épicos:** `EPIC-086`, `EPIC-110`
- **Evidência ou teste canônico:** `test_thin_vertical_integrable_slices_and_pr_sequence`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
