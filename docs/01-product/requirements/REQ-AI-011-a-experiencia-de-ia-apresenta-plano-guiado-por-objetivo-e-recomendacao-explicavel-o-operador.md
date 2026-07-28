# REQ-AI-011 — A experiência de IA apresenta plano guiado por objetivo e recomendação explicável; o operador não é exposto a um conjunto bruto de modos técnicos concorrentes.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-051`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

A experiência de IA apresenta plano guiado por objetivo e recomendação explicável; o operador não é exposto a um conjunto bruto de modos técnicos concorrentes.

## Rastreabilidade

- **Épicos:** `EPIC-029`, `EPIC-033`
- **Evidência ou teste canônico:** `test_guided_ai_plan_no_raw_seven_mode_confusion`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-004` — Plano de Processamento e Workflow.
- **Contexts consumidores:** `BC-004/BC-016`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
