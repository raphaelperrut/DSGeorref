# EPIC-004 — OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0004`
- **Dependências:** EPIC-003
- **Release gate:** `G1`
- **Referências arquiteturais:** ADR-051, ADR-002, ADR-018, ADR-034, ADR-044, ADR-041, ADR-026

- ADRs: `ADR-001`, `ADR-002`, `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-017`, `ADR-019`, `ADR-021`, `ADR-023`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-040`, `ADR-041`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-053`, `ADR-055`

## Resultado

Openapi, cliente typescript e contratos cli/jobs/eventos/artefatos/processingplan/qualityreport/failurediagnostic versionados.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-ARTLAYOUT-010, REQ-CRS-002, REQ-DBSCHEMA-002, REQ-DBSCHEMA-004, REQ-DBSCHEMA-007, REQ-DBSCHEMA-008, REQ-EPIC-031, REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-RUN-001, REQ-RUN-002, REQ-RUN-003, REQ-RUN-004, REQ-RUN-005, REQ-RUN-006, REQ-RUN-007, REQ-RUN-008, REQ-RUN-009, REQ-RUN-010, REQ-RUNTIME-001, REQ-RUNTIME-002, REQ-RUNTIME-003, REQ-RUNTIME-004, REQ-RUNTIME-006, REQ-RUNTIME-007, REQ-RUNTIME-008, REQ-SCM-001, REQ-TOOL-003, REQ-TOOL-005, REQ-TOP-001, REQ-UPG-005, REQ-UX-002
- Issue: `ISSUE-0004`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **10** histórias filhas:

- `STORY-0016` / `ISSUE-0126` / `TASK-0016` — Consolidar slices e liberar integração: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0017` / `ISSUE-0127` / `TASK-0017` — Consolidar slices e liberar integração: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0018` / `ISSUE-0128` / `TASK-0018` — Automatizar validações e controles: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0019` / `ISSUE-0129` / `TASK-0019` — Integrar a capacidade ao fluxo do repositório: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0020` / `ISSUE-0130` / `TASK-0020` — Validar evidência e realizar auditoria final: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0701` / `ISSUE-0811` / `TASK-0701` — Slice 1/2 — Definir escopo, contratos e invariantes: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-CRS, REQ-DBSCHEMA, REQ-EPIC, REQ-FS1, REQ-RUN]
- `STORY-0702` / `ISSUE-0812` / `TASK-0702` — Slice 2/2 — Definir escopo, contratos e invariantes: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-RUNTIME, REQ-SCM, REQ-TOOL, REQ-TOP, REQ-UX]
- `STORY-0703` / `ISSUE-0813` / `TASK-0703` — Slice 1/3 — Materializar a fundação executável: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-ARTLAYOUT, REQ-DBSCHEMA, REQ-FS1]
- `STORY-0704` / `ISSUE-0814` / `TASK-0704` — Slice 2/3 — Materializar a fundação executável: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-RUN, REQ-RUNTIME]
- `STORY-0705` / `ISSUE-0815` / `TASK-0705` — Slice 3/3 — Materializar a fundação executável: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-RUNTIME, REQ-TOOL, REQ-UPG]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-001`, `ADR-002`, `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-017`, `ADR-019`, `ADR-021`, `ADR-023`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-040`, `ADR-041`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
