# Requisitos não funcionais

Metas iniciais devem ser medidas, não presumidas:

- instalação reproduzível em servidor único;
- p95 de endpoints leves e tempo de fila observados separadamente do processamento;
- limite de arquivo, pixels, bandas, páginas, descompressão e espaço temporário;
- limites por instância/usuário de jobs, storage, concorrência, CPU e GPU;
- proteção contra path traversal, symlink escape e leitura fora das raízes registradas;
- RPO/RTO definidos antes de uso com acervo real;
- retenção e exclusão verificáveis;
- nenhuma vulnerabilidade High/Critical explorável no caminho exposto;
- throughput, memória, disco e tempo por imagem medidos em corpus representativo de diferentes décadas e condições;
- planos de processamento serializáveis e reproduzíveis;
- fluxo principal compreensível sem conhecimento prévio dos algoritmos;
- nenhum caminho automatizado capaz de efetuar compra ou aceitar cobrança em provider.
- Strong Geometric Verifier fail-closed: métrica crítica ausente ou gate crítico reprovado impede aceite automático;
- nenhuma pontuação agregada pode compensar shear, reflexão, degeneração, foldover ou outra falha crítica;
- lotes usuais de 40, 100 e 300 imagens devem ser benchmarkados com perfis de consumo e limites documentados;
- o catálogo acumulado deve permanecer consultável por paginação e filtros server-side na ordem de centenas de milhares de registros;
- ingestão, processamento e exportação de lote não carregam todo o inventário em memória;
- exports incluem nome e caminho relativo sem expor caminho absoluto do host por padrão;
- taxonomia de falhas e schemas de relatório são versionados e retrocompatíveis dentro da política definida;
- não gerar obrigatoriamente um conjunto de arquivos pequenos por imagem;
- o Image Deformation Profile deve separar transformação cartográfica esperada de deformação problemática e registrar p50/p95/máximo das métricas aplicáveis;
- foldover, inversão e Jacobiano inválido são falhas críticas não compensáveis.

- descoberta de vizinhos deve possuir custo e quantidade de candidatos limitados, observáveis e configuráveis por policy;
- agrupamentos provisórios, candidatos, arestas verificadas e componentes confirmados devem possuir estados não ambíguos;
- sucesso parcial deve permanecer visível em UI, API, CLI, relatórios e exports;
- retry de componente não deve reprocessar sucessos imutáveis nem utilizar seed superseded sem revalidação.
- providers externos devem permanecer substituíveis e isolados atrás de contratos de capacidade;
- toda consulta e aquisição externa deve possuir limites de tempo, páginas, candidatos e bytes;
- o cache deve suportar deduplicação, verificação de integridade, garbage collection e preservação de lineage;
- falhas e mudanças de provider não podem corromper o estado interno nem converter indisponibilidade em aceitação.

- retries técnicos devem possuir orçamento, backoff, jitter e idempotência observáveis;
- checkpoints devem declarar compatibilidade por hashes, schemas, profiles e versões, nunca apenas por existência;
- cancelamento deve atingir estado terminal ou alerta operacional dentro de limite configurado;
- nenhum ArtifactSet parcial pode tornar-se vigente após cancelamento ou perda de worker;
- snapshots históricos e visão vigente devem permanecer reconciliáveis em API, CLI, UI e exports.

## Recuperação e ciclo de vida

- BackupSets devem detectar divergência entre banco e arquivos por manifesto e checksum;
- restore drills devem medir RPO/RTO e produzir evidência consultável;
- retenção e GC devem operar em catálogos grandes sem carregar todo o inventário em memória;
- o GC deve ser idempotente, retomável e resistente a corrida com criação de novas referências;
- nenhuma política padrão pode apagar arquivos de raízes externas;
- quarentena e período de graça devem permitir recuperação antes da purga final.
## Segurança de instalação e evolução

