# REQ-RAS-003 — A resolução de saída preserva informação nativa, respeita limites Jacobianos e não declara super-resolução falsa.

- **Tipo:** `CONTRATO`
- **Categoria:** `RAS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-042`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

A resolução de saída preserva informação nativa, respeita limites Jacobianos e não declara super-resolução falsa.

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-097`
- **Evidência ou teste canônico:** `test_resolution_native_information_jacobian_limits_and_no_false_superresolution`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
