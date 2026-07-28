# REQ-AI-015 — O runtime de inferência monta pesos em modo somente leitura, valida assinatura e hash antes da execução e impede alteração persistente dos ModelPacks.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-033`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

O runtime de inferência monta pesos em modo somente leitura, valida assinatura e hash antes da execução e impede alteração persistente dos ModelPacks.

## Rastreabilidade

- **Épicos:** `EPIC-050`, `EPIC-080`
- **Evidência ou teste canônico:** `test_inference_only_runtime_no_training_or_weight_mutation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-009` — Recuperação Assistida por IA e Governança de Modelos.
- **Contexts consumidores:** `BC-009/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
