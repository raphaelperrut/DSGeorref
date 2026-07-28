# REQ-AI-010 — A capability de retrieval pode recuperar ou ranquear candidatos de referência, mas não pode gerar GCPs, estimar homografia nem emitir decisão de aceitação.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-009`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

A capability de retrieval pode recuperar ou ranquear candidatos de referência, mas não pode gerar GCPs, estimar homografia nem emitir decisão de aceitação.

## Rastreabilidade

- **Épicos:** `EPIC-022`, `EPIC-029`
- **Evidência ou teste canônico:** `test_retrieval_never_generates_gcp_homography_or_acceptance`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005/BC-004`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
