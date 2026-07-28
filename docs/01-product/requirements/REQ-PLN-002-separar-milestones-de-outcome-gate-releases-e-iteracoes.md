# REQ-PLN-002 — separar milestones de outcome/gate, releases e iterações

- **Tipo:** `FUNCIONAL`
- **Categoria:** `PLN`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-037`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

separar milestones de outcome/gate, releases e iterações

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-110`
- **Evidência ou teste canônico:** `test_layered_milestones_gate_release_mapping`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
