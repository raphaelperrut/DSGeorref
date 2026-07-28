# Fase C — Domain-Driven Design Review

- **Baseline:** `2.6.0`
- **Gerado em:** `2026-07-27T17:29:09+00:00`
- **Resultado:** `APROVADO`
- **Pendências bloqueantes:** `0`
- **Implementação autorizada:** `NÃO — BLOCKED_EXTERNAL`

## Parecer

A arquitetura foi reorganizada em bounded contexts sem alterar os requisitos nem distribuir prematuramente o monólito. O modelo pode avançar para a próxima fase quando o Product Owner fornecer o respectivo charter.

## Cobertura

- Bounded contexts: 16;
- Core contexts: 3;
- Relações no context map: 70;
- Dependências diretas entre implementações de contexts: 0;
- Ciclos diretos de import/modelo: 0;
- Épicos classificados: 110;
- Histórias/TaskEnvelopes classificados: 758;
- Requisitos classificados: 376;
- ADRs após a Fase C: 25;

## Contextos

| ID | Contexto | Tipo | Épicos | Histórias | Requisitos relacionados |
|---|---|---|---:|---:|---:|
| `BC-001` | Governança de Engenharia e Entrega | Enabling | 12 | 91 | 195 |
| `BC-002` | Identidade e Controle de Acesso | Generic | 4 | 26 | 21 |
| `BC-003` | Projetos, Workspace e Assets | Supporting | 1 | 9 | 30 |
| `BC-004` | Plano de Processamento e Workflow | Supporting | 1 | 7 | 6 |
| `BC-005` | Descoberta e Aquisição de Referências | Supporting | 9 | 67 | 67 |
| `BC-006` | Georreferenciamento | Core | 12 | 84 | 35 |
| `BC-007` | Verificação Geométrica e Qualidade | Core | 5 | 42 | 86 |
| `BC-008` | Mosaico Relativo | Core | 6 | 42 | 26 |
| `BC-009` | Recuperação Assistida por IA e Governança de Modelos | Supporting | 2 | 13 | 24 |
| `BC-010` | Orquestração de Jobs e Recursos | Supporting | 12 | 86 | 69 |
| `BC-011` | Revisão e Correção | Supporting | 4 | 25 | 6 |
| `BC-012` | Resultados, Diagnósticos e Exportação | Supporting | 4 | 28 | 26 |
| `BC-013` | Artifacts, Proveniência e Lifecycle | Supporting | 9 | 59 | 65 |
| `BC-014` | Operações, Auditoria e Suporte | Generic | 11 | 70 | 77 |
| `BC-015` | Release, Instalação e Supply Chain | Generic | 11 | 64 | 25 |
| `BC-016` | Experiência e Orientação do Operador | Supporting | 7 | 45 | 57 |

## Achados e resoluções

| ID | Severidade | Achado | Resolução |
|---|---|---|---|
| `DDD-001` | HIGH | Capacidades de negócio e componentes técnicos estavam no mesmo catálogo de módulos. | 16 bounded contexts definidos; 18 módulos reclassificados como implementação/adapters. |
| `DDD-002` | HIGH | Layout global por domain/application/adapters favorecia modelo global e big ball of mud. | Layout context-first/layer-second registrado em ADR-005 e aplicado aos 758 TaskEnvelopes. |
| `DDD-003` | HIGH | Épicos, histórias, requisitos e contratos não declaravam owner semântico único. | 110 épicos, 758 histórias, 376 requisitos e contratos receberam context owner. |
| `DDD-004` | HIGH | Integrações internas não possuíam context map normativo. | 70 relações direcionadas com padrão DDD e linguagem publicada. |
| `DDD-005` | MEDIUM | Job execution e georeferencing attempt podiam ser tratados como o mesmo conceito. | AttemptExecution pertence ao BC-010; GeoreferencingAttempt pertence ao BC-006. |
| `DDD-006` | MEDIUM | IA poderia parecer owner de aceitação geométrica. | BC-009 produz candidatos; somente BC-007 emite SGVVerdict. |
| `DDD-007` | MEDIUM | Storage podia ser interpretado como domínio único. | PostgreSQL/filesystem são infraestrutura; BC-013 possui semântica de artifacts, provenance e lifecycle. |
| `DDD-008` | MEDIUM | UI/API/CLI podiam duplicar regra de domínio. | Canais foram definidos como adapters; BC-016 possui apenas estado de interação e consome published languages. |
| `DDD-009` | LOW | Não havia catálogo único de aggregates, eventos e linguagem ubíqua. | Catálogos DDD-050, DDD-060 e DDD-070 criados. |

