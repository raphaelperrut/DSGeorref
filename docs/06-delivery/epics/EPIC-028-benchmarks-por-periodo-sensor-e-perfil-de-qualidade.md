# EPIC-028 — benchmarks por período, sensor e perfil de qualidade

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-007 — Verificação Geométrica e Qualidade`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0028`
- **Dependências:** EPIC-024
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-046, ADR-047, ADR-053

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-018`, `ADR-025`, `ADR-030`, `ADR-038`, `ADR-039`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`

## Resultado

Benchmarks por período, sensor e perfil de qualidade.

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

- Requisitos: REQ-AI-012, REQ-AIE-001, REQ-AIE-002, REQ-AIE-003, REQ-AIE-004, REQ-AIE-005, REQ-AIE-006, REQ-AIE-007, REQ-AIE-008, REQ-AIE-009, REQ-AIE-010, REQ-CLASSICPROFILE-001, REQ-CLASSICPROFILE-002, REQ-CLASSICPROFILE-003, REQ-CLASSICPROFILE-004, REQ-CLASSICPROFILE-005, REQ-CLASSICPROFILE-006, REQ-CLASSICPROFILE-007, REQ-CLASSICPROFILE-008, REQ-CLASSICPROFILE-009, REQ-CLASSICPROFILE-010, REQ-SCP-001, REQ-SDR-001, REQ-SDR-002, REQ-SDR-003, REQ-SDR-004, REQ-SGVCAL-001, REQ-SGVCAL-002, REQ-SGVCAL-003, REQ-SGVCAL-004, REQ-SGVCAL-005, REQ-SGVCAL-006, REQ-SGVCAL-007, REQ-SGVCAL-008, REQ-SGVCAL-009, REQ-SGVCAL-010, REQ-SRG-001, REQ-SRG-002, REQ-SRG-003, REQ-SRG-004, REQ-TOOL-007, REQ-TST-001
- Issue: `ISSUE-0028`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **10** histórias filhas:

- `STORY-0164` / `ISSUE-0274` / `TASK-0164` — Definir contrato científico e invariantes: benchmarks por período, sensor e perfil de qualidade
- `STORY-0165` / `ISSUE-0275` / `TASK-0165` — Consolidar slices e liberar integração: benchmarks por período, sensor e perfil de qualidade
- `STORY-0166` / `ISSUE-0276` / `TASK-0166` — Implementar o núcleo algorítmico: benchmarks por período, sensor e perfil de qualidade
- `STORY-0167` / `ISSUE-0277` / `TASK-0167` — Integrar ao ProcessingPlan e pipeline: benchmarks por período, sensor e perfil de qualidade
- `STORY-0168` / `ISSUE-0278` / `TASK-0168` — Produzir métricas, diagnóstico e lineage: benchmarks por período, sensor e perfil de qualidade
- `STORY-0169` / `ISSUE-0279` / `TASK-0169` — Executar benchmark, negativos e regressão científica: benchmarks por período, sensor e perfil de qualidade
- `STORY-0170` / `ISSUE-0280` / `TASK-0170` — Auditar evidência científica e final: benchmarks por período, sensor e perfil de qualidade
- `STORY-0735` / `ISSUE-0845` / `TASK-0735` — Slice 1/3 — Preparar corpus, fixtures e representação tipada: benchmarks por período, sensor e perfil de qualidade [REQ-AI, REQ-AIE, REQ-CLASSICPROFILE]
- `STORY-0736` / `ISSUE-0846` / `TASK-0736` — Slice 2/3 — Preparar corpus, fixtures e representação tipada: benchmarks por período, sensor e perfil de qualidade [REQ-CLASSICPROFILE, REQ-SCP, REQ-SDR, REQ-SGVCAL]
- `STORY-0737` / `ISSUE-0847` / `TASK-0737` — Slice 3/3 — Preparar corpus, fixtures e representação tipada: benchmarks por período, sensor e perfil de qualidade [REQ-SGVCAL, REQ-SRG, REQ-TOOL, REQ-TST]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-018`, `ADR-025`, `ADR-030`, `ADR-038`, `ADR-039`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`
- **Resultado:** `PASS`
