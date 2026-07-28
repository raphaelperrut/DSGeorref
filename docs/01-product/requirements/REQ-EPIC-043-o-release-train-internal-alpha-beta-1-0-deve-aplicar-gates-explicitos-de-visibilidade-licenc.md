# REQ-EPIC-043 — O release train internal/alpha/beta/1.0 deve aplicar gates explícitos de visibilidade, licença, sanitização, evidência e rollback antes de promover cada estágio.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-037`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

O release train internal/alpha/beta/1.0 deve aplicar gates explícitos de visibilidade, licença, sanitização, evidência e rollback antes de promover cada estágio.

## Rastreabilidade

- **Épicos:** `EPIC-042`, `EPIC-085`, `EPIC-089`
- **Evidência ou teste canônico:** `test_release_train_visibility_license_sanitization_and_beta_gate`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Contexts consumidores:** `BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
