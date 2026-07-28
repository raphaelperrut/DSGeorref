# REQ-RES-001 — O scheduler aplica Resource Governor adaptativo com orçamento de RAM, CPU, GPU e disco temporário

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RES`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-039`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Ops`

## Requisito

O scheduler aplica Resource Governor adaptativo com orçamento de RAM, CPU, GPU e disco temporário

## Rastreabilidade

- **Épicos:** `EPIC-019`, `EPIC-040`
- **Evidência ou teste canônico:** `test_resource_governor_admission_pressure_adaptation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
