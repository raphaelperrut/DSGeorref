# SAR-050 — Visão de containers/processos

| Node | Nome | Responsabilidade | ADRs |
|---|---|---|---|
| `cli` | CLI | Projetos, ingestão, jobs e resultados com contratos estáveis. | ADR-002 |
| `web` | Web UI | Experiência guiada, workspace cartográfico, triagem e revisão. | ADR-002, ADR-028, ADR-048 |
| `api` | HTTP API | Comandos e consultas REST, OpenAPI, SSE e polling de reconciliação. | ADR-002, ADR-028 |
| `domain` | Domínio + Application Services | Regras de negócio únicas, ports, UoW, ProcessingPlan e erros tipados. | ADR-002, ADR-026 |
| `geo` | Pipeline geoespacial | Matching coarse-to-fine, homografia projetiva, GCPs, grafo e mosaico relativo. | ADR-044, ADR-041, ADR-049, ADR-050 |
| `sgv` | Strong Geometric Verifier | Aceitação fail-closed, métricas geométricas e Image Deformation Profile. | ADR-046, ADR-053 |
| `ai` | IA governada | Escalonamento opcional, ModelRunner e ModelPacks assinados sem bypass do SGV. | ADR-051, ADR-053 |
| `direct` | Direct Runner | Execução síncrona sobre o mesmo núcleo. | ADR-002, ADR-036 |
| `workers` | Workers duráveis | Work units, retry classificado, checkpoints, cancelamento e idempotência. | ADR-036 |
| `scheduler` | Scheduler + Resource Governor | Fairness, backpressure, leases, fencing, quotas e budgets de CPU/RAM/GPU/disco. | ADR-039, ADR-054 |
| `postgres` | PostgreSQL/PostGIS | System of record para estado, geometrias, jobs, audit, lineage e outbox. | ADR-018, ADR-026 |
| `filesystem` | Filesystem gerenciado | Originais e ArtifactSets imutáveis, publicação atômica e checksums. | ADR-018, ADR-041, ADR-027 |
| `broker` | RabbitMQ | Transporte de work units; nunca fonte de verdade. | ADR-036 |
| `providers` | Providers externos | Busca e aquisição gratuita, guiada, allowlisted e license-governed. | ADR-047 |
| `oidc` | OIDC opcional | Federação opcional mantendo contas locais e autorização da instância. | ADR-028 |
| `observability` | Observabilidade + Auditoria | OpenTelemetry, sinais de baixa cardinalidade, audit append-only e redaction. | ADR-054 |
| `deployment` | Instalação + Supply Chain | OCI/Compose, TLS, secrets, SBOM, assinaturas, upgrades e rollback. | ADR-034, ADR-026 |
| `backup` | Backup + Retenção | BackupSet coordenado, restore drills, retention e GC reference-aware. | ADR-027 |

## Relações

| Origem | Relação | Destino |
|---|---|---|
| `cli` | `invoca` | `domain` |
| `web` | `REST/SSE/polling` | `api` |
| `api` | `adapta contratos` | `domain` |
| `domain` | `orquestra ProcessingPlan` | `geo` |
| `geo` | `submete candidatos` | `sgv` |
| `geo` | `escalona quando elegível` | `ai` |
| `ai` | `mesma aceitação independente` | `sgv` |
| `domain` | `execução síncrona` | `direct` |
| `domain` | `work units` | `workers` |
| `scheduler` | `admission/fairness/resources` | `workers` |
| `domain` | `UoW/system of record` | `postgres` |
| `domain` | `ArtifactSets/inputs` | `filesystem` |
| `workers` | `ack/redelivery` | `broker` |
| `workers` | `estado/checkpoints/outbox` | `postgres` |
| `geo` | `gateway governado` | `providers` |
| `api` | `federação opcional` | `oidc` |
