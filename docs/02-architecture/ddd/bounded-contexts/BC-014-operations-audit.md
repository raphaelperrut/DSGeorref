# BC-014 — Operações, Auditoria e Suporte

- **Classificação DDD:** `Generic`
- **Papel estratégico:** `Operação`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-039, EPIC-040, EPIC-041, EPIC-072, EPIC-075, EPIC-076, EPIC-077, EPIC-078, EPIC-079, EPIC-082, EPIC-083`

## Missão

Observar, auditar e suportar a instância por sinais derivados, health/readiness, drain, restore drills e support bundles sanitizados.

## Linguagem ubíqua local

- `audit record`
- `sinal operacional`
- `readiness`
- `drain`
- `support bundle`
- `restore drill`

## Aggregates e raízes

- `AuditRecord`
- `OperationalSignalPolicy`
- `SupportBundle`
- `RestoreDrill`
- `InstanceOperationalState`

## Comandos

- `RegistrarAuditoria`
- `AlterarDrain`
- `GerarSupportBundle`
- `ExecutarRestoreDrill`
- `AtualizarSignalPolicy`

## Eventos de domínio

- `AuditRecorded`
- `DrainStateChanged`
- `SupportBundleGenerated`
- `RestoreDrillCompleted`
- `OperationalAlertRaised`

## Relações

- **Upstream:** BC-002, BC-010, BC-012, BC-013, BC-015.
- **Downstream:** BC-016.
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
