# REQ-UPG-004 — Falhas devem seguir recuperação por fase, bloqueando writers em estado incerto e usando forward-fix ou restore após irreversibilidade

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `UPG`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-035`
- **Estado:** `PENDING`
- **Gate:** `Reliability/Operations/Data`

## Requisito

Falhas devem seguir recuperação por fase, bloqueando writers em estado incerto e usando forward-fix ou restore após irreversibilidade

## Rastreabilidade

- **Épicos:** `EPIC-072`, `EPIC-105`, `EPIC-107`
- **Evidência ou teste canônico:** `test_phase_aware_recovery_writer_blocking_forward_fix_compatible_rollback_and_validated_restore`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-013/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
