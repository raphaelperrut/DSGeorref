# EPIC-080 — lockfiles, pins por digest/SHA, scanners, SBOM, assinatura OCI, attestations e verificador de release

- **Domínio:** `SEC`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `Security`
- **Issue principal:** `ISSUE-0080`
- **Dependências:** EPIC-002, EPIC-005
- **Release gate:** `G5/G6/G7`
- **Referências arquiteturais:** ADR-051, ADR-034, ADR-054

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-024`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-052`

## Resultado

Lockfiles, pins por digest/sha, scanners, sbom, assinatura oci, attestations e verificador de release.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G5/G6/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AI-006, REQ-AI-015, REQ-EPIC-042, REQ-INS-004, REQ-SUP-001
- Issue: `ISSUE-0080`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0499` / `ISSUE-0609` / `TASK-0499` — Modelar ameaças e requisitos de controle: lockfiles, pins por digest/SHA, scanners, SBOM, assinatura OCI, attestations e verificador de release
- `STORY-0500` / `ISSUE-0610` / `TASK-0500` — Definir políticas e contratos fail-closed: lockfiles, pins por digest/SHA, scanners, SBOM, assinatura OCI, attestations e verificador de release
- `STORY-0501` / `ISSUE-0611` / `TASK-0501` — Implementar controles e enforcement: lockfiles, pins por digest/SHA, scanners, SBOM, assinatura OCI, attestations e verificador de release
- `STORY-0502` / `ISSUE-0612` / `TASK-0502` — Executar testes negativos e ofensivos: lockfiles, pins por digest/SHA, scanners, SBOM, assinatura OCI, attestations e verificador de release
- `STORY-0503` / `ISSUE-0613` / `TASK-0503` — Instrumentar detecção, resposta e runbook: lockfiles, pins por digest/SHA, scanners, SBOM, assinatura OCI, attestations e verificador de release
- `STORY-0504` / `ISSUE-0614` / `TASK-0504` — Auditar evidência de segurança final: lockfiles, pins por digest/SHA, scanners, SBOM, assinatura OCI, attestations e verificador de release

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-024`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-052`
- **Resultado:** `PASS`
