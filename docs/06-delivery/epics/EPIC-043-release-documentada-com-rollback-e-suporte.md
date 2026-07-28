# EPIC-043 — release documentada com rollback e suporte

- **Domínio:** `REL`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0043`
- **Dependências:** Nenhuma
- **Release gate:** `G7`
- **Referências arquiteturais:** ADR-053

- ADRs: `ADR-001`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-053`

## Resultado

Release documentada com rollback e suporte.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-SRG-003, REQ-SRG-004, REQ-TOOL-008, REQ-TOOL-010
- Issue: `ISSUE-0043`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0255` / `ISSUE-0365` / `TASK-0255` — Definir gate, versão e critérios de release: release documentada com rollback e suporte
- `STORY-0256` / `ISSUE-0366` / `TASK-0256` — Implementar pipeline e artifacts de release: release documentada com rollback e suporte
- `STORY-0257` / `ISSUE-0367` / `TASK-0257` — Implementar upgrade, rollback e compatibilidade: release documentada com rollback e suporte
- `STORY-0258` / `ISSUE-0368` / `TASK-0258` — Gerar evidências, SBOM e attestations: release documentada com rollback e suporte
- `STORY-0259` / `ISSUE-0369` / `TASK-0259` — Executar instalação limpa e rehearsal: release documentada com rollback e suporte
- `STORY-0260` / `ISSUE-0370` / `TASK-0260` — Auditar release candidata final: release documentada com rollback e suporte

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-001`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-053`
- **Resultado:** `PASS`