## Invariantes de saída

- todo épico, história, requisito e TaskEnvelope possui context owner;
- cada aggregate possui owner único;
- UI/API/CLI/workers/broker/banco/filesystem não são bounded contexts;
- comandos cross-context respeitam contratos do context map; feedback loops de negócio usam eventos/process managers e não criam ciclos de import;
- eventos são publicados após commit e consumidos de forma idempotente;
- acesso cross-context a tabelas, ORM models, repositories e state machines é proibido;
- IA não emite aceitação geométrica;
- Jobs não possui resultados científicos;
- shared kernel de domínio não existe;
- packages de produção são context-first;

## Riscos residuais

- boundaries precisam ser confirmados por código e testes arquiteturais durante a implementação;
- traduções e contratos acrescentam trabalho, mas reduzem acoplamento e alucinação;
- context maps podem evoluir somente por ADR quando alterarem autoridade ou direção;


## Revisão detalhada dos Bounded Contexts

### BC-001 — Governança de Engenharia e Entrega

- **Classificação:** `Enabling`;
- **Missão:** Governar decisões, portfolio, evidências e autorização de entrega sem participar do runtime do produto.
- **Aggregates:** ArchitectureDecision, PortfolioSnapshot, SprintEvidenceSet, ImplementationAuthorizationRecord;
- **Eventos principais:** ArchitectureDecisionAccepted, BaselinePromoted, ImplementationAuthorized, SprintClosed;
- **Épicos owners:** `EPIC-001/EPIC-002/EPIC-003/EPIC-004/EPIC-005/EPIC-006/EPIC-007/EPIC-086/EPIC-090/EPIC-091/EPIC-092/EPIC-110`.

### BC-002 — Identidade e Controle de Acesso

- **Classificação:** `Generic`;
- **Missão:** Gerenciar identidades, sessões, tokens, memberships e decisões de autorização da instância.
- **Aggregates:** Account, Session, PersonalAccessToken, ProjectMembership, AuthorizationPolicy;
- **Eventos principais:** AdminBootstrapped, SessionCreated, SessionRevoked, TokenIssued, MembershipChanged;
- **Épicos owners:** `EPIC-008/EPIC-009/EPIC-010/EPIC-011`.

### BC-003 — Projetos, Workspace e Assets

- **Classificação:** `Supporting`;
- **Missão:** Manter projetos, roots autorizados, catálogo de assets e snapshots de seleção sem expor paths arbitrários.
- **Aggregates:** Project, WorkspaceRoot, WorkspaceEntry, Asset, InputSelectionSnapshot;
- **Eventos principais:** ProjectCreated, WorkspaceRootRegistered, AssetIngested, InputSelectionFrozen;
- **Épicos owners:** `EPIC-012`.

### BC-004 — Plano de Processamento e Workflow

- **Classificação:** `Supporting`;
- **Missão:** Definir ProcessingPlans versionados, capacidades, consentimentos e políticas de escalonamento sem executar algoritmos diretamente.
- **Aggregates:** ProcessingPlan, ProcessingStage, CapabilitySelection, PlanVariant, ProcessingPolicy;
- **Eventos principais:** ProcessingPlanCreated, ProcessingPlanValidated, PlanPreviewed, CapabilitySelected, PlanVariantCreated;
- **Épicos owners:** `EPIC-029`.

