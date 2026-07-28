# STORY-0697 / ISSUE-0807 — Slice 6/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-PRM, REQ-RUN]

- **Tipo:** `História implementável`
- **Estado:** `Ready-after-authorization`
- **Épico pai:** `EPIC-002`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel executor:** `Tech Lead`
- **TaskEnvelope:** `.codex/tasks/TASK-0697.json`

## História de usuário

Como executor especializado, preciso entregar este slice limitado de requisitos para que a capacidade de **repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível** avance sem mudança ampla ou inferência não documentada.

## Resultado verificável

Slice 6/9 concluído com contrato, implementação ou evidência compatível com o papel executor e todos os requisitos abaixo demonstrados.

## Escopo

- `tools/governance/repositorio-privado-project-central-views-campos-label/prm-run-parte-6/**`
- `docs/03-engineering/contexts/engineering_governance/repositorio-privado-project-central-views-campos-label/prm-run-parte-6/**`
## Fora de escopo

- requisitos pertencentes a outro slice;
- alteração de ADR ou contrato congelado sem change control;
- código em diretórios orientados por ticket;
- refatoração não necessária à aceitação.

## Requisitos

`REQ-PRM-007`, `REQ-PRM-008`, `REQ-PRM-009`, `REQ-PRM-010`, `REQ-RUN-002`, `REQ-RUN-003`, `REQ-RUN-004`, `REQ-RUN-005`, `REQ-RUN-007`, `REQ-RUN-009`

## ADRs e contratos

- `ADR-007`
- `ADR-008`
- contratos e ADRs referenciados pelos requisitos.

## Dependências


`STORY-0006`

## Critérios de aceitação

- [ ] Cada requisito do slice possui evidência explícita: REQ-PRM-007, REQ-PRM-008, REQ-PRM-009, REQ-PRM-010, REQ-RUN-002, REQ-RUN-003, REQ-RUN-004, REQ-RUN-005, REQ-RUN-007, REQ-RUN-009.
- [ ] O write scope é estável, disjunto e não usa identificador de ticket em código de produção.
- [ ] Estados de falha aplicáveis são testados sem fallback silencioso.
- [ ] O handoff registra impacto em contratos, riscos e rollback.

## Testes obrigatórios

- `test_portfolio_materialization_decision_07`
- `test_portfolio_materialization_decision_08`
- `test_portfolio_materialization_decision_09`
- `test_portfolio_materialization_decision_10`
- `test_req_run_002`
- `test_req_run_003`
- `test_req_run_004`
- `test_req_run_005`
- `test_req_run_007`
- `test_req_run_009`

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

Leia `AGENTS.md`, o papel `.codex/roles/ROLE-003-tech-lead.md`, esta história e `TASK-0697`. Trabalhe somente nos paths permitidos, entregue apenas este slice e interrompa diante de qualquer condição de parada.

## Revisão SAR

- **Granularidade:** `PASS` — 10 requisitos;
- **Write scope:** `PASS` — package estável;
- **Contract freeze:** obrigatório quando aplicável;
- **Gate:** depende de autorização externa de implementação.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `Nenhum`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0807-01, AC-ISSUE-0807-02, AC-ISSUE-0807-03, AC-ISSUE-0807-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-040`, `ADR-045`, `ADR-053`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-017`, `ADR-040`, `ADR-045`, `ADR-053`, `ADR-055`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-003`, `SPEC-004`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessores explícitos | PASS |
| Arquivos | 2 write scopes; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | APPLICABLE | PASS |
| Testes | 10 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
