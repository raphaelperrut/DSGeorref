# SPRINT-006 — Correspondências, referências, providers e revisão assistida

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 12
- **Dependências externas:** EPIC-004, EPIC-012, EPIC-019, EPIC-021, EPIC-022, EPIC-023, EPIC-024, EPIC-025, EPIC-027, EPIC-029, EPIC-030, EPIC-033, EPIC-034, EPIC-037, EPIC-041, EPIC-045, EPIC-047, EPIC-049

## Objetivo da sprint

Correspondências, referências, providers e revisão assistida.

## Épicos incluídos

- `EPIC-050` / `ISSUE-0050` — registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark
- `EPIC-051` / `ISSUE-0051` — estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade
- `EPIC-052` / `ISSUE-0052` — seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados
- `EPIC-053` / `ISSUE-0053` — grafo de referências verificadas, componentes desconectados, invalidação e retry por componente
- `EPIC-054` / `ISSUE-0054` — componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica
- `EPIC-055` / `ISSUE-0055` — recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito
- `EPIC-056` / `ISSUE-0056` — máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente
- `EPIC-057` / `ISSUE-0057` — resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos
- `EPIC-058` / `ISSUE-0058` — gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `EPIC-059` / `ISSUE-0059` — busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento
- `EPIC-060` / `ISSUE-0060` — policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos
- `EPIC-063` / `ISSUE-0063` — modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports

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

- **Histórias:** `86`
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-006-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–058 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `86`.
- **Ondas topológicas globais presentes:** `24, 25, 26, 27, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51`.
- **Papéis executores:** `Arquiteto`, `Geoprocessamento`, `QA`, `Reviewer`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-009`, `BC-006`, `BC-005`, `BC-012`, `BC-011`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `98`
- **Critérios de aceite rastreados:** `416`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-017`, `ADR-030`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-045`, `ADR-046`, `ADR-047`, `ADR-048`, `ADR-049`, `ADR-050`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `98` (`12` envelopes + `86` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `24` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `0` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `7` histórias aplicáveis.
- **Geo:** `80` histórias aplicáveis.
- **IA:** `10` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `86` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `344` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-006-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `98`
- **Histórias revisadas:** `86`
- **Risk tier:** Critical `10`, High `76`, Medium `0`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-006-CTO-REVIEW.md`
