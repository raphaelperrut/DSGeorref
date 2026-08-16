# Fase D — ADR Definitivo

- **Baseline de entrada:** `SAR v2.6`
- **Baseline de saída:** `SAR v2.7`
- **Resultado:** `APROVADO`
- **ADRs definitivas:** `57`
- **Sequência:** `ADR-001` a `ADR-057`
- **Decisões abertas:** `0`
- **Ciclos no grafo de ADRs:** `0`
- **Requisitos sem owner ADR:** `0`

## Objetivo

Revisar se o inventário de 25 ADRs era suficiente e estabelecer um registro definitivo no qual cada decisão material, duradoura e de alto custo de reversão tenha um único owner normativo.

## Parecer

**O inventário de 25 ADRs era insuficientemente granular.** Ele cobria a arquitetura, mas concentrava vários drivers independentes em documentos únicos. Isso permitia que uma mudança local parecesse substituir um conjunto muito maior de decisões e dificultava a seleção de contexto mínimo para agentes.

A baseline passa a usar 57 ADRs atômicas. O número não foi escolhido como meta: resulta da decomposição de boundaries que possuem autoridades, alternativas, riscos ou gates diferentes.

## Distribuição

| Área | Faixa | Quantidade |
|---|---:|---:|
| Engenharia e estrutura | `001–010` | 10 |
| Interfaces e aplicação | `011–017` | 7 |
| Dados e artifacts | `018–027` | 10 |
| Identidade e segurança | `028–035` | 8 |
| Jobs e execução | `036–040` | 5 |
| Geoespacial | `041–050` | 10 |
| IA, ciência e operação | `051–057` | 7 |

## Critério de criação de ADR

Uma decisão recebeu ADR própria somente quando satisfaz pelo menos um dos critérios:

1. altera boundary, autoridade de dados ou direção de dependências;
2. define tecnologia estrutural ou trust boundary;
3. altera contrato público, semântica de consistência ou lifecycle persistente;
4. possui alternativas materialmente diferentes e alto custo de reversão;
5. precisa ser aplicada de maneira uniforme por múltiplos agentes ou superfícies.

Versões compatíveis, thresholds, tunables e convenções locais continuam em Application Profiles, Benchmark Profiles ou issues.

## Observação sobre os exemplos do Owner

- Monorepo, FastAPI, PostGIS, Storage, Object Model, Edit Bundle, AI Router, Inference Engine, Versioning, Audit, Raster Pipeline, CRS, Jobs e Authentication tornaram-se boundaries explícitos quando aplicáveis.
- “Prompt Bundle” não foi inventado como componente de runtime. O requisito real é governança de prompts permanentes e TaskEnvelopes do Codex, formalizado em `ADR-006`.

## Decomposição da baseline anterior

