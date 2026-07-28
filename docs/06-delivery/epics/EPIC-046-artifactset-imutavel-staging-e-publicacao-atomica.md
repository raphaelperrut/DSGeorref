# EPIC-046 — ArtifactSet imutável, staging e publicação atômica

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0046`
- **Dependências:** EPIC-012, EPIC-026, EPIC-044
- **Release gate:** `G3/G4`
- **Referências arquiteturais:** ADR-051, ADR-018, ADR-041, ADR-049

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-023`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-049`

## Resultado

Artifactset imutável, staging e publicação atômica.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AI-017, REQ-ANC-004, REQ-ART-002, REQ-ART-003, REQ-RAS-005
- Issue: `ISSUE-0046`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0275` / `ISSUE-0385` / `TASK-0275` — Definir contrato científico e invariantes: ArtifactSet imutável, staging e publicação atômica
- `STORY-0276` / `ISSUE-0386` / `TASK-0276` — Preparar corpus, fixtures e representação tipada: ArtifactSet imutável, staging e publicação atômica
- `STORY-0277` / `ISSUE-0387` / `TASK-0277` — Implementar o núcleo algorítmico: ArtifactSet imutável, staging e publicação atômica
- `STORY-0278` / `ISSUE-0388` / `TASK-0278` — Integrar ao ProcessingPlan e pipeline: ArtifactSet imutável, staging e publicação atômica
- `STORY-0279` / `ISSUE-0389` / `TASK-0279` — Produzir métricas, diagnóstico e lineage: ArtifactSet imutável, staging e publicação atômica
- `STORY-0280` / `ISSUE-0390` / `TASK-0280` — Executar benchmark, negativos e regressão científica: ArtifactSet imutável, staging e publicação atômica
- `STORY-0281` / `ISSUE-0391` / `TASK-0281` — Auditar evidência científica e final: ArtifactSet imutável, staging e publicação atômica

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-023`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-049`
- **Resultado:** `PASS`
