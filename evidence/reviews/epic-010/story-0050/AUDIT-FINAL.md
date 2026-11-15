# ISSUE #126 / TASK-0050 — conclusão da auditoria

Baseline integrada: `7062b1432479e256cc673b5b313932e9b41dcecf`.
Parcial preservado: `e68a894c0310a52ed97f660ce5f8da4af3f39f61`.
Papel executor: Reviewer. Owner técnico: BC-002; CODEOWNERS: @raphaelperrut.

## Decisão e alcance

Resultado técnico: PASS_WITH_RESIDUALS para a capacidade integrada, nos boundaries
efetivamente entregues. Pronto para preparar PR de revisão; não aprovado para merge,
produção, G2 ou encerramento independente de QA. Nenhum PR foi aberto.
Este documento sucede a conclusão parcial; não apaga nem altera seus arquivos.

A autorização complementar do Owner (author_association=OWNER) resolve F-01:
https://github.com/raphaelperrut/DSGeorref/issues/126#issuecomment-6886060123.
O novo test_acceptance.py materializa somente os dois entrypoints de aceite dentro
do path autorizado e chama testes já integrados por node ID ou nome Vitest exato.
Segue o precedente evidence/reviews/usuarios-e-papeis-da-instancia/test_acceptance.py.
Nenhuma fixture, regra de autorização ou lógica funcional de teste foi copiada.
O envelope corrigido no parcial foi preservado sem nova edição.

Os dois entrypoints foram nominalmente coletados e executados: 2 PASS, zero
falhas/erros/skips. Dentro deles: 9 casos Python happy, 1 caso frontend nominal e
35 casos Python negativos. final-run/acceptance-final.xml e os três JUnits canônicos
copiados fixam os nomes e os resultados. Os 27 casos frontend fora do filtro são
reportados pelo Vitest como skipped; não são contados como executados. O único
caso selecionado é exigido nominalmente, sem skip, e foi executado com sucesso.

run_report exige returncode=0, JUnit existente, contagens coerentes, número exato
de casos selecionados e ausência de falha/erro/skip nos selecionados. Nos casos
Python também exige ausência total de skips. Nenhum subprocesso falho é convertido
em sucesso. final-run/failure-propagation.json registra cinco rejeições por injeção
na fronteira do subprocesso/JUnit. A tentativa inicial preservada propagou exit 4
aos dois entrypoints; seu cálculo de raiz foi corrigido no harness. Após formatação
final, os dois testes foram repetidos com PASS. Não houve falha canônica mascarada.

## Capacidade única e encadeamento

integrated-artifacts.json, preservado do parcial, lista os seis SHAs de implementação,
os merges e os objetos Git na baseline. Todos são ancestrais. A dependência #125
está closed/completed e seu merge #1063 é a baseline. A cadeia técnica é:

| História | Entrega integrada e compatibilidade |
|---|---|
| STORY-0046 / #122 | Contrato resource-authorization 1.0.0 compõe política central 1.1.0 e freeze existente; default deny, predicados, exceções, estados e redaction explícitos. Oracle é contratual, não autoridade runtime. |
| STORY-0716 / #159 | ResourceAuthorization e builder conferem hashes UTF8/LF, conta/credencial/policy atuais, vínculo e existência de projeto. Reutilizam IdentityTransactions, Access, PostgreSQL e observações duráveis. |
| STORY-0717 / #160 | Builder CPU delega ao Slice 1; modo default/CPU explícito não muda concessões. Modos não suportados são rejeitados antes de compor CPU. |
| STORY-0047 / #123 | Consolidação comprova mesmos serviços/UoW/DTO, releitura de membership, negativas, logout e observações; não cria outra implementação. |
| STORY-0048 / #124 | UI usa SDK gerado e decisões do servidor, com invalidação da apresentação e tratamento de erros. Não concede autorização por role local. Duplicação de orchestration permanece MEDIUM residual. |
| STORY-0049 / #125 | Validação adversarial do mesmo builder/serviço: isolamento, abuso, path, credenciais, policy, persistência e redaction; fix integrado torna a coleta portátil. |

PostgreSQL permanece autoritativo; não há autorização por broker, logs, filesystem,
cache de allow ou por este harness. Uma decisão consultada não é ticket de execução.
Regras de projeto/operação/artefato/caminho representam uma única capacidade:
account/project têm concessões explícitas; artefato, artifact_path e physical_path
continuam negados para todos os papéis na política 1.1.0. O épico não promete grant
de download nem cria resolvedor de filesystem. BC-013 mantém manifest, ownership,
publicação, hashes, lineage e resolução segura sob SPEC-005.

## Critérios finais e limites de aceite

