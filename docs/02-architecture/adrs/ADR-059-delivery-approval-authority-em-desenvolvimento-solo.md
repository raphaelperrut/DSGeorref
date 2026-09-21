# ADR-059 — Delivery Approval Authority em desenvolvimento solo

- **Status:** `Accepted — efetiva prospectivamente para DAA 2.0.0`
- **Baseline proposta:** `Owner Decision — APPROVE_SOLO_GOVERNANCE_PROPOSAL — 2026-09-20`
- **Decisão do Owner:** `https://github.com/raphaelperrut/DSGeorref/issues/974#issuecomment-5752923713`
- **Pacote aprovado:** `sha256:8240a2096557dbc26a0f3546ebefafcad00b598c80f95ff1dd923eb33e20ca42`
- **Raiz DAA 2.0.0 aceita:** `daa2-operational-profile-root-2026`, fingerprint `sha256:7eee2d0b947f124fbacd9987e599e06fe5c1c8e36d3ba87b7c117669e5cd59ae`
- **Aceitação da raiz:** `https://github.com/raphaelperrut/DSGeorref/issues/974#issuecomment-5753593051`
- **Aprovador da direção:** `Project Owner`
- **Owner normativo:** `ADR-059`
- **Substitui:** `ADR-058` prospectivamente; DAA 1.0.0 permanece sob ADR-058
- **Boundary independente:** `SIM`
- **Bounded Contexts:** `BC-001` — Governança de Engenharia e Entrega

## Estado de vigência

Esta ADR está ativa prospectivamente para records DAA `2.0.0` selecionados pelo trust profile
operacional assinado e fixado pelo verifier. A `ADR-058` permanece a autoridade histórica e
semântica exclusiva de records DAA `1.0.0`; nenhum record anterior é reinterpretado.

## Contexto

O DSGeorref é desenvolvido por uma única pessoa, que exerce legitimamente as funções de
Project Owner, Tech Lead, Executor, QA e Reviewer. A `ADR-058` modela independência somente
como disjunção entre accountable subjects. Aplicar essa regra ao contexto real exigiria
identidades fictícias, uma alegação falsa de independência pessoal ou bloqueio permanente.

A ausência de independência pessoal não elimina a necessidade de autenticação, autorização
por papel, revisão separada, integridade das evidências, vínculo ao mesmo candidato e decisão
formal fail-closed. Ela precisa ser registrada como limitação explícita, e não ocultada por
contas, chaves ou sessões artificiais.

## Decisão proposta

- A Delivery Approval Authority mantém o regime `INDEPENDENT_SUBJECTS_V1` da `ADR-058` para
  evidências históricas e contextos com accountable subjects realmente disjuntos.
- É criado o regime `SOLO_FUNCTIONAL_SEGREGATION_V1`, autorizado apenas por política assinada
  no trust profile para TaskEnvelopes nominados.
- No regime solo, Executor, QA, Reviewer e Project Owner usam uma única identidade real no
  formato `issuer + subject` e um único accountable subject real.
- Todo record solo declara `PERSONAL_INDEPENDENCE=ABSENT_DECLARED`. Chaves distintas ou sessões
  distintas não constituem independência pessoal.
- Cada função possui binding, chave de attestation, evidence record e sessão funcional próprios.
  Esses elementos provam segregação funcional e impedem cross-use silencioso, mas permanecem
  sob responsabilidade da mesma pessoa.
- As atuações são sequenciais: Executor, QA, Reviewer e Project Owner. Cada atuação posterior
  vincula o digest canônico da attestation imediatamente anterior, além do mesmo TaskEnvelope,
  digest canônico e candidate SHA.
- O Executor registra `DELIVERED`; QA e Reviewer registram `APPROVE` ou `REJECT`; o Project Owner
  registra a decisão formal `PASS` ou `NO_GO`.
- `PASS` exige a cadeia completa e válida terminada por `DELIVERED`, `QA=APPROVE`,
  `Reviewer=APPROVE` e decisão autêntica `Project Owner=PASS`.
- `NO_GO` autêntico resulta em verdict de entrega `FAIL`. Ausência de decisão, record, binding,
  assinatura, escopo, predecessor ou vínculo exato permanece `FAIL` sem fallback.
- O modo de governança é resolvido exclusivamente da política operacional assinada. O caller
  não pode selecionar, enfraquecer ou substituir o modo.

## Independência funcional e independência pessoal

`Independência funcional` significa que cada função é executada em uma sessão distinta, sobre
um snapshot imutável, com objetivo, resultado, binding, chave de função, ordem e lineage
criptograficamente registrados.

`Independência pessoal` significa julgamento por accountable subjects humanos distintos. Ela
não existe no regime solo. O verdict e o gate devem expor essa ausência literalmente; não podem
usar `independent`, `independent approval` ou expressão equivalente para descrever pessoas.

## Records mínimos do regime solo

Cada role binding e attestation declara o regime autorizado. Cada attestation inclui:

- identidade e accountable subject reais;
- papel e decisão permitida para o papel;
- TaskEnvelope ID e digest canônico;
- candidate SHA exato;
- `session_id`, papel, sequência, início e digest do snapshot de entrada;
- digest da attestation predecessora, exceto para Executor;
- instante de emissão e assinatura com domínio da versão do contrato.

