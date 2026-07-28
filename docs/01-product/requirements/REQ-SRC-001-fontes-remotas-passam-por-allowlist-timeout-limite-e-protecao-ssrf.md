# REQ-SRC-001 — Fontes remotas passam por allowlist, timeout, limite e proteção SSRF

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SRC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-047`
- **Estado:** `PENDING`
- **Gate:** `Security`

## Requisito

Fontes remotas passam por allowlist, timeout, limite e proteção SSRF

## Rastreabilidade

- **Épicos:** `EPIC-027`
- **Evidência ou teste canônico:** `ssrf_provider_gateway`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
