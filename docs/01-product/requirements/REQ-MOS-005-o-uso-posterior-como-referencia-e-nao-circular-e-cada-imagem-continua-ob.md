# REQ-MOS-005 — O uso posterior como referência é não circular e cada imagem continua obrigada a reestimar e passar pelo SGV

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MOS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-049`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

O uso posterior como referência é não circular e cada imagem continua obrigada a reestimar e passar pelo SGV

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-098`
- **Evidência ou teste canônico:** `test_leave_one_out_non_circular_reference_and_independent_sgv`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
