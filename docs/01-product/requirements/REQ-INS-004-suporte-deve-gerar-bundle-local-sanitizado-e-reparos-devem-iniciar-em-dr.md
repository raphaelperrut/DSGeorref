# REQ-INS-004 — Suporte deve gerar bundle local sanitizado e reparos devem iniciar em dry-run sem exfiltração automática

- **Tipo:** `FUNCIONAL`
- **Categoria:** `INS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-034`
- **Estado:** `PENDING`
- **Gate:** `Operations/Security/Support`

## Requisito

Suporte deve gerar bundle local sanitizado e reparos devem iniciar em dry-run sem exfiltração automática

## Rastreabilidade

- **Épicos:** `EPIC-075`, `EPIC-080`, `EPIC-108`
- **Evidência ou teste canônico:** `test_sanitized_local_support_bundle_no_exfiltration_and_repair_dry_run`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
