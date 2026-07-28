# STORY-0718 / ISSUE-0828 — Slice 1/3 — Implementar persistência e migrations: raízes de workspace, API de navegação segura, catálogo, hashes e lineage [REQ-ART, REQ-ARTLAYOUT, REQ-CAT, REQ-DBSCHEMA, REQ-FS]

- **Tipo:** `História implementável`
- **Estado:** `Ready-after-authorization`
- **Épico pai:** `EPIC-012`
- **Sprint:** `SPRINT-002`
- **Domínio:** `DAT`
- **Bounded Context:** `BC-003 — Projetos, Workspace e Assets`
- **Papel executor:** `Backend`
- **TaskEnvelope:** `.codex/tasks/TASK-0718.json`

## História de usuário

Como executor especializado, preciso entregar este slice limitado de requisitos para que a capacidade de **raízes de workspace, API de navegação segura, catálogo, hashes e lineage** avance sem mudança ampla ou inferência não documentada.

## Resultado verificável

Slice 1/3 concluído com contrato, implementação ou evidência compatível com o papel executor e todos os requisitos abaixo demonstrados.

## Escopo

- `src/backend/dsgeorref/contexts/project_workspace/application/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/art-artlayout-cat-parte-1/**`
- `src/backend/dsgeorref/contexts/project_workspace/adapters/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/art-artlayout-cat-parte-1/**`
## Fora de escopo

- requisitos pertencentes a outro slice;
- alteração de ADR ou contrato congelado sem change control;
- código em diretórios orientados por ticket;
- refatoração não necessária à aceitação.

## Requisitos

`REQ-ART-001`, `REQ-ART-003`, `REQ-ARTLAYOUT-002`, `REQ-CAT-001`, `REQ-DBSCHEMA-002`, `REQ-DBSCHEMA-003`, `REQ-DBSCHEMA-004`, `REQ-DBSCHEMA-006`, `REQ-DBSCHEMA-009`, `REQ-FS-001`

## ADRs e contratos

- `ADR-007`
- `ADR-008`
- contratos e ADRs referenciados pelos requisitos.

## Dependências


`STORY-0056`

## Critérios de aceitação

- [ ] Cada requisito do slice possui evidência explícita: REQ-ART-001, REQ-ART-003, REQ-ARTLAYOUT-002, REQ-CAT-001, REQ-DBSCHEMA-002, REQ-DBSCHEMA-003, REQ-DBSCHEMA-004, REQ-DBSCHEMA-006, REQ-DBSCHEMA-009, REQ-FS-001.
- [ ] O write scope é estável, disjunto e não usa identificador de ticket em código de produção.
- [ ] Estados de falha aplicáveis são testados sem fallback silencioso.
- [ ] O handoff registra impacto em contratos, riscos e rollback.

## Testes obrigatórios

- `artifact_lineage_consistency`
- `test_atomic_artifactset_publication_failure_recovery`
- `test_req_artlayout_002`
- `test_catalog_190k_metadata_pagination_search`
- `test_req_dbschema_002`
- `test_req_dbschema_003`
- `test_req_dbschema_004`
- `test_req_dbschema_006`
- `test_req_dbschema_009`
- `test_directory_picker_path_traversal_symlink_escape`

## Evidências obrigatórias

- resultados dos testes no commit candidato;
- lista de arquivos alterados e justificativa de escopo;
- handoff com limitações e riscos residuais;
- aprovação independente aplicável.

## Condições de parada

- contrato necessário ausente ou contraditório;
- write scope colide com lane ativa;
- requisito exige decisão não registrada;
- aceitação não pode ser demonstrada objetivamente.

## Prompt de execução Codex

Leia `AGENTS.md`, o papel `.codex/roles/ROLE-004-backend.md`, esta história e `TASK-0718`. Trabalhe somente nos paths permitidos, entregue apenas este slice e interrompa diante de qualquer condição de parada.

## Revisão SAR

- **Granularidade:** `PASS` — 10 requisitos;
- **Write scope:** `PASS` — package estável;
- **Contract freeze:** obrigatório quando aplicável;
- **Gate:** depende de autorização externa de implementação.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Impacto no modelo:** `CROSS_CONTEXT_INTEGRATION`.
- **Upstreams permitidos:** `BC-002`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0828-01, AC-ISSUE-0828-02, AC-ISSUE-0828-03, AC-ISSUE-0828-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-016`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-025`, `ADR-043`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-025`, `ADR-026`, `ADR-043`, `ADR-055`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`, `SPEC-005`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessores explícitos | PASS |
| Arquivos | 2 write scopes; deny scopes declarados | PASS |
| API | APPLICABLE | PASS |
| Banco | APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 10 testes obrigatórios | PASS |
| Artefatos | PRODUCT_AND_EVIDENCE | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Arquiteto, QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-002-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
