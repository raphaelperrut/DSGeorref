# SAR-040 — Registro definitivo de decisões

## Snapshot histórico da Fase D

A Fase D substituiu o inventário agregado de 25 ADRs por **57 ADRs atômicas**, contínuas e sem decisões abertas.
Essa contagem é o snapshot histórico da Fase D; a tabela abaixo preserva o registro daquele fechamento e não representa, isoladamente, o inventário corrente.

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

## Estado corrente

- `TOTAL_ADR_RECORDS = 59` (`ADR-001`..`ADR-059`);
- `ACTIVE_ACCEPTED_ADRS = 58`;
- `SUPERSEDED_ADRS = 1` (`ADR-058`);
- `OPEN_ARCHITECTURAL_DECISIONS = 0`.

As decisões posteriores ao snapshot da Fase D são:

| ADR | Decisão | Estado | Contexts | Requisitos owned |
|---|---|---|---|---:|
| `ADR-058` | Delivery Approval Authority e attestations criptográficas independentes | `Superseded` prospectivamente por `ADR-059`; autoridade histórica para DAA 1.0.0 | BC-001 | 0 |
| `ADR-059` | Delivery Approval Authority em desenvolvimento solo | `Accepted`; autoridade prospectiva para DAA 2.0.0 | BC-001 | 0 |

Assim, “22 ADRs” permanece somente como snapshot histórico das Fases A/B, “57 ADRs” permanece como snapshot histórico da Fase D, e nenhuma dessas quantidades é a contagem ativa vigente.

## Regras

- um boundary material possui um único owner normativo;
- parâmetros reversíveis permanecem em profiles/benchmarks;
- detalhes de implementação permanecem nas issues;
- a matriz `ADR_APPLICABILITY_MATRIX.csv` e o grafo `ADR_DEPENDENCY_GRAPH.json` são canônicos.


## Registro prévio à atribuição de ID — recuperação #1026

- **Fonte:** [decisão consolidada do Owner](https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6102594277).
- **Baseline:** `eb22e2e34d9080a6486851cc609b848df7871ae5`.
- **Classificação anterior ao identificador:** `NEW_ADR`, em conformidade com REQ-GOV-DEC-001.
- **Objeto aprovado:** uma única sucessora da ADR-006, para reconciliação
  permanente da governança operacional solo e recuperação excepcional de uso
  único da #1026, em BC-001.
- **Boundary a substituir:** prompts permanentes, TaskEnvelope e precedência
  de instruções, quanto ao modelo de competências e à comprovação prévia de
  atribuição/execução na recuperação. As demais decisões e refinamentos da
  ADR-006, inclusive SharedPartialDeliveryGate, devem ser preservados.
- **Autoridades preservadas:** ADR-007 para scopes, lanes, isolamento e handoff;
  ADR-058/ADR-059 para DAA e trust, sem nova autorização de regime ou identidade.
- **ID e filename da sucessora:** não atribuídos; sequência do inventário não
  constitui ato de atribuição.
- **TaskEnvelope operacional da #1026:** não atribuído; TASK-0041 não é reutilizado.
- **Eficácia da alteração e da exceção:** não declarada; autorização técnica
  específica e avaliações segregadas continuam exigidas.
- **Registro do ato e do procedimento aprovado:** [CHANGE_CONTROL](../../00-governance/CHANGE_CONTROL.md#issue-1026-owner-decision).

Este registro administrativo de classificação não é uma ADR Accepted, não
reserva identificador e não altera os totais ou o grafo vigentes. A ADR-006
permanece Accepted e autoritativa até sucessão legitimamente formalizada.

## Atribuição manual e estado corrente — #1026

Fonte executiva: https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6103942173. Origem autenticada no GitHub: raphaelperrut, user ID
110496238. O registro prévio acima é histórico e permanece preservado.
Sua classificação está no commit 19d5dd00064d03f581b45881a5db73ada8344a74, digest do blob Git SHA-256
2b8c72b35bdb518f8cb5981d84ceeaed213d3d65843941c452cc99d2eaa59e22, anterior à atribuição dos IDs.

Conferência real: 59 ADRs contínuas, 774 envelopes únicos (765 canônicos e nove
operacionais), maiores IDs ADR-059/TASK-0774, sem colisão com ADR-060/TASK-0775.
Por delegação executiva do Owner, atribuição MANUAL de ADR-060 (docs/02-architecture/adrs/ADR-060-governanca-operacional-solo-e-recuperacao-excepcional-de-bootstrap.md) e
TASK-0775 (.codex/tasks/operations/TASK-0775.json), exclusivamente para #1026.
STORY-0688/EPIC-001/SPRINT-001 são linhagem existente, sem criar história canônica.

Estado prospectivo: TOTAL_ADR_RECORDS=60, ACTIVE_ACCEPTED_ADRS=58,
SUPERSEDED_ADRS=2 (ADR-006/ADR-058), OPEN_ARCHITECTURAL_DECISIONS=0.
A direção ADR-060 é Accepted por ato do Owner; QA/final review e merge pendentes.
Histórico, matrizes congeladas e DAA 1.0.0/2.0.0 permanecem preservados.


## Registro prévio de integração — recuperação #1026

- **Fonte:** [reconstrução autorizada pelo Owner](https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6113485169).
- **Baseline:** `be97cea01ea2a812e4206cfe0d446f5919b2a8dc`.
- **Classificação anterior ao identificador:** `NEW_ADR`, para reconstituir a prova anterior à rematerialização.
- **Objeto aprovado:** uma única sucessora da ADR-006, conservando o boundary e a identidade lógica originais.
- **Identidades:** sem nova atribuição lógica; unicidade conferida em main antes da rematerialização.
- **Controles preservados:** ADR-007, SharedPartialDeliveryGate, DAA/trust, scopes e fail-closed.
- **Sequência:** este registro antecede a primeira adição da sucessora no histórico de integração.
- **Evidências originais:** classificação em 19d5dd00064d03f581b45881a5db73ada8344a74 e candidato 8b8a97923bc573b08724a5aa9090f4b853417940 preservados.
- **QA/Reviewer:** novas avaliações exigidas; nenhuma aprovação anterior é transferida.


## Rematerialização autorizada das identidades — integração #1026

A decisão https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6113485169 mantém as identidades lógicas ADR-060/TASK-0775.
Conferência sobre main be97cea01ea2a812e4206cfe0d446f5919b2a8dc: 59 ADRs, 774 envelopes únicos,
sem colisão de ADR-060/TASK-0775; rematerialização não cria outro registro lógico.
Classificação substituta real: d1e62d26b5902e82dda5b96744ce5ac9e45fd65b; blob SHA-256 b848e98486728be4fd7b116a7ab80c6d9864fdf957b2a4069ba8dede773503dd.
A primeira adição de ADR-060 e TASK-0775 no novo histórico é este commit de
materialização, que constitui o checkpoint substituto autorizado uma única vez.
Envelope mantido com bytes originais; o digest canônico será recalculado, e a
correspondência do SHA real será registrada no commit candidato descendente.
A conferência administrativa é MANUAL / DEVIATION_DECLARED, sem PASS ordinário
retroativo. QA/Review incrementais permanecem pendentes.
