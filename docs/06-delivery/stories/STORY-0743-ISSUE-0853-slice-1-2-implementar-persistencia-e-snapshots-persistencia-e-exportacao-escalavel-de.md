# STORY-0743 / ISSUE-0853 — Slice 1/2 — Implementar persistência e snapshots: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums [REQ-BEX, REQ-EPIC, REQ-MSK, REQ-RMR]

- **Tipo:** `História implementável`
- **Estado:** `Ready-after-authorization`
- **Épico pai:** `EPIC-037`
- **Sprint:** `SPRINT-010`
- **Domínio:** `REP`
- **Bounded Context:** `BC-012 — Resultados, Diagnósticos e Exportação`
- **Papel executor:** `Backend`
- **TaskEnvelope:** `.codex/tasks/TASK-0743.json`

## História de usuário

Como executor especializado, preciso entregar este slice limitado de requisitos para que a capacidade de **persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums** avance sem mudança ampla ou inferência não documentada.

## Resultado verificável

Slice 1/2 concluído com contrato, implementação ou evidência compatível com o papel executor e todos os requisitos abaixo demonstrados.

## Escopo

- `src/backend/dsgeorref/contexts/results_reporting/application/persistencia-e-exportacao-escalavel-de-resultados-por/bex-epic-msk-parte-1/**`
- `src/backend/dsgeorref/contexts/results_reporting/adapters/persistencia-e-exportacao-escalavel-de-resultados-por/bex-epic-msk-parte-1/**`
## Fora de escopo

- requisitos pertencentes a outro slice;
- alteração de ADR ou contrato congelado sem change control;
- código em diretórios orientados por ticket;
- refatoração não necessária à aceitação.

## Requisitos

`REQ-BEX-002`, `REQ-BEX-004`, `REQ-BEX-006`, `REQ-BEX-007`, `REQ-BEX-008`, `REQ-BEX-009`, `REQ-BEX-010`, `REQ-EPIC-070`, `REQ-MSK-002`, `REQ-RMR-001`

## ADRs e contratos

- `ADR-007`
- `ADR-008`
- contratos e ADRs referenciados pelos requisitos.

## Dependências


`STORY-0220`

## Critérios de aceitação

- [ ] Cada requisito do slice possui evidência explícita: REQ-BEX-002, REQ-BEX-004, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010, REQ-EPIC-070, REQ-MSK-002, REQ-RMR-001.
- [ ] O write scope é estável, disjunto e não usa identificador de ticket em código de produção.
- [ ] Estados de falha aplicáveis são testados sem fallback silencioso.
- [ ] O handoff registra impacto em contratos, riscos e rollback.

## Testes obrigatórios

- `test_batch_execution_decision_02`
- `test_batch_execution_decision_04`
- `test_batch_execution_decision_06`
- `test_batch_execution_decision_07`
- `test_batch_execution_decision_08`
- `test_batch_execution_decision_09`
- `test_batch_execution_decision_10`
- `test_immutable_snapshots_current_view_historical_metrics`
- `test_marginal_metadata_pixels_preserved_and_classified`
- `test_relative_mosaic_report_snapshots_current_view_and_history`

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

Leia `AGENTS.md`, o papel `.codex/roles/ROLE-004-backend.md`, esta história e `TASK-0743`. Trabalhe somente nos paths permitidos, entregue apenas este slice e interrompa diante de qualquer condição de parada.

## Revisão SAR

- **Granularidade:** `PASS` — 10 requisitos;
- **Write scope:** `PASS` — package estável;
- **Contract freeze:** obrigatório quando aplicável;
- **Gate:** depende de autorização externa de implementação.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `BC-002, BC-003, BC-004, BC-006, BC-007, BC-008, BC-010, BC-011, BC-013`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0853-01, AC-ISSUE-0853-02, AC-ISSUE-0853-03, AC-ISSUE-0853-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-012`, `ADR-016`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-050`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-012`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-025`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-050`
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
| API | NOT_APPLICABLE | PASS |
| Banco | APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 10 testes obrigatórios | PASS |
| Artefatos | PRODUCT_AND_EVIDENCE | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Arquiteto, QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-010-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `HIGH`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-015`
- **Gate de produção:** `BENCHMARK_AND_OPERATIONS_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
