# REQ-EPIC-035 — Revisão humana altera apenas gates revisáveis; o veredito automático e hard gates permanecem imutáveis e auditáveis

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-046`
- **Estado:** `PENDING`
- **Gate:** `Quality/UX`

## Requisito

Revisão humana altera apenas gates revisáveis; o veredito automático e hard gates permanecem imutáveis e auditáveis

## Rastreabilidade

- **Épicos:** `EPIC-034`, `EPIC-035`
- **Evidência ou teste canônico:** `test_reviewable_gate_and_hard_gate_non_override`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-011`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
