# STORY-0040 / ISSUE-0150 — Executar QA e auditoria final: contas locais, bootstrap único, sessões, tokens e adapter OIDC

- **Tipo:** `História implementável`
- **Estado:** `QA` — aceitação da fase reconciliada; fechamento condicionado a QA e depois Reviewer independentes
- **Épico pai:** `EPIC-008`
- **Sprint:** `SPRINT-002`
- **Domínio:** `PLT`
- **Bounded Context:** `BC-002 — Identidade e Controle de Acesso`
- **Papel executor:** `Reviewer`
- **TaskEnvelope:** `.codex/tasks/TASK-0040.json`

## História de usuário

Como administrador da instância, preciso executar qa e auditoria final para “contas locais, bootstrap único, sessões, tokens e adapter OIDC”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável

Executar QA e auditoria final para a capacidade **contas locais, bootstrap único, sessões, tokens e adapter OIDC**, com saída versionada, testes e evidência no commit candidato.

## Escopo

A autorização administrativa excepcional de 2026-10-07 estende somente este passe aos paths documentais exatos de TASK-0040; não permite implementação ou autoaprovação.

- `evidence/reviews/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/**`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos

Nenhum requisito exclusivo; valida integração do épico.

## ADRs e contratos

- `ADR-018`
- `ADR-028`
- `ADR-034`
- `contracts/README.md`

## Dependências


`STORY-0039`, `STORY-0712`

## Critérios de aceitação

- [ ] AC-ISSUE-0150-01: a capacidade observável já integrada permanece sustentada por evidência histórica identificada; runtime final de throttling e integração de produção não são declarados executados.
- [ ] AC-ISSUE-0150-02: cada requisito do EPIC-008 possui rastreabilidade explícita; REQ-AUTH-IMPL-007 é parcialmente entregue no contrato e permanece não atendido em runtime, sob EPIC-008-REQ-AUTH-IMPL-007-PRODUCTION-READINESS; nenhum outro requisito pode ser coberto por esse deferimento.
- [ ] AC-ISSUE-0150-03: preservar evidência histórica dos caminhos de erro/fail-closed; os dois testes finais obrigatórios permanecem ausentes/não executados e sua produção e execução pertencem ao gate final de readiness, sem converter falta de teste em PASS.
- [ ] AC-ISSUE-0150-04: QA e Reviewer independentes devem avaliar esta aceitação alterada no mesmo commit candidato; até seus registros explícitos, FINAL_QA e FINAL_REVIEW permanecem PENDING e o fechamento CLOSED_WITH_ACCEPTED_DEFERRAL não é autorizado.

## Testes finais obrigatórios — deferred production readiness

- `test_epic_008_aceite_happy_path`
- `test_epic_008_aceite_negative_paths`

## Evidências obrigatórias

- Neste passe: conferência documental de links, escopo, índices, aceitação e grafo; sem execução de testes de produto. Resultados dos testes finais exigidos antes de production readiness.
- Lista de arquivos alterados e justificativa de escopo.
- Handoff com limitações, riscos residuais e impacto em contratos.
- Aprovação independente aplicável ao mesmo commit.

## Condições de parada

- Decisão material de produto ou arquitetura não resolvida.
- Contrato necessário ausente, contraditório ou não versionado.
- Colisão de write scope com lane ativa.
- Critério de aceitação sem teste ou evidência objetiva.

## Prompt de execução Codex

Leia `AGENTS.md`, `.codex/roles/ROLE-011-reviewer.md`, este documento, o épico `EPIC-008` e o TaskEnvelope `TASK-0040`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute os testes, registre evidências e interrompa quando qualquer condição de parada ocorrer.


## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `consistência`, `completude`, `risco residual`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** referências e schemas listados no TaskEnvelope.
- **Contrato de saída:** artifact, código, schema, teste ou evidência versionada no commit candidato.
- **Migration/rollback:** obrigatório quando a história altera schema, estado persistido, artifact ou deployment; caso contrário `não aplicável` deve ser justificado no handoff.
- **Observabilidade:** falhas e transições relevantes devem emitir signal/event/audit sem cardinalidade ilimitada.
- **Gate de completude:** nenhum heading obrigatório vazio, placeholder, ID obsoleto ou dependência implícita.

`EVIDENCE_BOUND` não representa decisão arquitetural em aberto: indica parâmetro quantitativo cujo valor é promovido pelo Benchmark Profile declarado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Impacto no modelo:** `CROSS_CONTEXT_INTEGRATION`.
- **Upstreams permitidos:** `Nenhum`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0150-01, AC-ISSUE-0150-02, AC-ISSUE-0150-03, AC-ISSUE-0150-04`
- **Base de requisitos:** `DERIVED_CONTROL`
- **ADRs governantes:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessores explícitos | PASS |
| Arquivos | 1 write scopes; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 2 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-002-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `MEDIUM`
- **Controles aplicáveis:** `CTO-003, CTO-004, CTO-006, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `IMPLEMENTATION_AUTHORIZATION`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.

## Prerequisite de throttling — bloqueio vigente

STORY-0762 / ISSUE-0873 / TASK-0769 calibra BP-003 e promove somente o recorte de throttling em AP-003. Cadeia: STORY-0762 -> STORY-0712 -> STORY-0040. O perfil aprovado deve estar integrado antes da correcao de ISSUE-0822; ISSUE-0150 depende tambem da implementacao e dos testes reais dessa correcao. O diagnostico 11df6dff79e7eaa33ac287cd576bcafd5344391c permanece preservado; nenhum gate foi aprovado por esta materializacao.

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
HTTP de sucesso não demonstrada e QA independente pendente são limitações
explícitas; não recebem PASS nem são escondidas pela exceção de REQ-007.
Os PASS das revisões estruturais Fases B–G abaixo não são QA atual ou production readiness.

ISSUE-0150 e EPIC-008 têm classificação de fechamento proposta
CLOSED_WITH_ACCEPTED_DEFERRAL; EPIC_008_DEVELOPMENT_COMPLETE = YES_FOR_CURRENT_PHASE;
EPIC_008_PRODUCTION_READY = NO. FINAL_QA = PENDING e FINAL_REVIEW = PENDING para
esta aceitação documental alterada. CLOSURE_ALLOWED = NO até os dois registros
independentes no mesmo commit documental e confirmação de ausência de outro
BLOCKER/HIGH independente. Nenhuma autoaprovação ou PASS técnico é emitido.
O próximo gate é revisão documental; não é nova prerequisite de infraestrutura.