- nenhum serviço interno é publicado por padrão;
- startup com secret ausente, fraco ou permissões inseguras falha de forma explícita;
- rotação de secrets críticos possui procedimento testado e downtime documentado;
- releases publicáveis são verificáveis por checksum, assinatura, SBOM e provenance;
- atualização não inicia sem preflight e BackupSet compatível quando exigido;
- migrations não são executadas implicitamente por simples restart do serviço;
- health checks e smoke tests determinam promoção ou rollback;
- a versão instalada é identificável por semver, digest, commit e manifesto.
## Hardware e operação desconectada

- CPU-only é configuração suportada e testada em toda release;
- GPU reduz tempo quando disponível, mas não é requisito funcional;
- memória estimada e observada orientam admission control por dispositivo;
- runner, formato, dispositivo e precisão são identificáveis por tentativa;
- ModelPacks são verificáveis e não são baixados por efeito colateral;
- o modo offline não realiza DNS, HTTP, telemetria ou checagem de atualização externa;
- providers e mirrors desabilitados geram erro acionável, não fallback oculto.

## Reprodutibilidade da fundação

- duração da SPRINT-001 não é SLO nem critério de qualidade;
- o foundation gate é repetível e produz evidência vinculada a commit e ambiente;
- bootstrap limpo não depende de caches privados ou downloads implícitos;
- ambientes host/container/CI declaram versões efetivas e divergências;
- corpora externos e protegidos são resolvidos por versão e checksum, nunca por caminho informal.

## Integridade de coordenadas e raster

As decisões consolidadas na ADR-041 proíbem defaults implícitos de espaço, eixo, arredondamento, nodata, CRS, grade, resolução e reamostragem. O gate Geo exigirá seleção explicável do `WorkingMetricCRS`, validação fail-closed da referência, distinção entre produto técnico e derivado web, grade determinística, resolução orientada à informação nativa/Jacobiano, kernels explícitos e validação multidimensional do COG.

A capacidade aprovada nas decisões consolidadas na ADR-049 não poderá bloquear o lote normal nem exigir todas as imagens em memória. Estado, descritores, matches, pirâmides, tiles e checkpoints serão persistidos em disco; a RAM será cache limitado pelo Resource Governor. Quotas de pares, CPU/GPU, RAM, I/O, disco e materialização serão explícitas. Componentes disjuntos, drift, blending usado como evidência e referência circular deverão falhar de modo explícito.

## Ancoragem de componentes relativos

- o ajuste conjunto deve operar com checkpoints e consumo governado para componentes com alta sobreposição;
- nenhuma âncora individual pode receber peso ilimitado ou determinar sozinha o veredito do componente;
- conflitos de datum, CRS, coordenada ou observação devem falhar de modo fechado e permanecer auditáveis;
- o tempo e o escopo da reotimização após edição devem ser previstos antes da execução;
- previews de impacto não podem publicar ArtifactSets nem alterar tentativas anteriores.

## Verificação do mosaico relativo

- métricas do componente devem ser calculáveis out-of-core e respeitar budgets de pares, ciclos, RAM, I/O e tempo;
- hard gates relativos não podem ser compensados por score agregado ou aprovação visual;
- o relatório deve localizar as piores arestas, ciclos, regiões de drift e elementos de alta sensibilidade;
- remover uma bridge ou imagem crítica deve produzir análise de impacto determinística e auditável;
- promoção de componente não pode alterar ou transferir o veredito SGV das imagens.

## Relatórios e visualização do mosaico relativo

- snapshots de relatório são imutáveis e a visão vigente deve ser reconstruível;
- o frontend deve aplicar paginação, tiling, generalização e level-of-detail, sem carregar todos os matches ou tiles;
- exports devem declarar perfil, schema, classificação autoritativa/visual e limites aplicados;
- provenance por tile/região é baseline; mapas densos por pixel são opcionais e orçados;
- preview blended não pode ser promovido como evidência geométrica autoritativa;
- comparação de snapshots deve permanecer determinística e auditável.


## Concorrência e isolamento de recursos

