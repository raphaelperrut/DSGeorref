# REQ-EPIC-088 — O laboratório experimental permanece desabilitado por padrão nos profiles operacionais e, quando ativado isoladamente, não pode publicar resultados aceitos nem alterar artifacts vigentes.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-009`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

O laboratório experimental permanece desabilitado por padrão nos profiles operacionais e, quando ativado isoladamente, não pode publicar resultados aceitos nem alterar artifacts vigentes.

## Rastreabilidade

- **Épicos:** `EPIC-050`, `EPIC-088`
- **Evidência ou teste canônico:** `test_experimental_lab_disabled_and_cannot_publish_accepted_artifactset`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-009` — Recuperação Assistida por IA e Governança de Modelos.
- **Contexts consumidores:** `BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
