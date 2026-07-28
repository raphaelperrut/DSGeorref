# BC-008 — Mosaico Relativo

- **Classificação DDD:** `Core`
- **Papel estratégico:** `Core domain`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-098, EPIC-099, EPIC-100, EPIC-101, EPIC-102, EPIC-103`

## Missão

Recuperar, otimizar, ancorar, verificar e materializar componentes de mosaico relativo com promoção explícita.

## Linguagem ubíqua local

- `mosaico relativo`
- `componente`
- `âncora`
- `otimização global`
- `promoção`

## Aggregates e raízes

- `RelativeMosaic`
- `RelativeComponent`
- `AnchorSet`
- `RelativeMosaicEvaluation`
- `MosaicMaterialization`

## Comandos

- `ConstruirGrafoSobreposicao`
- `OtimizarComponente`
- `AplicarAnchorSet`
- `VerificarMosaico`
- `PromoverComponente`
- `MaterializarMosaico`

## Eventos de domínio

- `RelativeComponentBuilt`
- `RelativeComponentOptimized`
- `AnchorSetApplied`
- `RelativeMosaicVerified`
- `RelativeComponentPromoted`
- `MosaicMaterialized`

## Relações

- **Upstream:** BC-006, BC-007, BC-011.
- **Downstream:** BC-012, BC-013.
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
