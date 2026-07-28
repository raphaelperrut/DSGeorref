# BC-003 — Projetos, Workspace e Assets

- **Classificação DDD:** `Supporting`
- **Papel estratégico:** `Suporte`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-012`

## Missão

Manter projetos, roots autorizados, catálogo de assets e snapshots de seleção sem expor paths arbitrários.

## Linguagem ubíqua local

- `projeto`
- `workspace root`
- `entrada do workspace`
- `asset`
- `snapshot de seleção`

## Aggregates e raízes

- `Project`
- `WorkspaceRoot`
- `WorkspaceEntry`
- `Asset`
- `InputSelectionSnapshot`

## Comandos

- `CriarProjeto`
- `RegistrarRoot`
- `NavegarWorkspace`
- `IngerirAsset`
- `CongelarSelecao`

## Eventos de domínio

- `ProjectCreated`
- `WorkspaceRootRegistered`
- `AssetIngested`
- `InputSelectionFrozen`

## Relações

- **Upstream:** BC-002.
- **Downstream:** BC-004, BC-005, BC-010, BC-011, BC-012, BC-013, BC-016.
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
