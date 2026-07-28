# BC-005 — Descoberta e Aquisição de Referências

- **Classificação DDD:** `Supporting`
- **Papel estratégico:** `Suporte ao core`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-022, EPIC-027, EPIC-053, EPIC-054, EPIC-055, EPIC-056, EPIC-058, EPIC-059, EPIC-060`

## Missão

Descobrir, ranquear e adquirir referências autorizadas, mantendo provider capabilities, licença e evidência de disponibilidade.

## Linguagem ubíqua local

- `provider`
- `candidate`
- `busca espaciotemporal`
- `aquisição`
- `grafo de referências`

## Aggregates e raízes

- `ProviderCapability`
- `ProviderSearch`
- `AcquisitionRequest`
- `ReferenceCandidateSet`
- `ReferenceGraph`

## Comandos

- `BuscarReferencias`
- `ExpandirBusca`
- `AdquirirReferencia`
- `AdmitirAresta`
- `InvalidarCandidato`

## Eventos de domínio

- `ReferenceSearchCompleted`
- `ReferenceCandidateRanked`
- `ReferenceAcquired`
- `ReferenceEdgeAdmitted`
- `ReferenceCandidateInvalidated`

## Relações

- **Upstream:** BC-003, BC-004.
- **Downstream:** BC-006, BC-013.
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
