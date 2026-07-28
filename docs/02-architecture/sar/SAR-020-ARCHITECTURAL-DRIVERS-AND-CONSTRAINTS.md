# SAR-020 — Drivers e restrições arquiteturais

## Drivers

1. Minimizar falso aceite geométrico.
2. Preservar reproducibilidade, lineage e auditabilidade.
3. Processar lotes de 40–300 imagens com sucesso parcial explícito.
4. Operar em single-instance por equipe pequena sem microservices prematuros.
5. Suportar execução offline/restricted e IA opcional.
6. Permitir implementação paralela por agentes com escopos disjuntos.

## Restrições fechadas

- Monólito modular; processos separados apenas por característica operacional.
- PostgreSQL 18/PostGIS 3.6 + filesystem gerenciado; sem object storage obrigatório.
- RabbitMQ/Celery como transporte/runner; sem autoridade de estado.
- REST/OpenAPI 3.1, SSE e polling de reconciliação.
- React/OpenLayers SPA, contas locais e OIDC opcional.
- OCI/Compose como deployment oficial.
- Software e dependências livres/open source; aquisição externa gratuita e license-governed.

## Limites

- Sem multitenancy, billing, treino automático, GPU obrigatória, download silencioso ou override de hard gate.
