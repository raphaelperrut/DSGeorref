# ISSUE-0675 — revisão do contrato de fechamento da SPRINT-001

## Decisão e limite

A `STORY-0565` congela o contrato público
`sprint-001-closure-authorization-contract` `1.0.0`, sob autoridade de `BC-001`.
Ele define quando um candidate SHA pode avançar de evidência pendente para revisão
independente e, depois das aprovações exigidas, para autorização da primeira fatia
funcional.

Esta história não autoriza a fatia, não cria endpoint, não altera runtime, banco,
workflow ou evidência hospedada. Ela consome o contrato versionado do walking skeleton
sem reinterpretá-lo; materialização e automação pertencem às histórias descendentes.

## Contrato, estados e autoridade

- Manifesto, schema fechado e exemplo estão registrados como contratos de `BC-001`.
- Os estados são `EVIDENCE_PENDING`, `READY_FOR_INDEPENDENT_REVIEW`,
  `AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE` e `BLOCKED`; estado desconhecido é rejeitado.
- O contrato no repositório governa o gate. PostgreSQL/PostGIS continua autoritativo
  para estado do runtime, filesystem gerenciado para binários, RabbitMQ somente para
  transporte e telemetria permanece derivada e não autoritativa.
- Evidências e aprovações devem apontar ao mesmo candidate SHA exato e o registro de
  aprovação é imutável. A execução do runtime é responsabilidade downstream.

## Invariantes e fail-closed

- `REQ-EPIC-001` somente passa com
  `test_executable_foundation_gate_clean_room_end_to_end` verde, cobrindo diagnóstico
  ponta a ponta, migrations, contratos, CI, segurança mínima e clean-room bootstrap.
- O gate também exige evidências das ADRs 019–022, contratos congelados, máximo de dez
  requisitos por história, ausência de write scope transitório e runtime resolvido e
  assinado.
- Evidência ausente, não verde, conflitante ou vinculada a outro SHA bloqueia; violação
  de limite ou write scope bloqueia; aprovação independente ausente bloqueia.
- Não há autorização parcial, fallback silencioso, estado implícito ou extensão de
  schema não versionada.

## Evidência dos critérios de aceitação

| Critério | Evidência no candidato |
|---|---|
| `AC-ISSUE-0675-01` | manifesto, schema fechado, exemplo e `test_epic_092_contrato` |
| `AC-ISSUE-0675-02` | `REQ-EPIC-001`, sua fonte, teste canônico e evidência candidata estão ligados no contrato |
| `AC-ISSUE-0675-03` | testes negativos cobrem prova ausente, condição de saída inválida, SHA divergente, aprovação ausente, estado desconhecido e extensão implícita |
| `AC-ISSUE-0675-04` | versão `1.0.0`, estado `FROZEN`, SemVer, estados, autoridades e review independente são explícitos |

## Compatibilidade, migration e rollback

Adições opcionais compatíveis permanecem na major 1. Alterar estados, condições de
saída, autoridade ou política fail-closed exige nova major e revisão do Arquiteto.
Não há mudança de estado persistido ou deployment nesta história; migration e rollback
operacional não se aplicam. Antes de consumo, rollback contratual é revert; depois de
consumo pinado, uma versão sucessora deve substituí-la.

## Riscos residuais e próximo gate

O candidato congela o contrato e não alega que a autorização já ocorreu. QA e Reviewer
devem aprovar independentemente o mesmo candidate SHA nas histórias previstas; nenhuma
autoaprovação é registrada aqui.

## TaskEnvelope

O envelope foi corrigido somente para incluir seu próprio arquivo, o registry de
ownership, o teste obrigatório e o locator de evidence já declarado. Não houve nova
prerequisite nem ampliação do data plane.
