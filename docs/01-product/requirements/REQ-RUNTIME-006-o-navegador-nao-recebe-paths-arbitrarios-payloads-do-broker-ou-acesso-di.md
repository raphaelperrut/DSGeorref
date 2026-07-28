# REQ-RUNTIME-006 — O navegador não recebe paths arbitrários, payloads do broker ou acesso direto à persistência.

- **Tipo:** `CONTRATO`
- **Categoria:** `RUNTIME`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-021`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

O navegador não recebe paths arbitrários, payloads do broker ou acesso direto à persistência.

## Rastreabilidade

- **Épicos:** `EPIC-004`, `EPIC-011`
- **Evidência ou teste canônico:** `test_runtime_decision_6`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-002`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
