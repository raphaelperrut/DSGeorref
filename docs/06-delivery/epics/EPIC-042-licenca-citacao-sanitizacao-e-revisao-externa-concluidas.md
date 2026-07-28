# EPIC-042 — licença, citação, sanitização e revisão externa concluídas

- **Domínio:** `PUB`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `Reviewer`
- **Issue principal:** `ISSUE-0042`
- **Dependências:** Nenhuma
- **Release gate:** `G6`
- **Referências arquiteturais:** ADR-034, ADR-047, ADR-054

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-056`

## Resultado

Licença, citação, sanitização e revisão externa concluídas.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G6` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-CIT-001, REQ-EPIC-042, REQ-EPIC-043, REQ-OSS-001, REQ-PUB-004
- Issue: `ISSUE-0042`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0250` / `ISSUE-0360` / `TASK-0250` — Definir critérios jurídicos e de publicação: licença, citação, sanitização e revisão externa concluídas
- `STORY-0251` / `ISSUE-0361` / `TASK-0251` — Materializar notices, citação e manifests: licença, citação, sanitização e revisão externa concluídas
- `STORY-0252` / `ISSUE-0362` / `TASK-0252` — Automatizar verificações de publicação: licença, citação, sanitização e revisão externa concluídas
- `STORY-0253` / `ISSUE-0363` / `TASK-0253` — Executar sanitização e revisão de segurança: licença, citação, sanitização e revisão externa concluídas
- `STORY-0254` / `ISSUE-0364` / `TASK-0254` — Registrar aprovação e evidência final: licença, citação, sanitização e revisão externa concluídas

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-056`
- **Resultado:** `PASS`
