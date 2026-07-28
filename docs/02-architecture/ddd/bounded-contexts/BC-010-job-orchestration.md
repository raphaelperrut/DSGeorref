# BC-010 — Orquestração de Jobs e Recursos

- **Classificação DDD:** `Supporting`
- **Papel estratégico:** `Execução`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-014, EPIC-015, EPIC-016, EPIC-017, EPIC-018, EPIC-019, EPIC-065, EPIC-066, EPIC-067, EPIC-068, EPIC-069, EPIC-104`

## Missão

Gerenciar jobs, work units, retries, checkpoints, cancelamento, scheduling, leases e budgets sem possuir resultados científicos.

## Linguagem ubíqua local

- `job`
- `work unit`
- `attempt de execução`
- `checkpoint`
- `lease`
- `scheduler policy`

## Aggregates e raízes

- `Job`
- `AttemptExecution`
- `WorkUnit`
- `Checkpoint`
- `ResourceLease`
- `SchedulerPolicy`
- `ExecutionSnapshot`

## Comandos

- `SubmeterJob`
- `AdmitirWorkUnit`
- `CancelarJob`
- `RetomarJob`
- `ConcederLease`
- `RegistrarCheckpoint`

## Eventos de domínio

- `JobSubmitted`
- `WorkUnitAdmitted`
- `JobCancelled`
- `JobResumed`
- `ResourceLeaseGranted`
- `CheckpointRecorded`
- `JobProgressed`

## Relações

- **Upstream:** BC-002, BC-003, BC-004.
- **Downstream:** BC-005, BC-006, BC-007, BC-008, BC-009, BC-012, BC-014.
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
