# BC-015 — Release, Instalação e Supply Chain

- **Classificação DDD:** `Generic`
- **Papel estratégico:** `Entrega operacional`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-042, EPIC-043, EPIC-080, EPIC-081, EPIC-085, EPIC-087, EPIC-089, EPIC-106, EPIC-107, EPIC-108, EPIC-109`

## Missão

Gerenciar instalação, bootstrap, upgrade, release train, licenciamento e attestations sem conter regras de domínio do produto.

## Linguagem ubíqua local

- `installation plan`
- `upgrade plan`
- `release candidate`
- `milestone`
- `attestation`
- `rights manifest`

## Aggregates e raízes

- `InstallationPlan`
- `UpgradePlan`
- `ReleaseCandidate`
- `ReleaseMilestone`
- `SupplyChainAttestation`
- `RightsManifest`

## Comandos

- `InstalarInstancia`
- `PrevalidarUpgrade`
- `ExecutarUpgrade`
- `PromoverRelease`
- `AssinarArtifact`
- `PublicarRelease`

## Eventos de domínio

- `InstanceInstalled`
- `UpgradePreflightPassed`
- `UpgradeCompleted`
- `ReleasePromoted`
- `ArtifactSigned`
- `ReleasePublished`

## Relações

- **Upstream:** BC-001, BC-013, BC-014.
- **Downstream:** BC-009.
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
