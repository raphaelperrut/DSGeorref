# REQ-PUB-003 — Providers e assets externos devem carregar policy versionada de direitos, atribuição, cache, transformação e redistribuição

- **Tipo:** `FUNCIONAL`
- **Categoria:** `PUB`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-012`
- **Estado:** `PENDING`
- **Gate:** `Providers/Data/Security`

## Requisito

Providers e assets externos devem carregar policy versionada de direitos, atribuição, cache, transformação e redistribuição

## Rastreabilidade

- **Épicos:** `EPIC-058`, `EPIC-060`, `EPIC-061`
- **Evidência ou teste canônico:** `test_provider_policy_manifest_asset_license_record_expiry_attribution_and_fail_closed_acquisition`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
