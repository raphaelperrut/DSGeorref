# Strong Geometric Verifier, resultados por imagem e relatórios de lotes

## Princípio de segurança científica

O DSGeorref considera mais seguro rejeitar uma solução do que produzir um raster aparentemente georreferenciado com deformação implausível. O **Strong Geometric Verifier (SGV)** é um gate independente e obrigatório entre a geração de uma transformação candidata e a publicação de artefatos definitivos.

O modelo final canônico é a **homografia projetiva** (ADR-044). Fits de similaridade ou afins podem existir como diagnósticos, mas não substituem o contrato final nem autorizam fallback para modelos polinomiais/TPS. A homografia deve passar todos os gates aplicáveis.

```text
candidatos/matches
        ↓
estimativa de modelos
        ↓
Strong Geometric Verifier
  ├─ accepted ───────► artefatos definitivos
  ├─ needs_review ───► inspeção humana; sem sucesso automático
  └─ rejected ───────► diagnóstico; sem raster operacional
```

Erros de infraestrutura ou execução são registrados separadamente de rejeições geométricas. Uma imagem pode ter sido processada corretamente e ainda assim ser rejeitada pelo gate de qualidade.

## Famílias de métricas esperadas

### Evidência de correspondência

- quantidade de matches brutos;
- quantidade e razão de inliers;
- método robusto e parâmetros utilizados;
- estabilidade entre tentativas, seeds ou subconjuntos quando aplicável.

### Erro de reprojeção

- RMSE;
- mediana;
- p95;
- erro máximo;
- leave-one-out, cross-validation espacial ou medida equivalente de estabilidade.

### Distribuição espacial dos GCPs

- quadrantes cobertos;
- convex hull em relação à imagem;
- concentração em bordas;
- clusters, lacunas e distância entre pontos;
- cobertura em relação à área útil da imagem.

### Plausibilidade da transformação

- modelo selecionado e modelos concorrentes;
- graus de liberdade;
- condition number e determinante;
- reflexão, inversão de eixos ou degeneração;
- área projetada;
- escala mínima, máxima e anisotropia;
- shear;
- rotação e orientação quando relevantes;
- Jacobiano local, continuidade, foldover e distorção espacial para modelos não lineares.

### Image Deformation Profile — entrada não georreferenciada → saída georreferenciada

O SGV calculará um perfil específico da deformação introduzida pelo warp. A análise deverá distinguir componentes esperados — como escala, rotação e mudança de projeção — de deformação excessiva ou espacialmente instável.

Métricas candidatas obrigatórias por modelo/perfil:

- determinante e sinal do Jacobiano em grade regular;
- fator local de expansão ou compressão de área;
- alongamentos principais obtidos pelos valores singulares do Jacobiano;
- razão de anisotropia;
- shear e rotação local;
- p50, p95, máximo e variabilidade espacial das métricas;
- deformação não afim residual em relação a uma transformação global de referência;
- foldover, inversões e descontinuidades;
- proporção de pixels sem origem válida, nodata introduzido e área efetivamente aproveitada;
- resolução de entrada/saída e método de reamostragem.

Relatórios poderão incluir uma miniatura ou heatmap amostrado da deformação. O raster denso de diagnóstico será gerado sob demanda, evitando artefatos pesados para todas as imagens.

### Consistência contextual

- score visual pós-warp, quando metodologicamente válido;
- consistência com imagens vizinhas do lote;
- sobreposição e distância de footprints;
- plausibilidade de GSD, CRS e extensão;
- concordância com referências independentes, quando disponíveis.

Nenhuma métrica única substitui o conjunto de gates. Métricas não aplicáveis devem ser declaradas como tal; métricas obrigatórias ausentes bloqueiam aceite automático.

## QualityProfile

Cada execução referencia um profile imutável contendo:

- identificador e versão;
- classe de entrada e modelos permitidos;
- thresholds e severidades;
- métricas obrigatórias/opcionais;
- política de `accepted`, `needs_review` e `rejected`;
- corpus e versão usados na calibração;
- justificativa da mudança em relação à versão anterior.

Profiles oficiais serão versionados e calibrados por corpus, classe de entrada e família de transformação, conforme ADR-046. O fluxo guiado selecionará um profile seguro; customizações só poderão ocorrer por clone auditado. O modo exploratório não poderá publicar artefato como sucesso sem passar por um profile de aceitação.

## Política de revisão

