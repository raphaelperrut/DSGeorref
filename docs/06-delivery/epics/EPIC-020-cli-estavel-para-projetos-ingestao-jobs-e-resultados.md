# EPIC-020 — CLI estável para projetos, ingestão, jobs e resultados

- **Domínio:** `CLI`
- **Bounded Context owner:** `BC-016 — Experiência e Orientação do Operador`
- **Sprint planejada:** `SPRINT-003`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0020`
- **Dependências:** EPIC-012, EPIC-015
- **Release gate:** `G1`
- **Referências arquiteturais:** ADR-002, ADR-018, ADR-036

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-016`, `ADR-023`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-055`

## Resultado

Cli estável para projetos, ingestão, jobs e resultados.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010
- Issue: `ISSUE-0020`
- Sprint: `SPRINT-003`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0110` / `ISSUE-0220` / `TASK-0110` — Definir comandos, opções e códigos de saída: CLI estável para projetos, ingestão, jobs e resultados
- `STORY-0111` / `ISSUE-0221` / `TASK-0111` — Implementar adapter CLI sobre o núcleo: CLI estável para projetos, ingestão, jobs e resultados
- `STORY-0112` / `ISSUE-0222` / `TASK-0112` — Implementar feedback, erros e ajuda: CLI estável para projetos, ingestão, jobs e resultados
- `STORY-0113` / `ISSUE-0223` / `TASK-0113` — Executar testes de contrato e integração: CLI estável para projetos, ingestão, jobs e resultados
- `STORY-0114` / `ISSUE-0224` / `TASK-0114` — Auditar compatibilidade e evidência final: CLI estável para projetos, ingestão, jobs e resultados

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-016`, `ADR-023`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-055`
- **Resultado:** `PASS`
