# REQ-BAT-001 — O lote suporta componentes independentes e sucesso parcial explícito, preservando sucessos válidos e falhas acionáveis por subconjunto

- **Tipo:** `FUNCIONAL`
- **Categoria:** `BAT`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-039`
- **Estado:** `ACCEPTED`
- **Gate:** `Jobs/UX`

## Requisito

O lote suporta componentes independentes e sucesso parcial explícito, preservando sucessos válidos e falhas acionáveis por subconjunto

## Rastreabilidade

- **Épicos:** `EPIC-034`, `EPIC-057`
- **Evidência ou teste canônico:** `test_independent_components_partial_success_retry_subset`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-012`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