### BC-005 — Descoberta e Aquisição de Referências

- **Classificação:** `Supporting`;
- **Missão:** Descobrir, ranquear e adquirir referências autorizadas, mantendo provider capabilities, licença e evidência de disponibilidade.
- **Aggregates:** ProviderCapability, ProviderSearch, AcquisitionRequest, ReferenceCandidateSet, ReferenceGraph;
- **Eventos principais:** ReferenceSearchCompleted, ReferenceCandidateRanked, ReferenceAcquired, ReferenceEdgeAdmitted, ReferenceCandidateInvalidated;
- **Épicos owners:** `EPIC-022/EPIC-027/EPIC-053/EPIC-054/EPIC-055/EPIC-056/EPIC-058/EPIC-059/EPIC-060`.

### BC-006 — Georreferenciamento

- **Classificação:** `Core`;
- **Missão:** Produzir correspondências, GCPs automáticos, homografia projetiva e raster georreferenciado candidato de forma reproduzível.
- **Aggregates:** GeoreferencingAttempt, MatchSet, HomographyCandidate, AutomaticGCPSelection, OutputGrid;
- **Eventos principais:** MatchesProduced, HomographyEstimated, AutomaticGCPsSelected, OutputGridBuilt, GeoreferencedCandidateProduced;
- **Épicos owners:** `EPIC-023/EPIC-044/EPIC-045/EPIC-047/EPIC-048/EPIC-051/EPIC-052/EPIC-093/EPIC-094/EPIC-095/EPIC-096/EPIC-097`.

### BC-007 — Verificação Geométrica e Qualidade

- **Classificação:** `Core`;
- **Missão:** Aplicar SGV fail-closed, QualityProfiles, métricas geométricas e Image Deformation Profile para aceitar ou rejeitar candidatos.
- **Aggregates:** SGVProfile, QualityProfile, SGVEvaluation, SGVVerdict, ImageDeformationProfile;
- **Eventos principais:** CandidateEvaluated, SGVVerdictIssued, QualityProfilePromoted, DeformationProfileProduced;
- **Épicos owners:** `EPIC-021/EPIC-024/EPIC-025/EPIC-028/EPIC-038`.

### BC-008 — Mosaico Relativo

- **Classificação:** `Core`;
- **Missão:** Recuperar, otimizar, ancorar, verificar e materializar componentes de mosaico relativo com promoção explícita.
- **Aggregates:** RelativeMosaic, RelativeComponent, AnchorSet, RelativeMosaicEvaluation, MosaicMaterialization;
- **Eventos principais:** RelativeComponentBuilt, RelativeComponentOptimized, AnchorSetApplied, RelativeMosaicVerified, RelativeComponentPromoted, MosaicMaterialized;
- **Épicos owners:** `EPIC-098/EPIC-099/EPIC-100/EPIC-101/EPIC-102/EPIC-103`.

### BC-009 — Recuperação Assistida por IA e Governança de Modelos

- **Classificação:** `Supporting`;
- **Missão:** Executar recuperação neural elegível por ModelRunner/ModelPack sem possuir autoridade de aceitação geométrica.
- **Aggregates:** ModelPack, ModelRunnerProfile, AICapability, AIRecoveryAttempt, ModelPromotionRecord;
- **Eventos principais:** ModelPackImported, AIRecoveryCompleted, AICapabilityRegistered, ModelPromoted, ModelRevoked;
- **Épicos owners:** `EPIC-050/EPIC-088`.

### BC-010 — Orquestração de Jobs e Recursos

