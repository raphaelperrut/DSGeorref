# Evidência de implementação — STORY-0566 / ISSUE-0676

## Critérios de aceitação

- `AC-ISSUE-0676-01`: registry, checkpoint e CLI versionados tornam o fechamento
  da SPRINT-001 observável e executável.
- `AC-ISSUE-0676-02`: o registry liga `REQ-DEV-001`, `REQ-FRZ-001`,
  `REQ-FRZ-002`, `REQ-FRZ-003`, `REQ-FRZ-004` e `REQ-GOV-005` aos testes
  atribuíveis exigidos pela issue.
- `AC-ISSUE-0676-03`: o teste fail-closed rejeita evidência ausente, stale ou
  conflitante, drift de comando e tentativa de declarar autorização.
- `AC-ISSUE-0676-04`: o checkpoint exige o mesmo comando local e de CI; o
  `make verify` executado por `.github/workflows/ci.yml` chama o validador e o
  teste sentinela.

## Validações sentinela

- CLI da fundação: `PASS`.
- Testes focados da ISSUE-0676: `2 passed`.
- Cinco testes obrigatórios da issue: `5 passed`.
- Ruff nos arquivos Python alterados: `PASS`.
- Mypy no validador: `PASS`.
- `git diff --check`: `PASS`.

Os resultados finais são repetidos no `PR_HEAD` e publicados no PR com o SHA
exato, preservando a vinculação exigida entre candidato e evidência.

## Arquivos e justificativa de escopo

- `.codex/tasks/TASK-0566.json`: corrige allow-paths omitidos para envelope,
  integração CI, teste sentinela e evidência exigida.
- `Makefile`: integra o mesmo validador e teste ao entrypoint usado pela CI.
- `docs/03-engineering/contexts/engineering_governance/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/README.md`:
  documenta comando e limites.
- `docs/03-engineering/contexts/engineering_governance/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/foundation-evidence-registry.json`:
  mantém o registry no control plane versionado.
- `tools/governance/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/foundation-checkpoint.json`:
  liga contrato, registry e comandos reproduzíveis.
- `tools/governance/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/foundation_validation.py`:
  implementa a interface executável fail-closed.
- `tests/fnd/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/test_sprint_001_foundation.py`:
  prova o comportamento alterado e regressões plausíveis.
- `evidence/implementation/epic-092/story-0566/IMPLEMENTATION.md`: registra o
  handoff exigido pela issue.

## Handoff

- Impacto em contratos: nenhum; o contrato congelado da STORY-0565 é apenas
  consumido e validado sem reinterpretação.
- Persistência e migration: não aplicáveis; nenhum estado persistido muda.
- Rollback: reverter o commit antes do consumo downstream ou superseder o
  contrato por nova versão, conforme a política congelada.
- Limitação: a fundação fica em `READY_FOR_INDEPENDENT_REVIEW` e não declara
  `AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE`.
- Risco residual: a aprovação independente no mesmo SHA permanece pendente ao
  reviewer; ausência ou SHA divergente bloqueia a autorização.
