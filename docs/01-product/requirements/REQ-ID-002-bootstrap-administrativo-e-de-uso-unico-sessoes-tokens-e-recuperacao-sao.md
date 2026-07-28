# REQ-ID-002 — Bootstrap administrativo é de uso único; sessões, tokens e recuperação são revogáveis e auditáveis

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ID`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-029`
- **Estado:** `PENDING`
- **Gate:** `Identity`

## Requisito

Bootstrap administrativo é de uso único; sessões, tokens e recuperação são revogáveis e auditáveis

## Rastreabilidade

- **Épicos:** `EPIC-008`, `EPIC-009`
- **Evidência ou teste canônico:** `test_bootstrap_session_token_recovery`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
