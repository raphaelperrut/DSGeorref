# EPIC-049 — lineage normalizado, manifestos e bundle de reprodução sob demanda

- **Domínio:** `DAT`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Sprint planejada:** `SPRINT-010`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0049`
- **Dependências:** EPIC-004, EPIC-012, EPIC-046, EPIC-062, EPIC-063, EPIC-066
- **Release gate:** `G3/G6`
- **Referências arquiteturais:** ADR-051, ADR-018, ADR-036, ADR-047, ADR-048, ADR-027, ADR-050, ADR-053

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-018`, `ADR-025`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-038`, `ADR-047`, `ADR-048`, `ADR-052`, `ADR-053`

## Resultado

Lineage normalizado, manifestos e bundle de reprodução sob demanda.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G6` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AI-009, REQ-BKP-001, REQ-CAC-001, REQ-EPIC-017, REQ-EPIC-070, REQ-PROV-001, REQ-RET-001, REQ-REV-003, REQ-RMQ-002, REQ-SDR-004, REQ-SRG-004
- Issue: `ISSUE-0049`
- Sprint: `SPRINT-010`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0296` / `ISSUE-0406` / `TASK-0296` — Definir modelo, invariantes e contratos de dados: lineage normalizado, manifestos e bundle de reprodução sob demanda
- `STORY-0297` / `ISSUE-0407` / `TASK-0297` — Implementar persistência e migrations: lineage normalizado, manifestos e bundle de reprodução sob demanda
- `STORY-0298` / `ISSUE-0408` / `TASK-0298` — Implementar armazenamento e lifecycle: lineage normalizado, manifestos e bundle de reprodução sob demanda
- `STORY-0299` / `ISSUE-0409` / `TASK-0299` — Expor serviços e integrar consumers: lineage normalizado, manifestos e bundle de reprodução sob demanda
- `STORY-0300` / `ISSUE-0410` / `TASK-0300` — Validar segurança, recuperação e concorrência: lineage normalizado, manifestos e bundle de reprodução sob demanda
- `STORY-0301` / `ISSUE-0411` / `TASK-0301` — Executar QA e auditoria final: lineage normalizado, manifestos e bundle de reprodução sob demanda

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-018`, `ADR-025`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-038`, `ADR-047`, `ADR-048`, `ADR-052`, `ADR-053`
- **Resultado:** `PASS`
