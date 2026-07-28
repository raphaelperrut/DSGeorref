# EPIC-044 — OutputProfile, COG canônico, preservação de resolução e validação da grade

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0044`
- **Dependências:** EPIC-012, EPIC-024
- **Release gate:** `G3/G4`
- **Referências arquiteturais:** ADR-018, ADR-041

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-025`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-049`

## Resultado

Outputprofile, cog canônico, preservação de resolução e validação da grade.

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

- Requisitos: REQ-ART-002, REQ-CRS-006, REQ-OUT-001, REQ-RAS-001, REQ-RAS-002
- Issue: `ISSUE-0044`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0261` / `ISSUE-0371` / `TASK-0261` — Definir contrato científico e invariantes: OutputProfile, COG canônico, preservação de resolução e validação da grade
- `STORY-0262` / `ISSUE-0372` / `TASK-0262` — Preparar corpus, fixtures e representação tipada: OutputProfile, COG canônico, preservação de resolução e validação da grade
- `STORY-0263` / `ISSUE-0373` / `TASK-0263` — Implementar o núcleo algorítmico: OutputProfile, COG canônico, preservação de resolução e validação da grade
- `STORY-0264` / `ISSUE-0374` / `TASK-0264` — Integrar ao ProcessingPlan e pipeline: OutputProfile, COG canônico, preservação de resolução e validação da grade
- `STORY-0265` / `ISSUE-0375` / `TASK-0265` — Produzir métricas, diagnóstico e lineage: OutputProfile, COG canônico, preservação de resolução e validação da grade
- `STORY-0266` / `ISSUE-0376` / `TASK-0266` — Executar benchmark, negativos e regressão científica: OutputProfile, COG canônico, preservação de resolução e validação da grade
- `STORY-0267` / `ISSUE-0377` / `TASK-0267` — Auditar evidência científica e final: OutputProfile, COG canônico, preservação de resolução e validação da grade

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-025`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-049`
- **Resultado:** `PASS`
