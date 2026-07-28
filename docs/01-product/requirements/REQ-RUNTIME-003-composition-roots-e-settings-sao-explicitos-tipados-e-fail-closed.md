# REQ-RUNTIME-003 — composition roots e settings são explícitos, tipados e fail-closed

- **Tipo:** `CONTRATO`
- **Categoria:** `RUNTIME`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-005`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

composition roots e settings são explícitos, tipados e fail-closed

## Rastreabilidade

- **Épicos:** `EPIC-004`
- **Evidência ou teste canônico:** `test_runtime_decision_3`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
