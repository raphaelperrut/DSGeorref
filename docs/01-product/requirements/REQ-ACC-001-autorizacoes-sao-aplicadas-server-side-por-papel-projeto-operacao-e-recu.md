# REQ-ACC-001 — Autorizações são aplicadas server-side por papel, projeto, operação e recurso

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ACC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-043`
- **Estado:** `PENDING`
- **Gate:** `Identity`

## Requisito

Autorizações são aplicadas server-side por papel, projeto, operação e recurso

## Rastreabilidade

- **Épicos:** `EPIC-009`, `EPIC-010`
- **Evidência ou teste canônico:** `test_role_project_operation_access`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