- **Classificação:** `Supporting`;
- **Missão:** Gerenciar jobs, work units, retries, checkpoints, cancelamento, scheduling, leases e budgets sem possuir resultados científicos.
- **Aggregates:** Job, AttemptExecution, WorkUnit, Checkpoint, ResourceLease, SchedulerPolicy, ExecutionSnapshot;
- **Eventos principais:** JobSubmitted, WorkUnitAdmitted, JobCancelled, JobResumed, ResourceLeaseGranted, CheckpointRecorded, JobProgressed;
- **Épicos owners:** `EPIC-014/EPIC-015/EPIC-016/EPIC-017/EPIC-018/EPIC-019/EPIC-065/EPIC-066/EPIC-067/EPIC-068/EPIC-069/EPIC-104`.

### BC-011 — Revisão e Correção

- **Classificação:** `Supporting`;
- **Missão:** Priorizar casos revisáveis, registrar CorrectionSets e GCPs manuais imutáveis e solicitar nova tentativa sem alterar hard gates.
- **Aggregates:** ReviewCase, ReviewQueue, CorrectionSet, ManualGCPSet, ReviewDecision;
- **Eventos principais:** ReviewCaseQueued, ReviewCasePrioritized, CorrectionSetCreated, ManualGCPRecorded, RetryRequested, ReviewClosed;
- **Épicos owners:** `EPIC-035/EPIC-062/EPIC-063/EPIC-064`.

### BC-012 — Resultados, Diagnósticos e Exportação

- **Classificação:** `Supporting`;
- **Missão:** Consolidar snapshots de resultado, diagnósticos, comparações, relatórios de lote e exports sem recalcular a verdade científica.
- **Aggregates:** ResultSnapshot, BatchResult, FailureDiagnostic, ResultComparison, ExportRequest;
- **Eventos principais:** ResultRecorded, CurrentResultChanged, ResultsCompared, ExportRequested, ExportCompleted;
- **Épicos owners:** `EPIC-030/EPIC-037/EPIC-057/EPIC-070`.

### BC-013 — Artifacts, Proveniência e Lifecycle

- **Classificação:** `Supporting`;
- **Missão:** Publicar ArtifactSets, manter manifests, hashes, lineage, cache, backup, retention e GC reference-aware.
- **Aggregates:** ArtifactObject, ArtifactSet, LineageRecord, BackupSet, RetentionPolicy, GarbageCollectionPlan, SchemaRegistry;
- **Eventos principais:** ArtifactSetPublished, LineageRecorded, BackupSetCreated, RetentionPolicyApplied, GarbageCollectionPlanned, ArtifactTombstoned, SchemaRegistered;
- **Épicos owners:** `EPIC-013/EPIC-026/EPIC-046/EPIC-049/EPIC-061/EPIC-071/EPIC-073/EPIC-074/EPIC-105`.

### BC-014 — Operações, Auditoria e Suporte

- **Classificação:** `Generic`;
- **Missão:** Observar, auditar e suportar a instância por sinais derivados, health/readiness, drain, restore drills e support bundles sanitizados.
- **Aggregates:** AuditRecord, OperationalSignalPolicy, SupportBundle, RestoreDrill, InstanceOperationalState;
- **Eventos principais:** AuditRecorded, DrainStateChanged, SupportBundleGenerated, RestoreDrillCompleted, OperationalAlertRaised;
- **Épicos owners:** `EPIC-039/EPIC-040/EPIC-041/EPIC-072/EPIC-075/EPIC-076/EPIC-077/EPIC-078/EPIC-079/EPIC-082/EPIC-083`.

### BC-015 — Release, Instalação e Supply Chain

- **Classificação:** `Generic`;
- **Missão:** Gerenciar instalação, bootstrap, upgrade, release train, licenciamento e attestations sem conter regras de domínio do produto.
- **Aggregates:** InstallationPlan, UpgradePlan, ReleaseCandidate, ReleaseMilestone, SupplyChainAttestation, RightsManifest;
- **Eventos principais:** InstanceInstalled, UpgradePreflightPassed, UpgradeCompleted, ReleasePromoted, ArtifactSigned, ReleasePublished;
- **Épicos owners:** `EPIC-042/EPIC-043/EPIC-080/EPIC-081/EPIC-085/EPIC-087/EPIC-089/EPIC-106/EPIC-107/EPIC-108/EPIC-109`.

