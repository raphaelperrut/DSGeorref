# REQ-EPIC-076 — Secrets são gerados com alta entropia, armazenados fora do repositório, injetados por necessidade mínima, rotacionáveis e bloqueiam startup quando inseguros

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-032`
- **Estado:** `PENDING`
- **Gate:** `Security/Ops`

## Requisito

Secrets são gerados com alta entropia, armazenados fora do repositório, injetados por necessidade mínima, rotacionáveis e bloqueiam startup quando inseguros

## Rastreabilidade

- **Épicos:** `EPIC-008`, `EPIC-078`
- **Evidência ou teste canônico:** `test_secret_permissions_rotation_redaction_fail_closed`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
