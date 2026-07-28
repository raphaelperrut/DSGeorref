# REQ-ANC-005 — O workspace deve vincular cada âncora criada no contexto do mosaico à imagem e ao pixel original, com referência sincronizada e provenance

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ANC`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-049`
- **Estado:** `PENDING`
- **Gate:** `Web/Geo`

## Requisito

O workspace deve vincular cada âncora criada no contexto do mosaico à imagem e ao pixel original, com referência sincronizada e provenance

## Rastreabilidade

- **Épicos:** `EPIC-032`, `EPIC-100`
- **Evidência ou teste canônico:** `test_multiview_anchor_workspace_source_pixel_provenance_and_refinement`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
