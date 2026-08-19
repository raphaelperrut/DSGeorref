# SPRINT-005 — Primeira fatia geoespacial classic-first

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 15
- **Dependências externas:** EPIC-004, EPIC-005, EPIC-006, EPIC-012, EPIC-019

## Objetivo da sprint

Primeira fatia geoespacial classic-first.

## Épicos incluídos

- `EPIC-021` / `ISSUE-0021` — corpus versionado com décadas e condições distintas
- `EPIC-022` / `ISSUE-0022` — busca provável greenfield validada
- `EPIC-023` / `ISSUE-0023` — correspondências e estimação robusta da homografia projetiva validadas
- `EPIC-024` / `ISSUE-0024` — Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `EPIC-025` / `ISSUE-0025` — registry, calibração, benchmark e lifecycle de QualityProfiles oficiais/customizados
- `EPIC-026` / `ISSUE-0026` — artefatos e lineage
- `EPIC-027` / `ISSUE-0027` — gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `EPIC-028` / `ISSUE-0028` — benchmarks por período, sensor e perfil de qualidade
- `EPIC-029` / `ISSUE-0029` — etapas/capacidades canônicas e ProcessingPlan reproduzível
- `EPIC-030` / `ISSUE-0030` — taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem
- `EPIC-044` / `ISSUE-0044` — OutputProfile, COG canônico, preservação de resolução e validação da grade
- `EPIC-045` / `ISSUE-0045` — máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais
- `EPIC-046` / `ISSUE-0046` — ArtifactSet imutável, staging e publicação atômica
- `EPIC-047` / `ISSUE-0047` — matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada
- `EPIC-048` / `ISSUE-0048` — extração opcional de metadados marginais com confiança, revisão e lineage

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

- **Histórias:** `120`
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-005-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–058 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `120`.
- **Ondas topológicas globais presentes:** `8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39`.
- **Papéis executores:** `Arquiteto`, `Geoprocessamento`, `QA`, `Reviewer`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-007`, `BC-005`, `BC-006`, `BC-013`, `BC-004`, `BC-012`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `135`
- **Critérios de aceite rastreados:** `570`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-015`, `ADR-018`, `ADR-019`, `ADR-023`, `ADR-024`, `ADR-025`, `ADR-030`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-047`, `ADR-048`, `ADR-049`, `ADR-050`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `135` (`15` envelopes + `120` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `15` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `0` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `0` histórias aplicáveis.
- **Geo:** `112` histórias aplicáveis.
- **IA:** `13` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `120` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `480` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-005-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `135`
- **Histórias revisadas:** `120`
- **Risk tier:** Critical `72`, High `47`, Medium `1`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, IMPLEMENTATION_AUTHORIZATION, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-005-CTO-REVIEW.md`
