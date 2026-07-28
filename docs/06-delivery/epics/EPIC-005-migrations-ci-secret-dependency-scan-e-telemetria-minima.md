# EPIC-005 — migrations, CI, secret/dependency scan e telemetria mínima

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0005`
- **Dependências:** EPIC-003
- **Release gate:** `G1/G5`
- **Referências arquiteturais:** ADR-034, ADR-046, ADR-039, ADR-047, ADR-054, ADR-053, ADR-026

- ADRs: `ADR-002`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-012`, `ADR-014`, `ADR-015`, `ADR-018`, `ADR-023`, `ADR-024`, `ADR-026`, `ADR-030`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-054`, `ADR-055`, `ADR-057`

## Resultado

Migrations, ci, secret/dependency scan e telemetria mínima.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G5` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AIE-001, REQ-AIE-002, REQ-AIE-003, REQ-AIE-004, REQ-AIE-005, REQ-AIE-006, REQ-AIE-007, REQ-AIE-008, REQ-AIE-009, REQ-AIE-010, REQ-BEX-001, REQ-BEX-002, REQ-BEX-003, REQ-BEX-004, REQ-BEX-005, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010, REQ-EPIC-012, REQ-EPIC-041, REQ-FRZ-002, REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-GOV-004, REQ-INS-003, REQ-ISS-007, REQ-OBS-002, REQ-SGVCAL-001, REQ-SGVCAL-002, REQ-SGVCAL-003, REQ-SGVCAL-004, REQ-SGVCAL-005, REQ-SGVCAL-006, REQ-SGVCAL-007, REQ-SGVCAL-008, REQ-SGVCAL-009, REQ-SGVCAL-010, REQ-SRG-002, REQ-SRP-002, REQ-SUP-001, REQ-TOOL-006, REQ-TOOL-007, REQ-TOOL-009, REQ-UPG-003
- Issue: `ISSUE-0005`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **11** histórias filhas:

- `STORY-0021` / `ISSUE-0131` / `TASK-0021` — Consolidar slices e liberar integração: migrations, CI, secret/dependency scan e telemetria mínima
- `STORY-0022` / `ISSUE-0132` / `TASK-0022` — Consolidar slices e liberar integração: migrations, CI, secret/dependency scan e telemetria mínima
- `STORY-0023` / `ISSUE-0133` / `TASK-0023` — Automatizar validações e controles: migrations, CI, secret/dependency scan e telemetria mínima
- `STORY-0024` / `ISSUE-0134` / `TASK-0024` — Integrar a capacidade ao fluxo do repositório: migrations, CI, secret/dependency scan e telemetria mínima
- `STORY-0025` / `ISSUE-0135` / `TASK-0025` — Validar evidência e realizar auditoria final: migrations, CI, secret/dependency scan e telemetria mínima
- `STORY-0706` / `ISSUE-0816` / `TASK-0706` — Slice 1/2 — Definir escopo, contratos e invariantes: migrations, CI, secret/dependency scan e telemetria mínima [REQ-AIE, REQ-BEX, REQ-EPIC, REQ-FS1, REQ-INS, REQ-ISS, REQ-OBS]
- `STORY-0707` / `ISSUE-0817` / `TASK-0707` — Slice 2/2 — Definir escopo, contratos e invariantes: migrations, CI, secret/dependency scan e telemetria mínima [REQ-SGVCAL]
- `STORY-0708` / `ISSUE-0818` / `TASK-0708` — Slice 1/4 — Materializar a fundação executável: migrations, CI, secret/dependency scan e telemetria mínima [REQ-AIE, REQ-BEX]
- `STORY-0709` / `ISSUE-0819` / `TASK-0709` — Slice 2/4 — Materializar a fundação executável: migrations, CI, secret/dependency scan e telemetria mínima [REQ-BEX, REQ-EPIC, REQ-FRZ, REQ-FS1]
- `STORY-0710` / `ISSUE-0820` / `TASK-0710` — Slice 3/4 — Materializar a fundação executável: migrations, CI, secret/dependency scan e telemetria mínima [REQ-FS1, REQ-GOV, REQ-SGVCAL]
- `STORY-0711` / `ISSUE-0821` / `TASK-0711` — Slice 4/4 — Materializar a fundação executável: migrations, CI, secret/dependency scan e telemetria mínima [REQ-SGVCAL, REQ-SRG, REQ-SRP, REQ-SUP, REQ-TOOL, REQ-UPG]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-012`, `ADR-014`, `ADR-015`, `ADR-018`, `ADR-023`, `ADR-024`, `ADR-026`, `ADR-030`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-054`, `ADR-055`, `ADR-057`
- **Resultado:** `PASS`
