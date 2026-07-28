# REQ-MOS-001 — A recuperação por mosaico relativo é opcional, posterior ao lote e não bloqueia sucessos já publicados

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MOS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-049`
- **Estado:** `PENDING`
- **Gate:** `Geo/Jobs`

## Requisito

A recuperação por mosaico relativo é opcional, posterior ao lote e não bloqueia sucessos já publicados

## Rastreabilidade

- **Épicos:** `EPIC-018`, `EPIC-098`
- **Evidência ou teste canônico:** `test_relative_mosaic_is_optional_post_batch_and_non_blocking`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
