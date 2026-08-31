# Design Review — consolidação de migrations, CI, scans e telemetria mínima

## Escopo e composição

`STORY-0021` consolida exclusivamente os contratos publicados por `STORY-0706`
e `STORY-0707`. Os dois slices pertencem a `BC-001`, usam as baselines
`SAR-v2.9-PHASE-F` e estão presentes juntos no commit imutável
`6b442137d2cca3c51d073cc1c46b65a4675a65f1`.

A integração preserva os dois perfis lado a lado. O profile
`MIGRATIONS-CI-OBSERVABILITY-FOUNDATION` continua responsável pelos controles de
migration, evidência de CI, readiness e telemetria; `SGVCAL-CONFORMANCE` continua
responsável pelas invariantes SGV. Não há merge de schemas, cópia de controles,
segunda autoridade normativa ou implementação de runtime.

## Rastreabilidade, lineage e compatibilidade

O contrato `migrations-ci-security-observability-slice-consolidation` fixa paths
e SHA-256 dos seis artifacts publicados pelos slices no baseline comum. A matriz
`ISSUE_REQUIREMENTS_REVIEW.csv` atribui dez requisitos a `ISSUE-0816` e
`REQ-SGVCAL-007` a `ISSUE-0817`; a união contém onze IDs sem interseção, ausência
ou duplicação normativa.

O profile SGVCAL publicado pelo predecessor contém a família completa de
controles SGVCAL. A consolidação não reatribui essa família: a responsabilidade
requisito→história permanece exatamente a da matriz canônica, com somente
`REQ-SGVCAL-007` atribuída ao slice vinculado `STORY-0707`.

IDs de contrato, `$id` dos schemas, profile IDs e namespaces de controles são
distintos. A consolidação não altera contrato congelado, OpenAPI, banco,
persistência, broker, runtime nem semântica geoespacial. Migration e rollback
operacional são `NOT_APPLICABLE`; rollback contratual é revert antes de consumo
ou supersessão por versão compatível.

## Limite da ISSUE-0131

Esta entrega materializa somente o checkpoint de integração. Migrations físicas,
configuração de CI, scanners, exporters e capacidade SGV permanecem nas histórias
downstream já existentes `STORY-0023` e `STORY-0708..0711`. Nenhuma delas é
implementada ou liberada pelo Writer.

O TaskEnvelope foi corrigido apenas para incluir seu próprio arquivo, o registry
de ownership, o teste obrigatório e a evidence exigida pela issue. Os deny paths
foram preservados e nenhum path de runtime/data plane foi adicionado.

## Gate independente e riscos residuais

O Writer entrega o candidate como `READY_FOR_INDEPENDENT_REVIEW`, com dependentes
elegíveis derivados do grafo e `released_dependents` vazio. Somente um `Reviewer`
distinto pode registrar riscos residuais contra o mesmo commit e liberar
`STORY-0023` e `STORY-0708..0711`; autoaprovação e liberação implícita são
rejeitadas pelo schema e pelo teste negativo.

Riscos para o Reviewer registrar:

- os digests pinados exigem nova versão da consolidação se um contrato de slice
  congelado for legitimamente supersedido;
- os perfis consolidados são declarativos e não provam execução real de
  migration, CI, scans, telemetria ou SGV;
- o predecessor SGVCAL publica controles da família completa, enquanto a matriz
  canônica atribui a este slice somente `REQ-SGVCAL-007`; a consolidação preserva
  essa alocação sem duplicar ownership.

O teste obrigatório `test_story_0021_slice_consolidation` valida schema, baseline,
lineage e digests, cobertura canônica, ausência de colisão, grafo, TaskEnvelope,
registry e gate de revisão fail-closed.
