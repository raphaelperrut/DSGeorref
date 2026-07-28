# REQ-SDR-004 — Replay científico e promoção devem preservar hashes do ambiente e classificar divergências sem retenção ilimitada

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SDR`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Quality/Operations/Reporting`

## Requisito

Replay científico e promoção devem preservar hashes do ambiente e classificar divergências sem retenção ilimitada

## Rastreabilidade

- **Épicos:** `EPIC-028`, `EPIC-037`, `EPIC-049`
- **Evidência ou teste canônico:** `test_scientific_reproducibility_record_replay_levels_promotion_matrix_and_retention`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-012/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