Conforme ADR-048, somente gates classificados como revisáveis podem receber aprovação humana. Foldover, inversão indevida, transformação degenerada e métricas críticas ausentes permanecem hard gates não anuláveis. O veredito automático é imutável e a decisão humana é registrada separadamente.

## Resource Governor

Conforme ADR-039, a concorrência será controlada por orçamento adaptativo de RAM, CPU, GPU e disco temporário. A decisão de admissão e os ajustes de concorrência serão registrados por job.

## Apresentação da deformação

Conforme ADR-046, todas as imagens recebem métricas resumidas; o frontend exibe heatmap amostrado; diagnósticos densos são gerados sob demanda ou para casos não aceitos. Score agregado serve apenas para ordenação.


## Correspondências, estimador e grafo de referências

Conforme decisões consolidadas em ADR-044, ADR-046 e ADR-049:

- matchers clássicos e opcionais de IA produzem candidatos com proveniência individual;
- `USAC_MAGSAC` é o estimador padrão e RANSAC só pode ser escolhido antecipadamente;
- o conjunto final de GCPs precisa equilibrar qualidade e evidência espacial;
- uma imagem `accepted` não é automaticamente referência para o lote;
- cada aresta intralote exige evidência direta, e cada imagem dependente produz sua própria homografia e passa novamente pelo SGV;
- componentes espaciais desconectados são permitidos e tratados de forma independente;
- ausência de seed ou overlap seguro gera diagnóstico, não relaxamento de gate.

A qualidade do seed é condição necessária, mas não suficiente. O SGV da imagem dependente é sempre autoritativo para seu próprio resultado.

## Resultado lógico por imagem

Todo item de lote terá um registro de resultado, inclusive se não alcançar a etapa geométrica. Campos mínimos:

```text
image_id
workspace_root_label
relative_directory
file_name
relative_path
sha256
batch_id / project_id / job_id / attempt_id
processing_plan_id + version
quality_profile_id + version
status geral
processing_stage alcançado
strong_geometric_verifier_verdict
quality gates e métricas
image_deformation_profile
failure_code / failure_stage
evidências, causas prováveis e ações recomendadas
retryable / review_required
artefatos e lineage
timestamps, duração e consumo de recursos
```

Caminhos exportados serão relativos a uma raiz nomeada, evitando expor caminhos absolutos do host por padrão.

## Diagnóstico de falha

Uma falha não será apenas uma mensagem. O contrato separará:

- `failure_domain`: input, catalog, reference, search, matching, model, strong_geometric_verifier, export, resource ou infrastructure;
- `failure_stage`;
- `failure_code` estável e versionado;
- resumo legível;
- detalhes técnicos;
- evidências e métricas;
- causas prováveis ordenadas;
- ações recomendadas e seus riscos;
- possibilidade de retry automático, retry com plano alterado ou revisão manual;
- referência à documentação contextual.

Sugestões de contorno não poderão prometer sucesso. Alterações perigosas, como relaxar shear ou aceitar reflexão, não serão apresentadas como solução automática.

## Lotes usuais e dimensão total do acervo

O fluxo esperado trabalha normalmente com lotes de **40 a 300 imagens**. Esse intervalo é uma referência operacional, não uma garantia universal: consumo depende das dimensões, bandas, compressão, modelos, uso de IA, resolução de saída e hardware.

O acervo acumulado pode alcançar aproximadamente **190.000 imagens**, portanto catálogo, pesquisa e relatórios devem continuar eficientes nessa ordem de grandeza. Isso não significa processar todas simultaneamente.

O desenho esperado inclui:

- inventário por streaming/chunks;
- batch pai com unidades de trabalho e concorrência limitada;
- estimação e medição de memória por etapa/imagem;
- admission control, backpressure, checkpoints e retomada;
- índices por status, diretório, nome, código de falha, profile e etapa;
- tabela virtualizada com paginação e filtros server-side;
- contagens agregadas e facetas calculadas no backend;
- seleção de subconjuntos para retry ou revisão;
- exportação streaming de sucessos, falhas ou filtros salvos;
- geração sob demanda do relatório humano detalhado de uma imagem;
- nenhum requisito de criar milhares de arquivos pequenos por padrão.

## Artefatos aceitos

- PostgreSQL como estado operacional e índice;
- dataset tabular particionado e versionado, preferencialmente Parquet e/ou JSONL comprimido;
- CSV streaming para interoperabilidade;
- GeoPackage para GCPs, footprints e geometrias do subconjunto solicitado;
- GeoJSON para interoperabilidade leve e inspeção;
- bundle por imagem gerado sob demanda com JSON técnico, GCPs, previews, perfil de deformação e relatório HTML acessível;
- `batch_manifest.json` e checksums para integridade e proveniência.

