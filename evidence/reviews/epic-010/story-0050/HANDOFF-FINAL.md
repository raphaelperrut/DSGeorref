# Handoff final para revisão — TASK-0050 / #126

PREVIOUS_PARTIAL_SHA=e68a894c0310a52ed97f660ce5f8da4af3f39f61.
BASELINE_SHA=7062b1432479e256cc673b5b313932e9b41dcecf.
Branch: codex/issue-126-final-audit. Continuação exclusivamente no path autorizado.
Todos os arquivos do parcial e o envelope corrigido permanecem byte a byte intactos.

## Candidato e independência

O novo candidato é o commit que introduz este arquivo. Resolver seu SHA exato:
`git log -1 --format=%H -- evidence/reviews/epic-010/story-0050/HANDOFF-FINAL.md`.
O SHA completo é entregue ao Owner na resposta da execução. Sem autorreferência.

QA e Reviewer devem usar exatamente esse SHA, test_acceptance.py, os relatórios
final-run/acceptance-final.log/xml, happy-canonical-python.xml,
happy-canonical-surface.xml, negative-canonical-python.xml, validation-final.json,
TRACEABILITY-FINAL.csv, AUDIT-FINAL.md e os riscos R-01 a R-04 ali registrados.
O inventário integrado do parcial também é entrada comum. O manifest fixa digests
LF dos inputs/testes/evidências; alterações de código invalidam o resultado.

QA_APPROVAL=PENDING; INDEPENDENT_REVIEW_APPROVAL=PENDING. A conclusão desta sessão
é auditoria técnica e handoff, não aprovação independente do pacote que ela criou.
AC_04 está preparado para revisão no mesmo candidato; aprovação conjunta não quitada.
Sessões de agentes não substituem independência pessoal exigida pela governança.

## Reprodução

Python: .venv/Scripts/python.exe, 3.12.10. PYTHONPATH=src/backend;
PYTHONDONTWRITEBYTECODE=1; PYTEST_DISABLE_PLUGIN_AUTOLOAD=1.
Toolchain existente workdir/task-0786-toolchain no PATH, Node 24.20.0/pnpm 10.26.1;
PNPM=pnpm.cmd. Nenhuma instalação ou alteração de dependência.

PostgreSQL 16 descartável em loopback 127.0.0.1:55497, usuário auth_test,
base privada local_identity_validation; trust apenas local. Dados em
evidence/reviews/epic-010/story-0050/workdir/pg-ready, excluídos pelo padrão
workdir/ existente. IDENTITY_TEST_DSN usa esse host/port/base/user;
IDENTITY_MIGRATION_DSN=postgresql+psycopg://auth_test@127.0.0.1:55497/local_identity_validation.
Fixtures canônicas aplicam migrations integradas e limpam somente a base privada.
Ports de projeto/profile são sintéticos; criptografia, transações e auditoria reais.
Servidor encerrado no término. Não usar banco da aplicação para reproduzir.

Comando executado na raiz: `.venv/Scripts/python.exe -X utf8 -m pytest -v -s
-p no:cacheprovider --import-mode=importlib
evidence/reviews/epic-010/story-0050/test_acceptance.py::test_epic_010_aceite_happy_path
evidence/reviews/epic-010/story-0050/test_acceptance.py::test_epic_010_aceite_negative_paths
--basetemp=evidence/reviews/epic-010/story-0050/workdir/pytest-formatted
--junitxml=evidence/reviews/epic-010/story-0050/final-run/acceptance-final.xml`.
Usar novos paths de saída em revisão para preservar evidência append-only.

Resultado: 2 coletados, 2 PASS; filhos 9 Python happy + 1 superfície + 35 negativos.
Vitest declara 27 casos fora do filtro como skipped; o caso nominal selecionado
executou e passou. O harness rejeita skip desse caso, contagem vazia ou erro.
Ruff check e format --check passaram. Cinco injeções de falha foram rejeitadas.

make verify: FAIL_ENVIRONMENT_PREEXISTING_CRLF, exit 2; quatro falhas/15 passes
na stack nativa. Chromium foi encontrado na execução atual; frontend passou.
integration-tests não alcançado. Não há dispensa automática de CI/gate global.

## Entrega e próximo gate

NOVOS arquivos: test_acceptance.py, AUDIT-FINAL.md, HANDOFF-FINAL.md,
TRACEABILITY-FINAL.csv, validation-final.json e relatórios em final-run/.
Sem modificação de qualquer arquivo do parcial. Nenhuma alteração em produção,
tests/**, contratos, migrations, workflows, ADRs ou envelope. Migration_required=false.

STOP_CONDITION=NONE. READY_FOR_PR=YES, para revisão, sem abertura nesta execução.
READY_FOR_MERGE=NO. Aprovações independentes, CI e publicação da evidência G2 na
issue/PR continuam pendentes. Nenhuma nova issue foi criada para riscos residuais.
