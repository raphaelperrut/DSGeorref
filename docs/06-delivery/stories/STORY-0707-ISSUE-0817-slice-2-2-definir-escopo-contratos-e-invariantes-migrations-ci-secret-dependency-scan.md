# STORY-0707 / ISSUE-0817 — Slice 2/2 — Definir escopo, contratos e invariantes: migrations, CI, secret/dependency scan e telemetria mínima [REQ-SGVCAL]

- **Tipo:** `História implementável`
- **Estado:** `Ready-after-authorization`
- **Épico pai:** `EPIC-005`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel executor:** `Arquiteto`
- **TaskEnvelope:** `.codex/tasks/TASK-0707.json`

## História de usuário

Como executor especializado, preciso entregar este slice limitado de requisitos para que a capacidade de **migrations, CI, secret/dependency scan e telemetria mínima** avance sem mudança ampla ou inferência não documentada.

## Resultado verificável

Slice 2/2 concluído com contrato, implementação ou evidência compatível com o papel executor e todos os requisitos abaixo demonstrados.

## Escopo

- `contracts/contexts/engineering_governance/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-parte-2/**`
- `docs/02-architecture/design-reviews/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-parte-2/**`
## Fora de escopo

- requisitos pertencentes a outro slice;
- alteração de ADR ou contrato congelado sem change control;
- código em diretórios orientados por ticket;
- refatoração não necessária à aceitação.

## Requisitos

`REQ-SGVCAL-007`

## ADRs e contratos

- `ADR-007`
- `ADR-008`
- contratos e ADRs referenciados pelos requisitos.

## Dependências


`STORY-0015`

## Critérios de aceitação

- [ ] Cada requisito do slice possui evidência explícita: REQ-SGVCAL-007.
- [ ] O write scope é estável, disjunto e não usa identificador de ticket em código de produção.
- [ ] Estados de falha aplicáveis são testados sem fallback silencioso.
- [ ] O handoff registra impacto em contratos, riscos e rollback.

## Testes obrigatórios

- `test_req_sgvcal_007`

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

Leia `AGENTS.md`, o papel `.codex/roles/ROLE-002-arquiteto.md`, esta história e `TASK-0707`. Trabalhe somente nos paths permitidos, entregue apenas este slice e interrompa diante de qualquer condição de parada.

## Revisão SAR

- **Granularidade:** `PASS` — 1 requisitos;
- **Write scope:** `PASS` — package estável;
- **Contract freeze:** obrigatório quando aplicável;
- **Gate:** depende de autorização externa de implementação.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Impacto no modelo:** `PUBLIC_CONTRACT`.
- **Upstreams permitidos:** `Nenhum`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0817-01, AC-ISSUE-0817-02, AC-ISSUE-0817-03, AC-ISSUE-0817-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-002`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-018`, `ADR-023`, `ADR-024`, `ADR-026`
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
| API | NOT_APPLICABLE | PASS |
| Banco | APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 1 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Arquiteto, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `HIGH`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-010, CTO-011, CTO-012, CTO-013, CTO-015`
- **Gate de produção:** `BENCHMARK_AND_OPERATIONS_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
