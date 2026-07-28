# REQ-SRG-004 — Bundles científicos devem coexistir, permitir canary/dual-run, pinning e rollback sem alterar artifacts históricos

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SRG`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Release/Operations/Data`

## Requisito

Bundles científicos devem coexistir, permitir canary/dual-run, pinning e rollback sem alterar artifacts históricos

## Rastreabilidade

- **Épicos:** `EPIC-028`, `EPIC-043`, `EPIC-049`
- **Evidência ou teste canônico:** `test_versioned_scientific_pipeline_bundle_dual_run_pinning_atomic_promotion_and_rollback`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-015/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
