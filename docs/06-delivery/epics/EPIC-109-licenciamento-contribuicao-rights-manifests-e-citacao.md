# EPIC-109 — Licenciamento, contribuição, rights manifests e citação

- **Domínio:** `PUB`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `Reviewer`
- **Issue principal:** `ISSUE-0109`
- **Dependências:** Nenhuma
- **Release gate:** `G0/G5/G6`
- **Referências arquiteturais:** ADR-034, ADR-047, ADR-054

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`

## Resultado

Licenciamento, contribuição, rights manifests e citação.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G0/G5/G6` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-CIT-001, REQ-EPIC-042, REQ-OSS-001, REQ-PUB-002, REQ-PUB-003, REQ-PUB-004
- Issue: `ISSUE-0109`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0678` / `ISSUE-0788` / `TASK-0678` — Definir critérios jurídicos e de publicação: Licenciamento, contribuição, rights manifests e citação
- `STORY-0679` / `ISSUE-0789` / `TASK-0679` — Materializar notices, citação e manifests: Licenciamento, contribuição, rights manifests e citação
- `STORY-0680` / `ISSUE-0790` / `TASK-0680` — Automatizar verificações de publicação: Licenciamento, contribuição, rights manifests e citação
- `STORY-0681` / `ISSUE-0791` / `TASK-0681` — Executar sanitização e revisão de segurança: Licenciamento, contribuição, rights manifests e citação
- `STORY-0682` / `ISSUE-0792` / `TASK-0682` — Registrar aprovação e evidência final: Licenciamento, contribuição, rights manifests e citação

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`
- **Resultado:** `PASS`
