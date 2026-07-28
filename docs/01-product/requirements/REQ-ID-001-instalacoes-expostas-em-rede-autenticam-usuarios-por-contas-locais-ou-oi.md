# REQ-ID-001 — Instalações expostas em rede autenticam usuários por contas locais ou OIDC e protegem operações administrativas

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ID`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-029`
- **Estado:** `PENDING`
- **Gate:** `Identity`

## Requisito

Instalações expostas em rede autenticam usuários por contas locais ou OIDC e protegem operações administrativas

## Rastreabilidade

- **Épicos:** `EPIC-008`
- **Evidência ou teste canônico:** `test_network_authentication_local_oidc`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
