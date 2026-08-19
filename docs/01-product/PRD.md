# Product Requirements Document — DSGeorref

- **Owner do documento:** Product Owner
- **Aprovador de arquitetura:** Arquiteto
- **Owner de engenharia:** Tech Lead
- **Estado:** `Aprovado para planejamento de implementação`
- **Versão:** `2.6.0`
- **Última atualização:** 2026-07-27

## 1. Resumo executivo

O DSGeorref é uma aplicação greenfield, single-instance e unificada para georreferenciamento controlado de imagens raster. O produto oferece um núcleo de domínio compartilhado, acessível por CLI, API REST, frontend React/OpenLayers e workers duráveis. A prioridade é produzir resultados geometricamente válidos, reproduzíveis, auditáveis e explicáveis, com sucesso parcial explícito, em vez de automação opaca.

O fluxo canônico seleciona entradas em roots autorizados, persiste um `ProcessingPlan` versionado, descobre ou adquire referências permitidas, executa matching classic-first e estimação de homografia projetiva, submete candidatos ao Strong Geometric Verifier (SGV) fail-closed e publica bundles `ArtifactSet` imutáveis somente após aceitação. Capacidades de IA podem ampliar a recuperação, mas jamais contornam o SGV, iniciam downloads implícitos ou reutilizam dados operacionais sem governança.

## 2. Problema

Acervos raster históricos, heterogêneos e incompletos são difíceis de georreferenciar com consistência e escala. Processos manuais são lentos, pouco reproduzíveis e frágeis em auditoria. Pipelines totalmente automáticos podem gerar resultados visualmente plausíveis, porém geometricamente incorretos; também podem esconder incerteza, perder metadados marginais, sobrescrever histórico ou invalidar um lote inteiro por causa de um subconjunto não resolvido.

O DSGeorref deve oferecer um processo que seja:

- conservador o suficiente para falhar fechado quando a evidência geométrica for insuficiente;
- escalável para lotes usuais de 40–300 imagens, sem tornar o broker fonte de verdade;
- explicável para operadores, revisores e administradores;
- reproduzível entre runners e ambientes suportados;
- seguro em instalações locais ou expostas em rede;
- extensível para IA opcional e recuperação por mosaico relativo sem enfraquecer a baseline clássica.

## 3. Usuários e trabalhos principais

### Personas de produto

- **Operador geoespacial:** configura projetos, seleciona imagens, executa processamento, interpreta qualidade e exporta resultados.
- **Revisor:** prioriza casos ambíguos, compara tentativas, cria correções e trata resultados revisáveis sem anular hard gates.
- **Administrador da instância:** configura roots, identidade, providers, recursos, backup, atualização e controles de segurança.
- **Mantenedor científico/engenharia:** calibra profiles, avalia equivalência, promove ModelPacks e preserva evidência científica.

### Jobs to be done

1. Criar projeto e selecionar assets locais sem expor paths arbitrários do host.
2. Construir um plano de processamento explicável e compreender custo, capacidades e limitações.
3. Processar uma imagem ou lote preservando estado e resultado individual por imagem.
4. Inspecionar evidência do SGV, deformação, provenance, lineage e diagnóstico de falha.
5. Revisar casos não resolvidos e criar `CorrectionSet` imutável que origine uma nova tentativa validada.
6. Exportar COGs canônicos, manifestos, geometrias, relatórios e bundles de reprodução.
7. Restaurar, atualizar e diagnosticar a instância sem corromper estado ou perder auditabilidade.

## 4. Objetivos

- Entregar um único produto coerente entre CLI, API, Web e workers sobre os mesmos application services.
- Manter PostgreSQL/PostGIS como estado autoritativo e filesystem gerenciado como armazenamento autoritativo de binários.
- Garantir imutabilidade de originais, attempts, correction sets, snapshots de resultado e publicações de artifacts.
- Tornar explícitos CRS, datum, ordem de eixos, nodata, pixel semantics, transforms, hashes e lineage.
- Adotar homografia projetiva como modelo geométrico final canônico e SGV como autoridade independente de aceitação.
- Suportar retry técnico classificado, checkpoints compatíveis, cancelamento cooperativo, quarantine, fairness e isolamento de recursos.
- Suportar aquisição externa guiada, limitada, gratuita e governada por licença, inclusive em operação offline/restricted.
- Permitir escalonamento de IA apenas após elegibilidade determinística e checkpoint classic-first.
- Operar um sistema de engenharia orientado por IA que permita trabalho especializado em paralelo sem conflito de arquivos nem bypass de revisão.

