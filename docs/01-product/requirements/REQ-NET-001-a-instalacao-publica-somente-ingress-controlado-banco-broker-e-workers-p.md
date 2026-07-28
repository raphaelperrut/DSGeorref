# REQ-NET-001 — A instalação publica somente ingress controlado; banco, broker e workers permanecem privados e acesso remoto exige TLS

- **Tipo:** `FUNCIONAL`
- **Categoria:** `NET`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-032`
- **Estado:** `PENDING`
- **Gate:** `Security/Ops`

## Requisito

A instalação publica somente ingress controlado; banco, broker e workers permanecem privados e acesso remoto exige TLS

## Rastreabilidade

- **Épicos:** `EPIC-041`, `EPIC-079`
- **Evidência ou teste canônico:** `test_single_ingress_tls_private_service_ports`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
