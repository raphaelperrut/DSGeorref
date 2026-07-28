# STORY-0704 / ISSUE-0814 — Slice 2/3 — Materializar a fundação executável: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-RUN, REQ-RUNTIME]

- **Tipo:** `História implementável`
- **Estado:** `Ready-after-authorization`
- **Épico pai:** `EPIC-004`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel executor:** `Tech Lead`
- **TaskEnvelope:** `.codex/tasks/TASK-0704.json`

## História de usuário

Como executor especializado, preciso entregar este slice limitado de requisitos para que a capacidade de **OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados** avance sem mudança ampla ou inferência não documentada.

## Resultado verificável

Slice 2/3 concluído com contrato, implementação ou evidência compatível com o papel executor e todos os requisitos abaixo demonstrados.

## Escopo

- `tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/run-runtime-parte-2/**`
- `docs/03-engineering/contexts/engineering_governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/run-runtime-parte-2/**`
## Fora de escopo

- requisitos pertencentes a outro slice;
- alteração de ADR ou contrato congelado sem change control;
- código em diretórios orientados por ticket;
- refatoração não necessária à aceitação.

## Requisitos

`REQ-RUN-002`, `REQ-RUN-003`, `REQ-RUN-004`, `REQ-RUN-005`, `REQ-RUN-007`, `REQ-RUN-009`, `REQ-RUNTIME-001`, `REQ-RUNTIME-002`, `REQ-RUNTIME-003`, `REQ-RUNTIME-004`

## ADRs e contratos

- `ADR-007`
- `ADR-008`
- contratos e ADRs referenciados pelos requisitos.

## Dependências


`STORY-0016`

## Critérios de aceitação

- [ ] Cada requisito do slice possui evidência explícita: REQ-RUN-002, REQ-RUN-003, REQ-RUN-004, REQ-RUN-005, REQ-RUN-007, REQ-RUN-009, REQ-RUNTIME-001, REQ-RUNTIME-002, REQ-RUNTIME-003, REQ-RUNTIME-004.
- [ ] O write scope é estável, disjunto e não usa identificador de ticket em código de produção.
- [ ] Estados de falha aplicáveis são testados sem fallback silencioso.
- [ ] O handoff registra impacto em contratos, riscos e rollback.

## Testes obrigatórios

- `test_req_run_002`
- `test_req_run_003`
- `test_req_run_004`
- `test_req_run_005`
- `test_req_run_007`
- `test_req_run_009`
- `test_runtime_decision_1`
- `test_runtime_decision_2`
- `test_runtime_decision_3`
- `test_runtime_decision_4`

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

Leia `AGENTS.md`, o papel `.codex/roles/ROLE-003-tech-lead.md`, esta história e `TASK-0704`. Trabalhe somente nos paths permitidos, entregue apenas este slice e interrompa diante de qualquer condição de parada.

## Revisão SAR

- **Granularidade:** `PASS` — 10 requisitos;
- **Write scope:** `PASS` — package estável;
- **Contract freeze:** obrigatório quando aplicável;
- **Gate:** depende de autorização externa de implementação.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Impacto no modelo:** `CROSS_CONTEXT_INTEGRATION`.
- **Upstreams permitidos:** `Nenhum`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0814-01, AC-ISSUE-0814-02, AC-ISSUE-0814-03, AC-ISSUE-0814-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-002`, `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-040`, `ADR-045`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-021`, `ADR-023`, `ADR-040`, `ADR-045`, `ADR-055`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessores explícitos | PASS |
| Arquivos | 2 write scopes; deny scopes declarados | PASS |
| API | APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 10 testes obrigatórios | PASS |
| Artefatos | PRODUCT_AND_EVIDENCE | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Arquiteto, QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
