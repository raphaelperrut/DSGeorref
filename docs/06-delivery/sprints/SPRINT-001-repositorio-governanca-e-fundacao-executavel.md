# SPRINT-001 — Repositório, governança e fundação executável

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 12
- **Dependências externas:** Nenhuma

## Objetivo da sprint

Repositório, governança e fundação executável.

## Épicos incluídos

- `EPIC-001` / `ISSUE-0001` — governança de decisões arquiteturais e manutenção da baseline normativa
- `EPIC-002` / `ISSUE-0002` — repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `EPIC-003` / `ISSUE-0003` — monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis
- `EPIC-004` / `ISSUE-0004` — OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `EPIC-005` / `ISSUE-0005` — migrations, CI, secret/dependency scan e telemetria mínima
- `EPIC-006` / `ISSUE-0006` — catálogo de conhecimento técnico e decomposição das capacidades de processamento
- `EPIC-007` / `ISSUE-0007` — LICENSE, CITATION.cff, contribuição, DCO/CLA e gate de publicação definidos
- `EPIC-086` / `ISSUE-0086` — walking skeleton frontend→API→PostgreSQL→RabbitMQ/Celery→worker→artefato diagnóstico, executável e testado ponta a ponta
- `EPIC-090` / `ISSUE-0090` — Issue Forms, templates e taxonomia de tipos com validação de campos obrigatórios
- `EPIC-091` / `ISSUE-0091` — ruleset de main, checks únicos, CODEOWNERS, política de branches e prova de bypass auditado
- `EPIC-092` / `ISSUE-0092` — fechamento da SPRINT-001 e autorização da primeira fatia funcional
- `EPIC-110` / `ISSUE-0110` — governança contínua do backlog e decomposição de épicos em histórias implementáveis

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

- **Histórias:** `94`
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-001-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–058 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `94`.
- **Ondas topológicas globais presentes:** `0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19`.
- **Papéis executores:** `Arquiteto`, `DevOps`, `QA`, `Reviewer`, `Tech Lead`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-001`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `106`
- **Critérios de aceite rastreados:** `444`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-021`, `ADR-022`, `ADR-023`, `ADR-024`, `ADR-025`, `ADR-026`, `ADR-030`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-050`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-054`, `ADR-055`, `ADR-056`, `ADR-057`, `ADR-058`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `106` (`12` envelopes + `94` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `19` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `18` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `7` histórias aplicáveis.
- **Geo:** `0` histórias aplicáveis.
- **IA:** `10` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `92` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `372` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `106`
- **Histórias revisadas:** `94`
- **Risk tier:** Critical `46`, High `19`, Medium `29`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, IMPLEMENTATION_AUTHORIZATION, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-001-CTO-REVIEW.md`
