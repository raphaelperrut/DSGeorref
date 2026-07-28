# EPIC-034 — painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos

- **Domínio:** `WEB`
- **Bounded Context owner:** `BC-016 — Experiência e Orientação do Operador`
- **Sprint planejada:** `SPRINT-009`
- **Papel responsável pela implementação:** `Frontend`
- **Issue principal:** `ISSUE-0034`
- **Dependências:** EPIC-018, EPIC-030, EPIC-032, EPIC-057, EPIC-069
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-046, ADR-039, ADR-048

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-025`, `ADR-030`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-053`

## Resultado

Painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-BAT-001, REQ-BEX-001, REQ-BEX-002, REQ-BEX-003, REQ-BEX-004, REQ-BEX-005, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010, REQ-CAT-001, REQ-EPIC-035, REQ-EPIC-037, REQ-EPIC-062, REQ-EPIC-070, REQ-QUAL-003, REQ-QUAL-005, REQ-SCL-002, REQ-SMO-002, REQ-SMO-004
- Issue: `ISSUE-0034`
- Sprint: `SPRINT-009`

## Histórias implementáveis


Este épico possui **8** histórias filhas:

- `STORY-0203` / `ISSUE-0313` / `TASK-0203` — Definir jornada, estados e acessibilidade: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0204` / `ISSUE-0314` / `TASK-0204` — Consolidar slices e liberar integração: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0205` / `ISSUE-0315` / `TASK-0205` — Implementar componentes e interação: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0206` / `ISSUE-0316` / `TASK-0206` — Integrar mapa, fluxo e estados de erro: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0207` / `ISSUE-0317` / `TASK-0207` — Executar testes de componente, acessibilidade e E2E: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0208` / `ISSUE-0318` / `TASK-0208` — Auditar UX, contrato e evidência final: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0741` / `ISSUE-0851` / `TASK-0741` — Slice 1/2 — Integrar contratos e cliente tipado: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos [REQ-BAT, REQ-BEX]
- `STORY-0742` / `ISSUE-0852` / `TASK-0742` — Slice 2/2 — Integrar contratos e cliente tipado: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos [REQ-EPIC, REQ-QUAL, REQ-SCL, REQ-SMO]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-025`, `ADR-030`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-053`
- **Resultado:** `PASS`
