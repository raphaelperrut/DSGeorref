# REQ-AI-016 — A interface explica quando a IA foi usada, qual capability e ModelPack foram selecionados, o motivo, custo, limitações e controles disponíveis, sem expor modos técnicos redundantes.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-009`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

A interface explica quando a IA foi usada, qual capability e ModelPack foram selecionados, o motivo, custo, limitações e controles disponíveis, sem expor modos técnicos redundantes.

## Rastreabilidade

- **Épicos:** `EPIC-036`, `EPIC-084`
- **Evidência ou teste canônico:** `test_guided_explainable_ai_ux_without_seven_modes`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
