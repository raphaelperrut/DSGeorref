# REQ-REV-003 — Toda correção manual cria CorrectionSet imutável, nova tentativa e revalidação integral pelo Strong Geometric Verifier

- **Tipo:** `FUNCIONAL`
- **Categoria:** `REV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-048`
- **Estado:** `PENDING`
- **Gate:** `Quality/UX`

## Requisito

Toda correção manual cria CorrectionSet imutável, nova tentativa e revalidação integral pelo Strong Geometric Verifier

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-049`, `EPIC-062`
- **Evidência ou teste canônico:** `test_correctionset_new_attempt_full_sgv_immutable_history`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-013/BC-011`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
