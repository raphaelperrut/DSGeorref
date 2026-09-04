# Evidência de implementação — ISSUE-0134

- Issue: `ISSUE-0134` / GitHub `#36`
- Story: `STORY-0024`
- TaskEnvelope: `TASK-0024`
- Base: `43919fc37c9c71d72ca4b9f6fd9e35c9217ff1a4`
- Vínculo do candidato: o SHA que contém este arquivo e os artefatos listados
  abaixo; aprovação independente permanece pendente.

## Critérios de aceitação

- `AC-ISSUE-0134-01`: o runner emite relatório JSON determinístico para as três
  evidências canônicas, a política de migration/rollback e o control plane
  automatizado da predecessora.
- `AC-ISSUE-0134-02`: os testes `test_batch_execution_decision_01`,
  `test_batch_execution_decision_06` e `test_first_functional_slice_decision_06`
  vinculam os requisitos, owners normativos e artefatos versionados.
- `AC-ISSUE-0134-03`: mutações permissivas da hierarquia, checkpoint,
  migration/rollback, estimador/fallback e relatório de quality são rejeitadas
  com findings estáveis.
- `AC-ISSUE-0134-04`: o gate usa somente biblioteca padrão e invoca o control
  plane de quality por subprocesso read-only, sem importar ou copiar sua regra.

## Validações executadas

- `py -3.12 -m pytest -q -p no:cacheprovider tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/test_repository_integration.py`:
  `PASS`, 6 testes.
- `py -3.12 -X utf8 tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/repository_integration.py --repository-root .`:
  `PASS`, zero findings.
- `py -3.12 -m ruff check tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/repository_integration.py tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/test_repository_integration.py`:
  `PASS` após correção mecânica da ordem de imports.
- `py -3.12 -m mypy --strict tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/repository_integration.py`:
  `PASS`.
- validação de `.codex/tasks/TASK-0024.json` com
  `.codex/tasks/TASK_ENVELOPE.schema.json`: `PASS`.
- `make verify PYTHON="py -3.12"`: executado conforme governança. Fora do
  sandbox, Ruff, mypy, TypeScript, Vitest, Playwright, repository validation e
  reviews de arquitetura, requisitos, DDD, ADR, specifications, sprint e
  arquitetura Python passaram. O gate agregado encerrou no walking skeleton
  global porque `FOUNDATION_INTEGRATION=1` e PostgreSQL/RabbitMQ pinados não
  estão disponíveis nesta execução (`1 failed, 4 passed`). A primeira tentativa
  dentro do sandbox havia parado antes em `spawn EPERM` do Vitest.

## Arquivos e justificativa

- `.codex/tasks/TASK-0024.json`: autoriza o próprio envelope e a evidência já
  obrigatória, mantendo o espelho de Phase F sincronizado.
- `tools/governance/.../repository_integration.py`: composição fail-closed e
  read-only dos contratos e controles existentes.
- `tools/governance/.../test_repository_integration.py`: quatro provas
  canônicas e casos negativos diretamente afetados.
- `docs/03-engineering/.../REPOSITORY_INTEGRATION.md`: operação, limites,
  migration/rollback e handoff.
- este arquivo: evidência versionada do candidato.

## Impacto, limitações e riscos residuais

- Contratos compartilhados, schema persistido, workflow e deployment não foram
  alterados. O diff valida a obrigação vigente de migration/rollback, mas não
  cria migration porque não muda schema ou estado.
- Rollback operacional antes do consumo: reverter o commit candidato. Após a
  fase contract, usar forward fix ou restore coordenado conforme a matriz
  congelada.
- O secret scan e as bases externas de advisories são exercidos pela CI
  hospedada da `STORY-0023`; não são simulados localmente.
- O Node local é 22, enquanto o pin do repositório é 24.20.0; o workflow
  hospedado mantém o runtime pinado.
- QA sentinela e Reviewer do mesmo SHA continuam pendentes; nenhuma aprovação
  independente é reivindicada por esta implementação.
