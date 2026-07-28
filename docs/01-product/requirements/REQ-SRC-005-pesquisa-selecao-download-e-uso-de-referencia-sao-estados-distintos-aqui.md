# REQ-SRC-005 — Pesquisa, seleção, download e uso de referência são estados distintos; aquisição automática exige ativo gratuito, autorizado e policy explícita

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SRC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-047`
- **Estado:** `PENDING`
- **Gate:** `Providers/Security`

## Requisito

Pesquisa, seleção, download e uso de referência são estados distintos; aquisição automática exige ativo gratuito, autorizado e policy explícita

## Rastreabilidade

- **Épicos:** `EPIC-029`, `EPIC-060`
- **Evidência ou teste canônico:** `test_free_acquisition_policy_states_fail_closed_paid_ambiguous`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-004` — Plano de Processamento e Workflow.
- **Contexts consumidores:** `BC-004/BC-005`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
