# REQ-AI-007 — Catálogo governado de capacidades sem importação de código anterior

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-051`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

O sistema deve manter um catálogo versionado das capacidades de processamento previstas pelo produto, com nome estável, estágio, entradas, saídas, requisitos de hardware, orçamento, nível de determinismo, limitações e forma de explicação ao operador. O catálogo pode usar sistemas anteriores somente como fonte de requisitos e corpus; importar código, plugins ou runtime desses sistemas é proibido.

## Rastreabilidade

- **Épicos:** `EPIC-006`
- **Evidência ou teste canônico:** `test_reference_capability_inventory_no_code_import`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é atendido quando o catálogo possui schemas versionados, cada capability tem owner e contrato, e os testes demonstram que nenhum pacote, módulo ou runtime de sistemas anteriores é importado pela aplicação greenfield.
