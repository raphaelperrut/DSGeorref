# REQ-CAC-001 — Cache externo é endereçado por conteúdo, deduplicado, governado por licença/retention e protegido quando ligado à reprodução

- **Tipo:** `FUNCIONAL`
- **Categoria:** `CAC`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-047`
- **Estado:** `PENDING`
- **Gate:** `Data/Providers`

## Requisito

Cache externo é endereçado por conteúdo, deduplicado, governado por licença/retention e protegido quando ligado à reprodução

## Rastreabilidade

- **Épicos:** `EPIC-049`, `EPIC-061`
- **Evidência ou teste canônico:** `test_content_addressed_cache_license_retention_lineage_gc`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
