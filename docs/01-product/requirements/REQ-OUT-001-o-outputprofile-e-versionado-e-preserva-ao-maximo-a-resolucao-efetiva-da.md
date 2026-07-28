# REQ-OUT-001 — O OutputProfile é versionado e preserva ao máximo a resolução efetiva da entrada, sem redução ou superamostragem injustificada

- **Tipo:** `FUNCIONAL`
- **Categoria:** `OUT`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-042`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

O OutputProfile é versionado e preserva ao máximo a resolução efetiva da entrada, sem redução ou superamostragem injustificada

## Rastreabilidade

- **Épicos:** `EPIC-040`, `EPIC-044`
- **Evidência ou teste canônico:** `test_native_resolution_policy_resampling_ratio`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
