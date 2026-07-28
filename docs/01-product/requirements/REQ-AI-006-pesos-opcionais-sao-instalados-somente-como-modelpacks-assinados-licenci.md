# REQ-AI-006 — Pesos opcionais são instalados somente como ModelPacks assinados, licenciados, opt-in e verificáveis

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-052`
- **Estado:** `PENDING`
- **Gate:** `AI/Security`

## Requisito

Pesos opcionais são instalados somente como ModelPacks assinados, licenciados, opt-in e verificáveis

## Rastreabilidade

- **Épicos:** `EPIC-080`
- **Evidência ou teste canônico:** `test_modelpack_signature_license_hash_offline_import`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Contexts consumidores:** `BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
