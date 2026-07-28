# BC-013 — Artifacts, Proveniência e Lifecycle

- **Classificação DDD:** `Supporting`
- **Papel estratégico:** `Integridade`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-013, EPIC-026, EPIC-046, EPIC-049, EPIC-061, EPIC-071, EPIC-073, EPIC-074, EPIC-105`

## Missão

Publicar ArtifactSets, manter manifests, hashes, lineage, cache, backup, retention e GC reference-aware.

## Linguagem ubíqua local

- `ArtifactSet`
- `artifact object`
- `manifest`
- `lineage`
- `BackupSet`
- `RetentionPolicy`
- `tombstone`

## Aggregates e raízes

- `ArtifactObject`
- `ArtifactSet`
- `LineageRecord`
- `BackupSet`
- `RetentionPolicy`
- `GarbageCollectionPlan`
- `SchemaRegistry`

## Comandos

- `PublicarArtifactSet`
- `RegistrarLineage`
- `CriarBackupSet`
- `AplicarRetentionPolicy`
- `PrevisualizarGC`
- `ExecutarGC`
- `RegistrarSchema`

## Eventos de domínio

- `ArtifactSetPublished`
- `LineageRecorded`
- `BackupSetCreated`
- `RetentionPolicyApplied`
- `GarbageCollectionPlanned`
- `ArtifactTombstoned`
- `SchemaRegistered`

## Relações

- **Upstream:** BC-003, BC-005, BC-006, BC-007, BC-008, BC-009, BC-011, BC-012.
- **Downstream:** BC-014, BC-015, BC-016.
- As relações normativas e os padrões de integração estão em `../DDD-040-CONTEXT-MAP.md`.

## Autoridade

O contexto é o único owner do significado, invariantes e transições de seus aggregates. Outros contextos recebem IDs, snapshots, eventos ou DTOs publicados; nunca importam entidades internas.

## Proibições

- não compartilhar ORM models, state machines ou repositories entre contexts;
- não acessar tabelas de outro contexto;
- não publicar evento antes do commit autoritativo;
- não usar UI, API, broker, filesystem ou banco como substituto do modelo de domínio;
- não criar módulo `common`, `utils` ou `shared-domain` para escapar do boundary.

## Contratos

Contratos públicos são registrados em `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`. Mudança breaking exige ADR ou versão nova do contrato, migration e rollback quando aplicável.