## 5. Não objetivos

- Multitenancy, billing, assinaturas ou planos comerciais.
- Microservices como topologia padrão.
- Treinamento automático com dados operacionais.
- Download silencioso de modelos ou dependência obrigatória de GPU.
- Aceitação baseada apenas em plausibilidade visual ou confiança de modelo.
- Acesso direto do navegador a PostgreSQL, RabbitMQ, paths do host ou roots internos.
- Mutação de resultados históricos ou override manual de hard gates do SGV.
- Compra de imagens ou uso de providers com direitos ambíguos.

## 6. Princípios do produto

1. **Evidência antes da aceitação.** Um resultado só é aceito por gates geométricos e científicos explícitos.
2. **Um núcleo semântico.** Interfaces adaptam contratos; não duplicam regra de negócio.
3. **Histórico imutável, visão corrente derivada.** Novos attempts e snapshots alteram ponteiros vigentes, não registros anteriores.
4. **Classic-first, IA governada.** IA pode recuperar candidatos, mas permanece substituível, auditável e subordinada ao SGV.
5. **Sucesso parcial explícito.** Um lote pode concluir com imagens aceitas, revisáveis e falhas sem ocultar componentes não resolvidos.
6. **Offline-capable por design.** Egress, providers e ModelPacks são capacidades explícitas.
7. **Contract-first.** API, eventos, schemas e manifestos mudam antes das implementações e exigem revisão de compatibilidade.

## 7. Requisitos funcionais

### Projeto, workspace e ingestão

- Gerenciar projetos, roots autorizados, assets, coleções de referência e permissões por projeto.
- Navegar diretórios por identificadores opacos, com proteção contra traversal, symlink escape e TOCTOU.
- Persistir identidade da fonte, hashes, metadados e lineage antes do processamento.
- Ingerir raster em modo fail-closed, preservando validade, nodata, alpha, bandas, resolução e metadados relevantes.

### Planejamento, processamento e qualidade

- Criar `ProcessingPlan` imutável com estratégias, budgets, profiles e capabilities selecionados.
- Executar preparação fotométrica, matching coarse-to-fine, filtragem robusta e estimação de homografia projetiva.
- Avaliar candidatos com invariantes rígidos e profiles estratificados do SGV.
- Preservar máscara de análise separada da extensão de saída e manter metadados marginais.
- Gerar grade determinística e COG canônico com validação independente.
- Produzir diagnóstico por imagem, QualityReport e Image Deformation Profile.

### Lotes e execução durável

- Modelar jobs, attempts e work units no PostgreSQL.
- Usar RabbitMQ apenas como transporte, com ack após transação autoritativa.
- Suportar redelivery, idempotência, retry técnico classificado, checkpoint compatível, cancelamento cooperativo e reconciliação.
- Aplicar fairness por classe, leases com fencing, backpressure e budgets de CPU, RAM, GPU e disco.
- Persistir progresso monotônico e representar ETA como estimativa incerta, nunca como fato.

### Revisão e resultados

- Exibir veredito por imagem, métricas, evidências, lineage, deformação e remediação segura.
- Manter fila de revisão explicável e workflow pós-lote não bloqueante.
- Persistir correções em `CorrectionSet` tipado, versionado e imutável.
- Publicar `ArtifactSet` de forma atômica somente após validação.
- Exportar resultados de imagem/lote, geometrias, manifestos, checksums e bundles de reprodução.

### Identidade, segurança e operação

- Disponibilizar contas locais, bootstrap administrativo one-time, sessões server-side, PATs escopados e OIDC opcional.
- Centralizar autorização e aplicar same-origin, CSRF, throttling, TLS, secrets e redaction.
- Suportar BackupSet coordenado, restore drill isolado, retenção por classe, GC reference-aware, upgrade controlado e rollback.
- Emitir sinais OpenTelemetry de cardinalidade limitada e canal de auditoria append-only protegido.

## 8. Requisitos não funcionais críticos

