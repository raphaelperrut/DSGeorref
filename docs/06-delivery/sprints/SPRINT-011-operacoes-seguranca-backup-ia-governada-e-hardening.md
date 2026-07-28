# SPRINT-011 — Operações, segurança, backup, IA governada e hardening

- **Estado:** `Planned`
- **Cadência:** incremento limitado por evidência; WIP controlado pelo Tech Lead
- **Épicos:** 14
- **Dependências externas:** EPIC-002, EPIC-003, EPIC-005, EPIC-008, EPIC-011, EPIC-012, EPIC-015, EPIC-024, EPIC-046, EPIC-049, EPIC-050, EPIC-058, EPIC-061

## Objetivo da sprint

Operações, segurança, backup, IA governada e hardening.

## Épicos incluídos

- `EPIC-039` / `ISSUE-0039` — instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `EPIC-040` / `ISSUE-0040` — benchmark, limites e orçamento de recursos
- `EPIC-071` / `ISSUE-0071` — BackupSet coordenado, manifests, checksums, watermark e policies de inclusão
- `EPIC-072` / `ISSUE-0072` — restore drills isolados, evidências, RPO/RTO e runbook executável
- `EPIC-073` / `ISSUE-0073` — RetentionPolicy por classe/estado/dependência, holds e preview de impacto
- `EPIC-074` / `ISSUE-0074` — GC reference-aware, tombstone, quarentena, período de graça e reconciliação
- `EPIC-075` / `ISSUE-0075` — canal append-only de auditoria, particionamento, digests, consulta e exportação assinada opcional
- `EPIC-076` / `ISSUE-0076` — catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados
- `EPIC-077` / `ISSUE-0077` — budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead
- `EPIC-078` / `ISSUE-0078` — contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault
- `EPIC-079` / `ISSUE-0079` — ingress único, TLS, redes privadas, limites e testes de exposição de portas
- `EPIC-080` / `ISSUE-0080` — lockfiles, pins por digest/SHA, scanners, SBOM, assinatura OCI, attestations e verificador de release
- `EPIC-083` / `ISSUE-0083` — modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped
- `EPIC-088` / `ISSUE-0088` — namespace experimental/labs, registry separado, ModelPacks isolados e bloqueio técnico de ArtifactSet aceito

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

- **Histórias:** `84`
- **Documento detalhado:** `docs/06-delivery/sprint-backlogs/SPRINT-011-BACKLOG.md`
- **TaskEnvelopes:** `.codex/tasks/TASK-*.json`
- **Grafo:** `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`


## Revisão SAR da sprint

- **Baseline arquitetural de entrada:** ADRs 001–057 aceitas, tecnologia fechada em `TECHNOLOGY_BASELINE`, contratos compartilhados versionados.
- **Decisões tecnológicas em aberto:** `0`.
- **Histórias:** `84`.
- **Ondas topológicas globais presentes:** `12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51`.
- **Papéis executores:** `Arquiteto`, `Backend`, `DevOps`, `IA`, `QA`, `Reviewer`, `Security`.
- **Regra de capacidade:** WIP por classe; nenhuma história inicia sem predecessores integrados e write scope disponível.
- **Gate arquitetural de saída:** contratos sem drift, migrations reversíveis/recuperáveis, observabilidade, testes e evidência; inconsistência bloqueia fechamento.
- **Handoff:** SprintEvidenceSet registra commit, versões/digests, stories, defects, riscos, benchmarks e decisões evidence-bound promovidas.


## Domain-Driven Design — Fase C

- **Bounded Contexts no incremento:** `BC-014`, `BC-013`, `BC-015`, `BC-009`.
- **Gate de entrada DDD:** toda história declara um único context owner e seus upstreams.
- **Gate de integração:** integração cross-context usa contrato publicado/ACL/evento; imports de modelo interno e acesso cross-schema bloqueiam o merge.
- **Gate de saída DDD:** nenhum drift entre context owner, TaskEnvelope, package, contrato e matriz de dependências.
- **Resultado:** `PASS`.

## Requirements Review — Fase B

- **Resultado:** `PASS`
- **Issues revisadas:** `98`
- **Critérios de aceite rastreados:** `420`
- **Conflitos bloqueantes:** `0`
- **Redundâncias funcionais não justificadas:** `0`
- **Requisitos faltantes:** `0`
- **Requisitos impossíveis:** `0`
- **Dependências circulares:** `0`
- **Matrizes:** `docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv`, `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-020`, `ADR-023`, `ADR-024`, `ADR-025`, `ADR-027`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-036`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-042`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-054`, `ADR-055`
- **Cobertura:** todas as histórias da sprint possuem ADRs explícitas no TaskEnvelope.
- **Decisão em aberto:** `Nenhuma`
- **Resultado:** `PASS`


## Specification Gate — Fase E

- todos os TaskEnvelopes da sprint declaram especificações aplicáveis e baseline `SAR-v2.9-PHASE-F`;
- nenhuma história entra em execução com schema, exemplo, versão ou validador ausente;
- mudanças breaking exigem major version e revisão do Arquiteto;
- hashes, signatures, state transitions, protocol order e artifact profiles aplicáveis devem ser demonstrados por testes.

## Sprint Review — Fase F

- **Issues revisadas:** `98` (`14` envelopes + `84` histórias).
- **Dependências:** `PASS`; DAG sem ciclos e sem retrocesso entre sprints.
- **Arquivos:** `PASS`; write scopes explícitos, estáveis e sem paths derivados de issue/story/task.
- **API:** `37` histórias aplicáveis; OpenAPI e catálogo de operações referenciados.
- **Banco:** `24` histórias aplicáveis; authority, migration e rollback declarados.
- **Frontend:** `0` histórias aplicáveis.
- **Geo:** `0` histórias aplicáveis.
- **IA:** `12` histórias aplicáveis; `SPEC-003` obrigatório quando aplicável.
- **Testes:** `84` histórias com testes explícitos.
- **Artefatos:** produto ou evidência explicitamente classificados em todas as histórias.
- **Critérios:** `336` critérios com IDs estáveis.
- **Review:** cadeia explícita e mesmo commit candidato.
- **Relatório detalhado:** `docs/07-assurance/phase-f/SPRINT-011-REVIEW.md`.
- **Resultado:** `PASS`.
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Issues revisadas:** `98`
- **Histórias revisadas:** `84`
- **Risk tier:** Critical `68`, High `16`, Medium `0`
- **Gates aplicáveis:** `BENCHMARK_AND_OPERATIONS_GATES, SECURITY_AND_PRIVACY_GATES`
- **Relatório:** `docs/07-assurance/phase-g/SPRINT-011-CTO-REVIEW.md`
