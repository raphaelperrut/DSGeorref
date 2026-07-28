# REQ-SRG-003 — Promoção deve aplicar gate multidimensional sem compensação de hard gates por médias globais

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SRG`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Quality/Release`

## Requisito

Promoção deve aplicar gate multidimensional sem compensação de hard gates por médias globais

## Rastreabilidade

- **Épicos:** `EPIC-028`, `EPIC-043`
- **Evidência ou teste canônico:** `test_multidimensional_promotion_gate_stratified_budgets_uncertainty_and_no_hard_gate_compensation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
