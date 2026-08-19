# SPRINT-009 — Frontend cartográfico, revisão e aprendizagem

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 9
- **Dependências externas:** EPIC-004, EPIC-010, EPIC-011, EPIC-018, EPIC-024, EPIC-025, EPIC-029, EPIC-030, EPIC-049, EPIC-050, EPIC-053

## Objetivo da sprint

Frontend cartográfico, revisão e aprendizagem.

## Épicos incluídos

- `EPIC-031` / `ISSUE-0031` — React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `EPIC-032` / `ISSUE-0032` — workspace OpenLayers, configuração, acompanhamento e revisão
- `EPIC-033` / `ISSUE-0033` — assistente guiado, recomendação explicável, consentimentos e modo avançado
- `EPIC-034` / `ISSUE-0034` — painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `EPIC-035` / `ISSUE-0035` — workflow de revisão com gates revisáveis, hard gates imutáveis, checklist e auditoria
- `EPIC-036` / `ISSUE-0036` — central Aprender, exemplos visuais, projeto demonstrativo e ajuda contextual, incluindo Strong Geometric Verifier e interpretação de falhas
- `EPIC-062` / `ISSUE-0062` — workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `EPIC-064` / `ISSUE-0064` — fila de revisão explicável, filtros, priorização, impacto em descendentes e operações em lote permitidas
- `EPIC-084` / `ISSUE-0084` — UX guiada de IA, explicação do plano, capacidades instaladas/bloqueadas e laboratório separado

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
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-009-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–058 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `58`.
- **Ondas topológicas globais presentes:** `28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51`.
- **Papéis executores:** `Arquiteto`, `Backend`, `Frontend`, `Product Owner`, `QA`, `Reviewer`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-016`, `BC-011`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `67`
- **Critérios de aceite rastreados:** `286`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-023`, `ADR-025`, `ADR-030`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-042`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-047`, `ADR-048`, `ADR-049`, `ADR-051`, `ADR-053`, `ADR-055`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `67` (`9` envelopes + `58` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `27` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `2` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `48` histórias aplicáveis.
- **Geo:** `0` histórias aplicáveis.
- **IA:** `2` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `58` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `232` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-009-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `67`
- **Histórias revisadas:** `58`
- **Risk tier:** Critical `9`, High `22`, Medium `27`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, IMPLEMENTATION_AUTHORIZATION, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-009-CTO-REVIEW.md`
