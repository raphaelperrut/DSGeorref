# ISSUE-0130 — evidência executável de aceite

Este diretório é o locator canônico da evidência versionada da `STORY-0020`,
dentro do subtree autorizado da capacidade.

## Evidência por critério

| Critério | Evidência executável reutilizada |
|---|---|
| `AC-ISSUE-0130-01` | contratos versionados, controles do cliente TypeScript, adapters e integração read-only do `EPIC-004` |
| `AC-ISSUE-0130-02` | manifests, registries, TaskEnvelopes e suites owner vinculam os requisitos do épico às evidências existentes |
| `AC-ISSUE-0130-03` | mutações determinísticas exercitam drift, major desconhecido, fallback permissivo, relatório inválido e falhas da autoridade de aprovação |
| `AC-ISSUE-0130-04` | a Delivery Approval Authority verifica candidate SHA, evidências, riscos residuais e independência entre Executor, QA e Reviewer |

Os entrypoints públicos exigidos são:

- `test_epic_004_aceite_happy_path`;
- `test_epic_004_aceite_negative_paths`.

Eles carregam e executam as suites canônicas por referência. Nenhuma regra de
contrato, integração, rastreabilidade ou aprovação é copiada para este bundle.

## Candidate SHA e independência

O bundle não contém SHA tracked. A Delivery Approval Authority existente recebe
o candidate SHA esperado do gate chamador e o compara com as attestations
assinadas. Seus probes negativos rejeitam TaskEnvelope divergente, replay ou
digest inválido, candidate SHA divergente ou replayado, identidade ou papel
divergente, aprovação ausente ou rejeitada e sobreposição de sujeitos
responsáveis.

Esta evidência não declara aprovação. Attestations reais de Executor, QA e
Reviewer devem ser emitidas posteriormente por sujeitos independentes para o
mesmo TaskEnvelope, candidate SHA, conjunto de evidências e riscos residuais.

## Validação direcionada

- `py -3.12 -m pytest -q -p no:cacheprovider evidence/reviews/openapi-cliente-typescript-e-contratos-cli-jobs-evento/story-0020/test_issue_0130_acceptance.py`:
  `PASS`, 2 testes em 30,93 s.
- Validação de `.codex/tasks/TASK-0020.json` contra
  `.codex/tasks/TASK_ENVELOPE.schema.json`: `PASS`.

## Escopo, impacto e rollback

- Arquivos da entrega: este README, o bundle executável ao lado e a correção do
  locator obrigatório em `.codex/tasks/TASK-0020.json`.
- O ajuste do TaskEnvelope apenas alinha a evidência obrigatória ao `allow_path`
  já aprovado; não amplia ownership nem capacidade.
- Contratos compartilhados, registries, checkpoints, código de produção,
  workflow, schema persistido e deployment permanecem inalterados.
- Migration e rollback de dados não se aplicam. O rollback é a reversão destes
  arquivos de evidência e do locator do TaskEnvelope.
- Risco residual funcional conhecido: nenhum. Aprovação independente do commit
  candidato permanece como próximo gate e não é produzida por esta entrega.