### BC-016 — Experiência e Orientação do Operador

- **Classificação:** `Supporting`;
- **Missão:** Oferecer UI, CLI, jornadas guiadas, filtros e explicações consumindo contratos públicos, sem duplicar regras dos bounded contexts.
- **Aggregates:** GuidedSession, SavedFilter, OperatorPreference, LearningProgress, WorkspaceViewState;
- **Eventos principais:** GuidedSessionStarted, SavedFilterCreated, OperatorPreferenceChanged, LearningProgressRecorded, ViewStateChanged;
- **Épicos owners:** `EPIC-020/EPIC-031/EPIC-032/EPIC-033/EPIC-034/EPIC-036/EPIC-084`.

## Context Map completo

A direção abaixo identifica o fornecedor semântico e o consumidor. Feedback loops de processo são permitidos por eventos/process managers; import de implementação permanece proibido.

| Upstream | Downstream | Padrão | Linguagem publicada |
|---|---|---|---|
| `BC-001` | `BC-002` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-003` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-004` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-005` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-006` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-007` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-008` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-009` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-010` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-011` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-012` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-013` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-014` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-015` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-001` | `BC-016` | Policy/Conformance | Normas de engenharia; sem dependência runtime |
| `BC-002` | `BC-003` | Open Host Service + Published Language | IdentityClaims e AuthorizationDecision |
| `BC-002` | `BC-004` | Open Host Service + Published Language | IdentityClaims e AuthorizationDecision |
| `BC-002` | `BC-010` | Open Host Service + Published Language | ActorIdentity e AuthorizationDecision |
| `BC-002` | `BC-011` | Open Host Service + Published Language | ActorIdentity e AuthorizationDecision |
| `BC-002` | `BC-012` | Open Host Service + Published Language | ActorIdentity e AuthorizationDecision |
| `BC-002` | `BC-013` | Open Host Service + Published Language | ActorIdentity e AuthorizationDecision |
| `BC-002` | `BC-014` | Open Host Service + Published Language | ActorIdentity e AuthorizationDecision |
| `BC-002` | `BC-016` | Open Host Service + Published Language | SessionView e PermissionSet |
| `BC-003` | `BC-004` | Customer/Supplier | ProjectRef, AssetRef e InputSelectionSnapshot |
| `BC-003` | `BC-005` | Customer/Supplier | AssetRef e spatial hints |
| `BC-003` | `BC-010` | Published Language | ProjectRef e JobSubjectRef |
| `BC-003` | `BC-011` | Published Language | ProjectRef e AssetRef |
| `BC-003` | `BC-012` | Published Language | ProjectRef e AssetRef |
| `BC-003` | `BC-013` | Published Language | AssetRef e managed locator |
| `BC-003` | `BC-016` | Open Host Service | ProjectView, AssetView e WorkspaceEntryView |
| `BC-004` | `BC-005` | Customer/Supplier | ReferenceSearchPolicy |
| `BC-004` | `BC-006` | Customer/Supplier | GeoreferencingStageSpec |
| `BC-004` | `BC-009` | Customer/Supplier | AIEligibility e capability budget |
| `BC-004` | `BC-010` | Open Host Service + Published Language | ExecutionPlanSnapshot |
| `BC-004` | `BC-011` | Published Language | RetryPlan e CorrectionApplication |
| `BC-004` | `BC-012` | Published Language | PlanIdentity e result expectations |
| `BC-005` | `BC-006` | Customer/Supplier + Anti-Corruption Layer | ReferenceCandidateSet traduzido para ReferenceInput |
| `BC-005` | `BC-013` | Published Language | AcquiredAsset e license record |
| `BC-006` | `BC-007` | Customer/Supplier + Published Language | GeometricCandidate |
| `BC-006` | `BC-008` | Published Language | AcceptedImageGeometry somente após veredito |
| `BC-006` | `BC-012` | Domain Events | AttemptOutcome e candidate diagnostics |
| `BC-006` | `BC-013` | Published Language | ArtifactPublicationRequest e lineage inputs |
| `BC-009` | `BC-007` | Customer/Supplier + Anti-Corruption Layer | NeuralCandidate convertido para GeometricCandidate; sem privilégio |
| `BC-009` | `BC-013` | Published Language | ModelPack manifest e inference artifacts |
| `BC-007` | `BC-008` | Published Language | VerifiedImageGeometry e QualitySummary |
| `BC-007` | `BC-011` | Domain Events | ReviewableVerdict |
| `BC-007` | `BC-012` | Domain Events | SGVVerdictIssued e QualityReport |
| `BC-007` | `BC-013` | Published Language | Quality artifact publication |
| `BC-010` | `BC-005` | Process Manager + Ports | Executa work units sem importar modelo interno |
| `BC-010` | `BC-006` | Process Manager + Ports | Executa work units sem importar modelo interno |
| `BC-010` | `BC-007` | Process Manager + Ports | Executa avaliação sem possuir veredito |
| `BC-010` | `BC-008` | Process Manager + Ports | Executa DAG sem possuir mosaico |
| `BC-010` | `BC-009` | Process Manager + Ports | Executa ModelRunner por contrato |
| `BC-010` | `BC-012` | Domain Events | JobProgressed e JobTerminalState |
| `BC-010` | `BC-014` | Published Language | Scheduler signals e execution ledger |
| `BC-011` | `BC-004` | Customer/Supplier | RetryRequested e CorrectionSetRef |
| `BC-011` | `BC-006` | Published Language | CorrectionSet e ManualGCPSet |
| `BC-011` | `BC-008` | Published Language | AnchorSet e correction impact |
| `BC-011` | `BC-012` | Domain Events | ReviewDecision e current result request |
| `BC-011` | `BC-013` | Published Language | Immutable correction artifacts |
| `BC-008` | `BC-012` | Domain Events | RelativeMosaicOutcome e report snapshot |
| `BC-008` | `BC-013` | Published Language | Mosaic materialization request e lineage |
| `BC-013` | `BC-012` | Open Host Service + Published Language | ArtifactRef, ManifestRef e ExportMaterial |
| `BC-013` | `BC-014` | Domain Events | Lifecycle, backup e GC events |
| `BC-013` | `BC-015` | Published Language | SchemaCompatibility e release artifacts |
| `BC-013` | `BC-016` | Open Host Service | Authorized artifact views e downloads |
| `BC-012` | `BC-016` | Open Host Service + Published Language | ResultView, QualityView, DiagnosticView |
| `BC-012` | `BC-014` | Domain Events | Result and export operational signals |
| `BC-014` | `BC-016` | Open Host Service | Health, readiness e admin views |
| `BC-015` | `BC-009` | Published Language | Verified ModelPack distribution |

