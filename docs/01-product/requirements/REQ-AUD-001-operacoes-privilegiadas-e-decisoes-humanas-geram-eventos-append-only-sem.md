# REQ-AUD-001 — Operações privilegiadas e decisões humanas geram eventos append-only, sem sampling, com schema, retenção, digest e acesso próprios

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `AUD`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-055`
- **Estado:** `PENDING`
- **Gate:** `Security/Ops`

## Requisito

Operações privilegiadas e decisões humanas geram eventos append-only, sem sampling, com schema, retenção, digest e acesso próprios

## Rastreabilidade

- **Épicos:** `EPIC-011`, `EPIC-075`
- **Evidência ou teste canônico:** `test_audit_append_only_digest_and_no_sampling`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
