# REQ-AUTH-IMPL-005 — linking OIDC é explícito e protegido contra account takeover

- **Tipo:** `CONTRATO`
- **Categoria:** `AUTH`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-029`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

linking OIDC é explícito e protegido contra account takeover

## Rastreabilidade

- **Épicos:** `EPIC-008`, `EPIC-009`, `EPIC-010`, `EPIC-011`, `EPIC-041`
- **Evidência ou teste canônico:** `test_req_auth_impl_005`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