## Impacto por Sprint

| Sprint | Bounded Contexts | Épicos | Histórias | Regra de integração |
|---|---|---:|---:|---|
| `SPRINT-001` | `BC-001` | 12 | 91 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-002` | `BC-002`, `BC-003`, `BC-013`, `BC-014` | 8 | 55 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-003` | `BC-010`, `BC-016` | 7 | 49 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-004` | `BC-010` | 6 | 42 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-005` | `BC-007`, `BC-005`, `BC-006`, `BC-013`, `BC-004`, `BC-012` | 15 | 120 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-006` | `BC-009`, `BC-006`, `BC-005`, `BC-012`, `BC-011` | 12 | 86 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-007` | `BC-006`, `BC-008` | 6 | 42 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-008` | `BC-008` | 5 | 35 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-009` | `BC-016`, `BC-011` | 9 | 58 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-010` | `BC-012`, `BC-007`, `BC-013` | 6 | 38 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-011` | `BC-014`, `BC-013`, `BC-015`, `BC-009` | 14 | 84 | contratos upstream congelados antes de lanes downstream |
| `SPRINT-012` | `BC-015` | 10 | 58 | contratos upstream congelados antes de lanes downstream |

## ADRs criadas na Fase C

- `ADR-003`: define subdomínios, bounded contexts e linguagem ubíqua;
- `ADR-004`: define context map, modelos publicados, ACLs, eventos e proibição de modelo compartilhado;
- `ADR-005`: define layout context-first/layer-second e write scopes por context.

