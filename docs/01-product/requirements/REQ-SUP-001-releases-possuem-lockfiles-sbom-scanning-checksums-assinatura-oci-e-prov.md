# REQ-SUP-001 — Releases possuem lockfiles, SBOM, scanning, checksums, assinatura OCI e provenance verificável

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SUP`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-024`
- **Estado:** `PENDING`
- **Gate:** `Security/Release`

## Requisito

Releases possuem lockfiles, SBOM, scanning, checksums, assinatura OCI e provenance verificável

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-080`
- **Evidência ou teste canônico:** `test_release_sbom_signature_provenance_immutable_pins`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
