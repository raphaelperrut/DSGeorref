# SPRINT-003 — Jobs, runners, lote básico e CLI

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 7
- **Dependências externas:** EPIC-004, EPIC-005, EPIC-012, EPIC-031, EPIC-039

## Objetivo da sprint

Jobs, runners, lote básico e CLI.

## Épicos incluídos

- `EPIC-014` / `ISSUE-0014` — modelo de job e máquina de estados no PostgreSQL
- `EPIC-015` / `ISSUE-0015` — runner direto e Celery/RabbitMQ sobre o mesmo núcleo
- `EPIC-016` / `ISSUE-0016` — retries, redelivery, cancelamento, retomada e idempotência
- `EPIC-017` / `ISSUE-0017` — REST, SSE e polling de reconciliação com contratos versionados
- `EPIC-018` / `ISSUE-0018` — batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens
- `EPIC-019` / `ISSUE-0019` — Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco
- `EPIC-020` / `ISSUE-0020` — CLI estável para projetos, ingestão, jobs e resultados

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

- **Histórias:** `49`
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-003-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–058 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `49`.
- **Ondas topológicas globais presentes:** `12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 28, 29, 30, 31, 32, 33, 34, 35`.
- **Papéis executores:** `Arquiteto`, `Backend`, `DevOps`, `QA`, `Reviewer`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-010`, `BC-016`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `56`
- **Critérios de aceite rastreados:** `238`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-030`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-047`, `ADR-049`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `56` (`7` envelopes + `49` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `19` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `26` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `5` histórias aplicáveis.
- **Geo:** `0` histórias aplicáveis.
- **IA:** `4` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `49` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `196` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-003-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `56`
- **Histórias revisadas:** `49`
- **Risk tier:** Critical `14`, High `34`, Medium `1`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, IMPLEMENTATION_AUTHORIZATION, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-003-CTO-REVIEW.md`
