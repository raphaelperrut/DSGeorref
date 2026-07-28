# EPIC-013 — backup/restore consistente entre banco e arquivos

- **Domínio:** `DAT`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Sprint planejada:** `SPRINT-002`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0013`
- **Dependências:** EPIC-012
- **Release gate:** `G3/G7`
- **Referências arquiteturais:** ADR-018, ADR-027, ADR-026

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-026`, `ADR-027`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-055`

## Resultado

Backup/restore consistente entre banco e arquivos.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-DBSCHEMA-001, REQ-DBSCHEMA-010, REQ-EPIC-039, REQ-PRV-001, REQ-RUNTIME-005, REQ-TOOL-004
- Issue: `ISSUE-0013`
- Sprint: `SPRINT-002`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0062` / `ISSUE-0172` / `TASK-0062` — Definir modelo, invariantes e contratos de dados: backup/restore consistente entre banco e arquivos
- `STORY-0063` / `ISSUE-0173` / `TASK-0063` — Implementar persistência e migrations: backup/restore consistente entre banco e arquivos
- `STORY-0064` / `ISSUE-0174` / `TASK-0064` — Implementar armazenamento e lifecycle: backup/restore consistente entre banco e arquivos
- `STORY-0065` / `ISSUE-0175` / `TASK-0065` — Expor serviços e integrar consumers: backup/restore consistente entre banco e arquivos
- `STORY-0066` / `ISSUE-0176` / `TASK-0066` — Validar segurança, recuperação e concorrência: backup/restore consistente entre banco e arquivos
- `STORY-0067` / `ISSUE-0177` / `TASK-0067` — Executar QA e auditoria final: backup/restore consistente entre banco e arquivos

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-026`, `ADR-027`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-055`
- **Resultado:** `PASS`
