# ISSUE-0670 — revisão do contrato do ruleset de `main`

## Decisão e limite

A `STORY-0560` congela o contrato público `main-ruleset-governance-contract`
`1.0.0`, sob autoridade de `BC-001`. O contrato define os invariantes do ruleset de
`main`, a identidade única de checks, a cobertura por CODEOWNERS, a política de
branches e a prova obrigatória para bypass auditado.

Esta história não altera o ruleset hospedado, `.github/CODEOWNERS`, workflows ou a
API HTTP. A materialização e a automação pertencem às histórias descendentes. O
OpenAPI é não aplicável porque o controle governa o repositório, não o runtime do
produto.

## Contrato, estados e autoridade

- Manifesto, schema fechado e exemplo versionado estão registrados no registry de
  ownership como contratos de `BC-001`.
- O estado contratual é `FROZEN`; `READY` é a condição de entrada e `IN_PROGRESS` o
  estado de execução da issue. A branch é curta e toda mudança em `main` passa por PR.
- O contrato versionado é a autoridade da política. O ruleset hospedado e a interface
  do GitHub são controles derivados; CODEOWNERS roteia review, mas não substitui a
  Delivery Approval Authority definida pela `ADR-058`.
- Estado de produto, banco e migration não se aplicam. RabbitMQ permanece somente
  transporte e telemetria permanece derivada e não autoritativa.

## Invariantes e fail-closed

- Push direto e automerge em `main` são rejeitados; decisões sobre gates sensíveis
  continuam exclusivas de humano autorizado.
- O contexto do check é sua chave de unicidade. Contexto duplicado, producer ambíguo,
  check obrigatório ausente ou resultado diferente de sucesso são rejeitados.
- Paths protegidos exigem owner resolvido. Aprovação de CODEOWNER é sinal de review,
  não attestation independente de entrega.
- Bypass é rejeitado por padrão. A exceção exige veredito da Delivery Approval
  Authority vinculado ao candidate SHA exato e record imutável com identidade do
  evento, ruleset, branch, ator, razão, instante e referência ao veredito.
- Ruleset ausente, owner ausente, evidência de bypass inválida ou SHA divergente não
  possuem fallback silencioso.

## Evidência dos critérios de aceitação

| Critério | Evidência no candidato |
|---|---|
| `AC-ISSUE-0670-01` | manifesto, schema fechado, exemplo e `test_epic_091_contrato` |
| `AC-ISSUE-0670-02` | os cinco requisitos do épico, suas fontes, testes canônicos e a evidência sentinela estão ligados no contrato |
| `AC-ISSUE-0670-03` | testes negativos cobrem push direto, automerge, checks duplicados, owner ausente, bypass inválido, SHA divergente e extensão implícita |
| `AC-ISSUE-0670-04` | versão `1.0.0`, estado `FROZEN`, SemVer, owners, autoridades e gate independente são explícitos |

## Compatibilidade, migration e rollback

Adições opcionais compatíveis permanecem na major 1. Relaxar qualquer rejeição,
alterar a chave de unicidade, a autoridade de aprovação ou os campos da prova de
bypass exige nova major e revisão do Arquiteto. Não há mudança de banco, estado
persistido, endpoint ou deployment; migration e rollback operacional não se aplicam.
Antes de consumo, rollback contratual é revert; depois de consumo pinado, a versão
permanece histórica e uma versão sucessora deve substituí-la.

## Riscos residuais e próximo gate

O candidato congela semântica e failure modes, mas não alega que o ruleset remoto ou
os workflows já foram materializados. A conta atual também pode não oferecer rulesets;
esse enforcement pertence às histórias descendentes. Aprovação independente do
`Reviewer` sobre o mesmo candidate SHA permanece obrigatória e não é autoatestada.

## TaskEnvelope

O envelope foi corrigido apenas para incluir seu próprio arquivo, os cinco requisitos
consumidos, a `ADR-058`, o registry de ownership, o teste obrigatório e o locator de
evidence já declarado. Não houve ampliação de data plane, dependência ou contrato
compartilhado.
