# REQ-ANC-006 — A suficiência das âncoras deve considerar cobertura, condicionamento, diversidade e ganho marginal, não somente contagem

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ANC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-049`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

A suficiência das âncoras deve considerar cobertura, condicionamento, diversidade e ganho marginal, não somente contagem

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-100`
- **Evidência ou teste canônico:** `test_anchor_coverage_conditioning_diversity_marginal_gain_and_stop_rule`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
