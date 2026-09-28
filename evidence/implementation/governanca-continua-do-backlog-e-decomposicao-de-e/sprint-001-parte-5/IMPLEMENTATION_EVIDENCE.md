# Implementation evidence — slice 5/5 da fundação SPRINT-001

## Identidade e scope

- Branch candidata: `codex/issue-0868-slice-5`.
- Commit candidato: o commit que contém esta evidence; o SHA autoritativo é o
  `HEAD` do PR e deve ser usado por QA e Reviewer.
- Base: `origin/main` em `97d6668`, após integração da `STORY-0683` pelo PR #989.
- TaskEnvelope: alterado somente para incluir a evidence obrigatória em
  `allow_paths` e no espelho de scope da Phase F.
- Novo prerequisite: não criado.

## Rastreabilidade

| Requisito | Controle | Teste canônico | Evidence local |
|---|---|---|---|
| `REQ-SPRINT-001-002` | `graph_selection` | `test_sprint_zero_baseline_decision_02` | `test_sprint_foundation_policy_decision_02` |
| `REQ-SPRINT-001-003` | `vertical_waves` | `test_sprint_zero_baseline_decision_03` | `test_sprint_foundation_policy_decision_03` |
| `REQ-SPRINT-001-005` | `essential_contracts` | `test_sprint_zero_baseline_decision_05` | `test_sprint_foundation_policy_decision_05` |
| `REQ-SPRINT-001-006` | `synthetic_diagnostic` | `test_sprint_zero_baseline_decision_06` | `test_sprint_foundation_policy_decision_06` |
| `REQ-SPRINT-001-007` | `progressive_ci` | `test_sprint_zero_baseline_decision_07` | `test_sprint_foundation_policy_decision_07` |
| `REQ-SPRINT-001-008` | `sprint_evidence_set` | `test_sprint_zero_baseline_decision_08` | `test_sprint_foundation_policy_decision_08` |
| `REQ-SPRINT-001-009` | `sprint_closure` | `test_sprint_zero_baseline_decision_09` | `test_sprint_foundation_policy_decision_09` |
| `REQ-SPRINT-001-010` | `first_slice_cutover` | `test_sprint_zero_baseline_decision_10` | `test_sprint_foundation_policy_decision_10` |

## Acceptance evidence

- `AC-ISSUE-0868-01`: PASS — oito requisitos mapeados para controles e testes.
- `AC-ISSUE-0868-02`: PASS — scope estável/disjunto; nenhum ticket ID em produção.
- `AC-ISSUE-0868-03`: PASS — mutações negadas por controle e hardening estrito sem
  fallback.
- `AC-ISSUE-0868-04`: PASS — `HANDOFF.md` registra impacto contratual, riscos,
  limitações e rollback.

## Validações do candidato

- Testes obrigatórios, pelos oito node IDs exatos: `8 passed`.
- Testes focados da policy: `9 passed`.
- Ruff nos dois arquivos Python novos: PASS.
- Mypy no validador novo: PASS.
- Parsing JSON do TaskEnvelope e da policy: PASS.
- Busca de ticket ID no código de produção novo: PASS, nenhuma ocorrência.
- `git diff --check`: PASS.

As execuções usam Python 3.12, `PYTHONDONTWRITEBYTECODE=1` e
`pytest -p no:cacheprovider` porque o worktree gerenciado não permite as escritas
não funcionais de cache/bytecode no sandbox. Isso não altera coleta, assertions ou
resultado dos testes. O warning preexistente de configuração do `pytest-asyncio`
não afeta os resultados.

## Arquivos e justificativa

- `.codex/tasks/TASK-0758.json` — correção administrativa do scope de evidence.
- `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/foundation-policy.json`
  — policy local dos oito controles.
- `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/HANDOFF.md`
  — handoff estruturado.
- `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/policy_validation.py`
  — validador estrito e preso por digest.
- `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/test_policy_validation.py`
  — oito testes de controle e um teste de hardening.
- `evidence/implementation/governanca-continua-do-backlog-e-decomposicao-de-e/sprint-001-parte-5/IMPLEMENTATION_EVIDENCE.md`
  — esta evidence append-only.

Cada arquivo pertence ao allow scope efetivo; nenhum deny path, contrato
congelado, ADR ou requisito de outro slice foi alterado.

## Contratos, riscos, limitações e rollback

Impacto contratual: nenhum contrato público ou congelado alterado. A policy local
espelha decisões já implementadas pelos validadores canônicos e não cria segunda
autoridade. Risco residual: enforcement continua dependendo dos gates canônicos;
o diff não executa operação produtiva nem cutover. Limitação: aprovação QA/Reviewer
permanece externa e deve usar o mesmo SHA. Rollback: revert conjunto dos seis
arquivos, sem rollback de dados ou migration.

Esta evidence registra implementação e validação; não declara aprovação
independente.
