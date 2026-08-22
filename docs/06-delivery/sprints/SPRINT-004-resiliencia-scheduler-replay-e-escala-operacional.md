# SPRINT-004 — Resiliência, scheduler, replay e escala operacional

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 6
- **Dependências externas:** EPIC-014, EPIC-015, EPIC-016, EPIC-018, EPIC-019, EPIC-030, EPIC-034, EPIC-039, EPIC-040, EPIC-049, EPIC-075, EPIC-082

## Objetivo da sprint

Resiliência, scheduler, replay e escala operacional.

## Épicos incluídos

- `EPIC-065` / `ISSUE-0065` — taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `EPIC-066` / `ISSUE-0066` — checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários
- `EPIC-067` / `ISSUE-0067` — cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação
- `EPIC-068` / `ISSUE-0068` — Concorrência, escalonamento e isolamento
- `EPIC-069` / `ISSUE-0069` — Observabilidade, SLOs e diagnóstico do scheduler
- `EPIC-104` / `ISSUE-0104` — Snapshots, replay e bundles do scheduler

## Gate de entrada

- Todas as issues selecionadas satisfazem a Definition of Ready.
- Contratos e migrations compartilhados são serializados.
- Lanes paralelas possuem file scopes disjuntos.

## Gate de saída

- Critérios de aceitação passam para as issues concluídas.
- Evidências de QA e Reviewer referenciam os mesmos commits candidatos.
- Trabalho incompleto retorna ao backlog sem carryover oculto.
- O SprintEvidenceSet registra decisões, testes, defects e riscos não resolvidos.

## Paralelização

- Contratos e migrations são integrados primeiro.
- Lanes Backend, Frontend, Geo, IA e Operações só executam em paralelo após freeze do contrato.
- QA e final review permanecem independentes e sequenciais após integração.

## Backlog implementável

- **Histórias:** `42`
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-004-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–058 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `42`.
- **Ondas topológicas globais presentes:** `0, 1, 2, 3, 24, 25, 26, 27, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47`.
- **Papéis executores:** `Arquiteto`, `Backend`, `DevOps`, `QA`, `Reviewer`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-010`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `48`
- **Critérios de aceite rastreados:** `204`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-030`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-048`, `ADR-053`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `48` (`6` envelopes + `42` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `12` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `18` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `0` histórias aplicáveis.
- **Geo:** `0` histórias aplicáveis.
- **IA:** `2` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `42` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `168` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-004-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `48`
- **Histórias revisadas:** `42`
- **Risk tier:** Critical `12`, High `30`, Medium `0`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-004-CTO-REVIEW.md`
