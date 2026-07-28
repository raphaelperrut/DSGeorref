# REQ-PLN-008 — exigir accountable owner único e papéis separados de colaboração/revisão/aprovação

- **Tipo:** `FUNCIONAL`
- **Categoria:** `PLN`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-016`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

exigir accountable owner único e papéis separados de colaboração/revisão/aprovação

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-110`
- **Evidência ou teste canônico:** `test_accountable_owner_collaborator_reviewer_and_gate_approver`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
