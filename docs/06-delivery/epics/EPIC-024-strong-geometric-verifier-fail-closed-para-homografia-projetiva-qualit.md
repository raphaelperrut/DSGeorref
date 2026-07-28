# EPIC-024 — Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-007 — Verificação Geométrica e Qualidade`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0024`
- **Dependências:** EPIC-022, EPIC-023
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-046, ADR-044, ADR-048, ADR-041, ADR-049, ADR-050, ADR-053

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-030`, `ADR-038`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-048`, `ADR-049`, `ADR-050`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`

## Resultado

Strong geometric verifier fail-closed para homografia projetiva, qualityprofiles e image deformation profile.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AIE-001, REQ-AIE-002, REQ-AIE-003, REQ-AIE-004, REQ-AIE-005, REQ-AIE-006, REQ-AIE-007, REQ-AIE-008, REQ-AIE-009, REQ-AIE-010, REQ-ANC-002, REQ-ANC-003, REQ-ANC-006, REQ-ANC-007, REQ-CRS-003, REQ-EPIC-021, REQ-EST-001, REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-GCP-001, REQ-HOM-001, REQ-MOS-003, REQ-MOS-005, REQ-MSK-001, REQ-QUAL-001, REQ-QUAL-002, REQ-QUAL-003, REQ-QUAL-004, REQ-RAS-003, REQ-REF-001, REQ-REF-002, REQ-REV-003, REQ-RMV-001, REQ-RMV-002, REQ-SDR-002
- Issue: `ISSUE-0024`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **10** histórias filhas:

- `STORY-0136` / `ISSUE-0246` / `TASK-0136` — Definir contrato científico e invariantes: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0137` / `ISSUE-0247` / `TASK-0137` — Consolidar slices e liberar integração: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0138` / `ISSUE-0248` / `TASK-0138` — Implementar o núcleo algorítmico: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0139` / `ISSUE-0249` / `TASK-0139` — Integrar ao ProcessingPlan e pipeline: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0140` / `ISSUE-0250` / `TASK-0140` — Produzir métricas, diagnóstico e lineage: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0141` / `ISSUE-0251` / `TASK-0141` — Executar benchmark, negativos e regressão científica: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0142` / `ISSUE-0252` / `TASK-0142` — Auditar evidência científica e final: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0729` / `ISSUE-0839` / `TASK-0729` — Slice 1/3 — Preparar corpus, fixtures e representação tipada: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile [REQ-AIE, REQ-ANC, REQ-CRS, REQ-EPIC]
- `STORY-0730` / `ISSUE-0840` / `TASK-0730` — Slice 2/3 — Preparar corpus, fixtures e representação tipada: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile [REQ-EST, REQ-FS1, REQ-MSK, REQ-QUAL, REQ-RAS, REQ-REF]
- `STORY-0731` / `ISSUE-0841` / `TASK-0731` — Slice 3/3 — Preparar corpus, fixtures e representação tipada: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile [REQ-RMV]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-030`, `ADR-038`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-048`, `ADR-049`, `ADR-050`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
