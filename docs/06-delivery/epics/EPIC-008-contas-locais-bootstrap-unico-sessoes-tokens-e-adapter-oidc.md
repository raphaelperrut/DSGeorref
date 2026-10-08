# EPIC-008 — contas locais, bootstrap único, sessões, tokens e adapter OIDC

- **Domínio:** `PLT`
- **Bounded Context owner:** `BC-002 — Identidade e Controle de Acesso`
- **Sprint planejada:** `SPRINT-002`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0008`
- **Dependências:** EPIC-004
- **Release gate:** `G2`
- **Referências arquiteturais:** ADR-018, ADR-028, ADR-034

- ADRs: `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-034`, `ADR-043`, `ADR-055`

## Resultado

Contas locais, bootstrap único, sessões, tokens e adapter oidc.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G2` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AUTH-IMPL-001, REQ-AUTH-IMPL-002, REQ-AUTH-IMPL-003, REQ-AUTH-IMPL-004, REQ-AUTH-IMPL-005, REQ-AUTH-IMPL-006, REQ-AUTH-IMPL-007, REQ-AUTH-IMPL-008, REQ-AUTH-IMPL-009, REQ-AUTH-IMPL-010, REQ-DBSCHEMA-003, REQ-EPIC-076, REQ-ID-001, REQ-ID-002, REQ-INS-002
- Issue: `ISSUE-0008`
- Sprint: `SPRINT-002`

## Histórias implementáveis


Este épico possui **10** histórias filhas:

- `STORY-0036` / `ISSUE-0146` / `TASK-0036` — Definir política, estados e contratos: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0037` / `ISSUE-0147` / `TASK-0037` — Consolidar slices e liberar integração: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0038` / `ISSUE-0148` / `TASK-0038` — Expor administração e fluxos de uso: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0039` / `ISSUE-0149` / `TASK-0039` — Validar ameaças, autorização e falhas: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0040` / `ISSUE-0150` / `TASK-0040` — Executar QA e auditoria final: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0712` / `ISSUE-0822` / `TASK-0712` — Slice 1/2 — Implementar domínio e persistência: contas locais, bootstrap único, sessões, tokens e adapter OIDC [REQ-AUTH-IMPL, REQ-DBSCHEMA]
- `STORY-0713` / `ISSUE-0823` / `TASK-0713` — Slice 2/2 — Implementar domínio e persistência: contas locais, bootstrap único, sessões, tokens e adapter OIDC [REQ-ID]

- `STORY-0762` / `ISSUE-0873` / `TASK-0769` — Calibrar e promover o perfil quantitativo de throttling requerido por REQ-AUTH-IMPL-007

- `STORY-0767` / `ISSUE-0874` / `TASK-0770` — Definir e aprovar o baseline de execução do BP-003 para throttling (hardware + workload)

- `STORY-0769` / `ISSUE-0876` / `TASK-0772` — Provisionar e evidenciar o venue de referência do benchmark de throttling BP-003

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-034`, `ADR-043`, `ADR-055`
- **Resultado:** `PASS`

## Reconciliação excepcional da fase atual — 2026-10-07

Decisão explícita do usuário: DEVELOPMENT_READINESS = ACCEPTED;
PRODUCTION_RELEASE_READINESS = BLOCKED_BY_DEFERRED_OBLIGATION.
[Único registro canônico](../../07-assurance/PHASE-G-CTO-REVIEW-REPORT.md#epic-008-req-auth-impl-007-production-readiness):
EPIC-008-REQ-AUTH-IMPL-007-PRODUCTION-READINESS, consumido como gate de release
por EPIC-108 / ISSUE-0108 / GitHub #816 / SPRINT-012, sem transferir REQ-007
para BC-015. Owner funcional permanece identity_access/Backend; benchmark Security.

A evidência integrada identifica atendimento histórico dos demais requisitos;
REQ-AUTH-IMPL-007 possui contrato/teste de contrato, mas runtime persistente final
permanece ausente. Não há novo defeito funcional conhecido fora de REQ-007 nas
fontes consultadas. Os dois testes finais ausentes/não executados, a integração
HTTP de sucesso não demonstrada são limitações
explícitas; não recebem PASS nem são escondidas pela exceção de REQ-007.
Os PASS das revisões estruturais Fases B–G abaixo não são QA atual ou production readiness.

ISSUE-0150 e EPIC-008 têm classificação de fechamento administrativo
CLOSED_WITH_ACCEPTED_DEFERRAL; EPIC_008_DEVELOPMENT_COMPLETE = YES_FOR_CURRENT_PHASE;
EPIC_008_PRODUCTION_READY = NO. FINAL_QA = PASS_WITH_ACCEPTED_DEFERRAL;
FINAL_REVIEW = PASS_WITH_ACCEPTED_DEFERRAL.
QA_APPROVED_SHA = bd8caa9bb40bf8093767a1f8800c132747392f56;
REVIEW_SHA = bd8caa9bb40bf8093767a1f8800c132747392f56;
APPROVED_SHA = bd8caa9bb40bf8093767a1f8800c132747392f56.
CLOSURE_ALLOWED = YES, somente administrativo, autorizado pelo usuário em 2026-10-07
após QA independente informado e parecer independente do Reviewer no mesmo SHA.
Nenhum outro BLOCKER/HIGH independente identificado nas fontes revisadas.
Registro posterior dos gates; nenhum PASS técnico integral ou de produção é emitido.
O DEFERRED_ID acima e sua quitação em SPRINT-012 / GitHub #816 permanecem vigentes.
