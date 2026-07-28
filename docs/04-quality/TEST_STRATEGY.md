# Estratégia de testes

- **Unit:** domínio, geometria, parsing e políticas.
- **Knowledge extraction:** comportamento relevante de sistemas anteriores convertido em especificação/teste novo, sem importar código.
- **Integration:** banco, workspace, fila e providers controlados, incluindo ativos gratuitos, indisponíveis, restritos e potencialmente pagos.
- **Contract:** CLI, OpenAPI, schemas, eventos e artefatos.
- **E2E:** registrar diretório/ingestão → plano guiado → job → review → artefatos, por CLI e browser; tutorial e projeto demonstrativo também terão jornadas E2E.
- **Geo regression:** corpus versionado com ground truth, décadas/sensores/condições distintas, tolerâncias por classe e diagnóstico de falso positivo.
- **Security:** autenticação/autorização, uploads hostis, SSRF, path traversal, symlink escape, zip bomb, limites, secrets e prova de que providers não executam compras ou pedidos pagos.
- **Performance:** lote, memória, disco, CPU/GPU, filas e throughput por imagem.
- **Resilience:** cancelamento, retry, worker loss, banco indisponível, disco cheio, restore e rollback.

Cobertura isolada não prova qualidade geométrica. Critérios críticos exigem testes semânticos e corpus real.


## Suites obrigatórias do Strong Geometric Verifier

- baixo RMSE com shear excessivo deve ser rejeitado;
- pontos concentrados, poucos quadrantes e convex hull insuficiente não podem ser autoaceitos;
- reflexão, inversão, homografia degenerada, condition number alto, escala/área implausível e foldover devem ser bloqueados;
- métrica crítica ausente ou NaN deve falhar em modo fechado;
- termos projetivos desnecessariamente extremos devem ser detectados pelo SGV, mantendo a homografia como contrato final;
- revisão humana deve preservar o veredito automático e a justificativa;
- artefato definitivo não é publicado para `needs_review` ou `rejected`;
- Image Deformation Profile detecta expansão/compressão, anisotropia, shear local, foldover e nodata introduzido;
- rotação, escala ou reprojeção esperada não são indevidamente classificadas como defeito.

## Suites de lotes, catálogo e relatórios

- benchmarks de processamento com lotes representativos de 40, 100 e 300 imagens;
- catálogo sintético na ordem de 190.000 registros sem alocação proporcional no browser;
- adaptação/redução de concorrência sob pressão de RAM e disco temporário;
- chunking, backpressure, checkpoint, cancelamento e retomada após perda de worker;
- reconciliação de contadores do batch pai com itens filhos;
- busca por nome/diretório/hash e filtros por status/failure code;
- exportação streaming de sucessos e falhas sem timeout ou materialização integral em memória;
- integridade de nome, raiz e caminho relativo em banco e exports;
- compatibilidade de schema de relatório e taxonomia entre versões suportadas;
- bundle sob demanda de uma imagem com métricas, gates, GCPs, previews e checksums.

## Suites de raster, margens e proveniência

- bordas exatamente pretas/brancas e próximas desses valores não produzem features ou matches de terreno;
- terreno realmente escuro/claro não é automaticamente descartado por threshold global;
- faixas de voo, marcas fiduciais, datas, legendas e identificadores marginais permanecem pixel a pixel na extensão de saída, salvo profile explícito;
- a máscara analítica altera apenas análise e métricas, nunca recorta silenciosamente o raster;
- resolução de saída, razão de reamostragem e método ficam registrados; redução e superamostragem injustificadas falham em policy;
- COG aceito passa validação estrutural, overviews, geotransform, CRS, nodata e checksum;
- falha durante staging não publica ArtifactSet parcial;
- troca de versão atual não altera artefatos antigos;
- manifesto e bundle resolvem hashes, profiles, software, modelos, referências e decisões humanas.

## Suites obrigatórias de máscara, multirresolução e homografia

