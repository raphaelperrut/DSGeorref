# REQ-UPG-003 — Cutover deve depender de evidence gate multidimensional incluindo invariantes, readers históricos, health e canary

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `UPG`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-035`
- **Estado:** `PENDING`
- **Gate:** `Quality/Release/Data`

## Requisito

Cutover deve depender de evidence gate multidimensional incluindo invariantes, readers históricos, health e canary

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-075`, `EPIC-107`
- **Evidência ou teste canônico:** `test_post_migration_multidimensional_evidence_gate_canary_and_atomic_cutover`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-014/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
