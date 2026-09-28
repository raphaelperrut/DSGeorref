# Handoff — execução governada da SPRINT-001

## Identidade do candidato

- Branch: `codex/issue-0868-slice-5`.
- Binding: o commit candidato é o commit que contém este handoff, a policy, o
  validador, os testes e a evidence. O SHA imutável deve ser lido do `HEAD` do PR;
  ele não é autoembutido no próprio commit.
- Dependência: `STORY-0683` satisfeita em `main` pelo PR #989, cujo merge contém
  `aead17a`.
- Aprovação independente: pendente de QA e Reviewer sobre o mesmo SHA.

## Escopo entregue

Este incremento materializa somente os controles de `REQ-SPRINT-001-002`, `003`,
`005`, `006`, `007`, `008`, `009` e `010`. A policy é local a `BC-001`,
declarativa, presa por digest e validada de forma estrita e fail-closed. Ela
reúne as decisões já executáveis pelos validadores canônicos; não cria registry,
checker compartilhado, endpoint, estado persistido, evento ou automação nova.

O TaskEnvelope foi corrigido administrativamente porque o diretório de evidence
obrigatório já estava declarado em `evidence`, mas ausente tanto de `allow_paths`
quanto do espelho `phase_f_review.files.allow_paths`. Nenhum outro campo de
ownership, requisito, dependência, AC ou deny path foi alterado.

## Requisito → controle/implementação → teste/evidência

| Requisito | Controle/implementação | Teste/evidência |
|---|---|---|
| `REQ-SPRINT-001-002` | seleção determinística pelo grafo e gates de dependência, requisito e risco; seleção arbitrária rejeitada | `test_sprint_zero_baseline_decision_02`; `test_sprint_foundation_policy_decision_02` |
| `REQ-SPRINT-001-003` | ondas como subconjunto pequeno derivado do grafo, com blockers concluídos e evidence | `test_sprint_zero_baseline_decision_03`; `test_sprint_foundation_policy_decision_03` |
| `REQ-SPRINT-001-005` | conjunto exato de contracts essenciais, versionado e exercitado com evidence | `test_sprint_zero_baseline_decision_05`; `test_sprint_foundation_policy_decision_05` |
| `REQ-SPRINT-001-006` | diagnóstico sintético ponta a ponta, sem claim de georreferenciamento funcional | `test_sprint_zero_baseline_decision_06`; `test_sprint_foundation_policy_decision_06` |
| `REQ-SPRINT-001-007` | capacidade derivada da revisão do repositório, teste por capacidade presente e paridade `make verify` | `test_sprint_zero_baseline_decision_07`; `test_sprint_foundation_policy_decision_07` |
| `REQ-SPRINT-001-008` | `SPRINT_EVIDENCE_SET` machine-readable, resumível e imutável por SHA-256 | `test_sprint_zero_baseline_decision_08`; `test_sprint_foundation_policy_decision_08` |
| `REQ-SPRINT-001-009` | encerramento por evidence; extensão somente por blocker direto do grafo e autoridade do Product Owner | `test_sprint_zero_baseline_decision_09`; `test_sprint_foundation_policy_decision_09` |
| `REQ-SPRINT-001-010` | cutover explícito após G1 aprovado, autorização da primeira fatia e lineage do candidato | `test_sprint_zero_baseline_decision_10`; `test_sprint_foundation_policy_decision_10` |

## Acceptance criteria

- `AC-ISSUE-0868-01`: PASS — os oito requisitos possuem controle, teste canônico
  e teste local explícitos.
- `AC-ISSUE-0868-02`: PASS — o package é estável, disjunto e não usa identificador
  de issue, story ou task em código de produção.
- `AC-ISSUE-0868-03`: PASS — cada teste local muta seu controle para um estado
  negado; o hardening adicional cobre campo desconhecido, controle/evidence
  ausente, raiz inválida, chave JSON duplicada e arquivo indisponível.
- `AC-ISSUE-0868-04`: PASS — este handoff registra contratos, riscos, limitações e
  rollback.

## Arquivos alterados e justificativa

- `.codex/tasks/TASK-0758.json` — autoriza somente a evidence obrigatória omitida e
  mantém o espelho Phase F idêntico.
- `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/foundation-policy.json`
  — policy local dos oito controles atribuídos.
- `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/HANDOFF.md`
  — handoff e rastreabilidade do candidato.
- `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/policy_validation.py`
  — validação estrita, determinística e presa ao digest da policy.
- `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/test_policy_validation.py`
  — failure modes locais e hardening fail-closed.
- `evidence/implementation/governanca-continua-do-backlog-e-decomposicao-de-e/sprint-001-parte-5/IMPLEMENTATION_EVIDENCE.md`
  — evidence append-only do candidato.

## Impacto em contratos

Nenhum contrato congelado, ADR, schema público, API ou formato de artifact é
alterado. A policy é evidence local de decisões vigentes e não substitui os
validadores ou contratos canônicos já versionados. PostgreSQL, RabbitMQ,
migration, frontend, geo, IA operacional e SGV não são aplicáveis ao diff.

## Riscos e limitações residuais

- A policy valida o espelho versionado dos controles; enforcement operacional
  permanece nos validadores canônicos e nos gates que os invocam.
- Este slice não executa cutover, encerra a sprint, cria extensão, roda diagnóstico
  produtivo ou declara production readiness.
- O status `CANDIDATE` exige QA e Reviewer independentes sobre o mesmo commit.

## Rollback

Reverter conjuntamente os seis arquivos deste incremento. Como não há banco,
migration, endpoint, fila ou estado operacional novo, não existe rollback de
dados. Se a policy já tiver sido consumida, publicar uma revisão governada em vez
de sobrescrever evidence histórica.

Este handoff não constitui autoaprovação.