- máscara adaptativa em bordas quase pretas/brancas, gradientes, textos, fiduciais e terreno extremo;
- correção visual reproduzível sem alteração de pixels nem recorte da saída;
- OCR opcional incapaz de modificar a homografia sem capability futura explícita;
- round-trip de coordenadas entre pirâmides/tiles e refinamento em resolução adequada;
- homografia projetiva em casos quase afins e perspectivas legítimas;
- rejeição de colinearidade, duplicatas, concentração, degeneração, inversão, foldover e fallback oculto;
- manifesto declara modelo, método robusto, matcher, máscara, escalas e parâmetros efetivos.

## Suites de correspondências, estimação e grafo de referências

- instalação sem IA/GPU executa caminho clássico completo;
- escalonamento para IA é determinístico, explicado e registrado;
- `USAC_MAGSAC` é o padrão e nenhuma tentativa troca silenciosamente para RANSAC;
- RANSAC explícito usa parâmetros/QualityProfile próprios e permanece submetido aos hard gates;
- seleção de GCPs evita clusters, preserva hull/quadrantes e exporta motivos de descarte;
- dois grupos espacialmente disjuntos no mesmo lote formam componentes independentes;
- nome, diretório, sequência ou similaridade visual isolada não criam aresta operacional;
- cada imagem dependente recalcula homografia e passa pelo SGV, mesmo com seed `accepted`;
- ausência de referência segura produz falha acionável sem bloquear sucessos de outros componentes;
- invalidação/supersessão de seed reavalia descendentes sem alterar artefatos imutáveis.

## Descoberta espacial e componentes

- lotes com uma, duas e múltiplas regiões disjuntas;
- agrupamentos provisórios incorretos que não podem criar aresta operacional;
- recall e custo do candidate budget, incluindo estado `not_examined_due_to_budget`;
- aresta com score visual alto, mas geometria inválida, obrigatoriamente rejeitada;
- aceitação A→B sem transitividade automática para C;
- sucesso parcial com retry somente do componente não resolvido;
- supersessão de seed e reavaliação dos descendentes.
## Providers, busca e cache

- testes de contrato para adapters STAC e APIs oficiais com capacidades ausentes explícitas;
- SSRF, redirects, DNS rebinding, URLs privadas, credenciais em URL, timeouts e limites de bytes;
- ativos `free`, `restricted`, `paid`, `unknown`, removidos e com licença alterada;
- garantia de que nenhuma credencial ou endpoint permite compra/pedido/checkout;
- buscas com AOI/época exatas, aproximadas e desconhecidas, respeitando budget e expansão;
- ranking explicado por critérios, sem transformar score em prova geométrica;
- cache hit/miss, deduplicação, checksum divergente, GC e proteção por lineage;
- bundle de reprodução que referencia, mas não redistribui, ativos sem permissão.

## Revisão visual, CorrectionSets e fila posterior

- lote conclui o ciclo automático e publica itens `accepted` mesmo com fila de revisão pendente;
- ausência de revisão não promove `needs_review`/`rejected`;
- CorrectionSet não altera tentativa anterior e sempre cria nova tentativa;
- nova tentativa recalcula homografia, resíduos, deformação e SGV integralmente;
- hard gates permanecem não revisáveis após edição manual;
- GCPs automáticos/manuais/inliers/outliers/desabilitados preservam identidade, eventos e proveniência;
- round-trip GeoPackage/GeoJSON/CSV/manifesto mantém coordenadas, versões e estados;
- priorização da fila é explicável, filtrável e não oculta itens de baixa prioridade;
- operações em lote não aprovam resultados, não editam GCPs e não promovem seeds;
- correção de seed exibe e reavalia impacto sobre descendentes.

## Retry, checkpoints, cancelamento e snapshots

- somente códigos transitórios configurados recebem retry automático;
- budget, backoff, jitter e idempotency key evitam loops e duplicação de efeitos;
- rejeição do SGV, entrada inválida e ausência de referência não repetem o mesmo plano cegamente;
- PlanVariant registra diff, motivo e versões da nova tentativa;
- checkpoint compatível retoma o estágio e checkpoint incompatível é invalidado com motivo;
- corrupção ou ausência de intermediário força recomputação segura;
- cancelamento por imagem, componente e lote preserva sucessos publicados não afetados;
- timeout de contenção não publica temporários e deixa estado reconciliável;
- snapshots anteriores permanecem imutáveis após retries e remediações;
- visão vigente é determinística e contadores distinguem sucesso automático, técnico, algorítmico e humano.

