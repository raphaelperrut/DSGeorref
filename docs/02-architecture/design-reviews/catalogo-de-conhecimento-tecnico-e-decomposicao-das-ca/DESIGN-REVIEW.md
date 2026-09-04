# ISSUE-0136 — revisão do contrato de catálogo de capacidades

## Decisão e limite

A `STORY-0026` congela o contrato público `capability-catalog-foundation-contract`
`1.0.0`, sob autoridade de `BC-001`. O contrato define os campos obrigatórios de
cada capability, a unidade de decomposição, a separação entre conhecimento técnico
e runtime anterior, a proteção dos corpora e os owners de estado.

Esta história não materializa o inventário, não importa código, plugin ou runtime de
sistemas anteriores, não muda `GET /capabilities` e não libera dependentes. A
materialização e a automação pertencem às histórias explicitamente dependentes.

## Contratos e autoridade

- O manifesto, o schema fechado e o exemplo versionado são os owners desta
  fundação; os três artifacts estão registrados em
  `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`.
- `GET /capabilities` continua sendo a projeção pública congelada de disponibilidade
  em runtime. Este contrato não amplia seu payload.
- O repositório versionado é autoritativo para esta definição contratual;
  PostgreSQL/PostGIS permanece autoritativo para estado de runtime, filesystem
  gerenciado para binários publicados, RabbitMQ somente para transporte e
  telemetria como derivação não autoritativa.
- O contrato usa SemVer, rejeita propriedades desconhecidas e exige nova major com
  revisão arquitetural para mudança incompatível.

## Invariantes e falhas

- Cada capability materializada deve possuir nome estável, estágio, entradas,
  saídas, requisitos de hardware, orçamento, determinismo, limitações, explicação ao
  operador, owner e contrato.
- Sistemas anteriores podem fornecer somente requisitos e corpus atribuível. Código,
  plugins e runtime anteriores são proibidos.
- Corpora exigem separação de desenvolvimento, validação protegida e holdout cego,
  além de origem, licença, SHA-256 e integridade de acesso.
- Descriptor inválido, evidência de corpus ausente, sobreposição de split, runtime
  anterior detectado e fallback silencioso falham fechados.

## Evidência dos critérios de aceitação

| Critério | Evidência no candidato |
|---|---|
| `AC-ISSUE-0136-01` | manifesto, schema, exemplo e referência à interface pública congelada |
| `AC-ISSUE-0136-02` | `REQ-AI-007` e `REQ-TST-001` rastreados no manifesto e no contrato |
| `AC-ISSUE-0136-03` | schema fechado e teste negativo contra fallback, importação de runtime e corpus sem evidência |
| `AC-ISSUE-0136-04` | versão, estado `FROZEN`, SemVer, owners de dados e gate de Reviewer explícitos |

## Compatibilidade, migration e rollback

Não há mudança de endpoint, banco, runtime ou deployment; migration e rollback
operacional não se aplicam. Antes de consumo, rollback contratual é revert; após
consumo, uma versão compatível substitui a anterior ou uma nova major passa por
revisão arquitetural.

## Riscos residuais e próximo gate

O contrato prova forma e invariantes, não a completude de um inventário executável
nem a segregação operacional dos corpora. Esses claims dependem das histórias
seguintes. Aprovação independente do `Reviewer` no mesmo candidato permanece
obrigatória; este documento não registra autoaprovação.
