# BC-001 — Governança de Engenharia e Entrega

- **Classificação DDD:** `Enabling`
- **Papel estratégico:** `Suporte organizacional`
- **Runtime:** `Não participa do runtime`
- **Épicos owners:** `EPIC-001, EPIC-002, EPIC-003, EPIC-004, EPIC-005, EPIC-006, EPIC-007, EPIC-086, EPIC-090, EPIC-091, EPIC-092, EPIC-110`

## Missão

Governar decisões, portfolio, evidências e autorização de entrega sem participar do runtime do produto.

## Linguagem ubíqua local

- `decisão arquitetural`
- `baseline normativa`
- `história implementável`
- `TaskEnvelope`
- `evidência de sprint`

## Aggregates e raízes

- `ArchitectureDecision`
- `PortfolioSnapshot`
- `SprintEvidenceSet`
- `ImplementationAuthorizationRecord`

## Comandos

- `RegistrarDecisao`
- `PromoverBaseline`
- `AutorizarImplementacao`
- `FecharSprint`

## Eventos de domínio

- `ArchitectureDecisionAccepted`
- `BaselinePromoted`
- `ImplementationAuthorized`
- `SprintClosed`

## Relações

- **Upstream:** Nenhum contexto de produto.
- **Downstream:** BC-002, BC-003, BC-004, BC-005, BC-006, BC-007, BC-008, BC-009, BC-010, BC-011, BC-012, BC-013, BC-014, BC-015, BC-016.
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