As ADRs `001–022` receberam contextualização DDD e foram mapeadas em `ADR_CONTEXT_MAP.csv`. Nenhuma decisão anterior foi invalidada.

## Revisão dos contratos

- operações HTTP congeladas: 56;
- operações sem owner context: 0;
- schemas usados como shared domain model: 0;
- `x-bounded-context` foi registrado no OpenAPI;
- ownership integral está em `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`;

| Contexto | Operações HTTP |
|---|---:|
| `BC-002` | 8 |
| `BC-003` | 10 |
| `BC-004` | 3 |
| `BC-005` | 5 |
| `BC-007` | 3 |
| `BC-010` | 3 |
| `BC-011` | 4 |
| `BC-012` | 6 |
| `BC-013` | 5 |
| `BC-014` | 6 |
| `BC-015` | 3 |

## Revisão de módulos e infraestrutura

- módulos técnicos revisados: 18;
- módulos tratados como bounded context: 0;
- PostgreSQL/PostGIS permanece system of record físico, mas cada aggregate possui owner context;
- filesystem permanece armazenamento físico; a semântica de ArtifactSet pertence ao `BC-013`;
- RabbitMQ permanece transporte; a semântica de Job/WorkUnit pertence ao `BC-010`;
- UI, API e CLI permanecem adapters; estado de interação próprio fica no `BC-016`.

## Revisão de dependências

- dependências de histórias: 1.165 hard blockers, 88 ondas, zero ciclo;
- relações de context map: 70;
- dependências diretas de implementação entre contexts: zero;
- acesso cross-schema/tabela: proibido;
- import cross-context de entity/repository/ORM/state machine: proibido;
- contracts e events podem formar feedback loops de negócio, mas não ciclos de package/import.

## Trade-offs aprovados

| Escolha | Benefício | Custo aceito |
|---|---|---|
| Monólito modular por context | operação simples e boundaries auditáveis | disciplina de package e testes arquiteturais |
| Sem shared kernel de domínio | reduz acoplamento semântico | possível duplicação local deliberada |
| Contratos publicados entre contexts | integração explícita e testável | mais DTOs, mappers e testes de contrato |
| `BC-010` separado do core científico | retry/scheduling não contaminam resultados | process manager e eventos adicionais |
| IA separada da aceitação | evita confiança neural como prova geométrica | toda recuperação passa novamente pelo SGV |
| Context-first/layer-second | evita arquivos gigantes e modelo global | mais packages pequenos e ownership rigoroso |

## Critérios de saída da Fase C

- [x] core, supporting, generic e enabling subdomains classificados;
- [x] 16 bounded contexts com missão e linguagem local;
- [x] aggregates e eventos catalogados;
- [x] context map e padrões de integração definidos;
- [x] 110 épicos, 758 histórias, 868 issues e 376 requisitos reconciliados;
- [x] 758 TaskEnvelopes com context owner e write scope context-first;
- [x] 57 ADRs consistentes após a consolidação definitiva da Fase D;
- [x] contratos com owner único;
- [x] módulos técnicos separados de contexts;
- [x] validators A, B, C, SAR e Python Architecture aprovados;
- [x] zero pendência bloqueante.

## Próxima fase

O charter da próxima fase não foi fornecido. Agentes não podem inventar objetivo, escopo ou gates. A Fase C está encerrada; a implementação continua bloqueada externamente.
