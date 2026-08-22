# STORY-0761 / ISSUE-0871 — Materializar verifier e trust operacional da Delivery Approval Authority

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-001`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel executor:** `Security`
- **TaskEnvelope:** `.codex/tasks/TASK-0761.json`

## História de usuário

Como Security, preciso materializar o verifier reutilizável e o trust operacional governado da Delivery Approval Authority, para que consumidores obtenham veredictos por repository/revision sem aceitar trust do caller nem promover chaves de conformance.

## Resultado verificável

Um componente de governança carrega verifier, trust-anchor-set e trust profile exclusivamente de paths governados em uma repository/revision explícita, valida o contrato publicado pela `STORY-0760` e falha fechado sem fallback para dados do caller ou material de teste.

## Escopo

- `tools/governance/delivery_approval_authority/**`
- `contracts/assurance/delivery-approval-authority/trust/**`
- `docs/03-engineering/contexts/engineering_governance/delivery_approval_authority/**`
- `tests/security/delivery_approval_authority/**`
- `evidence/security/delivery-approval-authority/**`

## Fora de escopo

- Integrar check, workflow, ruleset, merge gate ou API do GitHub.
- Alterar o authority source, a identidade canônica, a independência ou a semântica fail-closed da `ADR-058`.
- Gerar, armazenar ou versionar private keys, credentials ou secrets.
- Reutilizar verifier, chaves, anchors, profiles ou vectors sob `test-vectors/**` como trust operacional.
- Alterar ou implementar a `ISSUE-0799`; esta Story apenas publica seu prerequisite operacional.

## Requisitos

Nenhum requisito funcional novo; controle operacional derivado da `ADR-058` e do contrato versionado da Delivery Approval Authority.

## ADRs e contratos

- `ADR-001`
- `ADR-003`
- `ADR-006`
- `ADR-007`
- `ADR-010`
- `ADR-058`
- `contracts/assurance/delivery-approval-authority/README.md`
- `contracts/assurance/delivery-approval-authority/trust-anchor-set.schema.json`
- `contracts/assurance/delivery-approval-authority/trust-profile.schema.json`
- `contracts/assurance/delivery-approval-authority/verification-verdict.schema.json`

## Dependências

`STORY-0760`

## Critérios de aceitação

- [ ] Verifier reutilizável de governança valida o contrato DAA e retorna somente `verification-verdict` conforme, sem importar implementação do harness de conformance.
- [ ] Trust-anchor-set e trust profile operacionais são governados, versionados e resolvidos por repository/revision explícita; ausência, ambiguidade ou divergência falha fechado.
- [ ] A entrada não confiável não pode fornecer ou substituir verifier, trust profile, anchors, issuer, key ou policy, e material sob `test-vectors/**` nunca adquire autoridade operacional.
- [ ] Testes positivos e negativos demonstram resolução histórica, separação completa de conformance, revogação/expiração, assinatura inválida e trust ausente sem fallback.

## Testes obrigatórios

- `test_delivery_approval_operational_verifier`
- `test_delivery_approval_governed_trust_resolution`
- `test_delivery_approval_rejects_caller_and_conformance_trust`
- `test_delivery_approval_operational_fail_closed`

## Evidências obrigatórias

- `evidence/security/delivery-approval-authority/`
- Resultado dos testes e digests do verifier, trust-anchor-set e trust profile na repository/revision exercitada.
- Handoff com rotação/revogação, recuperação, compatibilidade, limitações e riscos residuais.
- Aprovações independentes de QA e Reviewer sobre o mesmo candidate SHA.

## Condição de conclusão no fluxo

Esta Story publica somente o prerequisite operacional. `ISSUE-0799` permanece bloqueada até esta Story estar integrada e seu consumo ser replanejado sem trust fornecido pelo caller.

## Condições de parada

- Anchors, profile ou signers operacionais não foram emitidos pela autoridade governada e a implementação exigiria inventá-los ou usar material de teste.
- A solução aceita configuração de trust do caller, carrega verifier do harness de conformance ou permite fallback manual implícito.
- A implementação exige ampliar o boundary definido pela `ADR-058` ou criar serviço, banco, endpoint ou autoridade nova.
- O write scope exige integração do GitHub ou alteração de código/evidência da `ISSUE-0799`.
- A separação entre trust operacional, `SPEC-001`, supply chain e conformance não pode ser demonstrada objetivamente.

## Prompt de execução Codex

Leia `AGENTS.md`, `.codex/roles/ROLE-010-security.md`, esta Story, `ADR-058`, `EPIC-001`, `TASK-0761` e o contrato DAA. Implemente somente verifier e trust operacional governados por repository/revision; não integre o GitHub, não altere a `ISSUE-0799` e interrompa se anchors/profile operacionais estiverem ausentes.

## Revisão SAR

- **Estado arquitetural:** `RESOLVED` pela `ADR-058`; nenhuma arquitetura nova é introduzida.
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`; algoritmos e trust scope já pertencem ao contrato, enquanto valores operacionais devem ser emitidos pela autoridade governada.
- **Atributos de qualidade dominantes:** `integridade`, `segurança`, `auditabilidade`, `reprodutibilidade`.
- **Autoridade:** `BC-001 / Delivery Approval Authority`; caller, GitHub, `SPEC-001`, supply chain e conformance não são trust sources.
- **Contrato de entrada:** repository, revision, TaskEnvelope validado, candidate SHA, verification time, bindings e attestations não confiáveis.
- **Contrato de saída:** `verification-verdict` fail-closed produzido com verifier e trust material governados.
- **Migration/rollback:** nenhuma migration; rollback remove o consumo do componente sem aceitar evidência não conforme.
- **Gate de completude:** testes provam origem governada, resolução histórica e rejeição de toda substituição de trust.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001 — Governança de Engenharia e Entrega`.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `Nenhum contexto de produto`.
- **Regra de integração:** consumidores recebem somente o veredito publicado e não controlam verifier ou trust material.
- **Package de produção:** ferramenta de governança context-first em path estável; não participa do runtime do produto.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0871-01, AC-ISSUE-0871-02, AC-ISSUE-0871-03, AC-ISSUE-0871-04`
- **Base de requisitos:** `DERIVED_CONTROL`
- **ADRs governantes:** `ADR-001`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-010`, `ADR-058`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`; a `STORY-0760` publicou contrato e conformance, não o prerequisite operacional.
- **Requisito faltante:** `Não`; o controle é consequência operacional explícita da `ADR-058`.
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`

## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-001`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-010`, `ADR-058`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** materializar somente o boundary aprovado; qualquer novo authority source retorna ao Owner.

## Specification Review — Fase E

- **Especificações de execução do agente:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- `SPEC-001` governa somente o Prompt Bundle da tarefa e nunca fornece trust para a DAA.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessor explícito | PASS |
| Arquivos | 5 write scopes mínimos; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 4 testes obrigatórios | PASS |
| Artefatos | PRODUCT_AND_EVIDENCE | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Security, QA e Reviewer independentes; mesmo candidate SHA | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`

## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-002, CTO-003, CTO-004, CTO-006, CTO-012, CTO-013, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** o prerequisite não autoriza claim de produção; trust material, rotação, revogação, recuperação e rollback exigem a evidência declarada no TaskEnvelope.
