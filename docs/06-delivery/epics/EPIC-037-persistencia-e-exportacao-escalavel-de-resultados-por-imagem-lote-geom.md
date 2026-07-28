# EPIC-037 — persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums

- **Domínio:** `REP`
- **Bounded Context owner:** `BC-012 — Resultados, Diagnósticos e Exportação`
- **Sprint planejada:** `SPRINT-010`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0037`
- **Dependências:** EPIC-012, EPIC-026, EPIC-030, EPIC-063
- **Release gate:** `G3/G4/G7`
- **Referências arquiteturais:** ADR-018, ADR-046, ADR-039, ADR-048, ADR-041, ADR-050, ADR-053, ADR-026

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-016`, `ADR-025`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-048`, `ADR-050`, `ADR-053`

## Resultado

Persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G4/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-BEX-001, REQ-BEX-002, REQ-BEX-003, REQ-BEX-004, REQ-BEX-005, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010, REQ-EPIC-037, REQ-EPIC-070, REQ-GCP-002, REQ-MSK-002, REQ-PROV-001, REQ-QUAL-002, REQ-QUAL-003, REQ-RMR-001, REQ-RMR-003, REQ-SCL-002, REQ-SCM-003, REQ-SDR-004, REQ-SRP-003
- Issue: `ISSUE-0037`
- Sprint: `SPRINT-010`

## Histórias implementáveis


Este épico possui **8** histórias filhas:

- `STORY-0220` / `ISSUE-0330` / `TASK-0220` — Definir schemas, formatos e invariantes de resultado: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums
- `STORY-0221` / `ISSUE-0331` / `TASK-0221` — Consolidar slices e liberar integração: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums
- `STORY-0222` / `ISSUE-0332` / `TASK-0222` — Implementar geração e exportação: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums
- `STORY-0223` / `ISSUE-0333` / `TASK-0223` — Expor consulta, download e visualização: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums
- `STORY-0224` / `ISSUE-0334` / `TASK-0224` — Validar escala, reprodutibilidade e integridade: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums
- `STORY-0225` / `ISSUE-0335` / `TASK-0225` — Auditar lineage e evidência final: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums
- `STORY-0743` / `ISSUE-0853` / `TASK-0743` — Slice 1/2 — Implementar persistência e snapshots: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums [REQ-BEX, REQ-EPIC, REQ-MSK, REQ-RMR]
- `STORY-0744` / `ISSUE-0854` / `TASK-0744` — Slice 2/2 — Implementar persistência e snapshots: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums [REQ-SCL, REQ-SCM, REQ-SDR, REQ-SRP]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-016`, `ADR-025`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-048`, `ADR-050`, `ADR-053`
- **Resultado:** `PASS`
