# EPIC-038 — métricas, heatmap amostrado e diagnóstico denso do Image Deformation Profile

- **Domínio:** `REP`
- **Bounded Context owner:** `BC-007 — Verificação Geométrica e Qualidade`
- **Sprint planejada:** `SPRINT-010`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0038`
- **Dependências:** EPIC-024, EPIC-037
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-046

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-046`

## Resultado

Métricas, heatmap amostrado e diagnóstico denso do image deformation profile.

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

- Requisitos: REQ-QUAL-005
- Issue: `ISSUE-0038`
- Sprint: `SPRINT-010`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0226` / `ISSUE-0336` / `TASK-0226` — Definir schemas, formatos e invariantes de resultado: métricas, heatmap amostrado e diagnóstico denso do Image Deformation Profile
- `STORY-0227` / `ISSUE-0337` / `TASK-0227` — Implementar persistência e snapshots: métricas, heatmap amostrado e diagnóstico denso do Image Deformation Profile
- `STORY-0228` / `ISSUE-0338` / `TASK-0228` — Implementar geração e exportação: métricas, heatmap amostrado e diagnóstico denso do Image Deformation Profile
- `STORY-0229` / `ISSUE-0339` / `TASK-0229` — Expor consulta, download e visualização: métricas, heatmap amostrado e diagnóstico denso do Image Deformation Profile
- `STORY-0230` / `ISSUE-0340` / `TASK-0230` — Validar escala, reprodutibilidade e integridade: métricas, heatmap amostrado e diagnóstico denso do Image Deformation Profile
- `STORY-0231` / `ISSUE-0341` / `TASK-0231` — Auditar lineage e evidência final: métricas, heatmap amostrado e diagnóstico denso do Image Deformation Profile

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-046`
- **Resultado:** `PASS`
