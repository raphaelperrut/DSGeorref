# EPIC-036 — central Aprender, exemplos visuais, projeto demonstrativo e ajuda contextual, incluindo Strong Geometric Verifier e interpretação de falhas

- **Domínio:** `EDU`
- **Bounded Context owner:** `BC-016 — Experiência e Orientação do Operador`
- **Sprint planejada:** `SPRINT-009`
- **Papel responsável pela implementação:** `Product Owner`
- **Issue principal:** `ISSUE-0036`
- **Dependências:** EPIC-030, EPIC-031, EPIC-033
- **Release gate:** `G7`
- **Referências arquiteturais:** ADR-051, ADR-046

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-014`

## Resultado

Central aprender, exemplos visuais, projeto demonstrativo e ajuda contextual, incluindo strong geometric verifier e interpretação de falhas.

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

- Requisitos: REQ-AI-016, REQ-EPIC-038, REQ-UX-003
- Issue: `ISSUE-0036`
- Sprint: `SPRINT-009`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0215` / `ISSUE-0325` / `TASK-0215` — Definir conteúdo, exemplos e objetivos de aprendizagem: central Aprender, exemplos visuais, projeto demonstrativo e ajuda contextual, incluindo Strong Geometric Verifier e interpretação de falhas
- `STORY-0216` / `ISSUE-0326` / `TASK-0216` — Implementar estrutura e navegação de aprendizagem: central Aprender, exemplos visuais, projeto demonstrativo e ajuda contextual, incluindo Strong Geometric Verifier e interpretação de falhas
- `STORY-0217` / `ISSUE-0327` / `TASK-0217` — Criar exemplos visuais e projeto demonstrativo: central Aprender, exemplos visuais, projeto demonstrativo e ajuda contextual, incluindo Strong Geometric Verifier e interpretação de falhas
- `STORY-0218` / `ISSUE-0328` / `TASK-0218` — Validar acessibilidade, clareza e consistência técnica: central Aprender, exemplos visuais, projeto demonstrativo e ajuda contextual, incluindo Strong Geometric Verifier e interpretação de falhas
- `STORY-0219` / `ISSUE-0329` / `TASK-0219` — Auditar conteúdo e evidência final: central Aprender, exemplos visuais, projeto demonstrativo e ajuda contextual, incluindo Strong Geometric Verifier e interpretação de falhas

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-014`
- **Resultado:** `PASS`
