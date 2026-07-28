# BC-004 — Plano de Processamento e Workflow

- **Classificação DDD:** `Supporting`
- **Papel estratégico:** `Coordenação`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-029`

## Missão

Definir ProcessingPlans versionados, capacidades, consentimentos e políticas de escalonamento sem executar algoritmos diretamente.

## Linguagem ubíqua local

- `ProcessingPlan`
- `estágio`
- `capability`
- `PlanVariant`
- `política de processamento`

## Aggregates e raízes

- `ProcessingPlan`
- `ProcessingStage`
- `CapabilitySelection`
- `PlanVariant`
- `ProcessingPolicy`

## Comandos

- `CriarPlano`
- `ValidarPlano`
- `PrevisualizarPlano`
- `SelecionarCapability`
- `CriarPlanVariant`

## Eventos de domínio

- `ProcessingPlanCreated`
- `ProcessingPlanValidated`
- `PlanPreviewed`
- `CapabilitySelected`
- `PlanVariantCreated`

## Relações

- **Upstream:** BC-002, BC-003.
- **Downstream:** BC-005, BC-006, BC-009, BC-010, BC-011, BC-012.
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
