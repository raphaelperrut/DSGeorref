# ISSUE-0665 — revisão do contrato de Issue Forms

## Decisão e limite

A `STORY-0555` congela o contrato público `issue-form-governance-contract`
`1.0.0`, sob autoridade de `BC-001`. O contrato define a taxonomia já presente no
repositório (`BUG`, `SPIKE`, `STORY` e `TASK`), o vínculo de cada tipo com seu
template e os campos semanticamente obrigatórios.

Esta história não altera `.github/ISSUE_TEMPLATE`, não implementa validator ou
workflow e não muda o OpenAPI. A materialização e a automação pertencem às histórias
descendentes. O HTTP foi classificado como não aplicável porque Issue Forms são uma
interface de governança do repositório, não uma operação do produto.

## Contrato, estados e autoridade

- Manifesto, schema fechado e exemplo versionado são os owners da fundação e estão
  registrados em `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`.
- O estado contratual é `FROZEN`; o repositório versionado é a autoridade da
  definição e dos sources de formulário. A interface do GitHub é projeção derivada.
- Estado de produto e migration não se aplicam. RabbitMQ permanece somente
  transporte e telemetria permanece derivada e não autoritativa.
- O contrato usa SemVer, rejeita propriedades desconhecidas e exige nova major com
  revisão arquitetural para qualquer mudança incompatível.

## Taxonomia e invariantes

- Os quatro tipos registrados correspondem aos templates versionados existentes:
  `bug.yml`, `spike.yml`, `story.yml` e `task.yml`.
- `STORY` representa trabalho implementável subordinado a épico encerrável. Além de
  identidade, parent, valor e escopo, exige critérios de aceitação, ADRs, riscos,
  testes, evidência, aplicabilidade de migration e rollback, conforme `REQ-GOV-002`.
- `BUG`, `SPIKE` e `TASK` preservam seus campos obrigatórios já publicados; nenhuma
  semântica adicional é introduzida por esta história.
- Issues em branco permanecem desabilitadas e relatos de segurança são direcionados
  ao canal privado.
- Tipo não registrado, campo obrigatório ausente, marker de obrigatoriedade inválido,
  bypass por issue em branco e fallback silencioso são rejeitados.

## Evidência dos critérios de aceitação

| Critério | Evidência no candidato |
|---|---|
| `AC-ISSUE-0665-01` | manifesto, schema fechado, exemplo e teste `test_epic_090_contrato` |
| `AC-ISSUE-0665-02` | `REQ-GOV-002`, sua fonte e seu teste canônico estão ligados no manifesto e no contrato |
| `AC-ISSUE-0665-03` | teste negativo cobre campo ausente, tipo desconhecido, issue em branco e fallback silencioso |
| `AC-ISSUE-0665-04` | versão `1.0.0`, estado `FROZEN`, SemVer, owners e gate de Reviewer são explícitos |

## Compatibilidade, migration e rollback

Adições opcionais compatíveis podem permanecer na major 1. Remoção ou renomeação de
tipo/campo, relaxamento de obrigatoriedade ou mudança de authority exige nova major e
revisão do Arquiteto. Não há mudança de banco, estado persistido, endpoint ou
deployment; migration e rollback operacional não se aplicam. Antes de consumo,
rollback contratual é revert; depois de consumo pinado, a versão permanece histórica
e uma versão sucessora deve substituí-la.

## Riscos residuais e próximo gate

O contrato prova taxonomia, campos e rejeições, mas não a conformidade atual dos
arquivos em `.github/ISSUE_TEMPLATE`; esse enforcement pertence às histórias
descendentes e não é alegado neste candidato. Aprovação independente do `Reviewer` no
mesmo commit permanece obrigatória; este documento não registra autoaprovação.

## TaskEnvelope

O envelope foi corrigido somente para incluir seu próprio arquivo, o registry de
ownership, o teste obrigatório e o locator de evidence já declarado. Não houve
ampliação de data plane, dependência ou contrato compartilhado.
