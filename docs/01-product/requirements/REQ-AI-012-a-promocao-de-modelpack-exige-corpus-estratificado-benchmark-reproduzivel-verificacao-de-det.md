# REQ-AI-012 — A promoção de ModelPack exige corpus estratificado, benchmark reproduzível, verificação de determinismo, gate científico e rollback para a versão anterior.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-052`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

A promoção de ModelPack exige corpus estratificado, benchmark reproduzível, verificação de determinismo, gate científico e rollback para a versão anterior.

## Rastreabilidade

- **Épicos:** `EPIC-028`, `EPIC-050`
- **Evidência ou teste canônico:** `test_modelpack_stratified_promotion_and_reproducibility_gate`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