- weighted fairness e aging devem impedir starvation sob carga sustentada;
- tarefas interativas devem manter reserva mínima sem monopolizar a instalação;
- fan-out e tasks pendentes devem respeitar backpressure de broker, banco, workers e filesystem;
- leases e heartbeats devem reconciliar perda de worker sem duplicar publicação;
- VRAM e residência de modelos devem respeitar budgets por dispositivo;
- fallback de runner ou dispositivo nunca ocorre sem autorização e registro;
- circuit breakers reduzem admissão e fan-out antes de falha sistêmica;
- prioridade efetiva, policy e motivo permanecem explicáveis e auditáveis.

## Observabilidade do scheduler — decisões consolidadas em ADR-039 e ADR-054

- métricas não podem usar job, imagem, path ou task como labels ilimitados;
- progresso não pode prometer percentual ou tempo sem unidades e evidência compatíveis;
- SLOs operacionais não podem relaxar gates científicos;
- ações administrativas devem respeitar RBAC, safe boundaries e audit trail;
- event ledger e timelines devem manter correlação verificável sem labels ilimitados;
- estimativas devem informar faixa, confiança, replanejamento e estado indisponível;
- alertas devem agregar sintomas e permitir drill-down sem tempestade por item.

## Reprodutibilidade operacional — decisões consolidadas em ADR-054 e ADR-053

- snapshots não podem conter secrets, bytes raster ou paths absolutos;
- replay do scheduler deve ser separado de reexecução científica;
- equivalência não deve exigir ordem temporal total idêntica em execução concorrente;
- bundles devem respeitar acesso, redaction, retenção, assinatura e limites de tamanho.

## Determinismo científico — decisões consolidadas na ADR-053

- seeds e fontes de aleatoriedade devem ser registradas por attempt e estágio;
- diferenças entre CPU/GPU devem obedecer níveis e tolerâncias calibradas, não igualdade presumida;
- não determinismo capaz de alterar hard gate deve reprovar a combinação runner/dispositivo/profile;
- replay e promoção devem distinguir identidade bitwise, equivalência numérica, decisão equivalente e estabilidade estatística.


## Regressão, promoção e rollback científico — decisões consolidadas na ADR-053

- médias globais não podem ocultar regressões em estratos ou hard gates;
- seleção incremental de testes deve manter sentinelas obrigatórias e rastreabilidade de impacto;
- promotion candidates devem executar matriz completa e conjunto cego aplicável;
- promoção exige evidence bundle e budgets por estrato sem compensação crítica;
- rollback científico não pode modificar attempts ou ArtifactSets históricos.

## Compatibilidade evolutiva — decisões consolidadas na ADR-026

- schemas devem ser identificáveis e rejeitar versões incompatíveis de forma explícita;
- migrations interrompidas precisam ser retomáveis e não podem publicar estado parcialmente migrado como saudável;
- artifacts históricos não podem ser reescritos no lugar;
- downgrade incompatível deve ser bloqueado e direcionado para forward-fix ou restore validado.

## Upgrade coordenado — decisões consolidadas na ADR-026

- a instalação não pode executar duas migrations concorrentes sobre o mesmo estado;
- convivência entre versões precisa ser limitada, observável e compatível pela matriz declarada;
- cutover não pode depender apenas de exit code;
- falha pós-irreversibilidade deve bloquear downgrade e preservar caminho de forward-fix ou restore;
- maintenance mode deve impedir writes enquanto a consistência não estiver comprovada.

## Instalação e suporte — decisões consolidadas em ADR-034 e ADR-054

- instalação não pode depender de credenciais padrão ou alteração destrutiva implícita do host;
- readiness deve provar o fluxo mínimo, não somente processos ativos;
- bundles de suporte não podem conter secrets, paths absolutos ou bytes de projetos por padrão;
- nenhuma telemetria ou bundle será enviado externamente sem ação explícita;
- reparos destrutivos devem exigir dry-run, confirmação, backup quando aplicável e audit trail.

## Publicação e direitos — regras consolidadas em ADR-034, ADR-047 e na política de citação

