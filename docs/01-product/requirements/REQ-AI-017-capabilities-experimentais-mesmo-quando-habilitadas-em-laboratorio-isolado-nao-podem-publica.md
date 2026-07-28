# REQ-AI-017 — Capabilities experimentais, mesmo quando habilitadas em laboratório isolado, não podem publicar ArtifactSet aceito nem alterar o resultado vigente sem promoção formal.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-009`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Capabilities experimentais, mesmo quando habilitadas em laboratório isolado, não podem publicar ArtifactSet aceito nem alterar o resultado vigente sem promoção formal.

## Rastreabilidade

- **Épicos:** `EPIC-046`, `EPIC-050`
- **Evidência ou teste canônico:** `test_experimental_capability_cannot_publish_accepted_artifactset`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
