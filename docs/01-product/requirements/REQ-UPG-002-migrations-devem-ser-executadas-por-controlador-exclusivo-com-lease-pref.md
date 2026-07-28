# REQ-UPG-002 — Migrations devem ser executadas por controlador exclusivo com lease, preflight, plano e checkpoints persistidos

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `UPG`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-026`
- **Estado:** `PENDING`
- **Gate:** `Release/Data/Operations`

## Requisito

Migrations devem ser executadas por controlador exclusivo com lease, preflight, plano e checkpoints persistidos

## Rastreabilidade

- **Épicos:** `EPIC-012`, `EPIC-106`, `EPIC-107`
- **Evidência ou teste canônico:** `test_singleton_upgrade_controller_lease_preflight_checkpoint_resume_and_split_brain_prevention`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Contexts consumidores:** `BC-003/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
