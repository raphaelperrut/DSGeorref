# REQ-ART-003 — ArtifactSets são imutáveis e publicados atomicamente somente após SGV, validação de formato e checksums

- **Tipo:** `CONTRATO`
- **Categoria:** `ART`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-023`
- **Estado:** `PENDING`
- **Gate:** `Data/Quality`

## Requisito

ArtifactSets são imutáveis e publicados atomicamente somente após SGV, validação de formato e checksums

## Rastreabilidade

- **Épicos:** `EPIC-012`, `EPIC-046`
- **Evidência ou teste canônico:** `test_atomic_artifactset_publication_failure_recovery`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Contexts consumidores:** `BC-003/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