## Suites de backup, restore e ciclo de vida

- inconsistência entre dump do banco e manifesto de arquivos bloqueia restauração;
- BackupSet com checksum inválido é rejeitado;
- restore drill abre amostras de COG, GPKG, manifests e reconstrói jobs pendentes;
- ausência de raiz externa é reportada explicitamente, sem substituição silenciosa;
- RetentionPolicy protege resultado vigente, snapshot fixado, lineage e hold;
- GC não remove conteúdo deduplicado ainda referenciado;
- corrida entre nova referência e purga é revalidada antes da exclusão;
- tombstone, quarentena, restauração e purga são idempotentes;
- arquivos de acervo externo nunca são apagados pela policy padrão.

## Observabilidade, auditoria e privacidade

- `test_opentelemetry_context_propagation`: request, job, attempt, worker e ArtifactSet preservam correlação sem acoplar o domínio ao backend;
- `test_audit_append_only_digest_and_no_sampling`: evento privilegiado não pode ser atualizado/apagado pela aplicação e é coberto por digest;
- `test_log_redaction_and_support_bundle_fail_closed`: secrets, paths absolutos e bytes de imagem não escapam em logs, traces ou bundles;
- `test_metric_cardinality_budget_and_scientific_data_separation`: labels de alta cardinalidade são rejeitadas e métricas científicas completas permanecem no banco;
- `test_observability_exporter_outage_does_not_corrupt_job`: falha do exporter não altera estado científico nem publica artefato inválido;
- `test_signal_retention_by_class`: logs, traces, métricas e auditoria respeitam policies independentes e holds aplicáveis.
## Segurança da instalação e releases

- testar permissões, proprietário, ausência, rotação e recuperação de cada classe de secret;
- verificar que secrets não aparecem em logs, traces, manifests, comandos ou bundles de suporte;
- inspecionar portas publicadas e provar isolamento de PostgreSQL, RabbitMQ e workers;
- executar cenários TLS válido, expirado, ausente e proxy institucional;
- validar lockfiles, digests de imagens base e SHAs completos de Actions;
- gerar e verificar SBOM, assinatura OCI, checksums e provenance em release de teste;
- executar upgrade compatível, falha durante migration, falha pós-start e rollback/restore;
- provar que `latest` ou artefato não assinado não é aceito pelo instalador.
## Hardware, ModelRunners, ModelPacks e offline

- executar smoke e integração do pipeline em ambiente CPU-only;
- validar GPU disponível, indisponível, incompatível, sem memória e perda durante tentativa;
- provar ausência de troca silenciosa de dispositivo, runner ou precisão;
- comparar runners/dispositivos em corpus de equivalência com tolerâncias versionadas;
- rejeitar ModelPack com assinatura, hash, licença, provenance ou compatibilidade inválida;
- importar ModelPack e release em ambiente air-gapped;
- executar modo offline com teste de rede que falha se qualquer egress ocorrer;
- validar modos restricted e connected, allowlists, budgets e auditoria.
## Corpus, Promotion Gate e portfólio neural

- provar separação entre desenvolvimento, calibração e teste cego;
- detectar vazamento de item ou hash entre splits proibidos;
- reprovar ModelPack com regressão crítica apesar de ganho médio;
- comparar runners/dispositivos conforme nível de reprodutibilidade declarado;
- provar que NetVLAD apenas ranqueia candidatos e nunca produz aprovação;
- provar escalonamento esparso → semi-denso/cross-modality → denso somente quando elegível e dentro do budget;
- provar que ausência de um ModelPack não altera silenciosamente algoritmo ou qualidade;
- provar que nenhum job atualiza pesos ou incorpora dados de usuário em treinamento;
- executar adapters de referência apenas como especificação de comportamento, sem importação de código.
## Testes de governança do portfólio de IA

- provar que cada capacidade possui estado independente: ausente, experimental, promovida, bloqueada ou retirada;
- provar que somente capacidades promovidas entram no planner operacional;
- provar que retrieval não produz GCP, homografia ou veredito;
- provar que o runtime não contém treinamento, mutação de pesos ou aprendizado online;
- provar que a UI guiada explica seleção e omissão sem exigir conhecimento dos sete nomes;
- provar que resultados experimentais permanecem diagnósticos e não são publicados como aceitos.

