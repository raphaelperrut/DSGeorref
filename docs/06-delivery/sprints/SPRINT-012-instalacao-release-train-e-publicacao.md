# SPRINT-012 — Instalação, release train e publicação

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 10
- **Dependências externas:** EPIC-002, EPIC-012, EPIC-018, EPIC-024, EPIC-034, EPIC-037, EPIC-044, EPIC-071, EPIC-072, EPIC-080, EPIC-086

## Objetivo da sprint

Instalação, release train e publicação.

## Épicos incluídos

- `EPIC-042` / `ISSUE-0042` — licença, citação, sanitização e revisão externa concluídas
- `EPIC-043` / `ISSUE-0043` — release documentada com rollback e suporte
- `EPIC-081` / `ISSUE-0081` — orquestrador de upgrade, preflight, migrations explícitas, health/smoke tests e rollback/restore
- `EPIC-085` / `ISSUE-0085` — definição e automação de milestones internal/alpha/beta/1.0, evidências e gate de abertura do repositório
- `EPIC-087` / `ISSUE-0087` — baseline operacional vertical privado com escopo da DELIVERY_PLAN e evidências do corpus controlado
- `EPIC-089` / `ISSUE-0089` — release train internal/alpha/beta/1.0, automação de evidências e gate de abertura pública
- `EPIC-106` / `ISSUE-0106` — Migrations compatíveis, upgrade e downgrade seguro
- `EPIC-107` / `ISSUE-0107` — Controlador e rollout coordenado de upgrades
- `EPIC-108` / `ISSUE-0108` — Instalador, bootstrap, readiness e suporte diagnóstico
- `EPIC-109` / `ISSUE-0109` — Licenciamento, contribuição, rights manifests e citação

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

- **Histórias:** `58`
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-012-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–057 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `58`.
- **Ondas topológicas globais presentes:** `0, 1, 2, 3, 8, 9, 10, 11, 40, 41, 42, 43, 48, 49, 50, 51`.
- **Papéis executores:** `DevOps`, `Product Owner`, `QA`, `Reviewer`, `Security`, `Tech Lead`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-015`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `68`
- **Critérios de aceite rastreados:** `292`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-026`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-037`, `ADR-053`, `ADR-056`, `ADR-057`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `68` (`10` envelopes + `58` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `15` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `12` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `0` histórias aplicáveis.
- **Geo:** `0` histórias aplicáveis.
- **IA:** `2` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `58` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `232` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-012-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `68`
- **Histórias revisadas:** `58`
- **Risk tier:** Critical `31`, High `27`, Medium `0`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-012-CTO-REVIEW.md`
