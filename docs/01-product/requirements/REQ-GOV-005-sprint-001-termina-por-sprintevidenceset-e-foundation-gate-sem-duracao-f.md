# REQ-GOV-005 — SPRINT-001 termina por SprintEvidenceSet e foundation gate, sem duração fixa ou aprovação automática por calendário

- **Tipo:** `GOVERNANCA`
- **Categoria:** `GOV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-006`
- **Estado:** `PENDING`
- **Gate:** `Foundation/Governance`

## Requisito

SPRINT-001 termina por SprintEvidenceSet e foundation gate, sem duração fixa ou aprovação automática por calendário

## Rastreabilidade

- **Épicos:** `EPIC-092`
- **Evidência ou teste canônico:** `test_sprint_zero_gate_evidence_driven_no_calendar_pass`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
