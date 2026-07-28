# REQ-MSK-001 — Bordas sem terreno são excluídas da análise por máscara tolerante a tons próximos de preto/branco, mas permanecem integralmente na saída por padrão

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MSK`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-042`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

Bordas sem terreno são excluídas da análise por máscara tolerante a tons próximos de preto/branco, mas permanecem integralmente na saída por padrão

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-045`
- **Evidência ou teste canônico:** `test_near_black_white_border_excluded_without_crop`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
