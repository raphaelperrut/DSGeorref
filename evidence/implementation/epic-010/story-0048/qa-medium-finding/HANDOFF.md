# Handoff — versionamento da avaliação residual

Data: 2026-11-14. ISSUE #124 / TASK-0048. Executor: Frontend.
Candidato anterior: `16a8c928244a3deb72dcedcbac196090e3b47cf5`.
Novo candidato: commit que adiciona este arquivo e `validation.json`; obter o SHA
com `git log -1 --format=%H -- evidence/implementation/epic-010/story-0048/qa-medium-finding/HANDOFF.md`.
A referência indireta evita autorreferência circular entre SHA e conteúdo.

O Owner autorizou nesta continuação versionar a avaliação já produzida. Os textos
em `DUPLICATION-ASSESSMENT.md` e `assessment.json` são snapshots da avaliação
anterior, quando os suplementos ainda eram locais e o SHA permanecia inalterado.
Seu conteúdo foi preservado; suas menções a arquivos não commitados e candidato
inalterado descrevem aquele instante. Este handoff e o novo `validation.json`
registram a posterior inclusão dessas evidências no novo candidato.
O handoff/validation originais do candidato revisado também permanecem intactos.

## Disposição do achado

- Duplicação efetiva de orquestração confirmada; não é apenas semelhança superficial.
- SAFE_REUSE_AVAILABLE=NO: a API pública existente não oferece composição seletiva
  compatível; o hook interno não preserva os dados HTTP/invalidação necessários.
- A correção adequada requer alteração do produtor fora do escopo TASK-0048.
  Nenhuma alteração de código, novo framework/package, contrato, arquitetura ou
  ampliação de allow_paths foi aplicada.
- MEDIUM_FINDING_STATUS=RESIDUAL. Risco: divergência futura entre duas
  orquestrações e necessidade de manutenção coordenada.
- Fail-closed, Problem Details, idempotência e os quatro contratos são preservados.
  A implementação é idêntica à do candidato anterior; detalhes e fundamento estão
  em `DUPLICATION-ASSESSMENT.md`.

## Validação do candidato somente de evidência

Reexecutado apenas o arquivo frontend co-localizado da nova feature:
`surface.test.tsx`: **28 PASS, zero falhas/skips**, incluindo nominalmente
`test_epic_010_superficie`. Comando e resultado em `evidence-only-tests.log`;
resultado individual no JUnit `evidence-only-tests.xml`.

Regressões amplas, browser, backend e make verify não foram repetidos, conforme
instrução explícita do Owner para esta etapa exclusivamente de evidência.
O último make verify permanece FAIL por quatro falhas preexistentes de raw digest
CRLF/LF na stack nativa; não se declara novo resultado nem gate global verde.

`validation.json` vincula o novo candidato ao pai, registra os arquivos de
evidência adicionados e os digests UTF8_LF. As comparações conferem os digests
originais, os arquivos inspecionados e a ausência de mudanças rastreadas no código,
na feature preexistente, TaskEnvelope, contratos e arquitetura.
O arquivo preexistente `src/frontend/debug.log` continua excluído.

BLOCKER_HIGH=NO, conforme resultado de QA fornecido pelo Owner; nenhum novo
BLOCKER/HIGH identificado nesta etapa. READY_FOR_QA=YES para revisar as evidências
no novo candidato. Não se transfere automaticamente a aprovação do SHA anterior:
QA/Reviewer devem referenciar o novo SHA. Nenhum PR foi aberto.
