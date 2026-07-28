# Catálogo de aggregates e invariantes

| Contexto | Aggregates | Invariante de ownership |
|---|---|---|
| `BC-001` | `ArchitectureDecision`, `PortfolioSnapshot`, `SprintEvidenceSet`, `ImplementationAuthorizationRecord` | Somente BC-001 altera estado e invariantes. |
| `BC-002` | `Account`, `Session`, `PersonalAccessToken`, `ProjectMembership`, `AuthorizationPolicy` | Somente BC-002 altera estado e invariantes. |
| `BC-003` | `Project`, `WorkspaceRoot`, `WorkspaceEntry`, `Asset`, `InputSelectionSnapshot` | Somente BC-003 altera estado e invariantes. |
| `BC-004` | `ProcessingPlan`, `ProcessingStage`, `CapabilitySelection`, `PlanVariant`, `ProcessingPolicy` | Somente BC-004 altera estado e invariantes. |
| `BC-005` | `ProviderCapability`, `ProviderSearch`, `AcquisitionRequest`, `ReferenceCandidateSet`, `ReferenceGraph` | Somente BC-005 altera estado e invariantes. |
| `BC-006` | `GeoreferencingAttempt`, `MatchSet`, `HomographyCandidate`, `AutomaticGCPSelection`, `OutputGrid` | Somente BC-006 altera estado e invariantes. |
| `BC-007` | `SGVProfile`, `QualityProfile`, `SGVEvaluation`, `SGVVerdict`, `ImageDeformationProfile` | Somente BC-007 altera estado e invariantes. |
| `BC-008` | `RelativeMosaic`, `RelativeComponent`, `AnchorSet`, `RelativeMosaicEvaluation`, `MosaicMaterialization` | Somente BC-008 altera estado e invariantes. |
| `BC-009` | `ModelPack`, `ModelRunnerProfile`, `AICapability`, `AIRecoveryAttempt`, `ModelPromotionRecord` | Somente BC-009 altera estado e invariantes. |
| `BC-010` | `Job`, `AttemptExecution`, `WorkUnit`, `Checkpoint`, `ResourceLease`, `SchedulerPolicy`, `ExecutionSnapshot` | Somente BC-010 altera estado e invariantes. |
| `BC-011` | `ReviewCase`, `ReviewQueue`, `CorrectionSet`, `ManualGCPSet`, `ReviewDecision` | Somente BC-011 altera estado e invariantes. |
| `BC-012` | `ResultSnapshot`, `BatchResult`, `FailureDiagnostic`, `ResultComparison`, `ExportRequest` | Somente BC-012 altera estado e invariantes. |
| `BC-013` | `ArtifactObject`, `ArtifactSet`, `LineageRecord`, `BackupSet`, `RetentionPolicy`, `GarbageCollectionPlan`, `SchemaRegistry` | Somente BC-013 altera estado e invariantes. |
| `BC-014` | `AuditRecord`, `OperationalSignalPolicy`, `SupportBundle`, `RestoreDrill`, `InstanceOperationalState` | Somente BC-014 altera estado e invariantes. |
| `BC-015` | `InstallationPlan`, `UpgradePlan`, `ReleaseCandidate`, `ReleaseMilestone`, `SupplyChainAttestation`, `RightsManifest` | Somente BC-015 altera estado e invariantes. |
| `BC-016` | `GuidedSession`, `SavedFilter`, `OperatorPreference`, `LearningProgress`, `WorkspaceViewState` | Somente BC-016 altera estado e invariantes. |
