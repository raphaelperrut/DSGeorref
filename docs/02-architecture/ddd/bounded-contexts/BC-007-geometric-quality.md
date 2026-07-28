# BC-007 — Verificação Geométrica e Qualidade

- **Classificação DDD:** `Core`
- **Papel estratégico:** `Core domain`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-021, EPIC-024, EPIC-025, EPIC-028, EPIC-038`

## Missão

Aplicar SGV fail-closed, QualityProfiles, métricas geométricas e Image Deformation Profile para aceitar ou rejeitar candidatos.

## Linguagem ubíqua local

- `SGV`
- `hard gate`
- `QualityProfile`
- `veredito`
- `deformação`

## Aggregates e raízes

- `SGVProfile`
- `QualityProfile`
- `SGVEvaluation`
- `SGVVerdict`
- `ImageDeformationProfile`

## Comandos

- `AvaliarCandidato`
- `CalcularMetricas`
- `AplicarQualityProfile`
- `EmitirVeredito`
- `CalibrarProfile`

## Eventos de domínio

- `CandidateEvaluated`
- `SGVVerdictIssued`
- `QualityProfilePromoted`
- `DeformationProfileProduced`

## Relações

- **Upstream:** BC-006, BC-009.
- **Downstream:** BC-008, BC-011, BC-012, BC-013.
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
