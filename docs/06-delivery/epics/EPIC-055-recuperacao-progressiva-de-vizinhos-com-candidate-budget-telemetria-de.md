# EPIC-055 — recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0055`
- **Dependências:** EPIC-019, EPIC-047, EPIC-050, EPIC-054
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-044, ADR-049

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`

## Resultado

Recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-DIS-002, REQ-MOS-002
- Issue: `ISSUE-0055`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0337` / `ISSUE-0447` / `TASK-0337` — Definir contrato científico e invariantes: recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito
- `STORY-0338` / `ISSUE-0448` / `TASK-0338` — Preparar corpus, fixtures e representação tipada: recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito
- `STORY-0339` / `ISSUE-0449` / `TASK-0339` — Implementar o núcleo algorítmico: recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito
- `STORY-0340` / `ISSUE-0450` / `TASK-0340` — Integrar ao ProcessingPlan e pipeline: recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito
- `STORY-0341` / `ISSUE-0451` / `TASK-0341` — Produzir métricas, diagnóstico e lineage: recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito
- `STORY-0342` / `ISSUE-0452` / `TASK-0342` — Executar benchmark, negativos e regressão científica: recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito
- `STORY-0343` / `ISSUE-0453` / `TASK-0343` — Auditar evidência científica e final: recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`
- **Resultado:** `PASS`