## Governança do fluxo de engenharia

A SPRINT-001 deverá testar o próprio caminho de contribuição:

- Issue Form produz issue completa e validável;
- branch protection/ruleset impede integração sem checks;
- nomes de checks obrigatórios são únicos;
- PR template exige issue, ADRs, testes, riscos e rollback;
- mudança criada com apoio do Codex permanece identificada;
- tentativa de push direto, force push ou bypass não autorizado falha;
- evidência de CI é vinculada ao commit e à PR.

Esses testes validam controles; não substituem revisão científica ou humana.

## SPRINT-001, ambiente e corpora

- `test_sprint_zero_gate_is_evidence_driven`: passagem de tempo isolada não produz `PASS`;
- `test_sprint_zero_can_finish_across_variable_cadence`: snapshots de evidência permanecem válidos independentemente do intervalo entre sessões;
- `test_host_container_ci_contract_equivalence`: comandos suportados produzem schemas e resultados equivalentes;
- `test_no_implicit_large_downloads`: bootstrap e testes padrão falham se tentarem baixar modelos, tiles ou corpora grandes;
- `test_corpus_license_hash_split_integrity`: todo item possui origem/licença/hash e nenhum item proibido vaza entre splits;
- `test_foundation_gate_end_to_end_diagnostic_flow`: frontend/API/fila/worker/artefato, migrations, logs e redaction são exercitados antes da funcionalidade Geo.

## Contratos geoespaciais aceitos e testes obrigatórios

As suítes deverão incluir:

- round-trip entre pixel, origem, referência, CRS métrico de trabalho, alvo e descoberta;
- inversão de eixos, CRS sem EPSG e antimeridiano quando aplicável;
- tolerâncias com espaço e unidade declarados, sem arredondamento prematuro;
- distinção entre nodata, alpha, cobertura, máscara de validade, máscara analítica e margens preservadas;
- pontos sentinela para detectar latitude/longitude, easting/northing e datum incorretos;
- comparação de escala e distância entre EPSG:3857, CRS autoritativo, UTM e projeção local no AOI;
- falha fechada quando CRS, grids, operação ou área de uso não forem comprovados;
- prova de que derivado web EPSG:3857 não substitui silenciosamente o produto canônico técnico.

## Grade raster e mosaico relativo

