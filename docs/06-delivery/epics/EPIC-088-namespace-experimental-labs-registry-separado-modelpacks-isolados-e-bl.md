# EPIC-088 — namespace experimental/labs, registry separado, ModelPacks isolados e bloqueio técnico de ArtifactSet aceito

- **Domínio:** `LAB`
- **Bounded Context owner:** `BC-009 — Recuperação Assistida por IA e Governança de Modelos`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `IA`
- **Issue principal:** `ISSUE-0088`
- **Dependências:** EPIC-046, EPIC-050, EPIC-080
- **Release gate:** `G4/G5`
- **Referências arquiteturais:** ADR-051, ADR-046, ADR-053

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-051`, `ADR-052`, `ADR-053`

## Resultado

Namespace experimental/labs, registry separado, modelpacks isolados e bloqueio técnico de artifactset aceito.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4/G5` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-EPIC-088
- Issue: `ISSUE-0088`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **4** histórias filhas:

- `STORY-0545` / `ISSUE-0655` / `TASK-0545` — Definir hipótese, isolamento e critérios de promoção: namespace experimental/labs, registry separado, ModelPacks isolados e bloqueio técnico de ArtifactSet aceito
- `STORY-0546` / `ISSUE-0656` / `TASK-0546` — Implementar experimento isolado: namespace experimental/labs, registry separado, ModelPacks isolados e bloqueio técnico de ArtifactSet aceito
- `STORY-0547` / `ISSUE-0657` / `TASK-0547` — Executar avaliação e comparação: namespace experimental/labs, registry separado, ModelPacks isolados e bloqueio técnico de ArtifactSet aceito
- `STORY-0548` / `ISSUE-0658` / `TASK-0548` — Auditar conclusão, bloqueios e evidência: namespace experimental/labs, registry separado, ModelPacks isolados e bloqueio técnico de ArtifactSet aceito

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-009` — Recuperação Assistida por IA e Governança de Modelos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-051`, `ADR-052`, `ADR-053`
- **Resultado:** `PASS`
