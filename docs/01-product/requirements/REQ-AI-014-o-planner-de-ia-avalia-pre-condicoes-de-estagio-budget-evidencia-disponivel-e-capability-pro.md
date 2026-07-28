# REQ-AI-014 — O planner de IA avalia pré-condições de estágio, budget, evidência disponível e capability profile, registrando de forma determinística a elegibilidade ou o motivo da recusa.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-009`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

O planner de IA avalia pré-condições de estágio, budget, evidência disponível e capability profile, registrando de forma determinística a elegibilidade ou o motivo da recusa.

## Rastreabilidade

- **Épicos:** `EPIC-029`
- **Evidência ou teste canônico:** `test_stage_precondition_budget_evidence_planner`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-004` — Plano de Processamento e Workflow.
- **Contexts consumidores:** `BC-004`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
