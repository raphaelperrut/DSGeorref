# STORY-0721 / ISSUE-0831 — Slice 1/2 — Implementar modelo e application services: modelo de job e máquina de estados no PostgreSQL [REQ-AIE, REQ-DBSCHEMA, REQ-FS1]

- **Tipo:** `História implementável`
- **Estado:** `Ready-after-authorization`
- **Épico pai:** `EPIC-014`
- **Sprint:** `SPRINT-003`
- **Domínio:** `JOB`
- **Bounded Context:** `BC-010 — Orquestração de Jobs e Recursos`
- **Papel executor:** `Backend`
- **TaskEnvelope:** `.codex/tasks/TASK-0721.json`

## História de usuário

Como executor especializado, preciso entregar este slice limitado de requisitos para que a capacidade de **modelo de job e máquina de estados no PostgreSQL** avance sem mudança ampla ou inferência não documentada.

## Resultado verificável

Slice 1/2 concluído com contrato, implementação ou evidência compatível com o papel executor e todos os requisitos abaixo demonstrados.

## Escopo

- `src/backend/dsgeorref/contexts/job_orchestration/application/modelo-de-job-e-maquina-de-estados-no-postgresql/aie-dbschema-fs1-parte-1/**`
- `src/backend/dsgeorref/contexts/job_orchestration/adapters/modelo-de-job-e-maquina-de-estados-no-postgresql/aie-dbschema-fs1-parte-1/**`
## Fora de escopo

- requisitos pertencentes a outro slice;
- alteração de ADR ou contrato congelado sem change control;
- código em diretórios orientados por ticket;
- refatoração não necessária à aceitação.

## Requisitos

`REQ-AIE-002`, `REQ-AIE-004`, `REQ-AIE-006`, `REQ-AIE-008`, `REQ-AIE-009`, `REQ-AIE-010`, `REQ-DBSCHEMA-009`, `REQ-FS1-002`, `REQ-FS1-003`, `REQ-FS1-006`

## ADRs e contratos

- `ADR-007`
- `ADR-008`
- contratos e ADRs referenciados pelos requisitos.

## Dependências


`STORY-0068`

## Critérios de aceitação

- [ ] Cada requisito do slice possui evidência explícita: REQ-AIE-002, REQ-AIE-004, REQ-AIE-006, REQ-AIE-008, REQ-AIE-009, REQ-AIE-010, REQ-DBSCHEMA-009, REQ-FS1-002, REQ-FS1-003, REQ-FS1-006.
- [ ] O write scope é estável, disjunto e não usa identificador de ticket em código de produção.
- [ ] Estados de falha aplicáveis são testados sem fallback silencioso.
- [ ] O handoff registra impacto em contratos, riscos e rollback.

## Testes obrigatórios

- `test_ai_escalation_decision_02`
- `test_ai_escalation_decision_04`
- `test_ai_escalation_decision_06`
- `test_ai_escalation_decision_08`
- `test_ai_escalation_decision_09`
- `test_ai_escalation_decision_10`
- `test_req_dbschema_009`
- `test_first_functional_slice_decision_02`
- `test_first_functional_slice_decision_03`
- `test_first_functional_slice_decision_06`

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

Leia `AGENTS.md`, o papel `.codex/roles/ROLE-004-backend.md`, esta história e `TASK-0721`. Trabalhe somente nos paths permitidos, entregue apenas este slice e interrompa diante de qualquer condição de parada.

## Revisão SAR

- **Granularidade:** `PASS` — 10 requisitos;
- **Write scope:** `PASS` — package estável;
- **Contract freeze:** obrigatório quando aplicável;
- **Gate:** depende de autorização externa de implementação.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `BC-002, BC-003, BC-004`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0831-01, AC-ISSUE-0831-02, AC-ISSUE-0831-03, AC-ISSUE-0831-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-016`, `ADR-020`, `ADR-030`, `ADR-038`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-051`, `ADR-052`, `ADR-053`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-030`, `ADR-038`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-051`, `ADR-052`, `ADR-053`
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
| Banco | APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | APPLICABLE | PASS |
| Testes | 10 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Arquiteto, QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-003-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
