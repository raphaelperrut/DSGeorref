# REQ-INS-001 — Instalação deve usar plano declarativo, preflight, execução idempotente, checkpoints e diagnóstico de estado parcial

- **Tipo:** `FUNCIONAL`
- **Categoria:** `INS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-016`
- **Estado:** `PENDING`
- **Gate:** `Release/Operations/Platform`

## Requisito

Instalação deve usar plano declarativo, preflight, execução idempotente, checkpoints e diagnóstico de estado parcial

## Rastreabilidade

- **Épicos:** `EPIC-081`, `EPIC-108`
- **Evidência ou teste canônico:** `test_declarative_installation_plan_preflight_idempotent_resume_and_partial_state_diagnostics`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Contexts consumidores:** `BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
