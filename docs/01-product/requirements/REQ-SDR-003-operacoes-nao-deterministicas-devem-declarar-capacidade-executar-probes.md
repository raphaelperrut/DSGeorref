# REQ-SDR-003 — Operações não determinísticas devem declarar capacidade, executar probes e usar consenso orçado quando aplicável

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SDR`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `AI/Platform/Quality`

## Requisito

Operações não determinísticas devem declarar capacidade, executar probes e usar consenso orçado quando aplicável

## Rastreabilidade

- **Épicos:** `EPIC-028`, `EPIC-050`, `EPIC-082`
- **Evidência ou teste canônico:** `test_nondeterministic_capability_declaration_repeatability_probes_and_bounded_consensus`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-009/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
