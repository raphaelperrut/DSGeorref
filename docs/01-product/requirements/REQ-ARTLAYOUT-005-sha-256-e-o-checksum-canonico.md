# REQ-ARTLAYOUT-005 — SHA-256 é o checksum canônico

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `ARTLAYOUT`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-024`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Todo ArtifactSet e todo objeto persistido sujeito a verificação de integridade devem registrar SHA-256 como checksum canônico; hashes auxiliares podem acelerar verificações locais, mas não podem substituir o valor normativo.

## Rastreabilidade

- **Épicos:** `EPIC-026`, `EPIC-078`
- **Evidência ou teste canônico:** `test_req_artlayout_005`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