Bindings, chaves de função, attestations e sessões são distintos entre os quatro papéis. O
verifier exige uma única identidade e um único accountable subject no modo solo, ao mesmo tempo
em que rejeita reutilização de chave, binding, attestation ou sessão entre funções.

## Autenticação, integridade e trust boundary

- O trust boundary, trust scope, SHA-256, Ed25519, canonicalização e custódia externa não
  mudam. A DAA `2.0.0` usa uma nova raiz pública versionada e explicitamente aceita pelo
  Project Owner; a raiz `1.0.0` permanece fixada para verificação histórica.
- O profile assinado autoriza o modo por TaskEnvelope, os issuers, as chaves e os papéis.
- Autenticação não concede papel; cada papel exige binding autêntico da autoridade competente.
- Nenhuma chave privada pertence ao repositório.
- GitHub, labels, CODEOWNERS, contagem de approvals, autoria Git, `SPEC-001` e assinatura de supply
  chain não substituem records da Delivery Approval Authority.
- Identidade, binding, assinatura, escopo, validade, revogação, TaskEnvelope, digest, candidate SHA,
  sequência, lineage e decisão são verificados antes de promover qualquer valor como confiável.

## Compatibilidade histórica

- Attestations DAA `1.0.0` preservam integralmente a semântica da `ADR-058`.
- Sobreposição de accountable subjects continua sendo `INDEPENDENCE_VIOLATION` sob DAA `1.0.0`.
- Nenhum record antigo é convertido, reinterpretado ou promovido para o regime solo.
- Verificação histórica usa a revisão governada original, seus schemas, profile e instante explícito.
- DAA `2.0.0` usa schemas e domínios de assinatura próprios para impedir downgrade ou cross-version
  ambiguity.

## Consequências e riscos residuais

- Segregação funcional melhora disciplina e auditabilidade, mas não remove self-review bias.
- Comprometimento ou coerção da única pessoa pode afetar todos os papéis, mesmo com chaves distintas.
- A cadeia assinada prova conteúdo, ordem declarada e imutabilidade; sem timestamp externo, ela não
  prova que as sessões foram criadas por pessoas diferentes ou em tempo independente.
- Perda da custódia externa pode bloquear entrega até rotação ou recuperação governada.
- Esses riscos são declarados no gate e aceitos pelo Project Owner; não são convertidos em
  independência pessoal por linguagem ou implementação.

## Alterações normativas requeridas

- Contrato DAA versionado para `2.0.0`, sem modificar os schemas `1.0.0` existentes.
- Profile operacional `2.0.0` assinado, com política solo limitada a `TASK-0764`.
- Bindings e attestations `2.0.0` para Executor, QA, Reviewer e Project Owner.
- Verifier com seleção de regime somente pelo profile assinado, validação da sequência e decisão
  formal do Owner.
- Verdict que exponha regime, `PERSONAL_INDEPENDENCE=ABSENT_DECLARED`, sessões validadas e decisão
  formal, retornando `FAIL` para `NO_GO` ou qualquer ausência/divergência.

Nenhum serviço, banco, endpoint, issuer, anchor, algoritmo ou autoridade nova é criado.

## Condições de ativação

A substituição da `ADR-058` somente se torna efetiva quando:

1. AC-03, AC-04 e AC-06 da Issue #974 estiverem atualizados com rastreabilidade à decisão do Owner;
2. `TASK-0764` estiver validado e explicitamente autorizado pelo Tech Lead por seu digest atual;
3. contrato e verifier DAA `2.0.0` passarem regressões focadas, incluindo preservação da semântica
   DAA `1.0.0` e casos negativos do regime solo;
4. profile operacional `2.0.0`, bindings e chaves públicas legítimas forem emitidos pelas autoridades
   competentes sem material privado no repositório;
5. nenhuma evidência histórica for reinterpretada e nenhum consumidor diretamente afetado regredir.

As condições foram satisfeitas pela atualização rastreável dos critérios, autorização do
`TASK-0764` pelo digest canônico, regressões focadas DAA `1.0.0`/`2.0.0` e integração do profile e
bindings autenticamente assinados. A ativação não aprova o gate da Issue #974: ele permanece
fail-closed até a cadeia sequencial de attestations e a decisão formal do Project Owner.

## Gate de mudança

Mudança na fonte de autoridade, identidade canônica, distinção entre independência pessoal e
funcional, sequência obrigatória, payload assinado ou semântica fail-closed exige nova ADR
substituta. Issuers, chaves, validade, rotação e revogação permanecem no profile versionado quando
preservarem esta decisão.

## Verificação de conformidade

- rejeitar seleção de modo fornecida pelo caller;
- rejeitar modo solo não autorizado para o TaskEnvelope;
- rejeitar identidade ou accountable subject fictício, ausente ou divergente;
- rejeitar declaração de independência pessoal no modo solo;
- rejeitar key, binding, attestation ou sessão reutilizada entre papéis;
- rejeitar ordem, predecessor, TaskEnvelope digest ou candidate SHA divergente;
- preservar todos os casos históricos DAA `1.0.0`;
- retornar `FAIL` para `NO_GO`, decisão ausente e qualquer evidência incompleta ou inválida.

## Relação com a ADR-058

Após ativação, esta ADR substitui a `ADR-058` prospectivamente. A `ADR-058` permanece a autoridade
histórica para records DAA `1.0.0`; sua semântica não é revogada nem reinterpretada.
