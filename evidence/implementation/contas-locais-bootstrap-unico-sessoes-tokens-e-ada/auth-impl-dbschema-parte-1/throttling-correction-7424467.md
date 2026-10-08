# STORY-0712 / ISSUE-0822 — correção de throttling interrompida

Data: 2026-10-05 (America/Sao_Paulo).
Base: `74244676336ed6770749acbfcba1bf6558d09884`.
Branch: `codex/issue-0822-task-0712-throttling`.
Resultado: BLOCKED; implementação e aceite runtime não demonstrados; sem aprovação QA.

## Alteração formal

TASK-0712 inclui REQ-AUTH-IMPL-007 em references/acceptance_criteria,
test_req_auth_impl_007 e os dois testes finais de aceite do EPIC-008 em
tests/phase_f_review.tests.items, e esta evidência em ambos os campos evidence.
Allow/deny paths e os demais requisitos permanecem iguais. Os registros históricos
de revisão do envelope não representam aprovação desta correção.

## Condição de parada

O contrato congelado `identity-access-local-auth-freeze`, em
`contracts/contexts/identity_access/plt/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/contract.json`,
define `invariants.quantitative_policy = APPROVED_PROFILE_ONLY` e
`policies.throttling.quantitative_values`: somente perfil aprovado no runtime;
ausência/invalidez implica DENY. ADR-031 reserva parâmetros quantitativos aos
Application Profiles ou Benchmark Profiles.

Nenhum perfil aplicável com limites de throttling foi fornecido ou referenciado
pelos insumos autorizados nesta execução. O `SecurityProfile` de local_identity
contém calibração Argon2id e lifetimes, mas não limites/janelas de throttling.
`examples.json` fornece somente valores explicitamente sintéticos. O fixture
atual injeta `lambda store, operation, actor: True` no port de elegibilidade.

Assim, escolher um limite aplicável ou tratar exemplos como perfil aprovado
exigiria inventar política quantitativa. A execução para conforme a instrução
do usuário e `TASK-0712.stop_conditions`: decisão material não resolvida.
É necessário fornecer o perfil aprovado aplicável antes de implementar e
demonstrar enforcement. Nenhum contrato compartilhado foi alterado.

## Verificação focada

Comando executado com `.venv/Scripts/python.exe`:

```text
python -m pytest contracts/contexts/identity_access/plt/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/test_auth_freeze.py -k 'test_req_auth_impl_007 or test_epic_008_aceite_happy_path or test_epic_008_aceite_negative_paths' -q
```

Observado: 1 passed, 169 deselected; aviso de permissão do cache pytest.
Esse PASS é somente o teste preexistente de contrato/examples, não evidência
de implementação. Os dois testes finais não existem e não foram criados.
Nenhum teste adjacente de runtime foi necessário para esta alteração de envelope.
Os Python global e bundled não tinham pytest; o ambiente `.venv` executou o teste.

`make verify` foi executado. A primeira tentativa usou Python global sem ruff.
Com `.venv/Scripts` no PATH, ruff, mypy, OpenAPI check/diff e frontend typecheck
passaram. O comando terminou com exit 1 em frontend:test:unit: as três suites
não coletaram testes porque o sandbox recusou rename de arquivos temporários
do Vitest (EPERM). Não houve correção de frontend ou alteração fora do slice.
Portanto, `make verify` não passou nesta execução.

## Runtime — ação -> esperado -> observado

- Operação abaixo do limite -> permitir conforme perfil aprovado -> não executada: perfil aplicável ausente.
- Consultar estado persistente -> bucket PostgreSQL observável -> não executada; estado de throttling não implementado.
- Exceder limite -> rejeitar fail-closed -> não executada: limite aplicável indefinido.
- Operação posterior -> respeitar bloqueio/liberação do perfil -> não executada: perfil aplicável ausente.

Nenhum serviço foi iniciado; nenhuma tabela/migration foi criada ou aplicada.
Não se afirma enforcement fail-closed de throttling nem compatibilidade runtime
validada nesta execução. Código e testes preexistentes não foram modificados.
Os arquivos untracked preexistentes em evidence/reviews foram preservados e
não pertencem a esta alteração. Não há rollback de dados; a alteração formal
pode ser revertida pelo commit correspondente.
