# REQ-RMV-004 — O lifecycle do componente deve separar candidato, verificado, ancorável e ancorado para recuperação sem transferir aceitação às imagens

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-050`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

O lifecycle do componente deve separar candidato, verificado, ancorável e ancorado para recuperação sem transferir aceitação às imagens

## Rastreabilidade

- **Épicos:** `EPIC-099`, `EPIC-101`
- **Evidência ou teste canônico:** `test_relative_component_promotion_lifecycle_and_no_image_acceptance_transfer`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-008` — Mosaico Relativo.
- **Contexts consumidores:** `BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
