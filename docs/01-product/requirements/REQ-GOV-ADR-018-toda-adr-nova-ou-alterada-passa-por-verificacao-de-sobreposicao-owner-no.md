# REQ-GOV-ADR-018 — Toda ADR nova ou alterada passa por verificação de sobreposição, owner normativo e gate de decisão do Owner.

- **Tipo:** `GOVERNANCA`
- **Categoria:** `GOV`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-006`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Toda ADR nova ou alterada passa por verificação de sobreposição, owner normativo e gate de decisão do Owner.

## Rastreabilidade

- **Épicos:** `EPIC-001`, `EPIC-002`
- **Evidência ou teste canônico:** `test_adr_governance_overlap`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
