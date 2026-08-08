# Design review — ISSUE-0111

- **Candidate:** `ISSUE-0111` / `STORY-0001` / `TASK-0001`
- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Status:** implementação candidata; revisão independente pendente
- **Contract version:** `1.0.0`

## Propósito

Congelar o menor contrato público que torna verificáveis o snapshot versionado do
portfólio reconciliado com GitHub, o forecast por intervalo e a separação declarativa
entre core, API e runners. O incremento pertence ao contexto habilitador BC-001 e não
materializa comportamento de runtime.

## Contratos publicados

O `contract-manifest.yaml` indexa três unidades semânticas independentes:

1. `portfolio-snapshot.schema.json`: identifica o registro estável no repositório e a
   issue nativa no GitHub, mantendo o Stable ID independente do número GitHub.
2. `issue-forecast.schema.json`: exige minimum, mode, maximum, confidence, snapshot
   versionado e variance vinculada ao mesmo snapshot.
3. `foundation-boundaries.schema.json`: declara core, API e runners como fronteiras
   distintas, todas ainda sem materialização de runtime nesta Story.

Cada schema possui um exemplo positivo. Todos os sete artefatos são registrados em
`contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv` com owner `BC-001`.

## Invariantes

- `schema_version`, versão do artefato e owner são obrigatórios; não há default
  silencioso.
- O snapshot contém os dois lados da reconciliação e somente aceita registros com
  status `RECONCILED`; Stable IDs e identidades GitHub devem formar relação um-para-um.
- `minimum <= mode <= maximum` e `confidence` é explícita no intervalo `(0, 1]`.
- A variance referencia exatamente o ID e a versão do snapshot declarado.
- Core, API e runners são obrigatórios, possuem IDs e concerns distintos e declaram
  `runtime_materialized: false`.
- Objetos normativos usam `additionalProperties: false`.

## Compatibilidade e versionamento

Os contratos seguem SemVer e JSON Schema Draft 2020-12. Adições opcionais compatíveis
podem evoluir dentro da major atual. Remoção, renomeação, mudança de tipo ou relaxamento
de invariante exige nova major; mudança material do boundary exige ADR substituta. Um
reader não ignora propriedades desconhecidas.

## Failure modes e comportamento fail-closed

- versão, owner, campo ou lado da reconciliação ausente: rejeitar;
- owner diferente de `BC-001`: rejeitar;
- Stable ID divergente do issue ID, Stable ID duplicado ou identidade GitHub duplicada:
  rejeitar;
- resumo incompatível ou reconciliação incompleta: rejeitar;
- intervalo fora de ordem, confidence ausente ou snapshot/variance divergentes: rejeitar;
- fronteira ausente, duplicada, semanticamente colapsada ou marcada como materializada:
  rejeitar;
- schema/exemplo referenciado ausente ou ownership não registrado: rejeitar;
- propriedade inesperada: rejeitar.

Não existe caminho de best effort nem preenchimento de campo obrigatório por inferência.

## Boundary BC-001

BC-001 publica somente schemas, snapshots, identificadores e decisão declarativa. Nenhuma
entidade interna, repository, ORM model ou state machine cruza o boundary. A linguagem
publicada continua sendo Policy/Conformance sem dependência runtime, conforme o Context
Map.

## Aplicabilidade operacional

- **Runtime:** não incluído.
- **HTTP / ADR-011 / ADR-012:** N/A; nenhum endpoint, OpenAPI, SSE ou polling é criado.
- **Persistence:** N/A; nenhum banco, tabela ou estado operacional é criado.
- **Migration:** N/A; não há schema persistido a migrar.
- **Operational rollback:** N/A; não há deployment ou processo em execução. Evolução ou
  reversão contratual ocorre por seleção explícita de versão, sem sobrescrever versões.

## Rastreabilidade e prova

| Requisito / AC | Artefato | Prova executável |
|---|---|---|
| `REQ-ISM-004`, `AC-ISSUE-0111-01..03` | portfolio snapshot + exemplo | `test_versioned_issue_portfolio_catalog_github_reconciliation` |
| `REQ-ISS-002`, `AC-ISSUE-0111-01..03` | issue forecast + exemplo | `test_issue_forecast_min_mode_max_confidence_and_snapshot_variance` |
| `REQ-SPRINT-001-004`, `AC-ISSUE-0111-01..03` | foundation boundaries + exemplo | `test_sprint_zero_baseline_decision_04` |
| `AC-ISSUE-0111-02..04` | manifesto + ownership registry | `test_epic_001_contrato` |

Este documento registra a decisão local reversível de decomposição dos contratos; não
cria ADR e não declara aprovação independente.
