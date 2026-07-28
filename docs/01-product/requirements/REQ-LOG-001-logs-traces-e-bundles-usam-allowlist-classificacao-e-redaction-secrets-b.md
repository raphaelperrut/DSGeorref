# REQ-LOG-001 — Logs, traces e bundles usam allowlist, classificação e redaction; secrets, bytes de imagem e paths absolutos são proibidos por padrão

- **Tipo:** `FUNCIONAL`
- **Categoria:** `LOG`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-032`
- **Estado:** `PENDING`
- **Gate:** `Security/Privacy`

## Requisito

Logs, traces e bundles usam allowlist, classificação e redaction; secrets, bytes de imagem e paths absolutos são proibidos por padrão

## Rastreabilidade

- **Épicos:** `EPIC-039`, `EPIC-076`
- **Evidência ou teste canônico:** `test_log_redaction_and_support_bundle_fail_closed`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
