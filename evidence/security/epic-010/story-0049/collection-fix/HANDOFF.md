# PR #1063 — correção mínima de coleta da #125

Candidato anterior: `bc878f010fbe6311331139f9c6e23f5811ae3969`.
Novo candidato: commit que contém este suplemento; resolver com
`git log -1 --format=%H -- evidence/security/epic-010/story-0049/collection-fix/HANDOFF.md`.

A falha hospedada de foundation-ci é de portabilidade/coleta dos testes. O modo
padrão prepend do pytest importa este arquivo sem package pai, tornando inválido
`from .conftest import ADAPTER, CONTRACT`. A coleta conjunta também encontra outro
test_security.py em diretório irmão, causando colisão de nome de módulo nesse modo.

A correção fornece ADAPTER/CONTRACT pela fixture local authorization_composition
e renomeia o arquivo para test_resource_authorization_security.py. Não adiciona
sys.path, package, helper global ou mudança de configuração/workflow. Todos os
nomes de testes, parâmetros, assertions e decisões esperadas foram preservados.
Uma comparação AST em validation.json demonstra que somente a dependência de
fixture, o import removido e os nomes locais da composição mudaram.

Validação focada, sem nova QA completa:

- Coleta com os mesmos seletores do gate hospedado, modo padrão: 113 coletados,
  zero erros; hosted-collection.log.
- Execução direta do diretório no modo padrão: 27 passed, zero skips/erros/falhas;
  default-tests.log/xml.
- Modo local importlib com as 11 regressões diretas: 38 passed, zero skips/erros/
  falhas; importlib-tests.log/xml. São 38 casos distintos e 65 execuções somando
  os dois modos. Happy path obrigatório e 10 cenários negativos preservados.
- Ruff check, format --check e git diff --check passaram nos arquivos alterados.

Comando de coleta: `python -m pytest -q -p no:cacheprovider --collect-only`, seguido
de tests/backend/identity_access/local_identity/test_requirements.py,
test_identity_requirements.py, test_http.py, test_development_surface.py,
test_slice_consolidation.py::test_oidc_session_can_issue_and_revoke_pat
(todos no mesmo diretório) e tests/security/contexts/identity_access.
Execução padrão: `python -m pytest -q -p no:cacheprovider` com o diretório de
segurança da #125. Execução local adiciona `--import-mode=importlib` e
tests/backend/identity_access/resource_authorization/test_resources.py.
Cada execução usa --junitxml apontando ao relatório correspondente e --basetemp
dentro de ../.runtime. Mesmo Python, ambiente e PostgreSQL privado documentados
no handoff original; nenhuma credencial é registrada. A base foi reiniciada
exclusivamente para esta validação focada.

Produção, contratos, domínio, frontend, migrations e workflows não foram alterados.
Fail-closed e controles de abuso, autorização, secrets, path e redaction mantêm
as mesmas assertions; egress segue NOT_APPLICABLE por ausência de saída externa.
Não existe autoridade paralela. A falha CRLF local e os relatórios antigos ficam
preservados como evidência histórica do candidato anterior. O usuário confirmou
make verify hospedado PASS nesse candidato; não houve nova execução do gate
global nesta correção de coleta. foundation-security anterior: SUCCESS confirmado
nos checks hospedados; resultado do novo SHA deve ser observado separadamente.

Este suplemento acrescenta os resultados e digests dos novos bytes sem reescrever
evidência revisada. A QA anterior não é atribuída ao novo SHA; a próxima etapa é
somente a revalidação curta solicitada. Publicar na mesma branch/PR, sem amend,
rebase ou PR novo.
