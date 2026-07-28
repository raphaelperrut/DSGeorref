# REQ-AI-008 — Cada capability de IA possui contrato versionado que declara estágio, pré-condições, orçamento, entradas, saídas e razão de elegibilidade antes da execução.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-009`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Cada capability de IA possui contrato versionado que declara estágio, pré-condições, orçamento, entradas, saídas e razão de elegibilidade antes da execução.

## Rastreabilidade

- **Épicos:** `EPIC-029`, `EPIC-050`
- **Evidência ou teste canônico:** `test_stage_capability_contract_preconditions_budget_reason`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-004` — Plano de Processamento e Workflow.
- **Contexts consumidores:** `BC-004/BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
