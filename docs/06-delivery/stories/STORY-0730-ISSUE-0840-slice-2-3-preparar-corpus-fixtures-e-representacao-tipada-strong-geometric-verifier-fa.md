# STORY-0730 / ISSUE-0840 — Slice 2/3 — Preparar corpus, fixtures e representação tipada: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile [REQ-EST, REQ-FS1, REQ-MSK, REQ-QUAL, REQ-RAS, REQ-REF]

- **Tipo:** `História implementável`
- **Estado:** `Ready-after-authorization`
- **Épico pai:** `EPIC-024`
- **Sprint:** `SPRINT-005`
- **Domínio:** `GEO`
- **Bounded Context:** `BC-007 — Verificação Geométrica e Qualidade`
- **Papel executor:** `Geoprocessamento`
- **TaskEnvelope:** `.codex/tasks/TASK-0730.json`

## História de usuário

Como executor especializado, preciso entregar este slice limitado de requisitos para que a capacidade de **Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile** avance sem mudança ampla ou inferência não documentada.

## Resultado verificável

Slice 2/3 concluído com contrato, implementação ou evidência compatível com o papel executor e todos os requisitos abaixo demonstrados.

## Escopo

- `src/geo/dsgeorref_geo/contexts/geometric_quality/strong-geometric-verifier-fail-closed-para-homografia/est-fs1-msk-parte-2/**`
## Fora de escopo

- requisitos pertencentes a outro slice;
- alteração de ADR ou contrato congelado sem change control;
- código em diretórios orientados por ticket;
- refatoração não necessária à aceitação.

## Requisitos

`REQ-EST-001`, `REQ-FS1-002`, `REQ-FS1-003`, `REQ-FS1-008`, `REQ-FS1-009`, `REQ-FS1-010`, `REQ-MSK-001`, `REQ-QUAL-003`, `REQ-RAS-003`, `REQ-REF-001`

## ADRs e contratos

- `ADR-007`
- `ADR-008`
- contratos e ADRs referenciados pelos requisitos.

## Dependências


`STORY-0136`

## Critérios de aceitação

- [ ] Cada requisito do slice possui evidência explícita: REQ-EST-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-MSK-001, REQ-QUAL-003, REQ-RAS-003, REQ-REF-001.
- [ ] O write scope é estável, disjunto e não usa identificador de ticket em código de produção.
- [ ] Estados de falha aplicáveis são testados sem fallback silencioso.
- [ ] O handoff registra impacto em contratos, riscos e rollback.

## Testes obrigatórios

- `test_usac_magsac_default_explicit_ransac_no_silent_switch`
- `test_first_functional_slice_decision_02`
- `test_first_functional_slice_decision_03`
- `test_first_functional_slice_decision_08`
- `test_first_functional_slice_decision_09`
- `test_first_functional_slice_decision_10`
- `test_near_black_white_border_excluded_without_crop`
- `test_input_output_deformation_profile_and_heatmap`
- `test_resolution_native_information_jacobian_limits_and_no_false_superresolution`
- `test_disjoint_components_no_forced_edge_per_image_sgv`

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

Leia `AGENTS.md`, o papel `.codex/roles/ROLE-007-geoprocessamento.md`, esta história e `TASK-0730`. Trabalhe somente nos paths permitidos, entregue apenas este slice e interrompa diante de qualquer condição de parada.

## Revisão SAR

- **Granularidade:** `PASS` — 10 requisitos;
- **Write scope:** `PASS` — package estável;
- **Contract freeze:** obrigatório quando aplicável;
- **Gate:** depende de autorização externa de implementação.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `BC-006, BC-009, BC-010`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0840-01, AC-ISSUE-0840-02, AC-ISSUE-0840-03, AC-ISSUE-0840-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-015`, `ADR-023`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-015`, `ADR-023`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-048`, `ADR-049`, `ADR-050`, `ADR-055`
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
| Arquivos | 1 write scopes; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 10 testes obrigatórios | PASS |
| Artefatos | PRODUCT_AND_EVIDENCE | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-005-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-010, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
