# SPRINT-002 — Identidade, autorização, workspace e persistência inicial

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 8
- **Dependências externas:** EPIC-004, EPIC-005, EPIC-027, EPIC-039

## Objetivo da sprint

Identidade, autorização, workspace e persistência inicial.

## Épicos incluídos

- `EPIC-008` / `ISSUE-0008` — contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `EPIC-009` / `ISSUE-0009` — usuários e papéis da instância
- `EPIC-010` / `ISSUE-0010` — autorização por projeto, operação, artefato e caminho
- `EPIC-011` / `ISSUE-0011` — limites, idempotência, audit log e controles administrativos
- `EPIC-012` / `ISSUE-0012` — raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `EPIC-013` / `ISSUE-0013` — backup/restore consistente entre banco e arquivos
- `EPIC-041` / `ISSUE-0041` — threat model validado, scanning e testes ofensivos
- `EPIC-082` / `ISSUE-0082` — preflight de hardware e ExecutionProfiles CPU/GPU/híbrido integrados ao Resource Governor

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

- **Histórias:** `55`
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-002-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–058 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `55`.
- **Ondas topológicas globais presentes:** `12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31`.
- **Papéis executores:** `Arquiteto`, `Backend`, `DevOps`, `Frontend`, `Reviewer`, `Security`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-002`, `BC-003`, `BC-013`, `BC-014`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `63`
- **Critérios de aceite rastreados:** `268`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-021`, `ADR-023`, `ADR-025`, `ADR-026`, `ADR-027`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-040`, `ADR-041`, `ADR-043`, `ADR-045`, `ADR-046`, `ADR-047`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `63` (`8` envelopes + `55` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `25` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `24` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `5` histórias aplicáveis.
- **Geo:** `0` histórias aplicáveis.
- **IA:** `2` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `55` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `220` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-002-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `63`
- **Histórias revisadas:** `55`
- **Risk tier:** Critical `45`, High `7`, Medium `3`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, IMPLEMENTATION_AUTHORIZATION, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-002-CTO-REVIEW.md`
