# REQ-PUB-004 — Releases públicas devem conter metadados de citação, autoria, terceiros e preservação coerentes com versão e digest

- **Tipo:** `FUNCIONAL`
- **Categoria:** `PUB`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-037`
- **Estado:** `PENDING`
- **Gate:** `Governance/Release/Reporting`

## Requisito

Releases públicas devem conter metadados de citação, autoria, terceiros e preservação coerentes com versão e digest

## Rastreabilidade

- **Épicos:** `EPIC-042`, `EPIC-089`
- **Evidência ou teste canônico:** `test_citation_cff_codemeta_authors_notices_release_digest_and_doi_consistency`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Contexts consumidores:** `BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
