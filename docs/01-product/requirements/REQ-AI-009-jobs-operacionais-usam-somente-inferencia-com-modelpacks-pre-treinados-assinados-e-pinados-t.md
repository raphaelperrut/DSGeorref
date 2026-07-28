# REQ-AI-009 — Jobs operacionais usam somente inferência com ModelPacks pré-treinados, assinados e pinados; treinamento, fine-tuning ou mutação de pesos durante jobs são proibidos.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-052`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Jobs operacionais usam somente inferência com ModelPacks pré-treinados, assinados e pinados; treinamento, fine-tuning ou mutação de pesos durante jobs são proibidos.

## Rastreabilidade

- **Épicos:** `EPIC-049`, `EPIC-050`
- **Evidência ou teste canônico:** `test_inference_first_no_training_or_weight_mutation_in_jobs`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
