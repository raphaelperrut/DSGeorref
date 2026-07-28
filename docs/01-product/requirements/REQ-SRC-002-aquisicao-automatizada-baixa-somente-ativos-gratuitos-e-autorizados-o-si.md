# REQ-SRC-002 — Aquisição automatizada baixa somente ativos gratuitos e autorizados; o sistema nunca efetua compra, pedido pago ou aceite de cobrança

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SRC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-047`
- **Estado:** `PENDING`
- **Gate:** `Providers/Security`

## Requisito

Aquisição automatizada baixa somente ativos gratuitos e autorizados; o sistema nunca efetua compra, pedido pago ou aceite de cobrança

## Rastreabilidade

- **Épicos:** `EPIC-027`, `EPIC-041`
- **Evidência ou teste canônico:** `test_free_download_only_and_purchase_blocked`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