| Agrupamento da v2.6 | Owners atômicos na v2.7 |
|---|---|
| ADR v2.6 001 | `ADR-051`, `ADR-052`, `ADR-053` |
| ADR v2.6 002 | `ADR-001`, `ADR-002`, `ADR-005`, `ADR-011`, `ADR-012`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-017` |
| ADR v2.6 003 | `ADR-018`, `ADR-019`, `ADR-020`, `ADR-021`, `ADR-022`, `ADR-023`, `ADR-024`, `ADR-025` |
| ADR v2.6 004 | `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032` |
| ADR v2.6 005 | `ADR-036`, `ADR-037`, `ADR-038`, `ADR-040` |
| ADR v2.6 006 | `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-057` |
| ADR v2.6 007 | `ADR-046` |
| ADR v2.6 008 | `ADR-039`, `ADR-040` |
| ADR v2.6 009 | `ADR-044`, `ADR-045`, `ADR-046` |
| ADR v2.6 010 | `ADR-047` |
| ADR v2.6 011 | `ADR-025`, `ADR-048` |
| ADR v2.6 012 | `ADR-027` |
| ADR v2.6 013 | `ADR-054`, `ADR-055` |
| ADR v2.6 014 | `ADR-041`, `ADR-042`, `ADR-043` |
| ADR v2.6 015 | `ADR-049` |
| ADR v2.6 016 | `ADR-050` |
| ADR v2.6 017 | `ADR-053` |
| ADR v2.6 018 | `ADR-026`, `ADR-035` |
| ADR v2.6 019 | `ADR-007` |
| ADR v2.6 020 | `ADR-008` |
| ADR v2.6 021 | `ADR-010`, `ADR-011`, `ADR-013`, `ADR-016` |
| ADR v2.6 022 | `ADR-009`, `ADR-033`, `ADR-043` |
| ADR v2.6 023 | `ADR-003` |
| ADR v2.6 024 | `ADR-004`, `ADR-020` |
| ADR v2.6 025 | `ADR-005` |

## Inventário definitivo completo

| ADR | Boundary normativo | Contexts | Requisitos owned | Dependências |
|---|---|---|---:|---|
| `ADR-001` | Topologia do repositório, monorepo e workspaces | `BC-001` | 4 | — |
| `ADR-002` | Topologia do produto: monólito modular e instância única | `BC-001` | 11 | ADR-001 |
| `ADR-003` | Bounded Contexts, subdomínios e linguagem ubíqua | `BC-001` | 0 | ADR-002 |
| `ADR-004` | Integração entre contexts e modelos publicados | `BC-001` | 1 | ADR-003 |
| `ADR-005` | Layout context-first e direção de dependências | `BC-001` | 2 | ADR-003/ADR-004 |
| `ADR-006` | Prompts permanentes, TaskEnvelope e precedência de instruções | `BC-001` | 16 | ADR-001/ADR-003 |
| `ADR-007` | Write scopes, lanes paralelas e isolamento de mudança | `BC-001` | 1 | ADR-005/ADR-006 |
| `ADR-008` | Granularidade de histórias e limites anti-monólito | `BC-001` | 13 | ADR-006/ADR-007 |
| `ADR-009` | Runtime Python 3.12, toolchain e stack nativa reproduzível | `BC-001, BC-015` | 14 | ADR-001 |
| `ADR-010` | API-first, versionamento e contract freeze | `BC-001` | 1 | ADR-003/ADR-004 |
| `ADR-011` | Boundary HTTP com FastAPI, Pydantic e OpenAPI | `BC-016` | 1 | ADR-002/ADR-010 |
| `ADR-012` | Modelo de interação REST, SSE e polling | `BC-016, BC-010` | 10 | ADR-011 |
| `ADR-013` | Cliente TypeScript gerado e diff gate OpenAPI | `BC-016` | 2 | ADR-010/ADR-011 |
| `ADR-014` | Frontend React, Vite, OpenLayers e workspace cartográfico | `BC-016` | 9 | ADR-010/ADR-013 |
| `ADR-015` | CLI, Direct Runner e núcleo compartilhado | `BC-016` | 2 | ADR-002/ADR-005/ADR-016 |
| `ADR-016` | Application services, Unit of Work, erros e idempotência | `BC-004` | 13 | ADR-005/ADR-018/ADR-020 |
| `ADR-017` | Feature flags e registro de capabilities | `BC-001, BC-009` | 3 | ADR-003/ADR-004 |
| `ADR-018` | PostgreSQL/PostGIS como system of record | `BC-013` | 5 | ADR-002/ADR-003 |
| `ADR-019` | Schemas físicos, UUIDv7, escopo e concorrência | `BC-003, BC-013` | 6 | ADR-018 |
| `ADR-020` | Transactional outbox e consumidores idempotentes | `BC-010` | 2 | ADR-018/ADR-019 |
| `ADR-021` | Filesystem gerenciado, roots e resolução segura | `BC-013` | 1 | ADR-002/ADR-003 |
| `ADR-022` | Object Model: aggregates, identidade e state machines | `BC-003, BC-004, BC-012, BC-013` | 9 | ADR-003/ADR-018 |
| `ADR-023` | ArtifactSet, manifest e bundles imutáveis | `BC-013` | 6 | ADR-021/ADR-022 |
| `ADR-024` | Publicação atômica, checksums e content addressing | `BC-013` | 3 | ADR-021/ADR-023 |
| `ADR-025` | Result snapshots, lineage e visão corrente | `BC-012, BC-013` | 6 | ADR-018/ADR-023 |
| `ADR-026` | Schema registry, migrations e compatibilidade | `BC-013, BC-015` | 4 | ADR-018/ADR-020/ADR-023 |
| `ADR-027` | Backup, restore, retenção e GC reference-aware | `BC-013, BC-014` | 1 | ADR-018/ADR-021/ADR-023/ADR-025 |
| `ADR-028` | Contas locais, sessões server-side e Argon2id | `BC-002` | 4 | ADR-018 |
| `ADR-029` | Federação OIDC e vínculo de identidade | `BC-002` | 3 | ADR-028 |
| `ADR-030` | PATs, autorização central e scopes | `BC-002` | 2 | ADR-028/ADR-029 |
| `ADR-031` | CSRF, CORS, security headers e proteção Web | `BC-002, BC-016` | 3 | ADR-028/ADR-030 |
| `ADR-032` | Secrets, TLS e ingress único | `BC-014, BC-015` | 3 | ADR-031 |
| `ADR-033` | Supply chain, SBOM, assinaturas e dependências | `BC-015` | 1 | ADR-009/ADR-032 |
| `ADR-034` | OCI/Compose, instalação, bootstrap e readiness | `BC-015, BC-014` | 5 | ADR-002/ADR-009/ADR-032/ADR-033 |
| `ADR-035` | Upgrade Controller, mixed versions e rollback | `BC-015` | 7 | ADR-026/ADR-027/ADR-034 |
| `ADR-036` | Celery, RabbitMQ e TaskEnvelope mínimo | `BC-010` | 2 | ADR-018/ADR-020/ADR-034 |
| `ADR-037` | Workers duráveis, leases e fencing | `BC-010` | 12 | ADR-018/ADR-036 |
| `ADR-038` | Retry, quarantine, checkpoints, cancelamento e drain | `BC-010` | 9 | ADR-036/ADR-037 |
| `ADR-039` | Scheduler, fairness, backpressure e Resource Governor | `BC-010` | 10 | ADR-018/ADR-036/ADR-037 |
| `ADR-040` | Progresso, event ledger, replay e ETA | `BC-010, BC-014` | 18 | ADR-036/ADR-039 |
| `ADR-041` | CRS, espaços de coordenadas e axis order | `BC-006, BC-007, BC-008` | 7 | ADR-018 |
| `ADR-042` | Raster validity, output grid, resampling e COG | `BC-006, BC-013` | 10 | ADR-021/ADR-023/ADR-041 |
| `ADR-043` | Stack geoespacial nativa, ABI e isolamento | `BC-006, BC-007` | 8 | ADR-009/ADR-042 |
| `ADR-044` | Pipeline clássico de matching coarse-to-fine | `BC-006` | 14 | ADR-041/ADR-042/ADR-043 |
| `ADR-045` | Estimação geométrica, homografia e seleção de GCPs | `BC-006, BC-007` | 6 | ADR-044 |
| `ADR-046` | SGV, Quality Profiles e aceitação fail-closed | `BC-007, BC-012` | 17 | ADR-041/ADR-044/ADR-045 |
| `ADR-047` | Referências, providers, aquisição e cache governado | `BC-005` | 8 | ADR-021/ADR-041 |
| `ADR-048` | Edit Bundles: CorrectionSet, AnchorSet e revisão humana | `BC-011, BC-012` | 5 | ADR-023/ADR-025/ADR-045/ADR-046 |
| `ADR-049` | Mosaico relativo: grafo, otimização e ancoragem | `BC-008` | 10 | ADR-041/ADR-044/ADR-046/ADR-047 |
| `ADR-050` | Mosaico relativo: verificador, reporting e materialização | `BC-008, BC-012, BC-013` | 8 | ADR-023/ADR-025/ADR-049 |
| `ADR-051` | AI Router, planner e escalonamento classic-first | `BC-009, BC-007` | 5 | ADR-017/ADR-046/ADR-047 |
| `ADR-052` | Inference Engine, ModelRunner, ModelPack e offline | `BC-009, BC-013, BC-015` | 6 | ADR-009/ADR-023/ADR-032/ADR-051 |
| `ADR-053` | Reprodutibilidade científica, benchmarks, promoção e rollback | `BC-006, BC-007, BC-008, BC-009` | 26 | ADR-009/ADR-042/ADR-044/ADR-046/ADR-049/ADR-051/ADR-052 |
| `ADR-054` | Observabilidade, telemetria e diagnósticos operacionais | `BC-014` | 3 | ADR-002/ADR-018/ADR-036 |
| `ADR-055` | Audit ledger, privacidade, redaction e support bundles | `BC-014` | 11 | ADR-018/ADR-021/ADR-028/ADR-054 |
| `ADR-056` | Licenciamento, contribuições, provider attribution e citação | `BC-015` | 1 | ADR-023/ADR-047/ADR-055 |
| `ADR-057` | Release train, publicação e gates de distribuição | `BC-015, BC-001` | 6 | ADR-026/ADR-033/ADR-034/ADR-035/ADR-056 |

## Consistência aplicada

- todos os 376 requisitos possuem exatamente um owner ADR;
- 759 histórias, 869 issues e 759 TaskEnvelopes foram reconciliados;
- sprints e épicos possuem união derivada das ADRs das histórias;
- referências de arquivos de ADR nos TaskEnvelopes apontam somente para arquivos existentes;
- o grafo de 57 decisões é acíclico;
- nenhuma ADR possui seção obrigatória vazia ou decisão aberta;
- ADRs não contêm thresholds ou versões reversíveis que pertençam a profiles, exceto o pin deliberadamente arquitetural do runtime inicial.

## Riscos residuais

| Risco | Tratamento |
|---|---|
| Inventário maior aumentar custo de navegação | Índice, matriz de aplicabilidade, grafo e seleção mínima por TaskEnvelope. |
| História listar ADRs transversais demais | `governing_adrs` é calculado por requisitos, papel e surface; revisão futura pode reduzir sem perder cobertura. |
| Mudança futura recriar sobreposição | `run_adr_review.py` bloqueia IDs ausentes, owners duplicados, ciclos e referências obsoletas. |
| ADR virar local de parâmetro | Gate explícito delega thresholds e tunables a profiles/benchmarks. |

## Conclusão

**Fase D aprovada.** O SAR possui inventário definitivo, contínuo, atômico e rastreável. Nenhuma decisão tecnológica ou arquitetural permanece em aberto para iniciar a próxima fase, sem prejuízo do `ImplementationAuthorizationRecord`.
