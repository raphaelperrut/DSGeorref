# REQ-RAS-004 — O kernel de reamostragem é escolhido por banda, escala de conteúdo e semântica de máscara, preservando validade.

- **Tipo:** `CONTRATO`
- **Categoria:** `RAS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-042`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

O kernel de reamostragem é escolhido por banda, escala de conteúdo e semântica de máscara, preservando validade.

## Rastreabilidade

- **Épicos:** `EPIC-095`, `EPIC-097`
- **Evidência ou teste canônico:** `test_resampling_kernel_by_band_content_scale_and_mask_integrity`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