| Critério | Conclusão verificável |
|---|---|
| AC_01 | PASS no escopo integrado. Contrato, DTO/SDK/UI, aplicação, composição CPU e observações PostgreSQL são observáveis nos testes canônicos executados. Não se afirma fluxo HTTP/UI/PostgreSQL ponta a ponta com produtores reais. |
| AC_02 | PASS. TRACEABILITY-FINAL.csv relaciona os quatro critérios, critérios de produto do épico, todos os requisitos vinculados, seis histórias, artefatos, testes e riscos. validation-final.json distingue reexecução atual de evidência histórica e fixa os bytes usados. |
| AC_03 | PASS no boundary aplicável. Negativas de projeto/conta/artefato/path/tipo/ação, abuso, autoridade, credencial/revisão/policy, PAT, auditoria obrigatória, contrato e modo não suportado continuam fail-closed. Nenhum allow de fallback. |
| AC_04 | Protocolo de mesmo candidato/evidência/risco estabelecido em HANDOFF-FINAL.md. QA independente e revisão do novo candidato permanecem PENDING. Não se declara que essas aprovações já ocorreram; o critério de aprovação conjunta não está quitado. |

Os invariantes de segurança e compatibilidade aplicáveis ao BC-002 foram
demonstrados pelos testes atuais e pelos outputs históricos preservados.
Nenhuma mudança geo/científica/IA: homografia, SGV e classic-first não foram
alterados nem recertificados. ADR-051 foi lida por referência, mas governa IA/SGV,
não concessões BC-002; a aplicabilidade já estava explicitada no design review
integrado da STORY-0046. ADR-028/030 governam identidade/autorização; ADR-055 rege
os campos de auditoria/redaction usados. Não se certifica todo BC-014.

REQ-AUTH-IMPL-007 tem evidência contratual na STORY-0046 e de conjunção de
elegibilidade na STORY-0049; calibração quantitativa permanece STORY-0762.
Não se transfere esse requisito ao Slice 1 nem se declara calibração de produção.
runtime_implemented=false no contrato é o snapshot de definição de STORY-0046,
explicado em handoffs integrados; o serviço runtime é observado nos testes atuais.
Nenhum desses registros históricos é interpretado como nova decisão normativa.

## Riscos residuais e gate global

| ID | Classe | Evidência, impacto e disposição |
|---|---|---|
| R-01 | MEDIUM herdado, não bloqueante | Assessment integrado da STORY-0048 confirma duplicação de sessão/SDK/expiração/reenvio. Risco futuro de divergência e manutenção; ambas delegam ao servidor. Sem evidência nova de violação dos ACs; não corrigido ou convertido em issue. |
| R-02 | MEDIUM herdado, não bloqueante | Ports de projeto/profile sintéticos nos testes; PostgreSQL real. UI usa HTTP controlado. Composição de recurso não certifica wiring HTTP ponta a ponta com BC-003/BC-013 reais. O adapter de desenvolvimento pode rejeitar tipos não suportados. Sem claim de produção, resolução física ou integração externa. |
| R-03 | LOW herdado | Calibração de throttling permanece STORY-0762. Estados/elegibilidade aplicáveis cobertos; não há claim de limiar, custo, SLA ou capacidade de produção. |
| R-04 | LOW ambiental/preexistente | make verify FAIL, exit 2: quatro falhas raw digest CRLF da stack nativa, 15 testes passaram. Os seis arquivos comparados são LF-idênticos à baseline; não alterados. Gate global verde em CI/checkout apropriado permanece obrigatório para integração. |

make verify foi executado com Node 24.20.0/pnpm 10.26.1 e Chromium instalado
explicitamente selecionado. Qualidade Python, frontend completo e etapas técnicas
anteriores à stack nativa passaram. integration-tests não foi alcançado.
final-run/make-verify.log e native-gate-diagnosis.json conservam a falha e a
comparação de bytes. A falha de Chromium do parcial continua preservada como
resultado anterior; não é o resultado da execução atual. Não houve correção fora
do escopo nem enfraquecimento do gate.

F-01=RESOLVED pela autorização e execução dos entrypoints. BLOCKER=0; HIGH=0.
MEDIUM=2 riscos herdados; LOW=2 limitações herdadas/ambientais; novos achados
funcionais=0. Esses riscos não impedem preparar PR para revisão, mas não dispensam
CI, revisão independente ou evidência G2 publicada na issue/PR. Nenhuma nova issue.

API/database/frontend/geo/AI, código de produção, tests/**, contratos, migrations,
workflows e ADRs inalterados. migration_required=false; rollback documental/harness,
sem backfill ou cutover. PostgreSQL descartável encerrado após a execução.
