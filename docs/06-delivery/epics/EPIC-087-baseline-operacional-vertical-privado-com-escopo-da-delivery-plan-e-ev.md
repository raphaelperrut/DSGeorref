# EPIC-087 — baseline operacional vertical privado com escopo da DELIVERY_PLAN e evidências do corpus controlado

- **Domínio:** `REL`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0087`
- **Dependências:** EPIC-012, EPIC-018, EPIC-024, EPIC-034, EPIC-037, EPIC-044, EPIC-086
- **Release gate:** `G1/G3/G4/G7`
- **Referências arquiteturais:** ADR-002, ADR-018, ADR-036, ADR-046, ADR-044, ADR-054, ADR-053

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-057`

## Resultado

Baseline operacional vertical privado com escopo da delivery_plan e evidências do corpus controlado.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G3/G4/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-DEL-002
- Issue: `ISSUE-0087`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0539` / `ISSUE-0649` / `TASK-0539` — Definir gate, versão e critérios de release: baseline operacional vertical privado com escopo da DELIVERY_PLAN e evidências do corpus controlado
- `STORY-0540` / `ISSUE-0650` / `TASK-0540` — Implementar pipeline e artifacts de release: baseline operacional vertical privado com escopo da DELIVERY_PLAN e evidências do corpus controlado
- `STORY-0541` / `ISSUE-0651` / `TASK-0541` — Implementar upgrade, rollback e compatibilidade: baseline operacional vertical privado com escopo da DELIVERY_PLAN e evidências do corpus controlado
- `STORY-0542` / `ISSUE-0652` / `TASK-0542` — Gerar evidências, SBOM e attestations: baseline operacional vertical privado com escopo da DELIVERY_PLAN e evidências do corpus controlado
- `STORY-0543` / `ISSUE-0653` / `TASK-0543` — Executar instalação limpa e rehearsal: baseline operacional vertical privado com escopo da DELIVERY_PLAN e evidências do corpus controlado
- `STORY-0544` / `ISSUE-0654` / `TASK-0544` — Auditar release candidata final: baseline operacional vertical privado com escopo da DELIVERY_PLAN e evidências do corpus controlado

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-057`
- **Resultado:** `PASS`
