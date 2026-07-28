# REQ-QUAL-004 — QualityProfiles oficiais são imutáveis, versionados, calibrados e vinculados ao corpus; customizações são clones auditados e não desativam hard gates

- **Tipo:** `FUNCIONAL`
- **Categoria:** `QUAL`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-046`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

QualityProfiles oficiais são imutáveis, versionados, calibrados e vinculados ao corpus; customizações são clones auditados e não desativam hard gates

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-025`
- **Evidência ou teste canônico:** `test_quality_profile_immutable_version_hash_calibration_clone`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
