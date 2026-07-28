# BC-006 — Georreferenciamento

- **Classificação DDD:** `Core`
- **Papel estratégico:** `Core domain`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-023, EPIC-044, EPIC-045, EPIC-047, EPIC-048, EPIC-051, EPIC-052, EPIC-093, EPIC-094, EPIC-095, EPIC-096, EPIC-097`

## Missão

Produzir correspondências, GCPs automáticos, homografia projetiva e raster georreferenciado candidato de forma reproduzível.

## Linguagem ubíqua local

- `attempt`
- `correspondência`
- `GCP automático`
- `homografia`
- `grade de saída`

## Aggregates e raízes

- `GeoreferencingAttempt`
- `MatchSet`
- `HomographyCandidate`
- `AutomaticGCPSelection`
- `OutputGrid`

## Comandos

- `ExecutarMatching`
- `EstimarHomografia`
- `SelecionarGCPs`
- `ConstruirGradeSaida`
- `GerarRasterCandidato`

## Eventos de domínio

- `MatchesProduced`
- `HomographyEstimated`
- `AutomaticGCPsSelected`
- `OutputGridBuilt`
- `GeoreferencedCandidateProduced`

## Relações

- **Upstream:** BC-003, BC-004, BC-005.
- **Downstream:** BC-007, BC-008, BC-012, BC-013.
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
