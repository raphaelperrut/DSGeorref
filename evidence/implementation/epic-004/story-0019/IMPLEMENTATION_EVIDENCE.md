# Evidência de implementação — ISSUE-0129

- Issue: `ISSUE-0129` / GitHub `#31`
- Story: `STORY-0019`
- TaskEnvelope: `TASK-0019`
- Executor: Tech Lead
- Estado: implementação validada; aprovação independente pendente

## Critérios de aceitação

- `AC-ISSUE-0129-01`: o runner emite relatório JSON determinístico para os sete
  contratos versionados e confirma a automação read-only publicada.
- `AC-ISSUE-0129-02`: `test_first_functional_slice_decision_06` vincula
  `REQ-FS1-006`, `ADR-045` e os controles que delegam o algoritmo geoespacial e
  proíbem bypass científico.
- `AC-ISSUE-0129-03`: mutação permissiva do gate científico e relatórios de
  quality com falha ou malformados são rejeitados.
- `AC-ISSUE-0129-04`: a integração invoca o control plane de quality por processo
  read-only, não importa módulos internos do repositório e não duplica regras.

## Validações executadas

- `python -B .../repository_integration.py --repository-root .`: `PASS`, zero
  findings, sete contratos.
- `py -3.12 -m pytest -q -p no:cacheprovider .../test_repository_integration.py`:
  `PASS`, 4 testes.
- `py -3.12 -m pytest -q -p no:cacheprovider test_contract_foundation.py
  test_runtime_schema_contract.py test_automation.py::test_epic_004_automacao`:
  19 testes de contrato passaram; automação não iniciou no `%TEMP%` restrito.
- Reexecução de `test_epic_004_automacao` com `TEMP=C:\tmp\i129`: `PASS`, 1 teste.
- Validação de `TASK-0019` contra `TASK_ENVELOPE.schema.json`: `PASS`.
- `make verify PYTHON="py -3.12"`: validators de repositório, arquitetura,
  requisitos, DDD, ADR, specifications, sprint, arquitetura Python e foundation
  passaram. O pytest final alheio à issue ficou bloqueado pelo ambiente:
  `FOUNDATION_INTEGRATION=1` e serviços PostgreSQL/RabbitMQ não disponíveis
  (`4 passed, 1 failed`).

O warning de configuração futura do `pytest-asyncio` não afeta estes testes.

## Arquivos e justificativa

- `.codex/tasks/TASK-0019.json`: inclui o path de evidência já obrigatório no
  envelope e mantém o espelho de Phase F sincronizado.
- `tools/governance/.../repository_integration.py`: composição read-only dos
  validators e contratos existentes.
- `tools/governance/.../test_repository_integration.py`: evidência canônica,
  integração, fail-closed e ausência de import interno.
- `docs/03-engineering/.../REPOSITORY_INTEGRATION.md`: operação e limites do gate.
- este arquivo: resultados, escopo, limitações e impacto contratual.

## Impacto e limitações

- Contratos compartilhados, registry, workflow, schema persistido e deployment:
  inalterados.
- Migration e rollback de dados: não aplicáveis; o runner é read-only.
- Risco residual funcional conhecido: nenhum.
- Aprovação independente do mesmo commit candidato: pendente e não produzida pelo
  executor.
