# Catálogo de módulos técnicos do sistema

Os 18 itens abaixo são componentes ou módulos técnicos. **Eles não são bounded contexts.** A visão semântica canônica está em `docs/02-architecture/ddd/DDD-030-BOUNDED-CONTEXT-CATALOG.md`.

| Módulo | Nome | Natureza DDD | Contexts servidos | Épicos | Histórias |
|---|---|---|---|---:|---:|
| `MOD-001` | CLI | Adapter/Component | `BC-016` | 1 | 5 |
| `MOD-002` | Web UI | Adapter/Component | `BC-016` | 9 | 53 |
| `MOD-003` | HTTP API | Adapter/Component | `BC-002`, `BC-003`, `BC-004`, `BC-005`, `BC-006`, `BC-007`, `BC-008`, `BC-009`, `BC-010`, `BC-011`, `BC-012`, `BC-013`, `BC-014`, `BC-015`, `BC-016` | 32 | 187 |
| `MOD-004` | Domínio + Application Services | Context implementation | `BC-002`, `BC-003`, `BC-004`, `BC-010`, `BC-011`, `BC-012`, `BC-013` | 37 | 217 |
| `MOD-005` | Pipeline geoespacial | Context implementation | `BC-005`, `BC-006`, `BC-008` | 38 | 266 |
| `MOD-006` | Strong Geometric Verifier | Context implementation | `BC-007` | 41 | 284 |
| `MOD-007` | IA governada | Context implementation | `BC-009` | 39 | 270 |
| `MOD-008` | Direct Runner | Adapter/Component | `BC-010` | 13 | 89 |
| `MOD-009` | Workers duráveis | Adapter/Component | `BC-010` | 12 | 84 |
| `MOD-010` | Scheduler + Resource Governor | Context implementation | `BC-010` | 19 | 126 |
| `MOD-011` | PostgreSQL/PostGIS | Adapter/Component | `BC-002`, `BC-003`, `BC-004`, `BC-005`, `BC-006`, `BC-007`, `BC-008`, `BC-009`, `BC-010`, `BC-011`, `BC-012`, `BC-013`, `BC-014`, `BC-015` | 25 | 157 |
| `MOD-012` | Filesystem gerenciado | Adapter/Component | `BC-013` | 49 | 332 |
| `MOD-013` | RabbitMQ | Adapter/Component | `BC-010` | 12 | 84 |
| `MOD-014` | Providers externos | Context implementation | `BC-005` | 42 | 290 |
| `MOD-015` | OIDC opcional | Adapter/Component | `BC-002` | 5 | 25 |
| `MOD-016` | Observabilidade + Auditoria | Adapter/Component | `BC-014` | 11 | 66 |
| `MOD-017` | Instalação + Supply Chain | Adapter/Component | `BC-015` | 33 | 184 |
| `MOD-018` | Backup + Retenção | Adapter/Component | `BC-013`, `BC-014` | 15 | 90 |
