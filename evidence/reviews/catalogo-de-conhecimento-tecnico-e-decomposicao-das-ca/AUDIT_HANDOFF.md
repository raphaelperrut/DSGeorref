# ISSUE-0140 / GitHub #42 — evidência para auditoria final

Entrega de **Writer/Implementation**, atribuída pelo solicitante, para
`TASK-0030` / `STORY-0030` / `EPIC-006` / `BC-001`. O papel normativo Reviewer
do envelope permanece inalterado: este documento não é sua aprovação.

Base integrada: `f711c8a3cc0c78287d944a116ef0528891b98f62` (`main`).
A implementação da dependência `STORY-0029` está presente nessa base; sua
evidência histórica não foi promovida a aprovação do novo candidato.

## Critérios e evidência executável

| Critério | Implementação/evidência | Resultado do Writer |
| --- | --- | --- |
| AC-ISSUE-0140-01 | `test_epic_006_aceite_happy_path` executa a integração real da fundação e automação duas vezes; exige saída determinística, PASS, ausência de findings e control plane read-only. | PASS |
| AC-ISSUE-0140-02 | O mesmo teste exige evidência de `REQ-AI-007` e `REQ-TST-001`, valida o TASK-0030 contra seu schema e confere paridade de allow/deny paths e destinos de evidência. Testes de contrato, inventário sem importação de legado e corpus verificam as fontes integradas. | PASS |
| AC-ISSUE-0140-03 | `test_epic_006_aceite_negative_paths` exige FAIL e exit code não zero para predecessores ausentes, SHA-256 adulterado e fallback silencioso. A automação existente também cobre contrato ausente, autoaprovação, drift, splits/acesso, fontes inseguras e ausência de ações destrutivas. | PASS |
| AC-ISSUE-0140-04 | QA sentinela e handoff para Reviewer compartilham o SHA final, os comandos e os riscos registrados no PR. Não há aprovação implícita; QA e Reviewer independentes devem registrar seus pareceres nesse mesmo SHA. | PENDENTE de evidência/aprovação independente |

`REQ-AI-007`: catálogo com owners e contratos publicados; nenhum runtime de
capability é implementado nesta entrega. `REQ-TST-001`: sentinelas sintéticas
com origem, licença, hashes, splits e classes de acesso verificáveis.
A política classic-first de ADR-051 não muda; estes resultados não autorizam
escalonamento neural nem aceitação científica.

## Validações

Comandos executados a partir da raiz, com Python 3.12:

```text
py -3.12 -m pytest -q -p no:cacheprovider evidence/reviews/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_acceptance.py tests/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca tools/governance/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_repository_integration.py
py -3.12 -m pytest -q -p no:cacheprovider evidence/reviews/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_acceptance.py tests/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_automation.py
py -3.12 -m ruff check evidence/reviews/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_acceptance.py
py -3.12 -m mypy --strict evidence/reviews/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_acceptance.py
make verify PYTHON="py -3.12"
git diff --check
```

A primeira execução produziu 13 passes, 1 falha e 3 erros: a falha e os erros
ocorreram por acesso negado aos diretórios temporários pelo sandbox. Somente
os arquivos afetados foram repetidos fora do sandbox: **5 passes**, incluindo
os quatro casos de aceite. Assim, os **17 casos distintos** da seleção foram
validados, reaproveitando os 12 passes não afetados da primeira execução.
Ruff passou. A validação do schema do envelope integra o teste happy path.
A checagem adicional de tipos do novo teste foi inconclusiva por ausência dos
stubs `types-jsonschema` (um erro `import-untyped`); não se alteraram dependências
nem se suprimiu o diagnóstico.

O `make verify` foi executado exclusivamente pela obrigação do `AGENTS.md`.
A primeira tentativa encontrou `spawn EPERM` no Vitest; foi repetida fora do
sandbox. Nessa repetição passaram Ruff, mypy do escopo global, TypeScript,
Vitest, Playwright Chromium, validação do repositório, arquitetura, requisitos,
DDD, ADRs, especificações, sprint, arquitetura Python e contrato da fundação.
O teste global final terminou com **4 passes e 1 falha**: o walking skeleton
exige `FOUNDATION_INTEGRATION=1` e os serviços PostgreSQL/RabbitMQ versionados.
A variável está ausente e não há comando Docker disponível neste ambiente.
O gate global permanece **ENVIRONMENT_BLOCKED**; não foi contornado nem tratado
como PASS. O mesmo impedimento já consta da evidência integrada de STORY-0029.

## Escopo e inspeção final

- `.codex/tasks/TASK-0030.json`: autoriza a correção do próprio envelope e
  alinha suas duas referências de evidência ao diretório já permitido;
  mantém deny paths, critérios, dependência e papel normativo.
- `evidence/reviews/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_acceptance.py`:
  os dois testes obrigatórios, sem novo checker, contrato ou camada de produção.
- Este handoff: rastreabilidade, resultados, limitações e próximo gate.

Os testes exercitam os entry points existentes via subprocessos e alteram
somente fixtures temporárias. Nenhum contrato, registry, checkpoint, código
de produto, endpoint, banco, broker ou estado foi modificado. Não há migration
ou rollback operacional aplicável; rollback da entrega é a reversão do commit.
Nenhuma prerequisite foi criada e nenhuma decisão arquitetural é necessária.

## SHA, independência e riscos residuais

O PR registra explicitamente `IMPLEMENTATION_SHA` e `PR_HEAD_SHA` após o commit.
Ambos identificam o mesmo candidato para os comandos acima e o handoff.
Para verificar os arquivos auditados, usar `git show <PR_HEAD_SHA>:<path>`;
mudança de código ou testes invalida estes resultados. A evidência deve ser
preservada e novos pareceres adicionados sem reescrever uma revisão concluída.

O Reviewer e o QA independente devem citar o **SHA final literal do PR**, este
handoff e os riscos abaixo. Seus pareceres ainda não foram produzidos pelo
Writer; a auditoria final da issue não está aprovada. Nenhum merge, fechamento
da issue ou autoaprovação integra esta entrega.

- O corpus é sintético e prova controles, não qualidade científica ou proteção
  operacional de dados reais. Não há claim de custo, escala ou performance.
- O pytest emite depreciação preexistente de `asyncio_default_fixture_loop_scope`.
- O Node local é 22.14.0 e o repositório pede 24.20.0; o gate frontend informa
  esse desvio. Esta issue não altera o runtime nem sua configuração.
- A evidência sentinela do Writer é suficiente para iniciar Review, mas não
  substitui a aprovação independente exigida pelo AC-ISSUE-0140-04.
- A conclusão integral está bloqueada pelo gate global e pela aprovação
  independente pendentes; o PR é draft. Não foi encontrado blocker ou HIGH
  arquitetural que justifique uma nova prerequisite.
