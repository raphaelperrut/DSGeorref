# SAR-090 — Visão de runtime e falhas

## Fluxo síncrono

CLI/API → application service → UoW → domínio/ports → PostgreSQL/filesystem → resposta tipada.

## Fluxo assíncrono

Comando → transação + outbox → scheduler/admission → RabbitMQ → worker → checkpoint/commit → ack → event ledger → SSE/polling.

## Falhas

- Retry somente para falha técnica classificada.
- Erro de domínio não é retry técnico.
- Crash/redelivery é idempotente e protegido por lease/fencing.
- Cancelamento é cooperativo em safe points; terminate é contenção final.
- Poison message vai para quarantine registrada no PostgreSQL.
- Artifact parcial nunca é publicado.
