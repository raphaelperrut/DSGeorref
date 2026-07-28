# REQ-RUNTIME-010 — Readiness e capability gates são explícitos, versionados e testáveis.

- **Tipo:** `CONTRATO`
- **Categoria:** `RUNTIME`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-017`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Readiness e capability gates são explícitos, versionados e testáveis.

## Rastreabilidade

- **Épicos:** `EPIC-011`, `EPIC-039`
- **Evidência ou teste canônico:** `test_runtime_decision_10`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
