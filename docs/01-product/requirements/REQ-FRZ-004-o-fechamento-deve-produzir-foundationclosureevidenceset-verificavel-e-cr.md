# REQ-FRZ-004 — O fechamento deve produzir `FoundationClosureEvidenceSet` verificável e critérios explícitos de reabertura

- **Tipo:** `GOVERNANCA`
- **Categoria:** `FRZ`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-057`
- **Estado:** `PENDING`
- **Gate:** `Governance/Audit`

## Requisito

O fechamento deve produzir `FoundationClosureEvidenceSet` verificável e critérios explícitos de reabertura

## Rastreabilidade

- **Épicos:** `EPIC-001`, `EPIC-092`
- **Evidência ou teste canônico:** `test_foundation_closure_evidence_set_and_material_reopening_criteria`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
