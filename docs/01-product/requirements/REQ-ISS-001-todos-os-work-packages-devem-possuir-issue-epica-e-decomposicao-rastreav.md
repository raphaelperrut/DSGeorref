# REQ-ISS-001 — Todos os épicos devem possuir issue épica e decomposição rastreável em fatias implementáveis

- **Tipo:** `GOVERNANCA`
- **Categoria:** `ISS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-008`
- **Estado:** `PENDING`
- **Gate:** `Delivery/Engineering`

## Requisito

Todos os épicos devem possuir issue épica e decomposição rastreável em fatias implementáveis

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-110`
- **Evidência ou teste canônico:** `test_all_work_packages_have_parent_issue_and_slice_skeleton`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
