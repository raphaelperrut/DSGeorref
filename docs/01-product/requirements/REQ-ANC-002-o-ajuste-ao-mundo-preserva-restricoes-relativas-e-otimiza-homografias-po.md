# REQ-ANC-002 — O ajuste ao mundo preserva restrições relativas e otimiza homografias por imagem, sem presumir uma única folha rígida

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ANC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-045`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

O ajuste ao mundo preserva restrições relativas e otimiza homografias por imagem, sem presumir uma única folha rígida

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-099`
- **Evidência ou teste canônico:** `test_joint_anchored_per_image_homography_optimization_and_component_split`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
