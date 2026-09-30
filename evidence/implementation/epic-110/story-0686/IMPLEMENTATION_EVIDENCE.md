# Implementation evidence — ISSUE-0796 / STORY-0686

## Candidate binding

- `CANDIDATE_SHA: CONTAINING_COMMIT`.
- O SHA imutável é o commit que contém esta evidence e deve ser informado no
  handoff final. Verificação: `git show <candidate-sha>:evidence/implementation/epic-110/story-0686/IMPLEMENTATION_EVIDENCE.md`.
- Esta evidence registra implementação e QA sentinela; aprovação independente:
  `NOT_PERFORMED`.

## Testes executados

- Obrigatório `test_epic_110_integracao`: `PASS` (`1 passed in 1.44s`).
- Casos existentes de cardinalidade duplicada e fail-closed diretamente ligados
  ao risco de integração: `PASS` (`7 passed in 3.87s`).
- Validações estáticas do diff: `PASS` para JSON do envelope, Ruff lint, Ruff
  format e `git diff --check`.
- `make verify`, obrigatório por `AGENTS.md`: `EXECUTED_WITH_EXTERNAL_ENVIRONMENT_FAILURE`.
  Com `.venv/Scripts/python.exe`, Ruff, mypy, typecheck, Vitest, Playwright,
  validação do repositório, reviews A-F, arquitetura e gates anteriores passaram.
  A execução parou no gate preexistente de walking skeleton porque o ambiente
  local não define `FOUNDATION_INTEGRATION=1` nem declara os serviços PostgreSQL e
  RabbitMQ fixados que esse teste exige. Nenhum arquivo desse gate foi alterado.

Comandos focados:

- `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/integracao/test_repository_integration.py::test_epic_110_integracao`
- `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/test_automation.py::test_six_mapping_and_proof_regression_is_fail_closed_and_idempotent tests/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/test_automation.py::test_contract_sentinel_rejects_six_mapping_and_proof_regression tests/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/test_automation.py::test_fail_closed_errors_have_actionable_diagnostics`

Nota de ambiente: tentativas iniciais do teste obrigatório dentro do sandbox
falharam na criação/leitura do diretório temporário do pytest. A execução
autoritativa acima ocorreu fora do sandbox e passou; não houve falha de assertion
nessas tentativas.

## Mapeamento dos critérios

| Critério | Evidência objetiva |
|---|---|
| `AC-ISSUE-0796-01` | `test_epic_110_integracao` executa a consolidação existente e exige relatório observável `PASS` do validador no mesmo checkout. |
| `AC-ISSUE-0796-02` | Este arquivo vincula ACs, predecessores, comandos, resultados e arquivos ao containing commit. |
| `AC-ISSUE-0796-03` | O teste obrigatório exige `FAIL_CLOSED`/`READ_ONLY`, rejeita inputs ausentes de modo determinístico e prova ausência de escrita; testes existentes cobrem duplicatas e diagnósticos. |
| `AC-ISSUE-0796-04` | O sentinela delega à consolidação e ao validador existentes; nenhum módulo de produção ou import entre packages é adicionado. |

## Arquivos alterados e justificativa

- `.codex/tasks/TASK-0686.json`: autoriza somente a evidence já obrigatória, com
  o espelho `phase_f_review.files` consistente.
- `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/integracao/test_repository_integration.py`:
  sentinela executável que reutiliza os predecessores sem copiar regra.
- `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/integracao/HANDOFF.md`:
  handoff mínimo da ISSUE-0796.
- `evidence/implementation/epic-110/story-0686/IMPLEMENTATION_EVIDENCE.md`:
  evidência versionada exigida pelo envelope.

## Impacto, rollback e riscos

- Impacto contratual: `NONE`; nenhum contrato compartilhado, ADR, schema, API,
  evento ou regra de produto foi alterado.
- Migration/rollback: `NOT_APPLICABLE`; não há estado persistido, artifact de
  runtime ou deployment alterado. Revert do commit não exige ação de dados.
- Limitação: prova restrita ao control plane versionado, sem mutação remota ou
  operação runtime.
- Risco residual: QA e Reviewer independentes ainda precisam validar o mesmo SHA.
- Risco residual não bloqueante: o restante de `make verify` depende do ambiente
  de integração com PostgreSQL/RabbitMQ exigido pelo gate preexistente; validar em
  CI com `FOUNDATION_INTEGRATION=1`.
- Novo prerequisite: `NO`. Blocker/HIGH aberto: `NONE`.
