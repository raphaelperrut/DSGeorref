# Observabilidade e auditoria

## Estado normativo

A arquitetura foi aprovada nas decisões consolidadas na ADR-054:

- OpenTelemetry com backends substituíveis;
- canal de auditoria append-only e separado;
- allowlist, classificação e redaction estruturada;
- sinais em camadas, cardinalidade limitada e retenção por finalidade.

## Separação obrigatória

1. **telemetria operacional:** diagnóstico de desempenho, disponibilidade e consumo;
2. **audit trail:** operações privilegiadas e decisões humanas, sem sampling;
3. **resultados científicos:** GCPs, SGV, deformação, falhas e lineage no PostgreSQL/exports;
4. **logs de desenvolvimento:** detalhes adicionais somente em ambiente controlado.

## Baseline de sinais

- logs estruturados;
- métricas de baixa cardinalidade;
- traces para request, job, attempt, worker e ArtifactSet;
- correlation IDs propagados por API, Celery e pipeline;
- dashboards e alertas para API, RabbitMQ, workers, PostgreSQL, filesystem, Resource Governor, providers, BackupSets e restore drills.

## Métricas operacionais mínimas

- fila, throughput, duração e idade dos jobs;
- falhas agregadas por taxonomia e estágio;
- retries, cancelamentos e checkpoints;
- RAM, CPU, GPU e disco temporário;
- cache, provider latency e downloads;
- accepted, needs_review e rejected em agregados seguros;
- backups, restore drills, retenção e GC;
- perda de export, sampling e budget de cardinalidade.

## Auditoria

Eventos de auditoria usam schema próprio, persistência append-only, permissões restritas, particionamento, digests periódicos e exportação opcional assinada. O nível de log não pode alterar sua emissão.

## Privacidade e redaction

- secrets, cookies, tokens, chaves e headers de autorização são proibidos;
- bytes de imagens e payloads integrais não são registrados;
- paths absolutos são proibidos por padrão;
- nomes e caminhos relativos aparecem apenas em contextos autorizados;
- novos atributos exigem classificação e teste de vazamento;
- bundles de suporte passam por preview e sanitização fail-closed.

## Cardinalidade e retenção

IDs de imagem, paths e jobs não são labels ilimitados. Métricas científicas completas permanecem no domínio. Retenção e acesso são definidos por tipo de sinal e integrados à RetentionPolicy.

## Perfil mínimo

A instalação continua funcional sem backend comercial ou stack completa. Logs JSON, métricas essenciais e audit trail permanecem disponíveis; exporters adicionais são opcionais.


## Scheduler e isolamento — decisões consolidadas na ADR-039

A telemetria deve permitir observar classes de serviço, espera, aging, prioridade solicitada/efetiva, fan-out, backpressure, leases, heartbeats, preempções seguras, reservas, quotas e circuit breakers. Esses sinais permanecem agregados em métricas e correlacionados por eventos/traces para drill-down.

## Observabilidade do scheduler — decisões consolidadas em ADR-039 e ADR-054

Métricas são agregadas por classe, estágio, estado, recurso e motivo de espera. IDs detalhados permanecem no event ledger, traces e timelines correlacionadas. Eventos registram policy, motivo e ator aplicável.

Progresso usa unidades de trabalho por estágio. Estimativas apresentam intervalo, confiança e fatores de variação, ou `estimativa_indisponivel`. SLOs por classe cobrem admissão, espera, aging, responsividade, jobs sem progresso, leases, backpressure e breakers.

O dashboard aplica RBAC e mostra aos usuários apenas seus jobs autorizados. Ações administrativas passam por preflight, safe boundaries, idempotência e audit trail append-only.

Snapshots seletivos, replay offline, equivalência por invariantes e bundles governados seguem as decisões consolidadas em ADR-054 e ADR-053. O replay operacional não executa imagens por padrão. O replay científico segue as decisões consolidadas na ADR-053 e correlaciona ambiente, seeds, tolerâncias, runners e artifacts sem misturá-lo com decisões de fila. Baselines, selection tiers, evidence bundles, canary e rollback científico seguem as decisões consolidadas na ADR-053 e devem permanecer correlacionáveis sem transformar IDs em labels de alta cardinalidade.
## SLI/SLO congelados pela Fase G

O catálogo normativo está em `contracts/operations/slo-sli-catalog.yaml`. Métricas de alta cardinalidade, secrets, paths absolutos, bytes raster e identificadores ilimitados são proibidos. Alertas são por sintomas e budget, com drill-down por correlação.
