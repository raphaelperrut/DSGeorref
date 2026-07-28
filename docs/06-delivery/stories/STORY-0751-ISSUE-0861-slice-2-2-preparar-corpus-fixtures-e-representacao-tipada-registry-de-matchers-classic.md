# STORY-0751 / ISSUE-0861 — Slice 2/2 — Preparar corpus, fixtures e representação tipada: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark [REQ-AIE, REQ-EPIC, REQ-SCH, REQ-SDR]

- **Tipo:** `História implementável`
- **Estado:** `Ready-after-authorization`
- **Épico pai:** `EPIC-050`
- **Sprint:** `SPRINT-006`
- **Domínio:** `GEO`
- **Bounded Context:** `BC-009 — Recuperação Assistida por IA e Governança de Modelos`
- **Papel executor:** `Geoprocessamento`
- **TaskEnvelope:** `.codex/tasks/TASK-0751.json`

## História de usuário

Como executor especializado, preciso entregar este slice limitado de requisitos para que a capacidade de **registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark** avance sem mudança ampla ou inferência não documentada.

## Resultado verificável

Slice 2/2 concluído com contrato, implementação ou evidência compatível com o papel executor e todos os requisitos abaixo demonstrados.

## Escopo

- `src/geo/dsgeorref_geo/contexts/ai_recovery/registry-de-matchers-classicos-ia-escalonamento-explic/aie-epic-sch-parte-2/**`
## Fora de escopo

- requisitos pertencentes a outro slice;
- alteração de ADR ou contrato congelado sem change control;
- código em diretórios orientados por ticket;
- refatoração não necessária à aceitação.

## Requisitos

`REQ-AIE-009`, `REQ-AIE-010`, `REQ-EPIC-088`, `REQ-SCH-003`, `REQ-SDR-001`

## ADRs e contratos

- `ADR-007`
- `ADR-008`
- contratos e ADRs referenciados pelos requisitos.

## Dependências


`STORY-0302`

## Critérios de aceitação

- [ ] Cada requisito do slice possui evidência explícita: REQ-AIE-009, REQ-AIE-010, REQ-EPIC-088, REQ-SCH-003, REQ-SDR-001.
- [ ] O write scope é estável, disjunto e não usa identificador de ticket em código de produção.
- [ ] Estados de falha aplicáveis são testados sem fallback silencioso.
- [ ] O handoff registra impacto em contratos, riscos e rollback.

## Testes obrigatórios

- `test_ai_escalation_decision_09`
- `test_ai_escalation_decision_10`
- `test_experimental_lab_disabled_and_cannot_publish_accepted_artifactset`
- `test_device_aware_gpu_leases_vram_budgets_model_residency_and_explicit_fallback`
- `test_hierarchical_seeds_rng_inventory_stable_ordering_and_checkpoint_compatibility`

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

Leia `AGENTS.md`, o papel `.codex/roles/ROLE-007-geoprocessamento.md`, esta história e `TASK-0751`. Trabalhe somente nos paths permitidos, entregue apenas este slice e interrompa diante de qualquer condição de parada.

## Revisão SAR

- **Granularidade:** `PASS` — 5 requisitos;
- **Write scope:** `PASS` — package estável;
- **Contract freeze:** obrigatório quando aplicável;
- **Gate:** depende de autorização externa de implementação.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-009` — Recuperação Assistida por IA e Governança de Modelos.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `BC-004, BC-010, BC-015`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0861-01, AC-ISSUE-0861-02, AC-ISSUE-0861-03, AC-ISSUE-0861-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-030`, `ADR-037`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-053`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-017`, `ADR-030`, `ADR-037`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-003`, `SPEC-004`, `SPEC-005`
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
| IA | APPLICABLE | PASS |
| Testes | 5 testes obrigatórios | PASS |
| Artefatos | PRODUCT_AND_EVIDENCE | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-006-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-010, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
