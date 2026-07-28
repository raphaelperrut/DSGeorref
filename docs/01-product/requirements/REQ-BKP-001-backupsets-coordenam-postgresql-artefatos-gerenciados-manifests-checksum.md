# REQ-BKP-001 — BackupSets coordenam PostgreSQL, artefatos gerenciados, manifests, checksums, versões e ponto de consistência sem copiar implicitamente acervos externos

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `BKP`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-018`
- **Estado:** `PENDING`
- **Gate:** `Ops/Data`

## Requisito

BackupSets coordenam PostgreSQL, artefatos gerenciados, manifests, checksums, versões e ponto de consistência sem copiar implicitamente acervos externos

## Rastreabilidade

- **Épicos:** `EPIC-049`, `EPIC-071`
- **Evidência ou teste canônico:** `test_backupset_consistency_manifest_external_roots`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
