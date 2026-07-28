# BC-009 — Recuperação Assistida por IA e Governança de Modelos

- **Classificação DDD:** `Supporting`
- **Papel estratégico:** `Diferenciador controlado`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-050, EPIC-088`

## Missão

Executar recuperação neural elegível por ModelRunner/ModelPack sem possuir autoridade de aceitação geométrica.

## Linguagem ubíqua local

- `ModelPack`
- `ModelRunner`
- `capability de IA`
- `recuperação neural`
- `promotion record`

## Aggregates e raízes

- `ModelPack`
- `ModelRunnerProfile`
- `AICapability`
- `AIRecoveryAttempt`
- `ModelPromotionRecord`

## Comandos

- `ImportarModelPack`
- `ExecutarRecuperacaoIA`
- `RegistrarCapability`
- `PromoverModelo`
- `RevogarModelo`

## Eventos de domínio

- `ModelPackImported`
- `AIRecoveryCompleted`
- `AICapabilityRegistered`
- `ModelPromoted`
- `ModelRevoked`

## Relações

- **Upstream:** BC-004, BC-006, BC-015.
- **Downstream:** BC-007, BC-013.
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