- nenhum arquivo público pode depender de licença inferida ou ausente;
- contribuições externas devem ter origem certificada e verificável;
- gratuidade de acesso não pode ser confundida com direito de cache, transformação ou redistribuição;
- citação recomendada deve permanecer distinta de obrigação jurídica da licença;
- DOI e metadados públicos não podem apresentar a fundação documental como software funcional.

## Fechamento da fase fundacional e planejamento do portfólio — regras da governança e de AP-008

- a contagem de ADRs não substitui evidence set de fechamento;
- o fechamento da fase fundacional não encerra o programa de decisões do portfólio;
- previsão de issues deve declarar faixa, confiança e data de revisão;
- implementação não pode contradizer ADR aceita sem supersession explícita;
- decisões locais devem permanecer reversíveis e dentro dos guardrails;
- SPRINT-001 pode começar apenas após autorização formal, e funcionalidades somente após o Foundation Gate;
- reabertura do baseline exige blocker ou evidência material, não preferência.

## Integridade da materialização do portfólio

- a criação e reconciliação de issues deve ser idempotente e retomável;
- conteúdo humano não gerenciado não pode ser sobrescrito silenciosamente;
- operações destrutivas devem possuir blast radius limitado, snapshot e aprovação;
- logs e records de sincronização não podem conter tokens ou secrets;
- o Project somente será considerado convergente após evidence set verificável.

## SPRINT-001 e primeira fatia funcional

- o `SprintEvidenceSet` deve ser imutável, machine-readable e vinculado ao commit e ambiente;
- a seleção da SPRINT-001 deve ser reproduzível pelo grafo de gates;
- nenhuma transformação geoespacial funcional pode integrar a SPRINT-001;
- a primeira fatia futura deve preservar originals, falhar fechada e produzir artifacts verificáveis.

## Classic-first e recuperação neural

- o caminho clássico deve funcionar sem GPU e sem ModelPack;
- escalonamento neural deve possuir budget, provenance e causa de elegibilidade;
- indisponibilidade de capability deve ser explícita e não causar fallback silencioso;
- toda tentativa neural deve ser reprodutível conforme seu tier e verificada pelo SGV independente.

## Escalonamento neural governado

A recuperação neural não pode tornar GPU obrigatória, ocultar indisponibilidade, monopolizar recursos ou reduzir critérios do SGV. O modo `extended_recovery` deverá usar prioridade e budgets separados do caminho normal.


## Matching clássico concreto

- a preparação, tiling, quotas e filtros devem ser determinísticos dentro do profile;
- o recall ANN deve possuir piso comprovado contra oracle exato;
- profiles não podem mudar em attempts existentes;
- ganho de throughput não compensa regressão crítica de falso aceite ou coverage;
- artifacts intermediários reutilizados devem possuir schema e digest compatíveis.
## SLOs, RPO e RTO iniciais — Fase G

| SLI | Objetivo inicial | Gate |
|---|---:|---|
| disponibilidade mensal | 99,0%, excluindo manutenção planejada | produção |
| readiness/health p95 | 250 ms | SPRINT-001 |
| consulta leve p95 / p99 | 500 ms / 1.500 ms | benchmark API |
| aceite de comando p95 | 1.000 ms | benchmark API |
| propagação SSE p95 | 2.000 ms | integração |
| espera interativa em fila p95 | 10.000 ms | BP-004 |
| starvation máximo após admissão | 300 s | BP-004 |
| terminal de cancelamento em safe point | 120 s | resiliência |
| RPO metadata autoritativa | 15 min | restore drill |
| RTO metadata autoritativa | 4 h | restore drill |
| RPO binaries irrecuperáveis | 24 h | backup gate |
| RTO binaries irrecuperáveis | 12 h | restore drill |

Tempos científicos de matching, SGV, IA e mosaico não recebem número inventado. São publicados por corpus, classe de deployment e Benchmark Profile. A aplicação não pode converter esses objetivos em claim antes de evidência.
