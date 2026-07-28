# EPIC-012 — raízes de workspace, API de navegação segura, catálogo, hashes e lineage

- **Domínio:** `DAT`
- **Bounded Context owner:** `BC-003 — Projetos, Workspace e Assets`
- **Sprint planejada:** `SPRINT-002`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0012`
- **Dependências:** EPIC-005, EPIC-010
- **Release gate:** `G3`
- **Referências arquiteturais:** ADR-002, ADR-018, ADR-039, ADR-048, ADR-027, ADR-041, ADR-026

- ADRs: `ADR-001`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-025`, `ADR-026`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-040`, `ADR-041`, `ADR-043`, `ADR-045`, `ADR-055`

## Resultado

Raízes de workspace, api de navegação segura, catálogo, hashes e lineage.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-ART-001, REQ-ART-003, REQ-ARTLAYOUT-002, REQ-CAT-001, REQ-DBSCHEMA-001, REQ-DBSCHEMA-002, REQ-DBSCHEMA-003, REQ-DBSCHEMA-004, REQ-DBSCHEMA-005, REQ-DBSCHEMA-006, REQ-DBSCHEMA-007, REQ-DBSCHEMA-008, REQ-DBSCHEMA-009, REQ-FS-001, REQ-PRV-001, REQ-RUN-001, REQ-RUN-002, REQ-RUN-003, REQ-RUN-004, REQ-RUN-005, REQ-RUN-006, REQ-RUN-007, REQ-RUN-008, REQ-RUN-009, REQ-RUN-010, REQ-RUNTIME-005, REQ-SCM-002, REQ-TOOL-004, REQ-TOOL-005, REQ-UPG-002
- Issue: `ISSUE-0012`
- Sprint: `SPRINT-002`

## Histórias implementáveis


Este épico possui **9** histórias filhas:

- `STORY-0056` / `ISSUE-0166` / `TASK-0056` — Definir modelo, invariantes e contratos de dados: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0057` / `ISSUE-0167` / `TASK-0057` — Consolidar slices e liberar integração: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0058` / `ISSUE-0168` / `TASK-0058` — Implementar armazenamento e lifecycle: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0059` / `ISSUE-0169` / `TASK-0059` — Expor serviços e integrar consumers: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0060` / `ISSUE-0170` / `TASK-0060` — Validar segurança, recuperação e concorrência: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0061` / `ISSUE-0171` / `TASK-0061` — Executar QA e auditoria final: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0718` / `ISSUE-0828` / `TASK-0718` — Slice 1/3 — Implementar persistência e migrations: raízes de workspace, API de navegação segura, catálogo, hashes e lineage [REQ-ART, REQ-ARTLAYOUT, REQ-CAT, REQ-DBSCHEMA, REQ-FS]
- `STORY-0719` / `ISSUE-0829` / `TASK-0719` — Slice 2/3 — Implementar persistência e migrations: raízes de workspace, API de navegação segura, catálogo, hashes e lineage [REQ-PRV, REQ-RUN, REQ-SCM, REQ-TOOL]
- `STORY-0720` / `ISSUE-0830` / `TASK-0720` — Slice 3/3 — Implementar persistência e migrations: raízes de workspace, API de navegação segura, catálogo, hashes e lineage [REQ-UPG]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-001`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-025`, `ADR-026`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-040`, `ADR-041`, `ADR-043`, `ADR-045`, `ADR-055`
- **Resultado:** `PASS`
