# REQ-UX-001 — Operações normais de seleção, configuração, submissão, acompanhamento e revisão não exigem terminal

- **Tipo:** `FUNCIONAL`
- **Categoria:** `UX`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-014`
- **Estado:** `PENDING`
- **Gate:** `UX`

## Requisito

Operações normais de seleção, configuração, submissão, acompanhamento e revisão não exigem terminal

## Rastreabilidade

- **Épicos:** `EPIC-031`, `EPIC-032`
- **Evidência ou teste canônico:** `e2e_no_terminal_primary_workflow`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
