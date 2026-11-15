# TASK-0050 / ISSUE #126 — auditoria interrompida

Data: 2026-11-14 (America/Sao_Paulo). Papel: Reviewer.
Baseline: `7062b1432479e256cc673b5b313932e9b41dcecf`.
Branch: `codex/issue-126-final-audit`. Migration_required=false.

## Resultado

Auditoria parcial, sem aprovação de produto, QA, Reviewer, integração ou produção.
A correção administrativa precedeu o fetch/switch. Somente as duas listas
allow_paths da TASK-0050 foram alteradas: path de evidência corrigido e exceção
nominal do próprio envelope, válida exclusivamente para esta correção. A autorização
foi consultada no comentário do Owner, author_association=OWNER:
https://github.com/raphaelperrut/DSGeorref/issues/126#issuecomment-6885518384.
scope-check.json comprova igualdade semântica de todos os demais campos.

A #125 foi consultada no GitHub: closed/completed. Seu merge #1063 é a própria
baseline. Os seis commits de implementação/fix e respectivos merges são ancestrais
da baseline, conforme integrated-artifacts.json. Isso confirma integração, sem
equivaler a aprovação ou cobertura integral das histórias.

## Condição material de parada F-01

Os dois testes obrigatórios da instrução atual, da história e do envelope não
possuem implementação na baseline: `test_epic_010_aceite_happy_path` e
`test_epic_010_aceite_negative_paths`. A busca versionada em tests, src e contracts
não encontra referências (exit 1). A seleção pytest nas suítes de autorização,
segurança e contrato termina sem erro de importação, com 184 casos desmarcados,
zero coletados e exit 5. Logs e JUnit acompanham este relatório.

Nenhum desses testes foi executado; zero testes coletados não constitui PASS.
Há testes existentes de consolidação e segurança e evidências históricas válidas
como entradas da auditoria. Não foi demonstrada ausência de cobertura funcional
por causa da ausência dos nomes. Entretanto, não há mapeamento autorizado nesta
execução que permita registrar os dois resultados obrigatórios como executados.
Criar, renomear ou introduzir wrappers/testes de evidência contrariaria o escopo.

F-01 é BLOCKER do fechamento solicitado, especificamente da comprovação executável
final exigida para AC_01/AC_03 e dos resultados obrigatórios. Não é classificação
de vulnerabilidade ou defeito de produção. A auditoria completa foi interrompida;
não se inventam equivalência, falha funcional ou aprovação. A retomada precisa
de definição do Owner sobre uso explícito dos node IDs existentes como os cenários
de aceite, ou de uma baseline que já contenha os testes exigidos. Não foi criada
issue nem alterado requisito, contrato ou teste.

## Observações de integração anteriores à parada

O contrato resource-authorization 1.0.0 declara default deny, PostgreSQL autoritativo,
releitura de credencial/vínculo/policy e ausência de grant de artefato/caminho em
policy 1.1.0. BC-013 conserva publicação, resolução física, hashes e lineage.
`runtime_implemented=false` é snapshot de definição, já explicado no handoff
integrado da STORY-0047, não prova de inexistência dos builders integrados.

O teste integrado `test_story_0047_slice_consolidation` compara os três builders,
mesma IdentityTransactions, alteração de membership, isolamento, negativas de
artefato/caminho, logout e decisões persistidas. Os handoffs de STORY-0716/0717,
0047/0048/0049 descrevem uma composição central, CPU explícita sem fallback,
UI via SDK e validação adversarial. Isto sustenta coerência documental preliminar;
a coerência final e o fail-closed final NÃO são certificados nesta execução.

A matriz registra evidências históricas e testes existentes como referências,
sem declará-los reexecutados. Nenhuma capacidade de leitura autorizada de artefato
ou caminho físico, calibração de produção, integração BC-003/BC-013 real ou backend
acelerado é inferida. O épico não quita o requisito de evidência G2 na issue/PR:
nenhum PR ou publicação de mensagem foi solicitado ou realizado.

## Verificação global

Executado `make verify PYTHON=.venv/Scripts/python.exe PNPM=pnpm.cmd`, com o
parâmetro adicional abaixo e a toolchain existente workdir/task-0786-toolchain
no PATH e PYTHONDONTWRITEBYTECODE=1.

| Parâmetro | Valor |
|---|---|
| `OPENAPI_BASE_SHA` | `7062b1432479e256cc673b5b313932e9b41dcecf` |

Resultado FAIL, exit 2: Playwright não encontra Chromium no caminho LOCALAPPDATA
da sandbox. Qualidade Python e etapas frontend anteriores ao browser passaram;
as etapas posteriores não são declaradas executadas. make-verify.log é a fonte.
Classificação: limitação ambiental local; não prova regressão desta entrega.
Não houve instalação de browser nem correção de paths fora do escopo.
As falhas CRLF da stack nativa registradas nas histórias anteriores permanecem
históricas; esta execução não chegou àquele target e não as confirmou novamente.

## Riscos residuais

| ID | Severidade | Disposição |
|---|---|---|
| R-01 | MEDIUM | Duplicação de orchestration frontend da STORY-0048 permanece residual. O assessment integrado identifica sessão, SDK, expiração, correlação e reenvio sobrepostos. Não são políticas concorrentes; risco de divergência futura. Não corrigido, não convertido em issue. |
| R-02 | MEDIUM | Integração/runtime: testes históricos usam port de projeto e profile sintéticos, PostgreSQL real; UI usa respostas HTTP controladas. Não certificam fluxo completo com produtores reais ou produção. Limitação herdada, sem falha objetiva nova demonstrada nos ACs. |
| R-03 | LOW | REQ-AUTH-IMPL-007 mantém calibração em STORY-0762; elegibilidade conjuntiva é coberta na STORY-0049. Não transferir ownership nem afirmar limiares de produção. |
| R-04 | LOW | Gate local indisponível por Chromium; gate global verde permanece pendente. Não se afirma que corrigir o browser tornaria todo o gate verde. |

Achados novos: BLOCKER=1 (F-01, fechamento de evidência); HIGH=0; MEDIUM=0;
LOW=0. Riscos herdados catalogados separadamente: MEDIUM=2, LOW=2.
Ausência de achado HIGH não certifica as partes não auditadas.

## Limites e próximo gate

AC_01=PARTIAL; AC_02=PARTIAL; AC_03=NOT_CONFIRMED; AC_04=PENDING.
O pacote é comum para futuros QA e Reviewer, mas nenhum desses papéis independentes
aprovou o candidato da STORY-0050. A própria sessão não aprova o trabalho que gera.
API/database/frontend/geo/AI não alterados; migrations não alteradas.
Rollback consiste em reverter a correção administrativa e o pacote documental.
Não há backfill, cutover ou estado de aplicação novo.
