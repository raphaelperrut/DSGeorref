# EPIC-051 — estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0051`
- **Dependências:** EPIC-021, EPIC-023, EPIC-025
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-044

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-045`

## Resultado

Estimadores usac_magsac/ransac explícitos, calibração, proveniência e testes de compatibilidade.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-EST-001
- Issue: `ISSUE-0051`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0309` / `ISSUE-0419` / `TASK-0309` — Definir contrato científico e invariantes: estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade
- `STORY-0310` / `ISSUE-0420` / `TASK-0310` — Preparar corpus, fixtures e representação tipada: estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade
- `STORY-0311` / `ISSUE-0421` / `TASK-0311` — Implementar o núcleo algorítmico: estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade
- `STORY-0312` / `ISSUE-0422` / `TASK-0312` — Integrar ao ProcessingPlan e pipeline: estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade
- `STORY-0313` / `ISSUE-0423` / `TASK-0313` — Produzir métricas, diagnóstico e lineage: estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade
- `STORY-0314` / `ISSUE-0424` / `TASK-0314` — Executar benchmark, negativos e regressão científica: estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade
- `STORY-0315` / `ISSUE-0425` / `TASK-0315` — Auditar evidência científica e final: estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-045`
- **Resultado:** `PASS`
