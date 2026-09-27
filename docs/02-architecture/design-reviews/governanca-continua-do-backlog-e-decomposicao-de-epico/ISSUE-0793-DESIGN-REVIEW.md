# Design review — ISSUE-0793

- **Candidate:** `ISSUE-0793` / GitHub `#68` / `STORY-0683` / `TASK-0683`
- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Status:** implementação candidata; revisão independente pendente
- **Contract version:** `1.0.0`

## Decisão local

Publicar um único profile de governança do backlog para o EPIC-110. O profile fixa,
sem duplicar modelos internos, os contratos já versionados que provam reconciliação do
catálogo, forecast, checkpoints de integração, workflow canônico e separação entre core,
API e runners. O incremento é declarativo: não cria runtime, endpoint, persistência,
registry funcional, checker ou abstração compartilhada.

## Contrato público

`contract-manifest.yaml` indexa o schema Draft 2020-12 e o exemplo positivo do
`backlog-governance-profile` na versão `1.0.0`. A linguagem publicada contém somente
Stable IDs, referências versionadas e controles de validação. Entidade, repository,
ORM model e state machine permanecem proibidos no boundary.

O profile referencia contratos públicos existentes do mesmo owner BC-001, sem copiá-los:

- portfolio snapshot reconciliado com GitHub;
- issue forecast com intervalo, confiança, snapshot e variance;
- foundation conformance para checkpoints produtor/consumidor;
- foundation boundaries para separação de core, API e runners.

## Invariantes e estados

- versão, owner e status `FROZEN` são obrigatórios e não possuem default;
- o catálogo versionado é a fonte contratual e o GitHub é contraparte de reconciliação;
- forecast exige minimum, mode, maximum, confidence, snapshot versionado e variance;
- checkpoint exige contratos produtor e consumidor e compatibilidade explícita de
  schema, inputs, versões e hashes;
- o catálogo de estados é `VERSIONED_CANONICAL`, na versão `1.0.0`, e somente
  transições registradas são aceitas;
- core, API e runners são obrigatórios, separados e apenas declarativos nesta story;
- propriedades desconhecidas, campos ausentes e qualquer política permissiva são
  rejeitados.

## Compatibilidade

O profile segue SemVer. Adição opcional pode ocorrer na major corrente; remoção,
renomeação, mudança de tipo, relaxamento fail-closed ou alteração do boundary exige nova
major e revisão do Arquiteto. Readers rejeitam propriedades desconhecidas. O contrato
permanece congelado antes das stories de implementação subsequentes.

## Autoridade de dados

- significado e invariantes: `BC-001`;
- definição contratual: repositório versionado;
- GitHub: contraparte externa de reconciliação, não substitui o Stable ID versionado;
- estado runtime: N/A, porque esta story não materializa runtime;
- transporte/broker: N/A e nunca autoridade de estado.

Se uma story futura materializar estado operacional, permanece aplicável a regra global
de PostgreSQL como autoridade e RabbitMQ somente como transporte; esta story não cria
esse estado nem antecipa seu modelo.

## Fail-closed

Os schemas e testes rejeitam owner incorreto, controle ausente, propriedade desconhecida,
reconciliação ausente ou divergente, forecast incompleto ou sem ordenação, variance sem
referência exata, checkpoint sem ambos os contratos, compatibilidade permissiva, estado
desconhecido, transição não registrada, boundary colapsado e materialização antecipada.
Não há fallback silencioso, best effort ou preenchimento por inferência.

## Rastreabilidade

| Requisito | Controle | Evidência executável |
|---|---|---|
| `REQ-ISM-004` | `/controls/portfolio_catalog` | `test_versioned_issue_portfolio_catalog_github_reconciliation` |
| `REQ-ISS-002` | `/controls/forecast` | `test_issue_forecast_min_mode_max_confidence_and_snapshot_variance` |
| `REQ-PLN-009` | `/controls/integration_checkpoint` | `test_cross_domain_contract_checkpoint_and_walking_skeleton_integration` |
| `REQ-PRJ-004` | `/controls/workflow` | `test_canonical_workflow_transitions` |
| `REQ-SPRINT-001-004` | `/controls/foundation_boundaries` | `test_epic_110_contrato` |
| `AC-ISSUE-0793-01..04` | manifesto, schema, exemplo, ownership e testes | `test_epic_110_contrato` e testes fail-closed |

## Aplicabilidade e rollback

- **HTTP/API:** N/A; nenhum endpoint ou alteração em OpenAPI.
- **Persistência/migration:** N/A; nenhum schema persistido, tabela ou dado é alterado.
- **Deployment/operational rollback:** N/A; não existe componente em execução.
- **Contract rollback:** reverter antes de consumo ou publicar nova versão; contratos
  consumidos não são sobrescritos silenciosamente.
- **SPEC-005:** não aplicável como artifact runtime; os arquivos desta story são
  contratos e evidência de implementação versionados, não `ArtifactSet` publicado.

Este design review registra uma decisão local e reversível dentro do ownership aprovado.
Não cria ADR, não aprova o próprio candidato e deixa o gate para Reviewer independente.
