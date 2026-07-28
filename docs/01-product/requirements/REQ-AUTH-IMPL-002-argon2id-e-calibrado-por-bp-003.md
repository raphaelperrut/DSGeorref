# REQ-AUTH-IMPL-002 — Argon2id é calibrado por BP-003

- **Tipo:** `CONTRATO`
- **Categoria:** `AUTH`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-028`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Os parâmetros de Argon2id usados para armazenamento de senhas devem ser selecionados e versionados pelo BP-003, respeitar os limites de recurso da instância e ser recalibrados somente mediante evidência reproduzível.

## Rastreabilidade

- **Épicos:** `EPIC-008`, `EPIC-009`, `EPIC-010`, `EPIC-011`, `EPIC-041`
- **Evidência ou teste canônico:** `test_req_auth_impl_002`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
