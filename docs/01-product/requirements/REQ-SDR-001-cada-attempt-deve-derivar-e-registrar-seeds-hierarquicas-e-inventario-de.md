# REQ-SDR-001 — Cada attempt deve derivar e registrar seeds hierárquicas e inventário de fontes de aleatoriedade

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SDR`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Geo/AI/Quality`

## Requisito

Cada attempt deve derivar e registrar seeds hierárquicas e inventário de fontes de aleatoriedade

## Rastreabilidade

- **Épicos:** `EPIC-023`, `EPIC-028`, `EPIC-050`
- **Evidência ou teste canônico:** `test_hierarchical_seeds_rng_inventory_stable_ordering_and_checkpoint_compatibility`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006/BC-007/BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
