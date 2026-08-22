# SPRINT-010 — Resultados, lineage, schemas e reprodutibilidade

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 6
- **Dependências externas:** EPIC-004, EPIC-012, EPIC-024, EPIC-026, EPIC-030, EPIC-046, EPIC-058, EPIC-062

## Objetivo da sprint

Resultados, lineage, schemas e reprodutibilidade.

## Épicos incluídos

- `EPIC-037` / `ISSUE-0037` — persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums
- `EPIC-038` / `ISSUE-0038` — métricas, heatmap amostrado e diagnóstico denso do Image Deformation Profile
- `EPIC-049` / `ISSUE-0049` — lineage normalizado, manifestos e bundle de reprodução sob demanda
- `EPIC-061` / `ISSUE-0061` — cache endereçado por conteúdo, deduplicação, quotas, retention, licença, GC e proteção de lineage
- `EPIC-070` / `ISSUE-0070` — snapshots imutáveis, regra de resultado vigente e comparação entre ciclos
- `EPIC-105` / `ISSUE-0105` — Registry de schemas e compatibilidade de artifacts

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

- **Histórias:** `38`
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-010-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–058 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `38`.
- **Ondas topológicas globais presentes:** `0, 1, 2, 3, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 48, 49, 50, 51`.
- **Papéis executores:** `Arquiteto`, `Backend`, `Frontend`, `QA`, `Reviewer`, `Security`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-012`, `BC-007`, `BC-013`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `44`
- **Critérios de aceite rastreados:** `188`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-016`, `ADR-018`, `ADR-025`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-035`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-047`, `ADR-048`, `ADR-050`, `ADR-052`, `ADR-053`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `44` (`6` envelopes + `38` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `12` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `20` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `3` histórias aplicáveis.
- **Geo:** `6` histórias aplicáveis.
- **IA:** `5` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `38` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `152` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-010-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `44`
- **Histórias revisadas:** `38`
- **Risk tier:** Critical `13`, High `25`, Medium `0`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-010-CTO-REVIEW.md`
