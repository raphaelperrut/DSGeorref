# SAR-100 — Deployment e operações

## Deployment oficial

Single-instance por imagens OCI assinadas e Compose: ingress TLS, API, worker(s), scheduler/controller, PostgreSQL/PostGIS, RabbitMQ, collector de telemetria e volumes gerenciados.

## Operação

- Bootstrap declarativo e idempotente; admin one-time sem credencial padrão.
- Health, readiness e capability probes separados.
- Upgrade por controller singleton, drain, migration faseada, cutover e rollback.
- Backup/restore testado em ambiente isolado.
- Secrets por files/secret store suportado; nunca em env dump, log ou manifest.
- Supply chain com lockfiles, SBOM, provenance, signatures e vulnerability/license gates.
