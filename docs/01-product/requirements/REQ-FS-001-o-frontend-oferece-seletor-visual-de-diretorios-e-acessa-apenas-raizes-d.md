# REQ-FS-001 — O frontend oferece seletor visual de diretórios e acessa apenas raízes de workspace registradas, sem path traversal ou escape por symlink

- **Tipo:** `FUNCIONAL`
- **Categoria:** `FS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-014`
- **Estado:** `PENDING`
- **Gate:** `Data/Security`

## Requisito

O frontend oferece seletor visual de diretórios e acessa apenas raízes de workspace registradas, sem path traversal ou escape por symlink

## Rastreabilidade

- **Épicos:** `EPIC-012`, `EPIC-031`, `EPIC-041`
- **Evidência ou teste canônico:** `test_directory_picker_path_traversal_symlink_escape`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Contexts consumidores:** `BC-003/BC-016/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