- **Integridade:** nenhum artifact parcial pode tornar-se vigente.
- **Reprodutibilidade:** cada resultado deve vincular inputs, versions, profiles, parameters, ambiente e digest.
- **Segurança:** paths, secrets, tokens, providers e egress devem falhar fechados.
- **Compatibilidade:** mudanças públicas exigem schema versionado, janela de compatibilidade e migration/rollback.
- **Observabilidade:** falhas, retries, filas, leases, recursos e publicação devem ser diagnosticáveis sem cardinalidade explosiva.
- **Acessibilidade:** os fluxos Web críticos devem ser navegáveis, legíveis e testados conforme a estratégia de qualidade.
- **Operabilidade:** instalação limpa, backup, restore, upgrade e rollback devem ter evidência executável.

## 9. Sistema de engenharia orientado por IA

Toda mudança percorre a cadeia:

1. **Product Owner:** cria ou aprova história, prioridade e critérios de aceitação de produto.
2. **Arquiteto:** aprova boundaries, contratos e escolhas técnicas materiais.
3. **Tech Lead:** decompõe a história em tarefas não sobrepostas e atribui escopo de arquivos.
4. **Implementadores especializados:** Backend, Frontend, IA, Geoprocessamento, DevOps ou Security executam dentro do escopo declarado.
5. **QA:** valida de forma independente requisitos funcionais, contratos, regressões, segurança e evidência científica.
6. **Reviewer:** audita integralmente a mudança e recomenda merge ou rejeição.
7. **Autoridade humana de merge:** realiza o merge final depois de todos os gates.

Nenhum agente aprova o próprio trabalho. Contratos compartilhados são aprovados e integrados antes de abrir lanes paralelas. Escopos de escrita e TaskEnvelopes são machine-readable em `.codex/`.

## 10. Métricas de sucesso

Os thresholds são promovidos por Benchmark Profiles, não por preferência abstrata. A baseline funcional terá sucesso quando:

- a primeira fatia processar uma imagem controlada ponta a ponta e publicar COG válido somente após aceitação do SGV;
- CLI, API e worker preservarem resultado de domínio equivalente conforme o DeterminismProfile;
- lotes preservarem resultados individuais, retomarem checkpoints compatíveis e contiverem cancelamento corretamente;
- budgets de falso aceite, qualidade, runtime e segurança passarem nos corpora promovidos;
- instalação, backup, restore, upgrade e rollback passarem nos gates aplicáveis;
- toda issue concluída estiver ligada a épico, sprint, ADR/profile/contrato, testes, QA e final review.

## 11. Estratégia de entrega

A execução está organizada de `SPRINT-001` a `SPRINT-012`. Sprint é um incremento limitado por evidência, dependências e WIP; não é autorização para ignorar gates. A abertura pública permanece bloqueada até aprovação de licença, segurança, reprodutibilidade, instalação, restore e rollback. Production readiness é uma claim separada e exige evidência operacional.

## 12. Estado das decisões

Não há decisão tecnológica pendente para iniciar a implementação. A baseline normativa está em `docs/03-engineering/TECHNOLOGY_BASELINE.md`. Thresholds e tuning não são suposições nem decisões abertas: são valores evidence-bound promovidos pelos Benchmark Profiles. O Product Owner só é acionado para mudança material de boundary, trust model, semântica científica ou custo de reversão.


## 13. Cobertura executável

Esta baseline materializa integralmente o roadmap em contexto mínimo por agente:

- **18 módulos arquiteturais** com boundaries, owners e escopo de código;
- **376 requisitos ativos** com classificação, prioridade, owner, evidência, épicos e histórias;
- **110 épicos** e **760 histórias implementáveis**;
- **870 issues** no total, incluindo envelopes pais e histórias filhas;
- **760 TaskEnvelopes Codex** com referências, paths, testes, evidências e condições de parada;
- **12 sprints** com backlog detalhado e árvore de dependências;
- **12 contratos HTTP por domínio**, OpenAPI raiz e schemas de domínio/eventos/artifacts.

## 14. Índices de navegação

- Módulos: `docs/02-architecture/MODULE_CATALOG.md`
- Requisitos: `docs/01-product/REQUIREMENT_INDEX.csv`
- Épicos: `docs/06-delivery/EPIC_INDEX.csv`
- Histórias: `docs/06-delivery/STORY_INDEX.csv`
- Issues: `docs/06-delivery/ISSUE_INDEX.csv`
- Sprints: `docs/06-delivery/SPRINT_INDEX.csv`
- Contratos: `contracts/http/API_CONTRACT_INDEX.csv`
- Dependências: `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`
