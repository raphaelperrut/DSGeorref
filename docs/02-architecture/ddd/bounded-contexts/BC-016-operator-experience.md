# BC-016 — Experiência e Orientação do Operador

- **Classificação DDD:** `Supporting`
- **Papel estratégico:** `Interação`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-020, EPIC-031, EPIC-032, EPIC-033, EPIC-034, EPIC-036, EPIC-084`

## Missão

Oferecer UI, CLI, jornadas guiadas, filtros e explicações consumindo contratos públicos, sem duplicar regras dos bounded contexts.

## Linguagem ubíqua local

- `jornada guiada`
- `filtro salvo`
- `preferência`
- `ajuda contextual`
- `view state`

## Aggregates e raízes

- `GuidedSession`
- `SavedFilter`
- `OperatorPreference`
- `LearningProgress`
- `WorkspaceViewState`

## Comandos

- `IniciarJornada`
- `SalvarFiltro`
- `AtualizarPreferencia`
- `RegistrarProgressoAprendizado`
- `AtualizarViewState`

## Eventos de domínio

- `GuidedSessionStarted`
- `SavedFilterCreated`
- `OperatorPreferenceChanged`
- `LearningProgressRecorded`
- `ViewStateChanged`

## Relações

- **Upstream:** BC-002, BC-003, BC-004, BC-005, BC-007, BC-010, BC-011, BC-012, BC-013, BC-014.
- **Downstream:** Nenhum.
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
