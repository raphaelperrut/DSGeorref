# STORY-0760 / ISSUE-0870 — Publicar contrato da Delivery Approval Authority

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-001`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel executor:** `Arquiteto`
- **TaskEnvelope:** `.codex/tasks/TASK-0760.json`

## História de usuário

Como Arquiteto, preciso publicar o contrato machine-readable da Delivery Approval Authority, para que consumidores comprovem identidade, papel, vínculo ao TaskEnvelope, candidate SHA e independência sem atribuir essa autoridade ao GitHub ou à `SPEC-001`.

## Resultado verificável

Contrato versionado e validável define trust profile, principal→role binding e delivery approval attestation, com canonicalização SHA-256, regras de independência e comportamento fail-closed conformes à `ADR-058`.

## Escopo

- `contracts/assurance/delivery-approval-authority/**`
- `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`
- `tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_delivery_approval_authority_contract.py`
- `evidence/implementation/delivery-approval-authority/**`

## Fora de escopo

- Implementar integração, check, workflow ou ruleset do GitHub.
- Implementar serviço autoritativo, banco, endpoint, UI ou identidade do produto.
- Alterar a `SPEC-001`, contratos de Prompt Bundle ou seus trust scopes.
- Emitir approvals para `ISSUE-0799` ou alterar sua story, TaskEnvelope, código ou evidência.
- Definir issuer, chave ou algoritmo por preferência fora do trust profile versionado.

## Requisitos

Nenhum requisito funcional novo; controle arquitetural derivado da `ADR-058`, da matriz de autoridade e da Definition of Done.

## ADRs e contratos

- `ADR-003`
- `ADR-006`
- `ADR-007`
- `ADR-010`
- `ADR-058`
- `.codex/tasks/TASK_ENVELOPE.schema.json`
- `docs/00-governance/ROLE_AUTHORITY_MATRIX.md`
- `docs/00-governance/DEFINITION_OF_DONE.md`

## Dependências

`STORY-0001`

## Critérios de aceitação

- [ ] Schemas versionados definem principal estável, accountable subject e binding autorizado de principal→papel, incluindo authority, scope, validade e revogação.
- [ ] A approval attestation vincula principal, papel, decisão, TaskEnvelope ID e digest canônico SHA-256, candidate SHA exato e versão da política, sob trust scope próprio.
- [ ] Regras machine-verifiable exigem conjuntos dois a dois disjuntos de accountable subjects para Executor, QA e Reviewer no mesmo TaskEnvelope/candidate SHA.
- [ ] Vetores de conformidade rejeitam, em modo fail-closed, trust ou binding ausente/inválido/revogado, assinatura inválida, mismatch/replay de digest ou SHA, approval ausente e sobreposição de papéis.

## Testes obrigatórios

- `test_delivery_approval_authority_contract`
- `test_delivery_approval_authority_fail_closed`

## Evidências obrigatórias

- `evidence/implementation/delivery-approval-authority/`
- Resultado dos testes e digests dos vetores no commit candidato.
- Handoff com compatibilidade, trust scopes, limitações e riscos residuais.
- Aprovação independente do Reviewer sobre o mesmo candidate SHA.

## Condição de conclusão no fluxo

Esta Story publica somente o prerequisite contratual. `ISSUE-0799` permanece bloqueada até o contrato estar integrado e sua implementação ser replanejada para consumi-lo; esta Story não altera a issue bloqueada.

## Condições de parada

- A implementação exige ampliar o authority source, a regra de independência ou o trust boundary definido pela `ADR-058`.
- O contrato mistura signatures ou key scopes da Delivery Approval Authority com a `SPEC-001` ou com supply chain.
- A prova depende isoladamente de role/label declarada, IDs distintos, CODEOWNERS, contagem de approvals, autoria Git não verificada ou assinatura de Prompt Bundle.
- O write scope exige alteração da `ISSUE-0799`, de `TASK-0689`, de código de produto ou de integração de plataforma.
- A aceitação não pode ser demonstrada por schemas, vetores e testes objetivos.

## Prompt de execução Codex

Leia `AGENTS.md`, `.codex/roles/ROLE-002-arquiteto.md`, esta Story, `ADR-058`, `EPIC-001` e `TASK-0760`. Publique somente o contrato prerequisite dentro dos paths permitidos; não implemente integração, não altere `ISSUE-0799` e interrompa diante de qualquer condição de parada.

## Revisão SAR

- **Estado arquitetural:** `RESOLVED` por `ADR-058` e `OWNER_DECISION = APPROVE_OPTION_B`.
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`; valores concretos de trust pertencem ao profile versionado.
- **Atributos de qualidade dominantes:** `integridade`, `auditabilidade`, `segurança`, `portabilidade`.
- **Autoridade:** `BC-001 / Delivery Approval Authority`; GitHub e `EPIC-091` são consumidores.
- **Contrato de entrada:** principals autenticados, role bindings, TaskEnvelope validado e candidate SHA.
- **Contrato de saída:** trust profile, role binding e approval attestation versionados e machine-verifiable.
- **Migration/rollback:** não há aprovação legada promovida; rollback remove consumo do novo contrato sem aceitar evidence não conforme.
- **Gate de completude:** vetores positivos e negativos demonstram todo o boundary fail-closed da `ADR-058`.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001 — Governança de Engenharia e Entrega`.
- **Impacto no modelo:** `PUBLIC_CONTRACT`.
- **Upstreams permitidos:** `Nenhum contexto de produto`.
- **Regra de integração:** consumidores recebem records e veredictos publicados; não reinterpretam identidade, papel ou independência.
- **Package de produção:** `não aplicável`; esta Story publica contrato e evidence, sem runtime do produto.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0870-01, AC-ISSUE-0870-02, AC-ISSUE-0870-03, AC-ISSUE-0870-04`
- **Base de requisitos:** `DERIVED_CONTROL`
- **ADRs governantes:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-010`, `ADR-058`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`; o boundary estava ausente e foi selecionado pelo Owner.
- **Requisito faltante:** `Não`; a Story não cria comportamento funcional de produto.
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`

## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-010`, `ADR-058`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente o contrato aprovado; mudança de authority ou trust boundary retorna ao Owner.

## Specification Review — Fase E

- **Especificações de execução do agente:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- `SPEC-001` governa somente o Prompt Bundle usado para executar a tarefa e não a Delivery Approval Authority produzida.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessor explícito | PASS |
| Arquivos | 4 write scopes mínimos; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 2 testes obrigatórios | PASS |
| Artefatos | PRODUCT_AND_EVIDENCE | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Arquiteto e Reviewer independentes; mesmo candidate SHA | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`

## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-002, CTO-003, CTO-004, CTO-006, CTO-012, CTO-013, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** o contrato não autoriza claim de produção e deve tratar trust, revogação, privacidade e rollback nos gates próprios.
