# REQ-AI-013 — Cada capability de IA possui lifecycle, versionamento, promoção, desativação e rollback independentes, sem acoplamento obrigatório às demais capabilities.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-009`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Cada capability de IA possui lifecycle, versionamento, promoção, desativação e rollback independentes, sem acoplamento obrigatório às demais capabilities.

## Rastreabilidade

- **Épicos:** `EPIC-050`
- **Evidência ou teste canônico:** `test_independent_ai_capability_lifecycle_and_promotion`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-009` — Recuperação Assistida por IA e Governança de Modelos.
- **Contexts consumidores:** `BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
