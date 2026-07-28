# SAR-040 — Registro definitivo de decisões

A Fase D substituiu o inventário agregado de 25 ADRs por **57 ADRs atômicas**, contínuas e sem decisões abertas.

| ADR | Decisão | Estado | Contexts | Requisitos owned |
|---|---|---|---|---:|
| `ADR-001` | Topologia do repositório, monorepo e workspaces | `Accepted` | BC-001 | 4 |
| `ADR-002` | Topologia do produto: monólito modular e instância única | `Accepted` | BC-001 | 11 |
| `ADR-003` | Bounded Contexts, subdomínios e linguagem ubíqua | `Accepted` | BC-001 | 0 |
| `ADR-004` | Integração entre contexts e modelos publicados | `Accepted` | BC-001 | 1 |
| `ADR-005` | Layout context-first e direção de dependências | `Accepted` | BC-001 | 2 |
| `ADR-006` | Prompts permanentes, TaskEnvelope e precedência de instruções | `Accepted` | BC-001 | 16 |
| `ADR-007` | Write scopes, lanes paralelas e isolamento de mudança | `Accepted` | BC-001 | 1 |
| `ADR-008` | Granularidade de histórias e limites anti-monólito | `Accepted` | BC-001 | 13 |
| `ADR-009` | Runtime Python 3.12, toolchain e stack nativa reproduzível | `Accepted` | BC-001, BC-015 | 14 |
| `ADR-010` | API-first, versionamento e contract freeze | `Accepted` | BC-001 | 1 |
| `ADR-011` | Boundary HTTP com FastAPI, Pydantic e OpenAPI | `Accepted` | BC-016 | 1 |
| `ADR-012` | Modelo de interação REST, SSE e polling | `Accepted` | BC-016, BC-010 | 10 |
| `ADR-013` | Cliente TypeScript gerado e diff gate OpenAPI | `Accepted` | BC-016 | 2 |
| `ADR-014` | Frontend React, Vite, OpenLayers e workspace cartográfico | `Accepted` | BC-016 | 9 |
| `ADR-015` | CLI, Direct Runner e núcleo compartilhado | `Accepted` | BC-016 | 2 |
| `ADR-016` | Application services, Unit of Work, erros e idempotência | `Accepted` | BC-004 | 13 |
| `ADR-017` | Feature flags e registro de capabilities | `Accepted` | BC-001, BC-009 | 3 |
| `ADR-018` | PostgreSQL/PostGIS como system of record | `Accepted` | BC-013 | 5 |
| `ADR-019` | Schemas físicos, UUIDv7, escopo e concorrência | `Accepted` | BC-003, BC-013 | 6 |
| `ADR-020` | Transactional outbox e consumidores idempotentes | `Accepted` | BC-010 | 2 |
| `ADR-021` | Filesystem gerenciado, roots e resolução segura | `Accepted` | BC-013 | 1 |
| `ADR-022` | Object Model: aggregates, identidade e state machines | `Accepted` | BC-003, BC-004, BC-012, BC-013 | 9 |
| `ADR-023` | ArtifactSet, manifest e bundles imutáveis | `Accepted` | BC-013 | 6 |
| `ADR-024` | Publicação atômica, checksums e content addressing | `Accepted` | BC-013 | 3 |
| `ADR-025` | Result snapshots, lineage e visão corrente | `Accepted` | BC-012, BC-013 | 6 |
| `ADR-026` | Schema registry, migrations e compatibilidade | `Accepted` | BC-013, BC-015 | 4 |
| `ADR-027` | Backup, restore, retenção e GC reference-aware | `Accepted` | BC-013, BC-014 | 1 |
| `ADR-028` | Contas locais, sessões server-side e Argon2id | `Accepted` | BC-002 | 4 |
| `ADR-029` | Federação OIDC e vínculo de identidade | `Accepted` | BC-002 | 3 |
| `ADR-030` | PATs, autorização central e scopes | `Accepted` | BC-002 | 2 |
| `ADR-031` | CSRF, CORS, security headers e proteção Web | `Accepted` | BC-002, BC-016 | 3 |
| `ADR-032` | Secrets, TLS e ingress único | `Accepted` | BC-014, BC-015 | 3 |
| `ADR-033` | Supply chain, SBOM, assinaturas e dependências | `Accepted` | BC-015 | 1 |
| `ADR-034` | OCI/Compose, instalação, bootstrap e readiness | `Accepted` | BC-015, BC-014 | 5 |
| `ADR-035` | Upgrade Controller, mixed versions e rollback | `Accepted` | BC-015 | 7 |
| `ADR-036` | Celery, RabbitMQ e TaskEnvelope mínimo | `Accepted` | BC-010 | 2 |
| `ADR-037` | Workers duráveis, leases e fencing | `Accepted` | BC-010 | 12 |
| `ADR-038` | Retry, quarantine, checkpoints, cancelamento e drain | `Accepted` | BC-010 | 9 |
| `ADR-039` | Scheduler, fairness, backpressure e Resource Governor | `Accepted` | BC-010 | 10 |
| `ADR-040` | Progresso, event ledger, replay e ETA | `Accepted` | BC-010, BC-014 | 18 |
| `ADR-041` | CRS, espaços de coordenadas e axis order | `Accepted` | BC-006, BC-007, BC-008 | 7 |
| `ADR-042` | Raster validity, output grid, resampling e COG | `Accepted` | BC-006, BC-013 | 10 |
| `ADR-043` | Stack geoespacial nativa, ABI e isolamento | `Accepted` | BC-006, BC-007 | 8 |
| `ADR-044` | Pipeline clássico de matching coarse-to-fine | `Accepted` | BC-006 | 14 |
| `ADR-045` | Estimação geométrica, homografia e seleção de GCPs | `Accepted` | BC-006, BC-007 | 6 |
| `ADR-046` | SGV, Quality Profiles e aceitação fail-closed | `Accepted` | BC-007, BC-012 | 17 |
| `ADR-047` | Referências, providers, aquisição e cache governado | `Accepted` | BC-005 | 8 |
| `ADR-048` | Edit Bundles: CorrectionSet, AnchorSet e revisão humana | `Accepted` | BC-011, BC-012 | 5 |
| `ADR-049` | Mosaico relativo: grafo, otimização e ancoragem | `Accepted` | BC-008 | 10 |
| `ADR-050` | Mosaico relativo: verificador, reporting e materialização | `Accepted` | BC-008, BC-012, BC-013 | 8 |
| `ADR-051` | AI Router, planner e escalonamento classic-first | `Accepted` | BC-009, BC-007 | 5 |
| `ADR-052` | Inference Engine, ModelRunner, ModelPack e offline | `Accepted` | BC-009, BC-013, BC-015 | 6 |
| `ADR-053` | Reprodutibilidade científica, benchmarks, promoção e rollback | `Accepted` | BC-006, BC-007, BC-008, BC-009 | 26 |
| `ADR-054` | Observabilidade, telemetria e diagnósticos operacionais | `Accepted` | BC-014 | 3 |
| `ADR-055` | Audit ledger, privacidade, redaction e support bundles | `Accepted` | BC-014 | 11 |
| `ADR-056` | Licenciamento, contribuições, provider attribution e citação | `Accepted` | BC-015 | 1 |
| `ADR-057` | Release train, publicação e gates de distribuição | `Accepted` | BC-015, BC-001 | 6 |

## Regras

- um boundary material possui um único owner normativo;
- parâmetros reversíveis permanecem em profiles/benchmarks;
- detalhes de implementação permanecem nas issues;
- a matriz `ADR_APPLICABILITY_MATRIX.csv` e o grafo `ADR_DEPENDENCY_GRAPH.json` são canônicos.