- testar origem, snapping, pixel-is-area e ausência de half-pixel shift;
- testar resolução escolhida contra distribuição da escala local, limites de pixels e proibição de falsa super-resolução;
- testar kernels por banda/conteúdo e integridade de máscaras/alpha;
- validar COG, overviews, bounds, round-trip e leitura amostral;
- para as decisões consolidadas na ADR-049, preparar corpora com um componente, múltiplos componentes, imagens isoladas, pontes falsas, ciclos inconsistentes, pouca e alta sobreposição, fontes radiometricamente divergentes, `leave-one-out`, retomada e limites de RAM/disco;
- para as decisões consolidadas na ADR-049, testar ancoragem única versus distribuída, âncoras contraditórias, subcomponentes parcialmente ancorados e SGV independente;
- para as decisões consolidadas em ADR-049 e ADR-048, testar criação multivisão, vínculo ao pixel fonte, lacunas de cobertura, leverage, pesos de incerteza, quarentena de conflitos, versionamento de AnchorSets e reotimização limitada ao subgrafo afetado;
- para as decisões consolidadas na ADR-050, testar gates independentes e fail-closed, base de ciclos, drift p50/p95/máximo, bridges, articulation points, remoção de arestas críticas, divisão de componentes e lifecycle de promoção;
- para as decisões consolidadas na ADR-050, testar snapshots imutáveis, visão consolidada reconstruível, level-of-detail no frontend, exports por perfil, limites de bundle e provenance hierárquica versus densa sob demanda;
- para as decisões consolidadas em ADR-050, ADR-018 e ADR-039, testar preflight e budgets, classes de persistência, retomada, materialização tileada, quotas, eviction, dry-run e recomputação;
- para as decisões consolidadas na ADR-039, testar weighted fairness, aging, starvation, backpressure, limites de tasks, leases/heartbeats, oversubscription de VRAM, residência de modelos, fallback explícito, safe-boundary preemption, circuit breakers e prioridade efetiva auditável;
- para as decisões consolidadas em ADR-039 e ADR-054, testar cardinalidade, correlação e perda de eventos, progresso por unidades, incerteza/indisponibilidade de ETA, replanejamento, SLOs por classe, jobs stalled, leases presos, RBAC e auditoria dos controles;
- para as decisões consolidadas em ADR-054 e ADR-053, testar snapshots seletivos, replay offline, invariantes sob variação temporal, classificação de divergências, redaction, retenção, assinatura e limites de bundles;
- para as decisões consolidadas na ADR-053, testar derivação de seeds, ordenação estável, equivalência CPU/GPU, tolerâncias, probes de repetibilidade, consenso orçado, replay científico e matriz de ambientes;
- para as decisões consolidadas na ADR-053, testar baselines estratificados, seleção de tiers por impacto, regressões de cauda/subgrupo, conjunto cego, promotion gate, dual-run/canary, pinning e rollback;
- para as decisões consolidadas na ADR-026, testar matriz de readers/writers, migrations interrompidas e retomadas, backfills idempotentes, adapters de artifacts, rematerialização com lineage e downgrade blockers;
- para as decisões consolidadas na ADR-026, testar rollout por fases, exclusão mútua do controlador, perda de lease, cutover, canary, estado incerto, forward-fix e restore;
- para as decisões consolidadas em ADR-034 e ADR-054, testar instalação idempotente, bootstrap único, readiness por evidências, canary sintético, redaction e reparo em dry-run;
- para as regras consolidadas em ADR-034, ADR-047 e na política de citação, testar SPDX/REUSE, compatibilidade de dependências, DCO, policy de providers/assets e validação de metadados de citação;
- para as regras da governança e de AP-008, testar fechamento da fase fundacional, autorização exclusiva da SPRINT-001, cobertura decisória e supersession preservando histórico;
- para as regras do modelo operacional do GitHub, testar integridade do inventário, contagens por épico, issues órfãs e variação da previsão;
- para as regras do modelo operacional do GitHub, testar Issue Forms, campos, transições, readiness, done, dependências, prioridade, tamanho e automações guardadas;
- para as regras do modelo operacional do GitHub, testar horizontes/milestones, sequência por gates, cadeia de enablers, WIP, capacidade, carryover, ownership, checkpoints de integração e snapshots de reforecast;
- para as regras do modelo operacional do GitHub, testar domínio primário/afetados, épicos encerráveis, fatias verticais, catálogo versionado, IDs estáveis, sincronização idempotente, critérios derivados, trabalho transversal, spikes limitados e tombstones;
- para as regras do modelo operacional do GitHub, testar staging/canary, ondas limitadas, autoridade por campo, reconciliação de três vias, ChangeSets destrutivos, retries/checkpoints, evidence set, run record, recuperação e least privilege;
- para AP-008, testar seleção do conjunto SPRINT-001, ondas verticais, scaffold, contracts finos, job diagnóstico, CI progressivo, evidence set e cutover do Foundation Gate;
- provar que mosaicos leave-one-out não contêm pixels da própria imagem-alvo e que aceitação relativa não substitui o SGV.

## Evolução de schemas e artifacts — decisões consolidadas na ADR-026

- versões adjacentes devem ser testadas conforme a matriz declarada de compatibilidade;
- migrations precisam ser testadas em banco vazio e snapshot representativo, inclusive falha, retomada e concorrência;
- adapters e rematerializações devem preservar semântica, lineage, hashes do original e invariantes de leitura;
- rollback deve funcionar somente dentro da janela compatível; downgrade bloqueado deve produzir diagnóstico e caminho de restore.

## Upgrade coordenado — decisões consolidadas na ADR-026

- rolling upgrade só pode ocorrer quando readers/writers adjacentes forem compatíveis;
- apenas um controlador pode manter o lease e alterar o estado da migration;
- perda de lease, restart e pausa devem preservar checkpoints e impedir dupla execução;
- cutover deve falhar quando qualquer invariável, reader histórico, canary ou health gate falhar;
- estado incerto deve bloquear novos writers;
- rollback, forward-fix e restore devem ser escolhidos conforme fase e irreversibilidade.