## Máscara analítica e preservação das margens

A área usada para matching e validação territorial é distinta da extensão do raster. Bordas homogêneas ou sem terreno serão mascaradas durante análise mesmo quando seus valores forem apenas próximos de preto ou branco. A detecção deve ser tolerante a variações de digitalização e deve registrar confiança e área excluída.

A máscara **não recorta a imagem de saída**. Margens podem conter faixas de voo, marcas fiduciais, datas, identificadores, legendas e outras evidências primárias. Esses pixels permanecem no COG por padrão e são transformados junto com o raster. O relatório distingue:

- área total da entrada;
- área útil para matching;
- fundo marginal provável;
- metadado marginal provável;
- regiões incertas;
- área preservada na saída.

O SGV calcula distribuição de GCPs e cobertura em relação à área útil analítica, sem premiar ou penalizar margens sem terreno. Recorte ou nodata de margens exige OutputProfile explícito e não será o comportamento padrão.

## Mosaico relativo de recuperação

As decisões consolidadas na ADR-049 definem um verificador geométrico relativo separado do SGV. Ele qualifica a consistência intracomponente, mas não atribui CRS e não produz aceitação geográfica. Mesmo depois de um componente ser ancorado, cada imagem deverá reestimar sua solução e executar o SGV integralmente. A referência usada no rematching deverá excluir todos os pixels da imagem-alvo e o blending visual não poderá servir como única evidência geométrica.

## Separação entre verificação relativa e SGV

As decisões consolidadas em ADR-049 e ADR-050 criam um fluxo de mosaico relativo, ancoragem e verificação, mas não alteram a autoridade do SGV por imagem. O `RelativeMosaicVerifier` usa gates independentes, ciclos/drift orçados, sensibilidade de bridges/articulações e lifecycle explícito para avaliar somente a consistência interna do componente.

Um veredito `relative_verified` ou `anchorable`:

- não significa que o componente possui CRS;
- não valida a acurácia absoluta;
- não aprova nenhuma imagem;
- não substitui `leave-one-out`, nova homografia, Image Deformation Profile e SGV individual.

## Relatórios e provenance do mosaico relativo — decisões consolidadas na ADR-050

Cada tentativa preserva snapshot imutável e a visão vigente é derivada. A visualização usa level-of-detail e carregamento incremental; exports são separados em perfis; previews visuais permanecem não autoritativos. Provenance de fontes e seamlines é hierárquica e mapas densos são gerados apenas sob demanda. Essas decisões não modificam os gates do verifier relativo nem do SGV individual.

## Recursos e materialização do mosaico relativo — decisões consolidadas em ADR-050, ADR-018 e ADR-039

Preflight, budgets e classes de persistência governam a operação sem alterar gates geométricos. O mosaico virtual é autoritativo; rasters materializados são derivados. Eviction nunca trata artifacts autoritativos como cache e sempre preserva lineage e plano de recomputação.

As decisões consolidadas na ADR-039 definem concorrência, escalonamento e isolamento; as decisões consolidadas em ADR-039 e ADR-054 definem observabilidade, estimativas, SLOs e diagnóstico. Nenhuma prioridade, pressão de fila, disponibilidade de GPU, preempção, breaker ou ação administrativa pode relaxar critérios geométricos. As decisões consolidadas em ADR-054 e ADR-053 tratam da reprodução das decisões operacionais. As decisões consolidadas na ADR-053 governam seeds, equivalência numérica, não determinismo e replay científico; as decisões consolidadas na ADR-053 governam baselines, seleção de testes, promoção e rollback científico. Qualquer variação capaz de alterar hard gate bloqueia a combinação ou a promoção.

## Aplicação ao classic-first e IA — regras consolidadas em AP-009 e AP-010

Tentativas clássicas e neurais produzem registros separados e passam pelo mesmo perfil SGV independente. Score/confiança do matcher não substitui gates geométricos. Falha técnica, inelegibilidade neural e verdict geométrico permanecem dimensões distintas.


## Calibração vigente — BP-002

O verificador permanece fail-closed e independente do matcher. BP-002 fixa `SGVProfile`, espaços/unidades, resíduos robustos, coverage, condicionamento, Jacobiano, footprint/topologia, calibração, zona cinzenta e evidence/promotion. Nenhum parâmetro permite override de hard gate.
