# REQ-MOS-006 — Sobreposições preservam a pilha de fontes; seamlines selecionam fontes analíticas e blending é restrito ao preview, com provenance por tile/região

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MOS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-049`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

Sobreposições preservam a pilha de fontes; seamlines selecionam fontes analíticas e blending é restrito ao preview, com provenance por tile/região

## Rastreabilidade

- **Épicos:** `EPIC-095`, `EPIC-098`
- **Evidência ou teste canônico:** `test_overlap_source_stack_seamline_analytical_preview_blend_and_provenance`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