## Instalação inicial e suporte — decisões consolidadas em ADR-034 e ADR-054

- repetir instalação após interrupção sem duplicar secrets, contas ou migrations;
- provar que nenhuma credencial padrão permite acesso antes do bootstrap;
- invalidar token de bootstrap após uso, expiração ou tentativa indevida;
- falhar readiness quando PostGIS, broker, filesystem, CRS sentinela, SSE/polling ou artifact sintético estiver inconsistente;
- operar em modo offline sem tornar providers externos gates obrigatórios;
- verificar por testes adversariais que bundles não contêm secrets, paths, nomes de arquivos ou bytes raster;
- executar reparos em dry-run, confirmar blockers e preservar audit trail.

## Licença, providers e citação — regras consolidadas em ADR-034, ADR-047 e na política de citação

- verificar expressão SPDX e copyright de todos os arquivos públicos;
- bloquear dependência, modelo ou asset sem licença compatível e notice exigido;
- validar sign-off ou instrumento de contribuição escolhido;
- testar expiração, ambiguidade e mudança de `ProviderPolicyManifest` em modo fail-closed;
- validar `CITATION.cff`, metadados de release e coerência entre versão, digest e DOI.

- para as regras consolidadas em AP-008, testar fechamento do conjunto SPRINT-001, percurso do grafo de gates, ondas verticais, fronteiras do skeleton, schemas/fixtures, runners do job diagnóstico, CI progressivo, integridade do evidence set, controle de escopo e cutover;
- para AP-009, testar par raster local, ingestão imutável, ProcessingPlan, correspondências clássicas, homografia/USAC_MAGSAC, SGV tri-state, COG/ArtifactSet, equivalência entre superfícies e corpus inicial estratificado.

- para as regras consolidadas em AP-009, testar fatia de uma imagem, roots autorizados, snapshot imutável, ProcessingPlan, classic-first com elegibilidade neural, homografia/USAC_MAGSAC, SGV, ArtifactSet/COG, equivalência entre superfícies e corpus estratificado;
- para AP-010, testar taxonomia de elegibilidade, triggers, recommender, budgets, compatibilidade de checkpoints, ausência de capability, SGV neural, pinning de ModelPacks, transparência da UX e rollout shadow/canary.

## Cobertura da escada neural — regras consolidadas em AP-010

Testes devem cobrir elegibilidade e inelegibilidade, seleção determinística do ModelPack, budgets `fast`/`balanced`/`extended_recovery`, poda, checkpoint reuse, ausência de GPU, SGV independente, provenance e rollback de promoção. A AP-011 define a escada de lote `1 → 10 → 40 → até 300`, com fault injection e invariantes de sucesso parcial.

## Auditoria de ADRs e overlap check

CI deve validar o relationship register, executar `tools/check_adr_overlap.py` e falhar quando uma ADR nova não estiver classificada. Similaridade é sinal para revisão humana, não decisão automática.

## Toolchain de testes — AP-001

- pytest para unit, contract, integration, smoke e acceptance;
- PostgreSQL/PostGIS e RabbitMQ reais nas suítes que dependem de sua semântica;
- TypeScript strict, Vitest, Testing Library e Playwright;
- Python 3.12 no gate obrigatório da baseline;
- Python 3.13 em lane futura não bloqueante após ativação do PythonRuntimeGate;
- Python 3.14 somente em lane experimental posterior à estabilização da lane 3.13;
- locks frozen e builds reproduzíveis;
- nenhuma substituição de PostGIS por SQLite nos gates relevantes.


## Testes do profile clássico — parâmetros consolidados em BP-001

- golden vectors para normalização RootSIFT float32;
- equivalência de coordenadas entre pirâmide, tile e source pixel;
- recall FLANN medido contra BF exato em estratos;
- property tests de unicidade, reciprocidade e determinismo;
- negativos para masks, priors e padrões repetitivos;
- benchmark multidimensional e canary do ClassicalMatchingProfile.

BP-002 define a matriz concreta de calibração e regressão do SGV.
