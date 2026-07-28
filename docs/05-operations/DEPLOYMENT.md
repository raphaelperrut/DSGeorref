# Deployment

A topologia de runtime ainda não foi implementada. A instalação oficial será reproduzível em servidor único e conterá frontend, API, worker, PostgreSQL/PostGIS, RabbitMQ, reverse proxy e workspaces montados, com CLI disponível ao operador.

## Decisões aceitas

- imagens OCI versionadas e Docker Compose como instalação oficial;
- Celery + RabbitMQ para transporte assíncrono;
- PostgreSQL como estado autoritativo;
- filesystem gerenciado para binários;
- autenticação local com OIDC opcional;
- frontend React/TypeScript/Vite com OpenLayers;
- REST para comandos e SSE com polling de fallback para progresso;
- ingress único publicado, serviços internos em redes privadas e TLS obrigatório em rede;
- secrets por arquivos/contrato em camadas, fora do repositório;
- releases assinadas e upgrades orquestrados por versão/digest verificável.

## Requisitos de implementação

O pacote de instalação implementará reverse proxy como único ingress, TLS, secrets fora do repositório, migrations explícitas, health checks, backup, restore, upgrade e rollback. O primeiro acesso terá assistente web para criação do administrador e registro de raízes de workspace. Arquivos Compose de desenvolvimento e produção serão distintos, sem credenciais padrão ou exposição de portas administrativas. O instalador validará assinatura, provenance, SBOM e digest antes de upgrades, exigirá preflight e BackupSet quando aplicável e nunca seguirá `latest` automaticamente.
## Perfis de hardware e conectividade

A instalação deverá detectar CPU, RAM, GPU/VRAM, drivers e backends compatíveis antes de habilitar ExecutionProfiles. ModelPacks não compatíveis permanecem instalados porém indisponíveis, com diagnóstico explícito. Os modos `offline`, `restricted` e `connected` controlam egress por configuração validada, rede e auditoria; nenhum serviço externo é requisito para o core.

## Evolução compatível de dados — decisões consolidadas na ADR-026

- schemas e artifacts declaram versão e janela de leitura/escrita;
- banco evolui por expand–migrate–contract, sem migration destrutiva automática no startup;
- artifacts originais permanecem imutáveis;
- downgrade incompatível é bloqueado antes de alterar serviços ou dados;
- preflight relaciona versão da aplicação, banco, workers, bundles e `BackupSet`.

As decisões consolidadas na ADR-026 definem rollout por fases, exclusão mútua do `UpgradeController`, evidence gate de cutover e recuperação por fase. As decisões consolidadas em ADR-034 e ADR-054 definem o instalador inicial, bootstrap administrativo, readiness e suporte diagnóstico. As regras consolidadas em ADR-034, ADR-047 e na política de citação definem licença, contribuições, rights manifests e citação; sua materialização continua gate de publicação. As regras da governança e de AP-008 fecham a fase fundacional e autorizam somente a SPRINT-001. O planejamento integral de issues e ADRs continuará em paralelo, sem ampliar a autorização de execução.
## Limite de disponibilidade e escala

A instalação oficial é single-instance, escala verticalmente e não declara HA. Multi-host, active-active, object storage obrigatório ou failover automático exigem nova ADR.
