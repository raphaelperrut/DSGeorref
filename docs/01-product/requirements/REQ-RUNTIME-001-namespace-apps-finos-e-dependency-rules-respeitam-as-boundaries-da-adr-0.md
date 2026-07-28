# REQ-RUNTIME-001 — namespace, apps finos e dependency rules respeitam as boundaries da ADR-002

- **Tipo:** `CONTRATO`
- **Categoria:** `RUNTIME`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-002`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

namespace, apps finos e dependency rules respeitam as boundaries da ADR-002

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-004`
- **Evidência ou teste canônico:** `test_runtime_decision_1`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
