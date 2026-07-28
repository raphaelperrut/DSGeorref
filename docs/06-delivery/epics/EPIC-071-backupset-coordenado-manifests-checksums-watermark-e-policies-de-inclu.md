# EPIC-071 — BackupSet coordenado, manifests, checksums, watermark e policies de inclusão

- **Domínio:** `DAT`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0071`
- **Dependências:** EPIC-012, EPIC-049
- **Release gate:** `G3/G7`
- **Referências arquiteturais:** ADR-027, ADR-026

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-018`, `ADR-025`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-035`

## Resultado

Backupset coordenado, manifests, checksums, watermark e policies de inclusão.

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

- Requisitos: REQ-BKP-001, REQ-BKP-002, REQ-SCM-004, REQ-UPG-001
- Issue: `ISSUE-0071`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0445` / `ISSUE-0555` / `TASK-0445` — Definir modelo, invariantes e contratos de dados: BackupSet coordenado, manifests, checksums, watermark e policies de inclusão
- `STORY-0446` / `ISSUE-0556` / `TASK-0446` — Implementar persistência e migrations: BackupSet coordenado, manifests, checksums, watermark e policies de inclusão
- `STORY-0447` / `ISSUE-0557` / `TASK-0447` — Implementar armazenamento e lifecycle: BackupSet coordenado, manifests, checksums, watermark e policies de inclusão
- `STORY-0448` / `ISSUE-0558` / `TASK-0448` — Expor serviços e integrar consumers: BackupSet coordenado, manifests, checksums, watermark e policies de inclusão
- `STORY-0449` / `ISSUE-0559` / `TASK-0449` — Validar segurança, recuperação e concorrência: BackupSet coordenado, manifests, checksums, watermark e policies de inclusão
- `STORY-0450` / `ISSUE-0560` / `TASK-0450` — Executar QA e auditoria final: BackupSet coordenado, manifests, checksums, watermark e policies de inclusão

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-018`, `ADR-025`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-035`
- **Resultado:** `PASS`
