# Integração da capacidade no repositório

`repository_integration.py` é o gate executável da `ISSUE-0129`. Ele mantém a
separação do control plane ao invocar em modo `--dry-run` o validator publicado
em `tools/quality`, sem importar ou duplicar suas regras.

O gate confirma:

- identidade, ownership, dependências, escopo e testes do `TASK-0019`;
- presença da automação read-only já publicada para o EPIC-004;
- os sete contratos versionados registrados para OpenAPI, eventos, artefatos,
  ProcessingPlan, QualityReport e FailureDiagnostic;
- o vínculo de `REQ-FS1-006` à evidência canônica
  `test_first_functional_slice_decision_06`;
- delegação do algoritmo geoespacial ao contexto owner e rejeição de bypass dos
  gates do ProcessingPlan.

Execução focada:

```text
python -B tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/repository_integration.py --repository-root .
python -m pytest -q -p no:cacheprovider tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/test_repository_integration.py
```

O gate é fail-closed: documento ausente ou inválido, drift do TaskEnvelope,
automação incompleta, validator de contratos com falha, saída malformada ou
bypass científico produzem status `FAIL` e código de saída não zero.

Não há migration nem rollback de dados: esta integração é read-only e não altera
schema, estado persistido, contratos compartilhados ou deployment.
