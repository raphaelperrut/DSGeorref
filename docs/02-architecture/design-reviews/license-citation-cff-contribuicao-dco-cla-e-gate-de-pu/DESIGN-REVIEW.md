# ISSUE-0141 — revisão do contrato de licença, citação, contribuição e publicação

## Decisão e limite

A `STORY-0031` congela o contrato público
`license-publication-governance-contract` `1.0.0`, sob autoridade de `BC-001`.
Ele consolida as decisões já aprovadas para licenças por classe de conteúdo,
metadados de citação, DCO/CLA e bloqueio da publicação por evidência incompleta.

Esta história é somente contratual. Ela não materializa `CITATION.cff`, textos
integrais de licença, notices, inventários, automações ou release gates, e não
declara o repositório pronto para publicação. Esses resultados pertencem às
histórias downstream do épico.

## Contratos e autoridade

- O manifesto, o schema fechado e o exemplo versionado são os owners desta
  fundação e estão registrados em
  `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`.
- O repositório versionado é autoritativo para a política; a decisão de licença é
  do Product Owner e a revisão jurídica antes de G6 permanece obrigatória.
- PostgreSQL/PostGIS permanece autoritativo para estado de runtime, o filesystem
  gerenciado para artifacts publicados, RabbitMQ somente para transporte e a
  telemetria como derivação não autoritativa.
- O contrato usa SemVer, rejeita propriedades desconhecidas e exige nova major com
  revisão arquitetural para mudança incompatível.

## Invariantes de licença, citação e contribuição

- Código da aplicação usa `AGPL-3.0-or-later`; SDKs, schemas e exemplos de
  integração reutilizáveis usam `Apache-2.0`; documentação autoral usa
  `CC-BY-4.0`; assets exigem licença explícita por item.
- SPDX/REUSE, notices aplicáveis e inventário de dependências são obrigatórios para
  publicação. Licença ausente, ambígua ou incompatível é rejeitada.
- Releases públicas exigem `CITATION.cff` validado e coerência entre metadados,
  versão, digest e identificador persistente quando aplicável.
- Contribuições externas usam DCO 1.1, `Signed-off-by`, `inbound=outbound` e
  verificação automatizada. CLA não integra a baseline inicial; introduzi-lo exige
  decisão jurídica específica.

## Gate e falhas

Os gates `G0/G6` bloqueiam por padrão enquanto qualquer evidência aplicável estiver
ausente ou falhar. Isso inclui textos de licença, inventário SPDX/REUSE, notices,
inventário de dependências/SBOM, citação, verificação DCO, revisão jurídica antes de
G6 e os gates aplicáveis de segurança, licença, restore, compatibilidade e ciência.
Não existe fallback silencioso. Metadado de citação inválido ou evidência incompleta
bloqueia publicação; contribuição externa sem sign-off é rejeitada.

## Evidência dos critérios de aceitação

| Critério | Evidência no candidato |
|---|---|
| `AC-ISSUE-0141-01` | manifesto, schema fechado e exemplo versionado observável |
| `AC-ISSUE-0141-02` | `REQ-CIT-001`, `REQ-EPIC-042`, `REQ-OSS-001` e `REQ-PUB-002` rastreados no manifesto, exemplo e teste obrigatório |
| `AC-ISSUE-0141-03` | política fail-closed e teste negativo contra licença, citação, DCO, gate, autoridade e extensão inválidos |
| `AC-ISSUE-0141-04` | versão `1.0.0`, estado `FROZEN`, SemVer, owners de dados e gate de Reviewer explícitos e testados |

## Compatibilidade, migration e rollback

Não há mudança de endpoint, banco, runtime ou deployment; migration e rollback
operacional não se aplicam. Antes do consumo, o rollback contratual é revert; após
consumo, uma versão compatível substitui a anterior ou uma nova major passa por
revisão arquitetural.

## Riscos residuais e próximo gate

O contrato prova forma, decisões e invariantes, não a presença nem a execução dos
artifacts e checkers downstream. Publicação continua bloqueada até materialização,
automação, integração, evidência e revisão independente. O `Reviewer` deve avaliar
o mesmo commit candidato; este documento não registra autoaprovação.
