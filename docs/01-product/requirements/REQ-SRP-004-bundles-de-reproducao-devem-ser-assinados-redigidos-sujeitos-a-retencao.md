# REQ-SRP-004 — Bundles de reprodução devem ser assinados, redigidos, sujeitos a retenção e livres de payloads raster e credenciais

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SRP`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Operations/Security/Reporting`

## Requisito

Bundles de reprodução devem ser assinados, redigidos, sujeitos a retenção e livres de payloads raster e credenciais

## Rastreabilidade

- **Épicos:** `EPIC-073`, `EPIC-076`, `EPIC-104`
- **Evidência ou teste canônico:** `test_signed_redacted_retained_scheduler_reproduction_bundle_limits`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-014/BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
