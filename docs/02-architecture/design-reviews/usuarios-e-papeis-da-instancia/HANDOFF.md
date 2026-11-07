# Entrega contratual da STORY-0041

Autorização verificada no [ato Owner 6695717784](https://github.com/raphaelperrut/DSGeorref/issues/117#issuecomment-6695717784). Baseline `023cfc22bf6bf2f3b6bc7dca06fb6ac24231fb69`. Branch exclusiva `codex/issue-117-contract`. TASK-0041 preservado. A entrega contém política parametrizada, matriz de concessões, seis transições de conta, referências aos oito contratos HTTP, dois testes e proposta AC04 v1.

## Validação do conteúdo

No candidato de conteúdo `478f9b54793b6383b94e5737ee3613608eabbdd2`, 173 testes passaram com CPython 3.12.13, usando as dependências instaladas em `.venv/Lib/site-packages` via PYTHONPATH. A seleção incluiu os dois testes novos, os 170 testes do freeze e o teste de idempotência de membros existente. Comando pytest usado, com `-B -m pytest -q -p no:cacheprovider`, sobre os seguintes alvos.

- `contracts/contexts/identity_access/plt/usuarios-e-papeis-da-instancia`
- `contracts/contexts/identity_access/plt/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/test_auth_freeze.py`
- `tests/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento/test_contract_foundation.py::test_project_members_idempotency_owner_decision`

Ruff no teste novo e `git diff --check` passaram. `validate_effective_task_scope` retornou lista vazia de findings para baseline/checkpoint `023cfc2`, candidato de conteúdo acima e TASK-0041. Esse resultado verifica paths e integridade do envelope. A decisão Owner é a autoridade externa para executar este incremento.

## Gates e limites

`make verify` foi executado com Python 3.12.13, Node 24.20.0 e Corepack selecionando pnpm 10.26.1. Ruff e mypy passaram. O agregado parou em `openapi:check` com `Generated artifact drift`. Os inputs OpenAPI, tooling e artefatos gerados em frontend são idênticos à baseline no diff Git. O resultado limita a verificação agregada, sem diagnóstico fechado da causa do drift.

A verificação de specifications executada com `-X utf8` confirmou dois erros `contract without owner`, um para cada arquivo novo em `contracts/`. O verificador regenerou seu relatório global durante a execução. Esse relatório foi restaurado ao conteúdo anterior e ficou fora do diff.

A correção mínima exige autorização para acrescentar duas linhas em `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`, registrando BC-002 como owner de `policy.json` e `test_instance_policy.py`. Esse catálogo está fora dos dois write scopes. A integração permanece bloqueada até a correção autorizada e repetição dos gates.

O READY ordinário exige predecessores `done`. O índice da baseline registra STORY-0025 como `planned` e STORY-0040 como `closed-with-accepted-deferral`. A execução contratual foi autorizada pelo ato Owner sem declaração de READY ordinário.

A matriz de permissões é parametrizada pela política central explícita, conforme o freeze. As fontes examinadas não publicam concessões fixas para cada rótulo de papel. O preenchimento de uma matriz de privilégios concretos exige a definição aprovada dessas concessões. Esse limite impede declarar a matriz concreta integralmente entregue.

AC04_ORIGINAL_PACKAGE=MISSING. A proposta de reconstrução v1 exige aprovação específica. A rastreabilidade integral das 36 obrigações e seus vínculos individuais permanece pendente.

## Passes separados no candidato de conteúdo

QA executou dois testes novos, seleção ampliada de 173 testes, Ruff e diff check. Confirmou scopes e coerência da política parametrizada, com ressalva sobre a ausência de concessões concretas por papel. Reviewer executou os dois testes novos e os 170 do freeze e solicitou mudanças pelo catálogo de ownership. Ambos os passes usaram CPython 3.12.10 da venv e referenciaram o candidato de conteúdo acima. A repetição com o pin 3.12.13 foi feita pelo executor.

Os passes ocorreram em sessões Codex distintas. Independência pessoal é ausente no modelo solo. Esses registros preservam seus limites e não conferem DAA, READY, produção ou autorização de merge.

Migration não se aplica ao incremento contratual. Rollback por reversão do commit da entrega. Enforcement, persistência e calibração de produção continuam nos responsáveis executáveis do EPIC-009.
