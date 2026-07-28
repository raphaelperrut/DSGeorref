# BC-011 — Revisão e Correção

- **Classificação DDD:** `Supporting`
- **Papel estratégico:** `Suporte ao core`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-035, EPIC-062, EPIC-063, EPIC-064`

## Missão

Priorizar casos revisáveis, registrar CorrectionSets e GCPs manuais imutáveis e solicitar nova tentativa sem alterar hard gates.

## Linguagem ubíqua local

- `caso de revisão`
- `fila de revisão`
- `CorrectionSet`
- `GCP manual`
- `decisão de revisão`

## Aggregates e raízes

- `ReviewCase`
- `ReviewQueue`
- `CorrectionSet`
- `ManualGCPSet`
- `ReviewDecision`

## Comandos

- `EnfileirarRevisao`
- `PriorizarCaso`
- `CriarCorrectionSet`
- `RegistrarGCPManual`
- `SolicitarNovaTentativa`
- `EncerrarRevisao`

## Eventos de domínio

- `ReviewCaseQueued`
- `ReviewCasePrioritized`
- `CorrectionSetCreated`
- `ManualGCPRecorded`
- `RetryRequested`
- `ReviewClosed`

## Relações

- **Upstream:** BC-002, BC-003, BC-007, BC-008, BC-012.
- **Downstream:** BC-004, BC-006, BC-008, BC-012, BC-013.
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
