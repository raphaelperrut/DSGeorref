# Ondas de paralelização

- **Histórias:** 758
- **Ondas topológicas:** 88
- **Hard blockers:** 1165
- **Semântica:** uma história pode iniciar somente quando todas as dependências anteriores estiverem integradas e seu write scope estiver livre.

## Onda 001

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0001` | `ISSUE-0111` | `EPIC-001` | `SPRINT-001` | Arquiteto | `contracts/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/**`<br>`docs/02-architecture/design-reviews/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/**` |
| `STORY-0250` | `ISSUE-0360` | `EPIC-042` | `SPRINT-012` | Product Owner | `docs/01-product/capabilities/licenca-citacao-sanitizacao-e-revisao-externa-concluid/**` |
| `STORY-0255` | `ISSUE-0365` | `EPIC-043` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/release-documentada-com-rollback-e-suporte/**` |
| `STORY-0577` | `ISSUE-0687` | `EPIC-094` | `SPRINT-007` | Arquiteto | `contracts/geo/registry-e-transformacoes-de-crs/**`<br>`docs/02-architecture/design-reviews/registry-e-transformacoes-de-crs/**` |
| `STORY-0584` | `ISSUE-0694` | `EPIC-095` | `SPRINT-007` | Arquiteto | `contracts/geo/validade-raster-explicita/**`<br>`docs/02-architecture/design-reviews/validade-raster-explicita/**` |
| `STORY-0591` | `ISSUE-0701` | `EPIC-096` | `SPRINT-007` | Arquiteto | `contracts/geo/seletor-e-validador-de-crs/**`<br>`docs/02-architecture/design-reviews/seletor-e-validador-de-crs/**` |
| `STORY-0598` | `ISSUE-0708` | `EPIC-097` | `SPRINT-007` | Arquiteto | `contracts/geo/grade-resolucao-e-reamostragem/**`<br>`docs/02-architecture/design-reviews/grade-resolucao-e-reamostragem/**` |
| `STORY-0605` | `ISSUE-0715` | `EPIC-098` | `SPRINT-007` | Arquiteto | `contracts/geo/mosaico-relativo-de-recuperacao/**`<br>`docs/02-architecture/design-reviews/mosaico-relativo-de-recuperacao/**` |
| `STORY-0612` | `ISSUE-0722` | `EPIC-099` | `SPRINT-008` | Arquiteto | `contracts/geo/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo/**`<br>`docs/02-architecture/design-reviews/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo/**` |
| `STORY-0619` | `ISSUE-0729` | `EPIC-100` | `SPRINT-008` | Arquiteto | `contracts/geo/workspace-e-lifecycle-de-ancoras/**`<br>`docs/02-architecture/design-reviews/workspace-e-lifecycle-de-ancoras/**` |
| `STORY-0626` | `ISSUE-0736` | `EPIC-101` | `SPRINT-008` | Arquiteto | `contracts/geo/relative-mosaic-verifier-e-promotion-lifecycle/**`<br>`docs/02-architecture/design-reviews/relative-mosaic-verifier-e-promotion-lifecycle/**` |
| `STORY-0633` | `ISSUE-0743` | `EPIC-102` | `SPRINT-008` | Arquiteto | `contracts/geo/relatorios-visualizacao-e-exports-do-mosaico-relativo/**`<br>`docs/02-architecture/design-reviews/relatorios-visualizacao-e-exports-do-mosaico-relativo/**` |
| `STORY-0640` | `ISSUE-0750` | `EPIC-103` | `SPRINT-008` | Arquiteto | `contracts/geo/budgets-persistencia-e-materializacao-do-mosaico-relat/**`<br>`docs/02-architecture/design-reviews/budgets-persistencia-e-materializacao-do-mosaico-relat/**` |
| `STORY-0647` | `ISSUE-0757` | `EPIC-104` | `SPRINT-004` | Arquiteto | `contracts/job/snapshots-replay-e-bundles-do-scheduler/**`<br>`docs/02-architecture/design-reviews/snapshots-replay-e-bundles-do-scheduler/**` |
| `STORY-0654` | `ISSUE-0764` | `EPIC-105` | `SPRINT-010` | Arquiteto | `contracts/dat/registry-de-schemas-e-compatibilidade-de-artifacts/**`<br>`docs/02-architecture/design-reviews/registry-de-schemas-e-compatibilidade-de-artifacts/**` |
| `STORY-0660` | `ISSUE-0770` | `EPIC-106` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/migrations-compativeis-upgrade-e-downgrade-seguro/**` |
| `STORY-0666` | `ISSUE-0776` | `EPIC-107` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/controlador-e-rollout-coordenado-de-upgrades/**` |
| `STORY-0672` | `ISSUE-0782` | `EPIC-108` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/instalador-bootstrap-readiness-e-suporte-diagnostico/**` |
| `STORY-0678` | `ISSUE-0788` | `EPIC-109` | `SPRINT-012` | Product Owner | `docs/01-product/capabilities/licenciamento-contribuicao-rights-manifests-e-citacao/**` |
| `STORY-0683` | `ISSUE-0793` | `EPIC-110` | `SPRINT-001` | Arquiteto | `contracts/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/**`<br>`docs/02-architecture/design-reviews/governanca-continua-do-backlog-e-decomposicao-de-epico/**` |

## Onda 002

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0003` | `ISSUE-0113` | `EPIC-001` | `SPRINT-001` | DevOps | `tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/**`<br>`tools/quality/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/**`<br>`.github/workflows/governanca-de-decisoes-arquiteturais-e-manutencao-da-b.yaml` |
| `STORY-0251` | `ISSUE-0361` | `EPIC-042` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/licenca-citacao-sanitizacao-e-revisao-externa-concluid/**` |
| `STORY-0252` | `ISSUE-0362` | `EPIC-042` | `SPRINT-012` | DevOps | `tests/pub/licenca-citacao-sanitizacao-e-revisao-externa-concluid/**`<br>`tools/quality/licenca-citacao-sanitizacao-e-revisao-externa-concluid/**`<br>`.github/workflows/licenca-citacao-sanitizacao-e-revisao-externa-concluid.yaml` |
| `STORY-0256` | `ISSUE-0366` | `EPIC-043` | `SPRINT-012` | DevOps | `tests/rel/release-documentada-com-rollback-e-suporte/**`<br>`tools/quality/release-documentada-com-rollback-e-suporte/**`<br>`.github/workflows/release-documentada-com-rollback-e-suporte.yaml` |
| `STORY-0257` | `ISSUE-0367` | `EPIC-043` | `SPRINT-012` | DevOps | `tests/rel/release-documentada-com-rollback-e-suporte/**`<br>`tools/quality/release-documentada-com-rollback-e-suporte/**`<br>`.github/workflows/release-documentada-com-rollback-e-suporte.yaml` |
| `STORY-0258` | `ISSUE-0368` | `EPIC-043` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/release-documentada-com-rollback-e-suporte/**`<br>`tests/security/release-documentada-com-rollback-e-suporte/**` |
| `STORY-0578` | `ISSUE-0688` | `EPIC-094` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-e-transformacoes-de-crs/**` |
| `STORY-0579` | `ISSUE-0689` | `EPIC-094` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-e-transformacoes-de-crs/**` |
| `STORY-0580` | `ISSUE-0690` | `EPIC-094` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-e-transformacoes-de-crs/**` |
| `STORY-0581` | `ISSUE-0691` | `EPIC-094` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-e-transformacoes-de-crs/**` |
| `STORY-0585` | `ISSUE-0695` | `EPIC-095` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/validade-raster-explicita/**` |
| `STORY-0586` | `ISSUE-0696` | `EPIC-095` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/validade-raster-explicita/**` |
| `STORY-0587` | `ISSUE-0697` | `EPIC-095` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/validade-raster-explicita/**` |
| `STORY-0588` | `ISSUE-0698` | `EPIC-095` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/validade-raster-explicita/**` |
| `STORY-0592` | `ISSUE-0702` | `EPIC-096` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/seletor-e-validador-de-crs/**` |
| `STORY-0593` | `ISSUE-0703` | `EPIC-096` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/seletor-e-validador-de-crs/**` |
| `STORY-0594` | `ISSUE-0704` | `EPIC-096` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/seletor-e-validador-de-crs/**` |
| `STORY-0595` | `ISSUE-0705` | `EPIC-096` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/seletor-e-validador-de-crs/**` |
| `STORY-0599` | `ISSUE-0709` | `EPIC-097` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/grade-resolucao-e-reamostragem/**` |
| `STORY-0600` | `ISSUE-0710` | `EPIC-097` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/grade-resolucao-e-reamostragem/**` |
| `STORY-0601` | `ISSUE-0711` | `EPIC-097` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/grade-resolucao-e-reamostragem/**` |
| `STORY-0602` | `ISSUE-0712` | `EPIC-097` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/grade-resolucao-e-reamostragem/**` |
| `STORY-0606` | `ISSUE-0716` | `EPIC-098` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/mosaico-relativo-de-recuperacao/**` |
| `STORY-0607` | `ISSUE-0717` | `EPIC-098` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/mosaico-relativo-de-recuperacao/**` |
| `STORY-0608` | `ISSUE-0718` | `EPIC-098` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/mosaico-relativo-de-recuperacao/**` |
| `STORY-0609` | `ISSUE-0719` | `EPIC-098` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/mosaico-relativo-de-recuperacao/**` |
| `STORY-0613` | `ISSUE-0723` | `EPIC-099` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo/**` |
| `STORY-0614` | `ISSUE-0724` | `EPIC-099` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo/**` |
| `STORY-0615` | `ISSUE-0725` | `EPIC-099` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo/**` |
| `STORY-0616` | `ISSUE-0726` | `EPIC-099` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo/**` |
| `STORY-0620` | `ISSUE-0730` | `EPIC-100` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/workspace-e-lifecycle-de-ancoras/**` |
| `STORY-0621` | `ISSUE-0731` | `EPIC-100` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/workspace-e-lifecycle-de-ancoras/**` |
| `STORY-0622` | `ISSUE-0732` | `EPIC-100` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/workspace-e-lifecycle-de-ancoras/**` |
| `STORY-0623` | `ISSUE-0733` | `EPIC-100` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/workspace-e-lifecycle-de-ancoras/**` |
| `STORY-0627` | `ISSUE-0737` | `EPIC-101` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/relative-mosaic-verifier-e-promotion-lifecycle/**` |
| `STORY-0628` | `ISSUE-0738` | `EPIC-101` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/relative-mosaic-verifier-e-promotion-lifecycle/**` |
| `STORY-0629` | `ISSUE-0739` | `EPIC-101` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/relative-mosaic-verifier-e-promotion-lifecycle/**` |
| `STORY-0630` | `ISSUE-0740` | `EPIC-101` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/relative-mosaic-verifier-e-promotion-lifecycle/**` |
| `STORY-0634` | `ISSUE-0744` | `EPIC-102` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/relatorios-visualizacao-e-exports-do-mosaico-relativo/**` |
| `STORY-0635` | `ISSUE-0745` | `EPIC-102` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/relatorios-visualizacao-e-exports-do-mosaico-relativo/**` |
| `STORY-0636` | `ISSUE-0746` | `EPIC-102` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/relatorios-visualizacao-e-exports-do-mosaico-relativo/**` |
| `STORY-0637` | `ISSUE-0747` | `EPIC-102` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/relatorios-visualizacao-e-exports-do-mosaico-relativo/**` |
| `STORY-0641` | `ISSUE-0751` | `EPIC-103` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/budgets-persistencia-e-materializacao-do-mosaico-relat/**` |
| `STORY-0642` | `ISSUE-0752` | `EPIC-103` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/budgets-persistencia-e-materializacao-do-mosaico-relat/**` |
| `STORY-0643` | `ISSUE-0753` | `EPIC-103` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/budgets-persistencia-e-materializacao-do-mosaico-relat/**` |
| `STORY-0644` | `ISSUE-0754` | `EPIC-103` | `SPRINT-008` | Geoprocessamento | `src/geo/dsgeorref_geo/budgets-persistencia-e-materializacao-do-mosaico-relat/**` |
| `STORY-0648` | `ISSUE-0758` | `EPIC-104` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/snapshots-replay-e-bundles-do-scheduler/**`<br>`src/backend/dsgeorref/adapters/snapshots-replay-e-bundles-do-scheduler/**` |
| `STORY-0649` | `ISSUE-0759` | `EPIC-104` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/snapshots-replay-e-bundles-do-scheduler/**`<br>`src/backend/dsgeorref/adapters/snapshots-replay-e-bundles-do-scheduler/**` |
| `STORY-0650` | `ISSUE-0760` | `EPIC-104` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/snapshots-replay-e-bundles-do-scheduler/**`<br>`src/backend/dsgeorref/adapters/snapshots-replay-e-bundles-do-scheduler/**` |
| `STORY-0651` | `ISSUE-0761` | `EPIC-104` | `SPRINT-004` | DevOps | `tests/job/snapshots-replay-e-bundles-do-scheduler/**`<br>`tools/quality/snapshots-replay-e-bundles-do-scheduler/**`<br>`.github/workflows/snapshots-replay-e-bundles-do-scheduler.yaml` |
| `STORY-0655` | `ISSUE-0765` | `EPIC-105` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/registry-de-schemas-e-compatibilidade-de-artifacts/**`<br>`src/backend/dsgeorref/adapters/registry-de-schemas-e-compatibilidade-de-artifacts/**` |
| `STORY-0656` | `ISSUE-0766` | `EPIC-105` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/registry-de-schemas-e-compatibilidade-de-artifacts/**`<br>`src/backend/dsgeorref/adapters/registry-de-schemas-e-compatibilidade-de-artifacts/**` |
| `STORY-0657` | `ISSUE-0767` | `EPIC-105` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/registry-de-schemas-e-compatibilidade-de-artifacts/**`<br>`src/backend/dsgeorref/adapters/registry-de-schemas-e-compatibilidade-de-artifacts/**` |
| `STORY-0661` | `ISSUE-0771` | `EPIC-106` | `SPRINT-012` | DevOps | `tests/rel/migrations-compativeis-upgrade-e-downgrade-seguro/**`<br>`tools/quality/migrations-compativeis-upgrade-e-downgrade-seguro/**`<br>`.github/workflows/migrations-compativeis-upgrade-e-downgrade-seguro.yaml` |
| `STORY-0662` | `ISSUE-0772` | `EPIC-106` | `SPRINT-012` | DevOps | `tests/rel/migrations-compativeis-upgrade-e-downgrade-seguro/**`<br>`tools/quality/migrations-compativeis-upgrade-e-downgrade-seguro/**`<br>`.github/workflows/migrations-compativeis-upgrade-e-downgrade-seguro.yaml` |
| `STORY-0663` | `ISSUE-0773` | `EPIC-106` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/migrations-compativeis-upgrade-e-downgrade-seguro/**`<br>`tests/security/migrations-compativeis-upgrade-e-downgrade-seguro/**` |
| `STORY-0667` | `ISSUE-0777` | `EPIC-107` | `SPRINT-012` | DevOps | `tests/rel/controlador-e-rollout-coordenado-de-upgrades/**`<br>`tools/quality/controlador-e-rollout-coordenado-de-upgrades/**`<br>`.github/workflows/controlador-e-rollout-coordenado-de-upgrades.yaml` |
| `STORY-0668` | `ISSUE-0778` | `EPIC-107` | `SPRINT-012` | DevOps | `tests/rel/controlador-e-rollout-coordenado-de-upgrades/**`<br>`tools/quality/controlador-e-rollout-coordenado-de-upgrades/**`<br>`.github/workflows/controlador-e-rollout-coordenado-de-upgrades.yaml` |
| `STORY-0669` | `ISSUE-0779` | `EPIC-107` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/controlador-e-rollout-coordenado-de-upgrades/**`<br>`tests/security/controlador-e-rollout-coordenado-de-upgrades/**` |
| `STORY-0673` | `ISSUE-0783` | `EPIC-108` | `SPRINT-012` | DevOps | `tests/rel/instalador-bootstrap-readiness-e-suporte-diagnostico/**`<br>`tools/quality/instalador-bootstrap-readiness-e-suporte-diagnostico/**`<br>`.github/workflows/instalador-bootstrap-readiness-e-suporte-diagnostico.yaml` |
| `STORY-0674` | `ISSUE-0784` | `EPIC-108` | `SPRINT-012` | DevOps | `tests/rel/instalador-bootstrap-readiness-e-suporte-diagnostico/**`<br>`tools/quality/instalador-bootstrap-readiness-e-suporte-diagnostico/**`<br>`.github/workflows/instalador-bootstrap-readiness-e-suporte-diagnostico.yaml` |
| `STORY-0675` | `ISSUE-0785` | `EPIC-108` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/instalador-bootstrap-readiness-e-suporte-diagnostico/**`<br>`tests/security/instalador-bootstrap-readiness-e-suporte-diagnostico/**` |
| `STORY-0679` | `ISSUE-0789` | `EPIC-109` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/licenciamento-contribuicao-rights-manifests-e-citacao/**` |
| `STORY-0680` | `ISSUE-0790` | `EPIC-109` | `SPRINT-012` | DevOps | `tests/pub/licenciamento-contribuicao-rights-manifests-e-citacao/**`<br>`tools/quality/licenciamento-contribuicao-rights-manifests-e-citacao/**`<br>`.github/workflows/licenciamento-contribuicao-rights-manifests-e-citacao.yaml` |
| `STORY-0685` | `ISSUE-0795` | `EPIC-110` | `SPRINT-001` | DevOps | `tests/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/**`<br>`tools/quality/governanca-continua-do-backlog-e-decomposicao-de-epico/**`<br>`.github/workflows/governanca-continua-do-backlog-e-decomposicao-de-epico.yaml` |
| `STORY-0688` | `ISSUE-0798` | `EPIC-001` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/frz-gov-adr-gov-dec-parte-1/**`<br>`docs/03-engineering/capabilities/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/frz-gov-adr-gov-dec-parte-1/**` |
| `STORY-0689` | `ISSUE-0799` | `EPIC-001` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/sprint-001-tool-parte-2/**`<br>`docs/03-engineering/capabilities/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/sprint-001-tool-parte-2/**` |
| `STORY-0754` | `ISSUE-0864` | `EPIC-110` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/ism-iss-parte-1/**`<br>`docs/03-engineering/capabilities/governanca-continua-do-backlog-e-decomposicao-de-epico/ism-iss-parte-1/**` |
| `STORY-0755` | `ISSUE-0865` | `EPIC-110` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/iss-pln-parte-2/**`<br>`docs/03-engineering/capabilities/governanca-continua-do-backlog-e-decomposicao-de-epico/iss-pln-parte-2/**` |
| `STORY-0756` | `ISSUE-0866` | `EPIC-110` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/prj-prm-parte-3/**`<br>`docs/03-engineering/capabilities/governanca-continua-do-backlog-e-decomposicao-de-epico/prj-prm-parte-3/**` |
| `STORY-0757` | `ISSUE-0867` | `EPIC-110` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/prm-sprint-001-parte-4/**`<br>`docs/03-engineering/capabilities/governanca-continua-do-backlog-e-decomposicao-de-epico/prm-sprint-001-parte-4/**` |
| `STORY-0758` | `ISSUE-0868` | `EPIC-110` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/**`<br>`docs/03-engineering/capabilities/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/**` |

## Onda 003

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0002` | `ISSUE-0112` | `EPIC-001` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/consolidacao/**`<br>`docs/03-engineering/capabilities/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/consolidacao/**` |
| `STORY-0253` | `ISSUE-0363` | `EPIC-042` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/licenca-citacao-sanitizacao-e-revisao-externa-concluid/**`<br>`tests/security/licenca-citacao-sanitizacao-e-revisao-externa-concluid/**` |
| `STORY-0259` | `ISSUE-0369` | `EPIC-043` | `SPRINT-012` | QA | `tests/rel/release-documentada-com-rollback-e-suporte/**`<br>`tools/quality/release-documentada-com-rollback-e-suporte/**`<br>`.github/workflows/release-documentada-com-rollback-e-suporte.yaml` |
| `STORY-0582` | `ISSUE-0692` | `EPIC-094` | `SPRINT-007` | QA | `tests/geo/registry-e-transformacoes-de-crs/**`<br>`tools/quality/registry-e-transformacoes-de-crs/**`<br>`.github/workflows/registry-e-transformacoes-de-crs.yaml` |
| `STORY-0589` | `ISSUE-0699` | `EPIC-095` | `SPRINT-007` | QA | `tests/geo/validade-raster-explicita/**`<br>`tools/quality/validade-raster-explicita/**`<br>`.github/workflows/validade-raster-explicita.yaml` |
| `STORY-0596` | `ISSUE-0706` | `EPIC-096` | `SPRINT-007` | QA | `tests/geo/seletor-e-validador-de-crs/**`<br>`tools/quality/seletor-e-validador-de-crs/**`<br>`.github/workflows/seletor-e-validador-de-crs.yaml` |
| `STORY-0603` | `ISSUE-0713` | `EPIC-097` | `SPRINT-007` | QA | `tests/geo/grade-resolucao-e-reamostragem/**`<br>`tools/quality/grade-resolucao-e-reamostragem/**`<br>`.github/workflows/grade-resolucao-e-reamostragem.yaml` |
| `STORY-0610` | `ISSUE-0720` | `EPIC-098` | `SPRINT-007` | QA | `tests/geo/mosaico-relativo-de-recuperacao/**`<br>`tools/quality/mosaico-relativo-de-recuperacao/**`<br>`.github/workflows/mosaico-relativo-de-recuperacao.yaml` |
| `STORY-0617` | `ISSUE-0727` | `EPIC-099` | `SPRINT-008` | QA | `tests/geo/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo/**`<br>`tools/quality/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo/**`<br>`.github/workflows/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo.yaml` |
| `STORY-0624` | `ISSUE-0734` | `EPIC-100` | `SPRINT-008` | QA | `tests/geo/workspace-e-lifecycle-de-ancoras/**`<br>`tools/quality/workspace-e-lifecycle-de-ancoras/**`<br>`.github/workflows/workspace-e-lifecycle-de-ancoras.yaml` |
| `STORY-0631` | `ISSUE-0741` | `EPIC-101` | `SPRINT-008` | QA | `tests/geo/relative-mosaic-verifier-e-promotion-lifecycle/**`<br>`tools/quality/relative-mosaic-verifier-e-promotion-lifecycle/**`<br>`.github/workflows/relative-mosaic-verifier-e-promotion-lifecycle.yaml` |
| `STORY-0638` | `ISSUE-0748` | `EPIC-102` | `SPRINT-008` | QA | `tests/geo/relatorios-visualizacao-e-exports-do-mosaico-relativo/**`<br>`tools/quality/relatorios-visualizacao-e-exports-do-mosaico-relativo/**`<br>`.github/workflows/relatorios-visualizacao-e-exports-do-mosaico-relativo.yaml` |
| `STORY-0645` | `ISSUE-0755` | `EPIC-103` | `SPRINT-008` | QA | `tests/geo/budgets-persistencia-e-materializacao-do-mosaico-relat/**`<br>`tools/quality/budgets-persistencia-e-materializacao-do-mosaico-relat/**`<br>`.github/workflows/budgets-persistencia-e-materializacao-do-mosaico-relat.yaml` |
| `STORY-0652` | `ISSUE-0762` | `EPIC-104` | `SPRINT-004` | QA | `tests/job/snapshots-replay-e-bundles-do-scheduler/**`<br>`tools/quality/snapshots-replay-e-bundles-do-scheduler/**`<br>`.github/workflows/snapshots-replay-e-bundles-do-scheduler.yaml` |
| `STORY-0658` | `ISSUE-0768` | `EPIC-105` | `SPRINT-010` | Security | `src/backend/dsgeorref/security/registry-de-schemas-e-compatibilidade-de-artifacts/**`<br>`tests/security/registry-de-schemas-e-compatibilidade-de-artifacts/**` |
| `STORY-0664` | `ISSUE-0774` | `EPIC-106` | `SPRINT-012` | QA | `tests/rel/migrations-compativeis-upgrade-e-downgrade-seguro/**`<br>`tools/quality/migrations-compativeis-upgrade-e-downgrade-seguro/**`<br>`.github/workflows/migrations-compativeis-upgrade-e-downgrade-seguro.yaml` |
| `STORY-0670` | `ISSUE-0780` | `EPIC-107` | `SPRINT-012` | QA | `tests/rel/controlador-e-rollout-coordenado-de-upgrades/**`<br>`tools/quality/controlador-e-rollout-coordenado-de-upgrades/**`<br>`.github/workflows/controlador-e-rollout-coordenado-de-upgrades.yaml` |
| `STORY-0676` | `ISSUE-0786` | `EPIC-108` | `SPRINT-012` | QA | `tests/rel/instalador-bootstrap-readiness-e-suporte-diagnostico/**`<br>`tools/quality/instalador-bootstrap-readiness-e-suporte-diagnostico/**`<br>`.github/workflows/instalador-bootstrap-readiness-e-suporte-diagnostico.yaml` |
| `STORY-0681` | `ISSUE-0791` | `EPIC-109` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/licenciamento-contribuicao-rights-manifests-e-citacao/**`<br>`tests/security/licenciamento-contribuicao-rights-manifests-e-citacao/**` |
| `STORY-0684` | `ISSUE-0794` | `EPIC-110` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/consolidacao/**`<br>`docs/03-engineering/capabilities/governanca-continua-do-backlog-e-decomposicao-de-epico/consolidacao/**` |

## Onda 004

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0004` | `ISSUE-0114` | `EPIC-001` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/**`<br>`docs/03-engineering/capabilities/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/**` |
| `STORY-0254` | `ISSUE-0364` | `EPIC-042` | `SPRINT-012` | Reviewer | `evidence/reviews/licenca-citacao-sanitizacao-e-revisao-externa-concluid/**` |
| `STORY-0260` | `ISSUE-0370` | `EPIC-043` | `SPRINT-012` | Reviewer | `evidence/reviews/release-documentada-com-rollback-e-suporte/**` |
| `STORY-0583` | `ISSUE-0693` | `EPIC-094` | `SPRINT-007` | Reviewer | `evidence/reviews/registry-e-transformacoes-de-crs/**` |
| `STORY-0590` | `ISSUE-0700` | `EPIC-095` | `SPRINT-007` | Reviewer | `evidence/reviews/validade-raster-explicita/**` |
| `STORY-0597` | `ISSUE-0707` | `EPIC-096` | `SPRINT-007` | Reviewer | `evidence/reviews/seletor-e-validador-de-crs/**` |
| `STORY-0604` | `ISSUE-0714` | `EPIC-097` | `SPRINT-007` | Reviewer | `evidence/reviews/grade-resolucao-e-reamostragem/**` |
| `STORY-0611` | `ISSUE-0721` | `EPIC-098` | `SPRINT-007` | Reviewer | `evidence/reviews/mosaico-relativo-de-recuperacao/**` |
| `STORY-0618` | `ISSUE-0728` | `EPIC-099` | `SPRINT-008` | Reviewer | `evidence/reviews/ancoragem-e-recuperacao-a-partir-do-mosaico-relativo/**` |
| `STORY-0625` | `ISSUE-0735` | `EPIC-100` | `SPRINT-008` | Reviewer | `evidence/reviews/workspace-e-lifecycle-de-ancoras/**` |
| `STORY-0632` | `ISSUE-0742` | `EPIC-101` | `SPRINT-008` | Reviewer | `evidence/reviews/relative-mosaic-verifier-e-promotion-lifecycle/**` |
| `STORY-0639` | `ISSUE-0749` | `EPIC-102` | `SPRINT-008` | Reviewer | `evidence/reviews/relatorios-visualizacao-e-exports-do-mosaico-relativo/**` |
| `STORY-0646` | `ISSUE-0756` | `EPIC-103` | `SPRINT-008` | Reviewer | `evidence/reviews/budgets-persistencia-e-materializacao-do-mosaico-relat/**` |
| `STORY-0653` | `ISSUE-0763` | `EPIC-104` | `SPRINT-004` | Reviewer | `evidence/reviews/snapshots-replay-e-bundles-do-scheduler/**` |
| `STORY-0659` | `ISSUE-0769` | `EPIC-105` | `SPRINT-010` | Reviewer | `evidence/reviews/registry-de-schemas-e-compatibilidade-de-artifacts/**` |
| `STORY-0665` | `ISSUE-0775` | `EPIC-106` | `SPRINT-012` | Reviewer | `evidence/reviews/migrations-compativeis-upgrade-e-downgrade-seguro/**` |
| `STORY-0671` | `ISSUE-0781` | `EPIC-107` | `SPRINT-012` | Reviewer | `evidence/reviews/controlador-e-rollout-coordenado-de-upgrades/**` |
| `STORY-0677` | `ISSUE-0787` | `EPIC-108` | `SPRINT-012` | Reviewer | `evidence/reviews/instalador-bootstrap-readiness-e-suporte-diagnostico/**` |
| `STORY-0682` | `ISSUE-0792` | `EPIC-109` | `SPRINT-012` | Reviewer | `evidence/reviews/licenciamento-contribuicao-rights-manifests-e-citacao/**` |
| `STORY-0686` | `ISSUE-0796` | `EPIC-110` | `SPRINT-001` | Tech Lead | `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/**`<br>`docs/03-engineering/capabilities/governanca-continua-do-backlog-e-decomposicao-de-epico/**` |

## Onda 005

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0005` | `ISSUE-0115` | `EPIC-001` | `SPRINT-001` | Reviewer | `evidence/reviews/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/**` |
| `STORY-0687` | `ISSUE-0797` | `EPIC-110` | `SPRINT-001` | Reviewer | `evidence/reviews/governanca-continua-do-backlog-e-decomposicao-de-epico/**` |

## Onda 006

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0011` | `ISSUE-0121` | `EPIC-003` | `SPRINT-001` | Arquiteto | `contracts/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**`<br>`docs/02-architecture/design-reviews/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**` |
| `STORY-0026` | `ISSUE-0136` | `EPIC-006` | `SPRINT-001` | Arquiteto | `contracts/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/**`<br>`docs/02-architecture/design-reviews/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/**` |
| `STORY-0031` | `ISSUE-0141` | `EPIC-007` | `SPRINT-001` | Arquiteto | `contracts/fnd/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/**`<br>`docs/02-architecture/design-reviews/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/**` |
| `STORY-0690` | `ISSUE-0800` | `EPIC-002` | `SPRINT-001` | Arquiteto | `contracts/fnd/repositorio-privado-project-central-views-campos-label/classicprofile-iss-native-parte-1/**`<br>`docs/02-architecture/design-reviews/repositorio-privado-project-central-views-campos-label/classicprofile-iss-native-parte-1/**` |
| `STORY-0691` | `ISSUE-0801` | `EPIC-002` | `SPRINT-001` | Arquiteto | `contracts/fnd/repositorio-privado-project-central-views-campos-label/worker-parte-2/**`<br>`docs/02-architecture/design-reviews/repositorio-privado-project-central-views-campos-label/worker-parte-2/**` |

## Onda 007

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0006` | `ISSUE-0116` | `EPIC-002` | `SPRINT-001` | Arquiteto | `contracts/fnd/repositorio-privado-project-central-views-campos-label/consolidacao/**`<br>`docs/02-architecture/design-reviews/repositorio-privado-project-central-views-campos-label/consolidacao/**` |
| `STORY-0012` | `ISSUE-0122` | `EPIC-003` | `SPRINT-001` | Tech Lead | `tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**`<br>`docs/03-engineering/capabilities/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**` |
| `STORY-0013` | `ISSUE-0123` | `EPIC-003` | `SPRINT-001` | DevOps | `tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**`<br>`tools/quality/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**`<br>`.github/workflows/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r.yaml` |
| `STORY-0027` | `ISSUE-0137` | `EPIC-006` | `SPRINT-001` | Tech Lead | `tools/governance/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/**`<br>`docs/03-engineering/capabilities/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/**` |
| `STORY-0028` | `ISSUE-0138` | `EPIC-006` | `SPRINT-001` | DevOps | `tests/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/**`<br>`tools/quality/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/**`<br>`.github/workflows/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca.yaml` |
| `STORY-0032` | `ISSUE-0142` | `EPIC-007` | `SPRINT-001` | Tech Lead | `tools/governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/**`<br>`docs/03-engineering/capabilities/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/**` |
| `STORY-0033` | `ISSUE-0143` | `EPIC-007` | `SPRINT-001` | DevOps | `tests/fnd/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/**`<br>`tools/quality/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/**`<br>`.github/workflows/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu.yaml` |

## Onda 008

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0008` | `ISSUE-0118` | `EPIC-002` | `SPRINT-001` | DevOps | `tests/fnd/repositorio-privado-project-central-views-campos-label/**`<br>`tools/quality/repositorio-privado-project-central-views-campos-label/**`<br>`.github/workflows/repositorio-privado-project-central-views-campos-label.yaml` |
| `STORY-0014` | `ISSUE-0124` | `EPIC-003` | `SPRINT-001` | Tech Lead | `tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**`<br>`docs/03-engineering/capabilities/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**` |
| `STORY-0029` | `ISSUE-0139` | `EPIC-006` | `SPRINT-001` | Tech Lead | `tools/governance/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/**`<br>`docs/03-engineering/capabilities/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/**` |
| `STORY-0034` | `ISSUE-0144` | `EPIC-007` | `SPRINT-001` | Tech Lead | `tools/governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/**`<br>`docs/03-engineering/capabilities/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/**` |
| `STORY-0692` | `ISSUE-0802` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/classicprofile-gov-gov-adr-parte-1/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/classicprofile-gov-gov-adr-parte-1/**` |
| `STORY-0693` | `ISSUE-0803` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/gov-adr-ism-iss-parte-2/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/gov-adr-ism-iss-parte-2/**` |
| `STORY-0694` | `ISSUE-0804` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/native-pln-parte-3/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/native-pln-parte-3/**` |
| `STORY-0695` | `ISSUE-0805` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/pln-prj-parte-4/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/pln-prj-parte-4/**` |
| `STORY-0696` | `ISSUE-0806` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/prj-prm-parte-5/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/prj-prm-parte-5/**` |
| `STORY-0697` | `ISSUE-0807` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/prm-run-parte-6/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/prm-run-parte-6/**` |
| `STORY-0698` | `ISSUE-0808` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/runtime-sprint-001-parte-7/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/runtime-sprint-001-parte-7/**` |
| `STORY-0699` | `ISSUE-0809` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/sprint-001-tool-worker-parte-8/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/sprint-001-tool-worker-parte-8/**` |
| `STORY-0700` | `ISSUE-0810` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/worker-parte-9/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/worker-parte-9/**` |

## Onda 009

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0007` | `ISSUE-0117` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/consolidacao/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/consolidacao/**` |
| `STORY-0015` | `ISSUE-0125` | `EPIC-003` | `SPRINT-001` | Reviewer | `evidence/reviews/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**` |
| `STORY-0030` | `ISSUE-0140` | `EPIC-006` | `SPRINT-001` | Reviewer | `evidence/reviews/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/**` |
| `STORY-0035` | `ISSUE-0145` | `EPIC-007` | `SPRINT-001` | Reviewer | `evidence/reviews/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/**` |

## Onda 010

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0009` | `ISSUE-0119` | `EPIC-002` | `SPRINT-001` | Tech Lead | `tools/governance/repositorio-privado-project-central-views-campos-label/**`<br>`docs/03-engineering/capabilities/repositorio-privado-project-central-views-campos-label/**` |
| `STORY-0115` | `ISSUE-0225` | `EPIC-021` | `SPRINT-005` | Arquiteto | `contracts/geo/corpus-versionado-com-decadas-e-condicoes-distintas/**`<br>`docs/02-architecture/design-reviews/corpus-versionado-com-decadas-e-condicoes-distintas/**` |
| `STORY-0701` | `ISSUE-0811` | `EPIC-004` | `SPRINT-001` | Arquiteto | `contracts/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento/crs-dbschema-epic-parte-1/**`<br>`docs/02-architecture/design-reviews/openapi-cliente-typescript-e-contratos-cli-jobs-evento/crs-dbschema-epic-parte-1/**` |
| `STORY-0702` | `ISSUE-0812` | `EPIC-004` | `SPRINT-001` | Arquiteto | `contracts/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento/runtime-scm-tool-parte-2/**`<br>`docs/02-architecture/design-reviews/openapi-cliente-typescript-e-contratos-cli-jobs-evento/runtime-scm-tool-parte-2/**` |
| `STORY-0706` | `ISSUE-0816` | `EPIC-005` | `SPRINT-001` | Arquiteto | `contracts/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/aie-bex-epic-parte-1/**`<br>`docs/02-architecture/design-reviews/migrations-ci-secret-dependency-scan-e-telemetria-mini/aie-bex-epic-parte-1/**` |
| `STORY-0707` | `ISSUE-0817` | `EPIC-005` | `SPRINT-001` | Arquiteto | `contracts/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-parte-2/**`<br>`docs/02-architecture/design-reviews/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-parte-2/**` |

## Onda 011

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0010` | `ISSUE-0120` | `EPIC-002` | `SPRINT-001` | Reviewer | `evidence/reviews/repositorio-privado-project-central-views-campos-label/**` |
| `STORY-0016` | `ISSUE-0126` | `EPIC-004` | `SPRINT-001` | Arquiteto | `contracts/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento/consolidacao/**`<br>`docs/02-architecture/design-reviews/openapi-cliente-typescript-e-contratos-cli-jobs-evento/consolidacao/**` |
| `STORY-0021` | `ISSUE-0131` | `EPIC-005` | `SPRINT-001` | Arquiteto | `contracts/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/consolidacao/**`<br>`docs/02-architecture/design-reviews/migrations-ci-secret-dependency-scan-e-telemetria-mini/consolidacao/**` |
| `STORY-0117` | `ISSUE-0227` | `EPIC-021` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/corpus-versionado-com-decadas-e-condicoes-distintas/**` |
| `STORY-0118` | `ISSUE-0228` | `EPIC-021` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/corpus-versionado-com-decadas-e-condicoes-distintas/**` |
| `STORY-0119` | `ISSUE-0229` | `EPIC-021` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/corpus-versionado-com-decadas-e-condicoes-distintas/**` |
| `STORY-0723` | `ISSUE-0833` | `EPIC-021` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/corpus-versionado-com-decadas-e-condicoes-distintas/requirements-epic-fs1-native-parte-1/**` |
| `STORY-0724` | `ISSUE-0834` | `EPIC-021` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/corpus-versionado-com-decadas-e-condicoes-distintas/native-scp-parte-2/**` |

## Onda 012

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0018` | `ISSUE-0128` | `EPIC-004` | `SPRINT-001` | DevOps | `tests/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento/**`<br>`tools/quality/openapi-cliente-typescript-e-contratos-cli-jobs-evento/**`<br>`.github/workflows/openapi-cliente-typescript-e-contratos-cli-jobs-evento.yaml` |
| `STORY-0023` | `ISSUE-0133` | `EPIC-005` | `SPRINT-001` | DevOps | `tests/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/**`<br>`tools/quality/migrations-ci-secret-dependency-scan-e-telemetria-mini/**`<br>`.github/workflows/migrations-ci-secret-dependency-scan-e-telemetria-mini.yaml` |
| `STORY-0116` | `ISSUE-0226` | `EPIC-021` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/corpus-versionado-com-decadas-e-condicoes-distintas/consolidacao/**` |
| `STORY-0528` | `ISSUE-0638` | `EPIC-085` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/definicao-e-automacao-de-milestones-internal-alpha-bet/**` |
| `STORY-0555` | `ISSUE-0665` | `EPIC-090` | `SPRINT-001` | Arquiteto | `contracts/fnd/issue-forms-templates-e-taxonomia-de-tipos-com-validac/**`<br>`docs/02-architecture/design-reviews/issue-forms-templates-e-taxonomia-de-tipos-com-validac/**` |
| `STORY-0703` | `ISSUE-0813` | `EPIC-004` | `SPRINT-001` | Tech Lead | `tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/artlayout-dbschema-fs1-parte-1/**`<br>`docs/03-engineering/capabilities/openapi-cliente-typescript-e-contratos-cli-jobs-evento/artlayout-dbschema-fs1-parte-1/**` |
| `STORY-0704` | `ISSUE-0814` | `EPIC-004` | `SPRINT-001` | Tech Lead | `tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/run-runtime-parte-2/**`<br>`docs/03-engineering/capabilities/openapi-cliente-typescript-e-contratos-cli-jobs-evento/run-runtime-parte-2/**` |
| `STORY-0705` | `ISSUE-0815` | `EPIC-004` | `SPRINT-001` | Tech Lead | `tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/runtime-tool-upg-parte-3/**`<br>`docs/03-engineering/capabilities/openapi-cliente-typescript-e-contratos-cli-jobs-evento/runtime-tool-upg-parte-3/**` |
| `STORY-0708` | `ISSUE-0818` | `EPIC-005` | `SPRINT-001` | Tech Lead | `tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/aie-bex-parte-1/**`<br>`docs/03-engineering/capabilities/migrations-ci-secret-dependency-scan-e-telemetria-mini/aie-bex-parte-1/**` |
| `STORY-0709` | `ISSUE-0819` | `EPIC-005` | `SPRINT-001` | Tech Lead | `tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/bex-epic-frz-parte-2/**`<br>`docs/03-engineering/capabilities/migrations-ci-secret-dependency-scan-e-telemetria-mini/bex-epic-frz-parte-2/**` |
| `STORY-0710` | `ISSUE-0820` | `EPIC-005` | `SPRINT-001` | Tech Lead | `tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/fs1-gov-sgvcal-parte-3/**`<br>`docs/03-engineering/capabilities/migrations-ci-secret-dependency-scan-e-telemetria-mini/fs1-gov-sgvcal-parte-3/**` |
| `STORY-0711` | `ISSUE-0821` | `EPIC-005` | `SPRINT-001` | Tech Lead | `tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-srg-srp-parte-4/**`<br>`docs/03-engineering/capabilities/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-srg-srp-parte-4/**` |

## Onda 013

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0017` | `ISSUE-0127` | `EPIC-004` | `SPRINT-001` | Tech Lead | `tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/consolidacao/**`<br>`docs/03-engineering/capabilities/openapi-cliente-typescript-e-contratos-cli-jobs-evento/consolidacao/**` |
| `STORY-0022` | `ISSUE-0132` | `EPIC-005` | `SPRINT-001` | Tech Lead | `tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/consolidacao/**`<br>`docs/03-engineering/capabilities/migrations-ci-secret-dependency-scan-e-telemetria-mini/consolidacao/**` |
| `STORY-0120` | `ISSUE-0230` | `EPIC-021` | `SPRINT-005` | QA | `tests/geo/corpus-versionado-com-decadas-e-condicoes-distintas/**`<br>`tools/quality/corpus-versionado-com-decadas-e-condicoes-distintas/**`<br>`.github/workflows/corpus-versionado-com-decadas-e-condicoes-distintas.yaml` |
| `STORY-0529` | `ISSUE-0639` | `EPIC-085` | `SPRINT-012` | DevOps | `tests/rel/definicao-e-automacao-de-milestones-internal-alpha-bet/**`<br>`tools/quality/definicao-e-automacao-de-milestones-internal-alpha-bet/**`<br>`.github/workflows/definicao-e-automacao-de-milestones-internal-alpha-bet.yaml` |
| `STORY-0530` | `ISSUE-0640` | `EPIC-085` | `SPRINT-012` | DevOps | `tests/rel/definicao-e-automacao-de-milestones-internal-alpha-bet/**`<br>`tools/quality/definicao-e-automacao-de-milestones-internal-alpha-bet/**`<br>`.github/workflows/definicao-e-automacao-de-milestones-internal-alpha-bet.yaml` |
| `STORY-0531` | `ISSUE-0641` | `EPIC-085` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/definicao-e-automacao-de-milestones-internal-alpha-bet/**`<br>`tests/security/definicao-e-automacao-de-milestones-internal-alpha-bet/**` |
| `STORY-0556` | `ISSUE-0666` | `EPIC-090` | `SPRINT-001` | Tech Lead | `tools/governance/issue-forms-templates-e-taxonomia-de-tipos-com-validac/**`<br>`docs/03-engineering/capabilities/issue-forms-templates-e-taxonomia-de-tipos-com-validac/**` |
| `STORY-0557` | `ISSUE-0667` | `EPIC-090` | `SPRINT-001` | DevOps | `tests/fnd/issue-forms-templates-e-taxonomia-de-tipos-com-validac/**`<br>`tools/quality/issue-forms-templates-e-taxonomia-de-tipos-com-validac/**`<br>`.github/workflows/issue-forms-templates-e-taxonomia-de-tipos-com-validac.yaml` |

## Onda 014

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0019` | `ISSUE-0129` | `EPIC-004` | `SPRINT-001` | Tech Lead | `tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/**`<br>`docs/03-engineering/capabilities/openapi-cliente-typescript-e-contratos-cli-jobs-evento/**` |
| `STORY-0024` | `ISSUE-0134` | `EPIC-005` | `SPRINT-001` | Tech Lead | `tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/**`<br>`docs/03-engineering/capabilities/migrations-ci-secret-dependency-scan-e-telemetria-mini/**` |
| `STORY-0121` | `ISSUE-0231` | `EPIC-021` | `SPRINT-005` | Reviewer | `evidence/reviews/corpus-versionado-com-decadas-e-condicoes-distintas/**` |
| `STORY-0532` | `ISSUE-0642` | `EPIC-085` | `SPRINT-012` | QA | `tests/rel/definicao-e-automacao-de-milestones-internal-alpha-bet/**`<br>`tools/quality/definicao-e-automacao-de-milestones-internal-alpha-bet/**`<br>`.github/workflows/definicao-e-automacao-de-milestones-internal-alpha-bet.yaml` |
| `STORY-0558` | `ISSUE-0668` | `EPIC-090` | `SPRINT-001` | Tech Lead | `tools/governance/issue-forms-templates-e-taxonomia-de-tipos-com-validac/**`<br>`docs/03-engineering/capabilities/issue-forms-templates-e-taxonomia-de-tipos-com-validac/**` |

## Onda 015

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0020` | `ISSUE-0130` | `EPIC-004` | `SPRINT-001` | Reviewer | `evidence/reviews/openapi-cliente-typescript-e-contratos-cli-jobs-evento/**` |
| `STORY-0025` | `ISSUE-0135` | `EPIC-005` | `SPRINT-001` | Reviewer | `evidence/reviews/migrations-ci-secret-dependency-scan-e-telemetria-mini/**` |
| `STORY-0122` | `ISSUE-0232` | `EPIC-022` | `SPRINT-005` | Arquiteto | `contracts/geo/busca-provavel-greenfield-validada/**`<br>`docs/02-architecture/design-reviews/busca-provavel-greenfield-validada/**` |
| `STORY-0129` | `ISSUE-0239` | `EPIC-023` | `SPRINT-005` | Arquiteto | `contracts/geo/correspondencias-e-estimacao-robusta-da-homografia-pro/**`<br>`docs/02-architecture/design-reviews/correspondencias-e-estimacao-robusta-da-homografia-pro/**` |
| `STORY-0533` | `ISSUE-0643` | `EPIC-085` | `SPRINT-012` | Reviewer | `evidence/reviews/definicao-e-automacao-de-milestones-internal-alpha-bet/**` |
| `STORY-0559` | `ISSUE-0669` | `EPIC-090` | `SPRINT-001` | Reviewer | `evidence/reviews/issue-forms-templates-e-taxonomia-de-tipos-com-validac/**` |

## Onda 016

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0036` | `ISSUE-0146` | `EPIC-008` | `SPRINT-002` | Arquiteto | `contracts/plt/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/**`<br>`docs/02-architecture/design-reviews/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/**` |
| `STORY-0068` | `ISSUE-0178` | `EPIC-014` | `SPRINT-003` | Arquiteto | `contracts/job/modelo-de-job-e-maquina-de-estados-no-postgresql/**`<br>`docs/02-architecture/design-reviews/modelo-de-job-e-maquina-de-estados-no-postgresql/**` |
| `STORY-0124` | `ISSUE-0234` | `EPIC-022` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-provavel-greenfield-validada/**` |
| `STORY-0125` | `ISSUE-0235` | `EPIC-022` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-provavel-greenfield-validada/**` |
| `STORY-0126` | `ISSUE-0236` | `EPIC-022` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-provavel-greenfield-validada/**` |
| `STORY-0130` | `ISSUE-0240` | `EPIC-023` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/correspondencias-e-estimacao-robusta-da-homografia-pro/**` |
| `STORY-0131` | `ISSUE-0241` | `EPIC-023` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/correspondencias-e-estimacao-robusta-da-homografia-pro/**` |
| `STORY-0132` | `ISSUE-0242` | `EPIC-023` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/correspondencias-e-estimacao-robusta-da-homografia-pro/**` |
| `STORY-0133` | `ISSUE-0243` | `EPIC-023` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/correspondencias-e-estimacao-robusta-da-homografia-pro/**` |
| `STORY-0171` | `ISSUE-0281` | `EPIC-029` | `SPRINT-005` | Arquiteto | `contracts/geo/etapas-capacidades-canonicas-e-processingplan-reproduz/**`<br>`docs/02-architecture/design-reviews/etapas-capacidades-canonicas-e-processingplan-reproduz/**` |
| `STORY-0499` | `ISSUE-0609` | `EPIC-080` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**`<br>`tests/security/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**` |
| `STORY-0534` | `ISSUE-0644` | `EPIC-086` | `SPRINT-001` | Arquiteto | `contracts/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/**`<br>`docs/02-architecture/design-reviews/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/**` |
| `STORY-0560` | `ISSUE-0670` | `EPIC-091` | `SPRINT-001` | Arquiteto | `contracts/fnd/ruleset-de-main-checks-unicos-codeowners-politica-de-b/**`<br>`docs/02-architecture/design-reviews/ruleset-de-main-checks-unicos-codeowners-politica-de-b/**` |
| `STORY-0725` | `ISSUE-0835` | `EPIC-022` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-provavel-greenfield-validada/aie-classicprofile-parte-1/**` |
| `STORY-0726` | `ISSUE-0836` | `EPIC-022` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-provavel-greenfield-validada/classicprofile-fs1-native-parte-2/**` |
| `STORY-0727` | `ISSUE-0837` | `EPIC-022` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-provavel-greenfield-validada/native-sgvcal-parte-3/**` |
| `STORY-0728` | `ISSUE-0838` | `EPIC-022` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-provavel-greenfield-validada/sgvcal-parte-4/**` |

## Onda 017

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0038` | `ISSUE-0148` | `EPIC-008` | `SPRINT-002` | Frontend | `src/frontend/src/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/**` |
| `STORY-0070` | `ISSUE-0180` | `EPIC-014` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/modelo-de-job-e-maquina-de-estados-no-postgresql/**`<br>`src/backend/dsgeorref/adapters/modelo-de-job-e-maquina-de-estados-no-postgresql/**` |
| `STORY-0071` | `ISSUE-0181` | `EPIC-014` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/modelo-de-job-e-maquina-de-estados-no-postgresql/**`<br>`src/backend/dsgeorref/adapters/modelo-de-job-e-maquina-de-estados-no-postgresql/**` |
| `STORY-0072` | `ISSUE-0182` | `EPIC-014` | `SPRINT-003` | DevOps | `tests/job/modelo-de-job-e-maquina-de-estados-no-postgresql/**`<br>`tools/quality/modelo-de-job-e-maquina-de-estados-no-postgresql/**`<br>`.github/workflows/modelo-de-job-e-maquina-de-estados-no-postgresql.yaml` |
| `STORY-0123` | `ISSUE-0233` | `EPIC-022` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-provavel-greenfield-validada/consolidacao/**` |
| `STORY-0134` | `ISSUE-0244` | `EPIC-023` | `SPRINT-005` | QA | `tests/geo/correspondencias-e-estimacao-robusta-da-homografia-pro/**`<br>`tools/quality/correspondencias-e-estimacao-robusta-da-homografia-pro/**`<br>`.github/workflows/correspondencias-e-estimacao-robusta-da-homografia-pro.yaml` |
| `STORY-0172` | `ISSUE-0282` | `EPIC-029` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/etapas-capacidades-canonicas-e-processingplan-reproduz/**` |
| `STORY-0173` | `ISSUE-0283` | `EPIC-029` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/etapas-capacidades-canonicas-e-processingplan-reproduz/**` |
| `STORY-0174` | `ISSUE-0284` | `EPIC-029` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/etapas-capacidades-canonicas-e-processingplan-reproduz/**` |
| `STORY-0175` | `ISSUE-0285` | `EPIC-029` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/etapas-capacidades-canonicas-e-processingplan-reproduz/**` |
| `STORY-0500` | `ISSUE-0610` | `EPIC-080` | `SPRINT-011` | Arquiteto | `contracts/sec/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**`<br>`docs/02-architecture/design-reviews/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**` |
| `STORY-0501` | `ISSUE-0611` | `EPIC-080` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**`<br>`src/backend/dsgeorref/adapters/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**` |
| `STORY-0502` | `ISSUE-0612` | `EPIC-080` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**`<br>`tests/security/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**` |
| `STORY-0536` | `ISSUE-0646` | `EPIC-086` | `SPRINT-001` | DevOps | `tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/**`<br>`tools/quality/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/**`<br>`.github/workflows/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw.yaml` |
| `STORY-0561` | `ISSUE-0671` | `EPIC-091` | `SPRINT-001` | Tech Lead | `tools/governance/ruleset-de-main-checks-unicos-codeowners-politica-de-b/**`<br>`docs/03-engineering/capabilities/ruleset-de-main-checks-unicos-codeowners-politica-de-b/**` |
| `STORY-0562` | `ISSUE-0672` | `EPIC-091` | `SPRINT-001` | DevOps | `tests/fnd/ruleset-de-main-checks-unicos-codeowners-politica-de-b/**`<br>`tools/quality/ruleset-de-main-checks-unicos-codeowners-politica-de-b/**`<br>`.github/workflows/ruleset-de-main-checks-unicos-codeowners-politica-de-b.yaml` |
| `STORY-0712` | `ISSUE-0822` | `EPIC-008` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/auth-impl-dbschema-parte-1/**`<br>`src/backend/dsgeorref/adapters/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/auth-impl-dbschema-parte-1/**` |
| `STORY-0713` | `ISSUE-0823` | `EPIC-008` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/id-parte-2/**`<br>`src/backend/dsgeorref/adapters/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/id-parte-2/**` |
| `STORY-0721` | `ISSUE-0831` | `EPIC-014` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/modelo-de-job-e-maquina-de-estados-no-postgresql/aie-dbschema-fs1-parte-1/**`<br>`src/backend/dsgeorref/adapters/modelo-de-job-e-maquina-de-estados-no-postgresql/aie-dbschema-fs1-parte-1/**` |
| `STORY-0722` | `ISSUE-0832` | `EPIC-014` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/modelo-de-job-e-maquina-de-estados-no-postgresql/fs1-runtime-worker-parte-2/**`<br>`src/backend/dsgeorref/adapters/modelo-de-job-e-maquina-de-estados-no-postgresql/fs1-runtime-worker-parte-2/**` |
| `STORY-0752` | `ISSUE-0862` | `EPIC-086` | `SPRINT-001` | Tech Lead | `tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/del-ism-sprint-001-parte-1/**`<br>`docs/03-engineering/capabilities/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/del-ism-sprint-001-parte-1/**` |
| `STORY-0753` | `ISSUE-0863` | `EPIC-086` | `SPRINT-001` | Tech Lead | `tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/sprint-001-parte-2/**`<br>`docs/03-engineering/capabilities/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/sprint-001-parte-2/**` |

## Onda 018

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0037` | `ISSUE-0147` | `EPIC-008` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/consolidacao/**`<br>`src/backend/dsgeorref/adapters/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/consolidacao/**` |
| `STORY-0069` | `ISSUE-0179` | `EPIC-014` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/modelo-de-job-e-maquina-de-estados-no-postgresql/consolidacao/**`<br>`src/backend/dsgeorref/adapters/modelo-de-job-e-maquina-de-estados-no-postgresql/consolidacao/**` |
| `STORY-0127` | `ISSUE-0237` | `EPIC-022` | `SPRINT-005` | QA | `tests/geo/busca-provavel-greenfield-validada/**`<br>`tools/quality/busca-provavel-greenfield-validada/**`<br>`.github/workflows/busca-provavel-greenfield-validada.yaml` |
| `STORY-0135` | `ISSUE-0245` | `EPIC-023` | `SPRINT-005` | Reviewer | `evidence/reviews/correspondencias-e-estimacao-robusta-da-homografia-pro/**` |
| `STORY-0176` | `ISSUE-0286` | `EPIC-029` | `SPRINT-005` | QA | `tests/geo/etapas-capacidades-canonicas-e-processingplan-reproduz/**`<br>`tools/quality/etapas-capacidades-canonicas-e-processingplan-reproduz/**`<br>`.github/workflows/etapas-capacidades-canonicas-e-processingplan-reproduz.yaml` |
| `STORY-0503` | `ISSUE-0613` | `EPIC-080` | `SPRINT-011` | DevOps | `tests/sec/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**`<br>`tools/quality/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**`<br>`.github/workflows/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura.yaml` |
| `STORY-0535` | `ISSUE-0645` | `EPIC-086` | `SPRINT-001` | Tech Lead | `tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/consolidacao/**`<br>`docs/03-engineering/capabilities/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/consolidacao/**` |
| `STORY-0563` | `ISSUE-0673` | `EPIC-091` | `SPRINT-001` | Tech Lead | `tools/governance/ruleset-de-main-checks-unicos-codeowners-politica-de-b/**`<br>`docs/03-engineering/capabilities/ruleset-de-main-checks-unicos-codeowners-politica-de-b/**` |

## Onda 019

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0039` | `ISSUE-0149` | `EPIC-008` | `SPRINT-002` | Security | `src/backend/dsgeorref/security/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/**`<br>`tests/security/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/**` |
| `STORY-0073` | `ISSUE-0183` | `EPIC-014` | `SPRINT-003` | QA | `tests/job/modelo-de-job-e-maquina-de-estados-no-postgresql/**`<br>`tools/quality/modelo-de-job-e-maquina-de-estados-no-postgresql/**`<br>`.github/workflows/modelo-de-job-e-maquina-de-estados-no-postgresql.yaml` |
| `STORY-0128` | `ISSUE-0238` | `EPIC-022` | `SPRINT-005` | Reviewer | `evidence/reviews/busca-provavel-greenfield-validada/**` |
| `STORY-0177` | `ISSUE-0287` | `EPIC-029` | `SPRINT-005` | Reviewer | `evidence/reviews/etapas-capacidades-canonicas-e-processingplan-reproduz/**` |
| `STORY-0504` | `ISSUE-0614` | `EPIC-080` | `SPRINT-011` | Reviewer | `evidence/reviews/lockfiles-pins-por-digest-sha-scanners-sbom-assinatura/**` |
| `STORY-0537` | `ISSUE-0647` | `EPIC-086` | `SPRINT-001` | Tech Lead | `tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/**`<br>`docs/03-engineering/capabilities/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/**` |
| `STORY-0564` | `ISSUE-0674` | `EPIC-091` | `SPRINT-001` | Reviewer | `evidence/reviews/ruleset-de-main-checks-unicos-codeowners-politica-de-b/**` |

## Onda 020

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0040` | `ISSUE-0150` | `EPIC-008` | `SPRINT-002` | Reviewer | `evidence/reviews/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/**` |
| `STORY-0074` | `ISSUE-0184` | `EPIC-014` | `SPRINT-003` | Reviewer | `evidence/reviews/modelo-de-job-e-maquina-de-estados-no-postgresql/**` |
| `STORY-0136` | `ISSUE-0246` | `EPIC-024` | `SPRINT-005` | Arquiteto | `contracts/geo/strong-geometric-verifier-fail-closed-para-homografia/**`<br>`docs/02-architecture/design-reviews/strong-geometric-verifier-fail-closed-para-homografia/**` |
| `STORY-0538` | `ISSUE-0648` | `EPIC-086` | `SPRINT-001` | Reviewer | `evidence/reviews/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/**` |

## Onda 021

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0041` | `ISSUE-0151` | `EPIC-009` | `SPRINT-002` | Arquiteto | `contracts/plt/usuarios-e-papeis-da-instancia/**`<br>`docs/02-architecture/design-reviews/usuarios-e-papeis-da-instancia/**` |
| `STORY-0075` | `ISSUE-0185` | `EPIC-015` | `SPRINT-003` | Arquiteto | `contracts/job/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**`<br>`docs/02-architecture/design-reviews/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**` |
| `STORY-0089` | `ISSUE-0199` | `EPIC-017` | `SPRINT-003` | Arquiteto | `contracts/job/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**`<br>`docs/02-architecture/design-reviews/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**` |
| `STORY-0138` | `ISSUE-0248` | `EPIC-024` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/strong-geometric-verifier-fail-closed-para-homografia/**` |
| `STORY-0139` | `ISSUE-0249` | `EPIC-024` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/strong-geometric-verifier-fail-closed-para-homografia/**` |
| `STORY-0140` | `ISSUE-0250` | `EPIC-024` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/strong-geometric-verifier-fail-closed-para-homografia/**` |
| `STORY-0487` | `ISSUE-0597` | `EPIC-078` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**`<br>`tests/security/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**` |
| `STORY-0565` | `ISSUE-0675` | `EPIC-092` | `SPRINT-001` | Arquiteto | `contracts/fnd/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/**`<br>`docs/02-architecture/design-reviews/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/**` |
| `STORY-0729` | `ISSUE-0839` | `EPIC-024` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/strong-geometric-verifier-fail-closed-para-homografia/aie-anc-crs-parte-1/**` |
| `STORY-0730` | `ISSUE-0840` | `EPIC-024` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/strong-geometric-verifier-fail-closed-para-homografia/est-fs1-msk-parte-2/**` |
| `STORY-0731` | `ISSUE-0841` | `EPIC-024` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/strong-geometric-verifier-fail-closed-para-homografia/rmv-parte-3/**` |

## Onda 022

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0043` | `ISSUE-0153` | `EPIC-009` | `SPRINT-002` | Frontend | `src/frontend/src/features/usuarios-e-papeis-da-instancia/**` |
| `STORY-0076` | `ISSUE-0186` | `EPIC-015` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**`<br>`src/backend/dsgeorref/adapters/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**` |
| `STORY-0077` | `ISSUE-0187` | `EPIC-015` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**`<br>`src/backend/dsgeorref/adapters/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**` |
| `STORY-0078` | `ISSUE-0188` | `EPIC-015` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**`<br>`src/backend/dsgeorref/adapters/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**` |
| `STORY-0079` | `ISSUE-0189` | `EPIC-015` | `SPRINT-003` | DevOps | `tests/job/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**`<br>`tools/quality/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**`<br>`.github/workflows/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo.yaml` |
| `STORY-0090` | `ISSUE-0200` | `EPIC-017` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**`<br>`src/backend/dsgeorref/adapters/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**` |
| `STORY-0091` | `ISSUE-0201` | `EPIC-017` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**`<br>`src/backend/dsgeorref/adapters/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**` |
| `STORY-0092` | `ISSUE-0202` | `EPIC-017` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**`<br>`src/backend/dsgeorref/adapters/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**` |
| `STORY-0093` | `ISSUE-0203` | `EPIC-017` | `SPRINT-003` | DevOps | `tests/job/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**`<br>`tools/quality/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**`<br>`.github/workflows/rest-sse-e-polling-de-reconciliacao-com-contratos-vers.yaml` |
| `STORY-0137` | `ISSUE-0247` | `EPIC-024` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/strong-geometric-verifier-fail-closed-para-homografia/consolidacao/**` |
| `STORY-0488` | `ISSUE-0598` | `EPIC-078` | `SPRINT-011` | Arquiteto | `contracts/sec/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**`<br>`docs/02-architecture/design-reviews/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**` |
| `STORY-0489` | `ISSUE-0599` | `EPIC-078` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**`<br>`src/backend/dsgeorref/adapters/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**` |
| `STORY-0490` | `ISSUE-0600` | `EPIC-078` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**`<br>`tests/security/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**` |
| `STORY-0566` | `ISSUE-0676` | `EPIC-092` | `SPRINT-001` | Tech Lead | `tools/governance/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/**`<br>`docs/03-engineering/capabilities/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/**` |
| `STORY-0567` | `ISSUE-0677` | `EPIC-092` | `SPRINT-001` | DevOps | `tests/fnd/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/**`<br>`tools/quality/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/**`<br>`.github/workflows/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat.yaml` |
| `STORY-0714` | `ISSUE-0824` | `EPIC-009` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/usuarios-e-papeis-da-instancia/acc-auth-impl-parte-1/**`<br>`src/backend/dsgeorref/adapters/usuarios-e-papeis-da-instancia/acc-auth-impl-parte-1/**` |
| `STORY-0715` | `ISSUE-0825` | `EPIC-009` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/usuarios-e-papeis-da-instancia/id-parte-2/**`<br>`src/backend/dsgeorref/adapters/usuarios-e-papeis-da-instancia/id-parte-2/**` |

## Onda 023

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0042` | `ISSUE-0152` | `EPIC-009` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/usuarios-e-papeis-da-instancia/consolidacao/**`<br>`src/backend/dsgeorref/adapters/usuarios-e-papeis-da-instancia/consolidacao/**` |
| `STORY-0080` | `ISSUE-0190` | `EPIC-015` | `SPRINT-003` | QA | `tests/job/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**`<br>`tools/quality/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**`<br>`.github/workflows/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo.yaml` |
| `STORY-0094` | `ISSUE-0204` | `EPIC-017` | `SPRINT-003` | QA | `tests/job/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**`<br>`tools/quality/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**`<br>`.github/workflows/rest-sse-e-polling-de-reconciliacao-com-contratos-vers.yaml` |
| `STORY-0141` | `ISSUE-0251` | `EPIC-024` | `SPRINT-005` | QA | `tests/geo/strong-geometric-verifier-fail-closed-para-homografia/**`<br>`tools/quality/strong-geometric-verifier-fail-closed-para-homografia/**`<br>`.github/workflows/strong-geometric-verifier-fail-closed-para-homografia.yaml` |
| `STORY-0491` | `ISSUE-0601` | `EPIC-078` | `SPRINT-011` | DevOps | `tests/sec/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**`<br>`tools/quality/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**`<br>`.github/workflows/contrato-de-secrets-setup-permissoes-rotacao-recuperac.yaml` |
| `STORY-0568` | `ISSUE-0678` | `EPIC-092` | `SPRINT-001` | Tech Lead | `tools/governance/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/**`<br>`docs/03-engineering/capabilities/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/**` |

## Onda 024

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0044` | `ISSUE-0154` | `EPIC-009` | `SPRINT-002` | Security | `src/backend/dsgeorref/security/usuarios-e-papeis-da-instancia/**`<br>`tests/security/usuarios-e-papeis-da-instancia/**` |
| `STORY-0081` | `ISSUE-0191` | `EPIC-015` | `SPRINT-003` | Reviewer | `evidence/reviews/runner-direto-e-celery-rabbitmq-sobre-o-mesmo-nucleo/**` |
| `STORY-0095` | `ISSUE-0205` | `EPIC-017` | `SPRINT-003` | Reviewer | `evidence/reviews/rest-sse-e-polling-de-reconciliacao-com-contratos-vers/**` |
| `STORY-0142` | `ISSUE-0252` | `EPIC-024` | `SPRINT-005` | Reviewer | `evidence/reviews/strong-geometric-verifier-fail-closed-para-homografia/**` |
| `STORY-0492` | `ISSUE-0602` | `EPIC-078` | `SPRINT-011` | Reviewer | `evidence/reviews/contrato-de-secrets-setup-permissoes-rotacao-recuperac/**` |
| `STORY-0569` | `ISSUE-0679` | `EPIC-092` | `SPRINT-001` | Reviewer | `evidence/reviews/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/**` |

## Onda 025

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0045` | `ISSUE-0155` | `EPIC-009` | `SPRINT-002` | Reviewer | `evidence/reviews/usuarios-e-papeis-da-instancia/**` |
| `STORY-0082` | `ISSUE-0192` | `EPIC-016` | `SPRINT-003` | Arquiteto | `contracts/job/retries-redelivery-cancelamento-retomada-e-idempotenci/**`<br>`docs/02-architecture/design-reviews/retries-redelivery-cancelamento-retomada-e-idempotenci/**` |
| `STORY-0143` | `ISSUE-0253` | `EPIC-025` | `SPRINT-005` | Arquiteto | `contracts/geo/registry-calibracao-benchmark-e-lifecycle-de-qualitypr/**`<br>`docs/02-architecture/design-reviews/registry-calibracao-benchmark-e-lifecycle-de-qualitypr/**` |
| `STORY-0164` | `ISSUE-0274` | `EPIC-028` | `SPRINT-005` | Arquiteto | `contracts/geo/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/**`<br>`docs/02-architecture/design-reviews/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/**` |
| `STORY-0178` | `ISSUE-0288` | `EPIC-030` | `SPRINT-005` | Arquiteto | `contracts/geo/taxonomia-versionada-de-falhas-evidencias-remediacoes/**`<br>`docs/02-architecture/design-reviews/taxonomia-versionada-de-falhas-evidencias-remediacoes/**` |
| `STORY-0404` | `ISSUE-0514` | `EPIC-065` | `SPRINT-004` | Arquiteto | `contracts/job/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**`<br>`docs/02-architecture/design-reviews/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**` |
| `STORY-0493` | `ISSUE-0603` | `EPIC-079` | `SPRINT-011` | DevOps | `tests/ops/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**`<br>`tools/quality/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**`<br>`.github/workflows/ingress-unico-tls-redes-privadas-limites-e-testes-de-e.yaml` |

## Onda 026

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0046` | `ISSUE-0156` | `EPIC-010` | `SPRINT-002` | Arquiteto | `contracts/plt/autorizacao-por-projeto-operacao-artefato-e-caminho/**`<br>`docs/02-architecture/design-reviews/autorizacao-por-projeto-operacao-artefato-e-caminho/**` |
| `STORY-0083` | `ISSUE-0193` | `EPIC-016` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/retries-redelivery-cancelamento-retomada-e-idempotenci/**`<br>`src/backend/dsgeorref/adapters/retries-redelivery-cancelamento-retomada-e-idempotenci/**` |
| `STORY-0084` | `ISSUE-0194` | `EPIC-016` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/retries-redelivery-cancelamento-retomada-e-idempotenci/**`<br>`src/backend/dsgeorref/adapters/retries-redelivery-cancelamento-retomada-e-idempotenci/**` |
| `STORY-0085` | `ISSUE-0195` | `EPIC-016` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/retries-redelivery-cancelamento-retomada-e-idempotenci/**`<br>`src/backend/dsgeorref/adapters/retries-redelivery-cancelamento-retomada-e-idempotenci/**` |
| `STORY-0086` | `ISSUE-0196` | `EPIC-016` | `SPRINT-003` | DevOps | `tests/job/retries-redelivery-cancelamento-retomada-e-idempotenci/**`<br>`tools/quality/retries-redelivery-cancelamento-retomada-e-idempotenci/**`<br>`.github/workflows/retries-redelivery-cancelamento-retomada-e-idempotenci.yaml` |
| `STORY-0144` | `ISSUE-0254` | `EPIC-025` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-calibracao-benchmark-e-lifecycle-de-qualitypr/**` |
| `STORY-0145` | `ISSUE-0255` | `EPIC-025` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-calibracao-benchmark-e-lifecycle-de-qualitypr/**` |
| `STORY-0146` | `ISSUE-0256` | `EPIC-025` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-calibracao-benchmark-e-lifecycle-de-qualitypr/**` |
| `STORY-0147` | `ISSUE-0257` | `EPIC-025` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-calibracao-benchmark-e-lifecycle-de-qualitypr/**` |
| `STORY-0166` | `ISSUE-0276` | `EPIC-028` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/**` |
| `STORY-0167` | `ISSUE-0277` | `EPIC-028` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/**` |
| `STORY-0168` | `ISSUE-0278` | `EPIC-028` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/**` |
| `STORY-0179` | `ISSUE-0289` | `EPIC-030` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/taxonomia-versionada-de-falhas-evidencias-remediacoes/**` |
| `STORY-0180` | `ISSUE-0290` | `EPIC-030` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/taxonomia-versionada-de-falhas-evidencias-remediacoes/**` |
| `STORY-0181` | `ISSUE-0291` | `EPIC-030` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/taxonomia-versionada-de-falhas-evidencias-remediacoes/**` |
| `STORY-0182` | `ISSUE-0292` | `EPIC-030` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/taxonomia-versionada-de-falhas-evidencias-remediacoes/**` |
| `STORY-0405` | `ISSUE-0515` | `EPIC-065` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**`<br>`src/backend/dsgeorref/adapters/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**` |
| `STORY-0406` | `ISSUE-0516` | `EPIC-065` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**`<br>`src/backend/dsgeorref/adapters/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**` |
| `STORY-0407` | `ISSUE-0517` | `EPIC-065` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**`<br>`src/backend/dsgeorref/adapters/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**` |
| `STORY-0408` | `ISSUE-0518` | `EPIC-065` | `SPRINT-004` | DevOps | `tests/job/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**`<br>`tools/quality/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**`<br>`.github/workflows/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten.yaml` |
| `STORY-0494` | `ISSUE-0604` | `EPIC-079` | `SPRINT-011` | DevOps | `tests/ops/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**`<br>`tools/quality/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**`<br>`.github/workflows/ingress-unico-tls-redes-privadas-limites-e-testes-de-e.yaml` |
| `STORY-0495` | `ISSUE-0605` | `EPIC-079` | `SPRINT-011` | DevOps | `tests/ops/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**`<br>`tools/quality/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**`<br>`.github/workflows/ingress-unico-tls-redes-privadas-limites-e-testes-de-e.yaml` |
| `STORY-0496` | `ISSUE-0606` | `EPIC-079` | `SPRINT-011` | QA | `tests/ops/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**`<br>`tools/quality/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**`<br>`.github/workflows/ingress-unico-tls-redes-privadas-limites-e-testes-de-e.yaml` |
| `STORY-0735` | `ISSUE-0845` | `EPIC-028` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/ai-aie-classicprofile-parte-1/**` |
| `STORY-0736` | `ISSUE-0846` | `EPIC-028` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/classicprofile-scp-sdr-parte-2/**` |
| `STORY-0737` | `ISSUE-0847` | `EPIC-028` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/sgvcal-srg-tool-parte-3/**` |

## Onda 027

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0048` | `ISSUE-0158` | `EPIC-010` | `SPRINT-002` | Frontend | `src/frontend/src/features/autorizacao-por-projeto-operacao-artefato-e-caminho/**` |
| `STORY-0087` | `ISSUE-0197` | `EPIC-016` | `SPRINT-003` | QA | `tests/job/retries-redelivery-cancelamento-retomada-e-idempotenci/**`<br>`tools/quality/retries-redelivery-cancelamento-retomada-e-idempotenci/**`<br>`.github/workflows/retries-redelivery-cancelamento-retomada-e-idempotenci.yaml` |
| `STORY-0148` | `ISSUE-0258` | `EPIC-025` | `SPRINT-005` | QA | `tests/geo/registry-calibracao-benchmark-e-lifecycle-de-qualitypr/**`<br>`tools/quality/registry-calibracao-benchmark-e-lifecycle-de-qualitypr/**`<br>`.github/workflows/registry-calibracao-benchmark-e-lifecycle-de-qualitypr.yaml` |
| `STORY-0165` | `ISSUE-0275` | `EPIC-028` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/consolidacao/**` |
| `STORY-0183` | `ISSUE-0293` | `EPIC-030` | `SPRINT-005` | QA | `tests/geo/taxonomia-versionada-de-falhas-evidencias-remediacoes/**`<br>`tools/quality/taxonomia-versionada-de-falhas-evidencias-remediacoes/**`<br>`.github/workflows/taxonomia-versionada-de-falhas-evidencias-remediacoes.yaml` |
| `STORY-0409` | `ISSUE-0519` | `EPIC-065` | `SPRINT-004` | QA | `tests/job/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**`<br>`tools/quality/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**`<br>`.github/workflows/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten.yaml` |
| `STORY-0497` | `ISSUE-0607` | `EPIC-079` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**`<br>`tests/security/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**` |
| `STORY-0716` | `ISSUE-0826` | `EPIC-010` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/autorizacao-por-projeto-operacao-artefato-e-caminho/acc-auth-impl-parte-1/**`<br>`src/backend/dsgeorref/adapters/autorizacao-por-projeto-operacao-artefato-e-caminho/acc-auth-impl-parte-1/**` |
| `STORY-0717` | `ISSUE-0827` | `EPIC-010` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/autorizacao-por-projeto-operacao-artefato-e-caminho/hw-parte-2/**`<br>`src/backend/dsgeorref/adapters/autorizacao-por-projeto-operacao-artefato-e-caminho/hw-parte-2/**` |

## Onda 028

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0047` | `ISSUE-0157` | `EPIC-010` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/autorizacao-por-projeto-operacao-artefato-e-caminho/consolidacao/**`<br>`src/backend/dsgeorref/adapters/autorizacao-por-projeto-operacao-artefato-e-caminho/consolidacao/**` |
| `STORY-0088` | `ISSUE-0198` | `EPIC-016` | `SPRINT-003` | Reviewer | `evidence/reviews/retries-redelivery-cancelamento-retomada-e-idempotenci/**` |
| `STORY-0149` | `ISSUE-0259` | `EPIC-025` | `SPRINT-005` | Reviewer | `evidence/reviews/registry-calibracao-benchmark-e-lifecycle-de-qualitypr/**` |
| `STORY-0169` | `ISSUE-0279` | `EPIC-028` | `SPRINT-005` | QA | `tests/geo/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/**`<br>`tools/quality/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/**`<br>`.github/workflows/benchmarks-por-periodo-sensor-e-perfil-de-qualidade.yaml` |
| `STORY-0184` | `ISSUE-0294` | `EPIC-030` | `SPRINT-005` | Reviewer | `evidence/reviews/taxonomia-versionada-de-falhas-evidencias-remediacoes/**` |
| `STORY-0410` | `ISSUE-0520` | `EPIC-065` | `SPRINT-004` | Reviewer | `evidence/reviews/taxonomia-de-retry-tecnico-orcamento-backoff-idempoten/**` |
| `STORY-0498` | `ISSUE-0608` | `EPIC-079` | `SPRINT-011` | Reviewer | `evidence/reviews/ingress-unico-tls-redes-privadas-limites-e-testes-de-e/**` |

## Onda 029

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0049` | `ISSUE-0159` | `EPIC-010` | `SPRINT-002` | Security | `src/backend/dsgeorref/security/autorizacao-por-projeto-operacao-artefato-e-caminho/**`<br>`tests/security/autorizacao-por-projeto-operacao-artefato-e-caminho/**` |
| `STORY-0170` | `ISSUE-0280` | `EPIC-028` | `SPRINT-005` | Reviewer | `evidence/reviews/benchmarks-por-periodo-sensor-e-perfil-de-qualidade/**` |
| `STORY-0309` | `ISSUE-0419` | `EPIC-051` | `SPRINT-006` | Arquiteto | `contracts/geo/estimadores-usac-magsac-ransac-explicitos-calibracao-p/**`<br>`docs/02-architecture/design-reviews/estimadores-usac-magsac-ransac-explicitos-calibracao-p/**` |

## Onda 030

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0050` | `ISSUE-0160` | `EPIC-010` | `SPRINT-002` | Reviewer | `evidence/reviews/autorizacao-por-projeto-operacao-artefato-e-caminho/**` |
| `STORY-0310` | `ISSUE-0420` | `EPIC-051` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/estimadores-usac-magsac-ransac-explicitos-calibracao-p/**` |
| `STORY-0311` | `ISSUE-0421` | `EPIC-051` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/estimadores-usac-magsac-ransac-explicitos-calibracao-p/**` |
| `STORY-0312` | `ISSUE-0422` | `EPIC-051` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/estimadores-usac-magsac-ransac-explicitos-calibracao-p/**` |
| `STORY-0313` | `ISSUE-0423` | `EPIC-051` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/estimadores-usac-magsac-ransac-explicitos-calibracao-p/**` |

## Onda 031

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0051` | `ISSUE-0161` | `EPIC-011` | `SPRINT-002` | Arquiteto | `contracts/plt/limites-idempotencia-audit-log-e-controles-administrat/**`<br>`docs/02-architecture/design-reviews/limites-idempotencia-audit-log-e-controles-administrat/**` |
| `STORY-0056` | `ISSUE-0166` | `EPIC-012` | `SPRINT-002` | Arquiteto | `contracts/dat/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/**`<br>`docs/02-architecture/design-reviews/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/**` |
| `STORY-0314` | `ISSUE-0424` | `EPIC-051` | `SPRINT-006` | QA | `tests/geo/estimadores-usac-magsac-ransac-explicitos-calibracao-p/**`<br>`tools/quality/estimadores-usac-magsac-ransac-explicitos-calibracao-p/**`<br>`.github/workflows/estimadores-usac-magsac-ransac-explicitos-calibracao-p.yaml` |
| `STORY-0511` | `ISSUE-0621` | `EPIC-082` | `SPRINT-002` | Arquiteto | `contracts/plt/preflight-de-hardware-e-executionprofiles-cpu-gpu-hibr/**`<br>`docs/02-architecture/design-reviews/preflight-de-hardware-e-executionprofiles-cpu-gpu-hibr/**` |

## Onda 032

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0052` | `ISSUE-0162` | `EPIC-011` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/limites-idempotencia-audit-log-e-controles-administrat/**`<br>`src/backend/dsgeorref/adapters/limites-idempotencia-audit-log-e-controles-administrat/**` |
| `STORY-0053` | `ISSUE-0163` | `EPIC-011` | `SPRINT-002` | Frontend | `src/frontend/src/features/limites-idempotencia-audit-log-e-controles-administrat/**` |
| `STORY-0058` | `ISSUE-0168` | `EPIC-012` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/**`<br>`src/backend/dsgeorref/adapters/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/**` |
| `STORY-0059` | `ISSUE-0169` | `EPIC-012` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/**`<br>`src/backend/dsgeorref/adapters/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/**` |
| `STORY-0315` | `ISSUE-0425` | `EPIC-051` | `SPRINT-006` | Reviewer | `evidence/reviews/estimadores-usac-magsac-ransac-explicitos-calibracao-p/**` |
| `STORY-0512` | `ISSUE-0622` | `EPIC-082` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/preflight-de-hardware-e-executionprofiles-cpu-gpu-hibr/**`<br>`src/backend/dsgeorref/adapters/preflight-de-hardware-e-executionprofiles-cpu-gpu-hibr/**` |
| `STORY-0513` | `ISSUE-0623` | `EPIC-082` | `SPRINT-002` | Frontend | `src/frontend/src/features/preflight-de-hardware-e-executionprofiles-cpu-gpu-hibr/**` |
| `STORY-0718` | `ISSUE-0828` | `EPIC-012` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/art-artlayout-cat-parte-1/**`<br>`src/backend/dsgeorref/adapters/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/art-artlayout-cat-parte-1/**` |
| `STORY-0719` | `ISSUE-0829` | `EPIC-012` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/prv-run-scm-parte-2/**`<br>`src/backend/dsgeorref/adapters/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/prv-run-scm-parte-2/**` |
| `STORY-0720` | `ISSUE-0830` | `EPIC-012` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/upg-parte-3/**`<br>`src/backend/dsgeorref/adapters/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/upg-parte-3/**` |

## Onda 033

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0054` | `ISSUE-0164` | `EPIC-011` | `SPRINT-002` | Security | `src/backend/dsgeorref/security/limites-idempotencia-audit-log-e-controles-administrat/**`<br>`tests/security/limites-idempotencia-audit-log-e-controles-administrat/**` |
| `STORY-0057` | `ISSUE-0167` | `EPIC-012` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/consolidacao/**`<br>`src/backend/dsgeorref/adapters/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/consolidacao/**` |
| `STORY-0514` | `ISSUE-0624` | `EPIC-082` | `SPRINT-002` | Security | `src/backend/dsgeorref/security/preflight-de-hardware-e-executionprofiles-cpu-gpu-hibr/**`<br>`tests/security/preflight-de-hardware-e-executionprofiles-cpu-gpu-hibr/**` |

## Onda 034

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0055` | `ISSUE-0165` | `EPIC-011` | `SPRINT-002` | Reviewer | `evidence/reviews/limites-idempotencia-audit-log-e-controles-administrat/**` |
| `STORY-0060` | `ISSUE-0170` | `EPIC-012` | `SPRINT-002` | Security | `src/backend/dsgeorref/security/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/**`<br>`tests/security/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/**` |
| `STORY-0515` | `ISSUE-0625` | `EPIC-082` | `SPRINT-002` | Reviewer | `evidence/reviews/preflight-de-hardware-e-executionprofiles-cpu-gpu-hibr/**` |

## Onda 035

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0061` | `ISSUE-0171` | `EPIC-012` | `SPRINT-002` | Reviewer | `evidence/reviews/raizes-de-workspace-api-de-navegacao-segura-catalogo-h/**` |
| `STORY-0185` | `ISSUE-0295` | `EPIC-031` | `SPRINT-009` | Product Owner | `docs/01-product/capabilities/react-typescript-vite-design-system-cliente-openapi-se/**` |

## Onda 036

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0062` | `ISSUE-0172` | `EPIC-013` | `SPRINT-002` | Arquiteto | `contracts/dat/backup-restore-consistente-entre-banco-e-arquivos/**`<br>`docs/02-architecture/design-reviews/backup-restore-consistente-entre-banco-e-arquivos/**` |
| `STORY-0096` | `ISSUE-0206` | `EPIC-018` | `SPRINT-003` | Arquiteto | `contracts/job/batch-hierarquico-chunking-backpressure-checkpoints-e/**`<br>`docs/02-architecture/design-reviews/batch-hierarquico-chunking-backpressure-checkpoints-e/**` |
| `STORY-0110` | `ISSUE-0220` | `EPIC-020` | `SPRINT-003` | Arquiteto | `contracts/cli/cli-estavel-para-projetos-ingestao-jobs-e-resultados/**`<br>`docs/02-architecture/design-reviews/cli-estavel-para-projetos-ingestao-jobs-e-resultados/**` |
| `STORY-0150` | `ISSUE-0260` | `EPIC-026` | `SPRINT-005` | Arquiteto | `contracts/geo/artefatos-e-lineage/**`<br>`docs/02-architecture/design-reviews/artefatos-e-lineage/**` |
| `STORY-0187` | `ISSUE-0297` | `EPIC-031` | `SPRINT-009` | Frontend | `src/frontend/src/features/react-typescript-vite-design-system-cliente-openapi-se/**` |
| `STORY-0188` | `ISSUE-0298` | `EPIC-031` | `SPRINT-009` | Frontend | `src/frontend/src/features/react-typescript-vite-design-system-cliente-openapi-se/**` |
| `STORY-0244` | `ISSUE-0354` | `EPIC-041` | `SPRINT-002` | Security | `src/backend/dsgeorref/security/threat-model-validado-scanning-e-testes-ofensivos/**`<br>`tests/security/threat-model-validado-scanning-e-testes-ofensivos/**` |
| `STORY-0261` | `ISSUE-0371` | `EPIC-044` | `SPRINT-005` | Arquiteto | `contracts/geo/outputprofile-cog-canonico-preservacao-de-resolucao-e/**`<br>`docs/02-architecture/design-reviews/outputprofile-cog-canonico-preservacao-de-resolucao-e/**` |
| `STORY-0738` | `ISSUE-0848` | `EPIC-031` | `SPRINT-009` | Frontend | `src/frontend/src/features/react-typescript-vite-design-system-cliente-openapi-se/requirements-epic-fs1-run-parte-1/**` |
| `STORY-0739` | `ISSUE-0849` | `EPIC-031` | `SPRINT-009` | Frontend | `src/frontend/src/features/react-typescript-vite-design-system-cliente-openapi-se/run-runtime-parte-2/**` |
| `STORY-0740` | `ISSUE-0850` | `EPIC-031` | `SPRINT-009` | Frontend | `src/frontend/src/features/react-typescript-vite-design-system-cliente-openapi-se/ux-parte-3/**` |

## Onda 037

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0063` | `ISSUE-0173` | `EPIC-013` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/backup-restore-consistente-entre-banco-e-arquivos/**`<br>`src/backend/dsgeorref/adapters/backup-restore-consistente-entre-banco-e-arquivos/**` |
| `STORY-0064` | `ISSUE-0174` | `EPIC-013` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/backup-restore-consistente-entre-banco-e-arquivos/**`<br>`src/backend/dsgeorref/adapters/backup-restore-consistente-entre-banco-e-arquivos/**` |
| `STORY-0065` | `ISSUE-0175` | `EPIC-013` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/backup-restore-consistente-entre-banco-e-arquivos/**`<br>`src/backend/dsgeorref/adapters/backup-restore-consistente-entre-banco-e-arquivos/**` |
| `STORY-0097` | `ISSUE-0207` | `EPIC-018` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/batch-hierarquico-chunking-backpressure-checkpoints-e/**`<br>`src/backend/dsgeorref/adapters/batch-hierarquico-chunking-backpressure-checkpoints-e/**` |
| `STORY-0098` | `ISSUE-0208` | `EPIC-018` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/batch-hierarquico-chunking-backpressure-checkpoints-e/**`<br>`src/backend/dsgeorref/adapters/batch-hierarquico-chunking-backpressure-checkpoints-e/**` |
| `STORY-0099` | `ISSUE-0209` | `EPIC-018` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/batch-hierarquico-chunking-backpressure-checkpoints-e/**`<br>`src/backend/dsgeorref/adapters/batch-hierarquico-chunking-backpressure-checkpoints-e/**` |
| `STORY-0100` | `ISSUE-0210` | `EPIC-018` | `SPRINT-003` | DevOps | `tests/job/batch-hierarquico-chunking-backpressure-checkpoints-e/**`<br>`tools/quality/batch-hierarquico-chunking-backpressure-checkpoints-e/**`<br>`.github/workflows/batch-hierarquico-chunking-backpressure-checkpoints-e.yaml` |
| `STORY-0111` | `ISSUE-0221` | `EPIC-020` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/cli-estavel-para-projetos-ingestao-jobs-e-resultados/**`<br>`src/backend/dsgeorref/adapters/cli-estavel-para-projetos-ingestao-jobs-e-resultados/**` |
| `STORY-0112` | `ISSUE-0222` | `EPIC-020` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/cli-estavel-para-projetos-ingestao-jobs-e-resultados/**`<br>`src/backend/dsgeorref/adapters/cli-estavel-para-projetos-ingestao-jobs-e-resultados/**` |
| `STORY-0152` | `ISSUE-0262` | `EPIC-026` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artefatos-e-lineage/**` |
| `STORY-0153` | `ISSUE-0263` | `EPIC-026` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artefatos-e-lineage/**` |
| `STORY-0154` | `ISSUE-0264` | `EPIC-026` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artefatos-e-lineage/**` |
| `STORY-0186` | `ISSUE-0296` | `EPIC-031` | `SPRINT-009` | Frontend | `src/frontend/src/features/react-typescript-vite-design-system-cliente-openapi-se/consolidacao/**` |
| `STORY-0246` | `ISSUE-0356` | `EPIC-041` | `SPRINT-002` | Backend | `src/backend/dsgeorref/application/threat-model-validado-scanning-e-testes-ofensivos/**`<br>`src/backend/dsgeorref/adapters/threat-model-validado-scanning-e-testes-ofensivos/**` |
| `STORY-0247` | `ISSUE-0357` | `EPIC-041` | `SPRINT-002` | Security | `src/backend/dsgeorref/security/threat-model-validado-scanning-e-testes-ofensivos/**`<br>`tests/security/threat-model-validado-scanning-e-testes-ofensivos/**` |
| `STORY-0262` | `ISSUE-0372` | `EPIC-044` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/outputprofile-cog-canonico-preservacao-de-resolucao-e/**` |
| `STORY-0263` | `ISSUE-0373` | `EPIC-044` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/outputprofile-cog-canonico-preservacao-de-resolucao-e/**` |
| `STORY-0264` | `ISSUE-0374` | `EPIC-044` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/outputprofile-cog-canonico-preservacao-de-resolucao-e/**` |
| `STORY-0265` | `ISSUE-0375` | `EPIC-044` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/outputprofile-cog-canonico-preservacao-de-resolucao-e/**` |
| `STORY-0732` | `ISSUE-0842` | `EPIC-026` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artefatos-e-lineage/art-artlayout-parte-1/**` |
| `STORY-0733` | `ISSUE-0843` | `EPIC-026` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artefatos-e-lineage/artlayout-dbschema-fs1-parte-2/**` |
| `STORY-0734` | `ISSUE-0844` | `EPIC-026` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artefatos-e-lineage/native-parte-3/**` |
| `STORY-0747` | `ISSUE-0857` | `EPIC-041` | `SPRINT-002` | Arquiteto | `contracts/sec/threat-model-validado-scanning-e-testes-ofensivos/aie-parte-1/**`<br>`docs/02-architecture/design-reviews/threat-model-validado-scanning-e-testes-ofensivos/aie-parte-1/**` |
| `STORY-0748` | `ISSUE-0858` | `EPIC-041` | `SPRINT-002` | Arquiteto | `contracts/sec/threat-model-validado-scanning-e-testes-ofensivos/artlayout-auth-impl-parte-2/**`<br>`docs/02-architecture/design-reviews/threat-model-validado-scanning-e-testes-ofensivos/artlayout-auth-impl-parte-2/**` |
| `STORY-0749` | `ISSUE-0859` | `EPIC-041` | `SPRINT-002` | Arquiteto | `contracts/sec/threat-model-validado-scanning-e-testes-ofensivos/auth-impl-epic-fs-parte-3/**`<br>`docs/02-architecture/design-reviews/threat-model-validado-scanning-e-testes-ofensivos/auth-impl-epic-fs-parte-3/**` |

## Onda 038

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0066` | `ISSUE-0176` | `EPIC-013` | `SPRINT-002` | Security | `src/backend/dsgeorref/security/backup-restore-consistente-entre-banco-e-arquivos/**`<br>`tests/security/backup-restore-consistente-entre-banco-e-arquivos/**` |
| `STORY-0101` | `ISSUE-0211` | `EPIC-018` | `SPRINT-003` | QA | `tests/job/batch-hierarquico-chunking-backpressure-checkpoints-e/**`<br>`tools/quality/batch-hierarquico-chunking-backpressure-checkpoints-e/**`<br>`.github/workflows/batch-hierarquico-chunking-backpressure-checkpoints-e.yaml` |
| `STORY-0113` | `ISSUE-0223` | `EPIC-020` | `SPRINT-003` | QA | `tests/cli/cli-estavel-para-projetos-ingestao-jobs-e-resultados/**`<br>`tools/quality/cli-estavel-para-projetos-ingestao-jobs-e-resultados/**`<br>`.github/workflows/cli-estavel-para-projetos-ingestao-jobs-e-resultados.yaml` |
| `STORY-0151` | `ISSUE-0261` | `EPIC-026` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artefatos-e-lineage/consolidacao/**` |
| `STORY-0189` | `ISSUE-0299` | `EPIC-031` | `SPRINT-009` | QA | `tests/web/react-typescript-vite-design-system-cliente-openapi-se/**`<br>`tools/quality/react-typescript-vite-design-system-cliente-openapi-se/**`<br>`.github/workflows/react-typescript-vite-design-system-cliente-openapi-se.yaml` |
| `STORY-0245` | `ISSUE-0355` | `EPIC-041` | `SPRINT-002` | Arquiteto | `contracts/sec/threat-model-validado-scanning-e-testes-ofensivos/consolidacao/**`<br>`docs/02-architecture/design-reviews/threat-model-validado-scanning-e-testes-ofensivos/consolidacao/**` |
| `STORY-0266` | `ISSUE-0376` | `EPIC-044` | `SPRINT-005` | QA | `tests/geo/outputprofile-cog-canonico-preservacao-de-resolucao-e/**`<br>`tools/quality/outputprofile-cog-canonico-preservacao-de-resolucao-e/**`<br>`.github/workflows/outputprofile-cog-canonico-preservacao-de-resolucao-e.yaml` |

## Onda 039

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0067` | `ISSUE-0177` | `EPIC-013` | `SPRINT-002` | Reviewer | `evidence/reviews/backup-restore-consistente-entre-banco-e-arquivos/**` |
| `STORY-0102` | `ISSUE-0212` | `EPIC-018` | `SPRINT-003` | Reviewer | `evidence/reviews/batch-hierarquico-chunking-backpressure-checkpoints-e/**` |
| `STORY-0114` | `ISSUE-0224` | `EPIC-020` | `SPRINT-003` | Reviewer | `evidence/reviews/cli-estavel-para-projetos-ingestao-jobs-e-resultados/**` |
| `STORY-0155` | `ISSUE-0265` | `EPIC-026` | `SPRINT-005` | QA | `tests/geo/artefatos-e-lineage/**`<br>`tools/quality/artefatos-e-lineage/**`<br>`.github/workflows/artefatos-e-lineage.yaml` |
| `STORY-0190` | `ISSUE-0300` | `EPIC-031` | `SPRINT-009` | Reviewer | `evidence/reviews/react-typescript-vite-design-system-cliente-openapi-se/**` |
| `STORY-0248` | `ISSUE-0358` | `EPIC-041` | `SPRINT-002` | DevOps | `tests/sec/threat-model-validado-scanning-e-testes-ofensivos/**`<br>`tools/quality/threat-model-validado-scanning-e-testes-ofensivos/**`<br>`.github/workflows/threat-model-validado-scanning-e-testes-ofensivos.yaml` |
| `STORY-0267` | `ISSUE-0377` | `EPIC-044` | `SPRINT-005` | Reviewer | `evidence/reviews/outputprofile-cog-canonico-preservacao-de-resolucao-e/**` |

## Onda 040

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0103` | `ISSUE-0213` | `EPIC-019` | `SPRINT-003` | Arquiteto | `contracts/job/resource-governor-admission-control-e-orcamento-adapta/**`<br>`docs/02-architecture/design-reviews/resource-governor-admission-control-e-orcamento-adapta/**` |
| `STORY-0156` | `ISSUE-0266` | `EPIC-026` | `SPRINT-005` | Reviewer | `evidence/reviews/artefatos-e-lineage/**` |
| `STORY-0191` | `ISSUE-0301` | `EPIC-032` | `SPRINT-009` | Product Owner | `docs/01-product/capabilities/workspace-openlayers-configuracao-acompanhamento-e-rev/**` |
| `STORY-0249` | `ISSUE-0359` | `EPIC-041` | `SPRINT-002` | Reviewer | `evidence/reviews/threat-model-validado-scanning-e-testes-ofensivos/**` |
| `STORY-0268` | `ISSUE-0378` | `EPIC-045` | `SPRINT-005` | Arquiteto | `contracts/geo/mascara-analitica-adaptativa-preview-correcao-area-uti/**`<br>`docs/02-architecture/design-reviews/mascara-analitica-adaptativa-preview-correcao-area-uti/**` |
| `STORY-0411` | `ISSUE-0521` | `EPIC-066` | `SPRINT-004` | Arquiteto | `contracts/job/checkpoints-canonicos-manifests-de-compatibilidade-ret/**`<br>`docs/02-architecture/design-reviews/checkpoints-canonicos-manifests-de-compatibilidade-ret/**` |

## Onda 041

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0104` | `ISSUE-0214` | `EPIC-019` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/resource-governor-admission-control-e-orcamento-adapta/**`<br>`src/backend/dsgeorref/adapters/resource-governor-admission-control-e-orcamento-adapta/**` |
| `STORY-0105` | `ISSUE-0215` | `EPIC-019` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/resource-governor-admission-control-e-orcamento-adapta/**`<br>`src/backend/dsgeorref/adapters/resource-governor-admission-control-e-orcamento-adapta/**` |
| `STORY-0106` | `ISSUE-0216` | `EPIC-019` | `SPRINT-003` | Backend | `src/backend/dsgeorref/application/resource-governor-admission-control-e-orcamento-adapta/**`<br>`src/backend/dsgeorref/adapters/resource-governor-admission-control-e-orcamento-adapta/**` |
| `STORY-0107` | `ISSUE-0217` | `EPIC-019` | `SPRINT-003` | DevOps | `tests/job/resource-governor-admission-control-e-orcamento-adapta/**`<br>`tools/quality/resource-governor-admission-control-e-orcamento-adapta/**`<br>`.github/workflows/resource-governor-admission-control-e-orcamento-adapta.yaml` |
| `STORY-0157` | `ISSUE-0267` | `EPIC-027` | `SPRINT-005` | Arquiteto | `contracts/geo/gateway-de-fontes-protecao-ssrf-estados-de-disponibili/**`<br>`docs/02-architecture/design-reviews/gateway-de-fontes-protecao-ssrf-estados-de-disponibili/**` |
| `STORY-0192` | `ISSUE-0302` | `EPIC-032` | `SPRINT-009` | Frontend | `src/frontend/src/features/workspace-openlayers-configuracao-acompanhamento-e-rev/**` |
| `STORY-0193` | `ISSUE-0303` | `EPIC-032` | `SPRINT-009` | Frontend | `src/frontend/src/features/workspace-openlayers-configuracao-acompanhamento-e-rev/**` |
| `STORY-0194` | `ISSUE-0304` | `EPIC-032` | `SPRINT-009` | Frontend | `src/frontend/src/features/workspace-openlayers-configuracao-acompanhamento-e-rev/**` |
| `STORY-0269` | `ISSUE-0379` | `EPIC-045` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/mascara-analitica-adaptativa-preview-correcao-area-uti/**` |
| `STORY-0270` | `ISSUE-0380` | `EPIC-045` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/mascara-analitica-adaptativa-preview-correcao-area-uti/**` |
| `STORY-0271` | `ISSUE-0381` | `EPIC-045` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/mascara-analitica-adaptativa-preview-correcao-area-uti/**` |
| `STORY-0272` | `ISSUE-0382` | `EPIC-045` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/mascara-analitica-adaptativa-preview-correcao-area-uti/**` |
| `STORY-0275` | `ISSUE-0385` | `EPIC-046` | `SPRINT-005` | Arquiteto | `contracts/geo/artifactset-imutavel-staging-e-publicacao-atomica/**`<br>`docs/02-architecture/design-reviews/artifactset-imutavel-staging-e-publicacao-atomica/**` |
| `STORY-0412` | `ISSUE-0522` | `EPIC-066` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/checkpoints-canonicos-manifests-de-compatibilidade-ret/**`<br>`src/backend/dsgeorref/adapters/checkpoints-canonicos-manifests-de-compatibilidade-ret/**` |
| `STORY-0413` | `ISSUE-0523` | `EPIC-066` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/checkpoints-canonicos-manifests-de-compatibilidade-ret/**`<br>`src/backend/dsgeorref/adapters/checkpoints-canonicos-manifests-de-compatibilidade-ret/**` |
| `STORY-0414` | `ISSUE-0524` | `EPIC-066` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/checkpoints-canonicos-manifests-de-compatibilidade-ret/**`<br>`src/backend/dsgeorref/adapters/checkpoints-canonicos-manifests-de-compatibilidade-ret/**` |
| `STORY-0415` | `ISSUE-0525` | `EPIC-066` | `SPRINT-004` | DevOps | `tests/job/checkpoints-canonicos-manifests-de-compatibilidade-ret/**`<br>`tools/quality/checkpoints-canonicos-manifests-de-compatibilidade-ret/**`<br>`.github/workflows/checkpoints-canonicos-manifests-de-compatibilidade-ret.yaml` |

## Onda 042

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0108` | `ISSUE-0218` | `EPIC-019` | `SPRINT-003` | QA | `tests/job/resource-governor-admission-control-e-orcamento-adapta/**`<br>`tools/quality/resource-governor-admission-control-e-orcamento-adapta/**`<br>`.github/workflows/resource-governor-admission-control-e-orcamento-adapta.yaml` |
| `STORY-0158` | `ISSUE-0268` | `EPIC-027` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/gateway-de-fontes-protecao-ssrf-estados-de-disponibili/**` |
| `STORY-0159` | `ISSUE-0269` | `EPIC-027` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/gateway-de-fontes-protecao-ssrf-estados-de-disponibili/**` |
| `STORY-0160` | `ISSUE-0270` | `EPIC-027` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/gateway-de-fontes-protecao-ssrf-estados-de-disponibili/**` |
| `STORY-0161` | `ISSUE-0271` | `EPIC-027` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/gateway-de-fontes-protecao-ssrf-estados-de-disponibili/**` |
| `STORY-0195` | `ISSUE-0305` | `EPIC-032` | `SPRINT-009` | QA | `tests/web/workspace-openlayers-configuracao-acompanhamento-e-rev/**`<br>`tools/quality/workspace-openlayers-configuracao-acompanhamento-e-rev/**`<br>`.github/workflows/workspace-openlayers-configuracao-acompanhamento-e-rev.yaml` |
| `STORY-0273` | `ISSUE-0383` | `EPIC-045` | `SPRINT-005` | QA | `tests/geo/mascara-analitica-adaptativa-preview-correcao-area-uti/**`<br>`tools/quality/mascara-analitica-adaptativa-preview-correcao-area-uti/**`<br>`.github/workflows/mascara-analitica-adaptativa-preview-correcao-area-uti.yaml` |
| `STORY-0276` | `ISSUE-0386` | `EPIC-046` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artifactset-imutavel-staging-e-publicacao-atomica/**` |
| `STORY-0277` | `ISSUE-0387` | `EPIC-046` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artifactset-imutavel-staging-e-publicacao-atomica/**` |
| `STORY-0278` | `ISSUE-0388` | `EPIC-046` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artifactset-imutavel-staging-e-publicacao-atomica/**` |
| `STORY-0279` | `ISSUE-0389` | `EPIC-046` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/artifactset-imutavel-staging-e-publicacao-atomica/**` |
| `STORY-0416` | `ISSUE-0526` | `EPIC-066` | `SPRINT-004` | QA | `tests/job/checkpoints-canonicos-manifests-de-compatibilidade-ret/**`<br>`tools/quality/checkpoints-canonicos-manifests-de-compatibilidade-ret/**`<br>`.github/workflows/checkpoints-canonicos-manifests-de-compatibilidade-ret.yaml` |

## Onda 043

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0109` | `ISSUE-0219` | `EPIC-019` | `SPRINT-003` | Reviewer | `evidence/reviews/resource-governor-admission-control-e-orcamento-adapta/**` |
| `STORY-0162` | `ISSUE-0272` | `EPIC-027` | `SPRINT-005` | QA | `tests/geo/gateway-de-fontes-protecao-ssrf-estados-de-disponibili/**`<br>`tools/quality/gateway-de-fontes-protecao-ssrf-estados-de-disponibili/**`<br>`.github/workflows/gateway-de-fontes-protecao-ssrf-estados-de-disponibili.yaml` |
| `STORY-0196` | `ISSUE-0306` | `EPIC-032` | `SPRINT-009` | Reviewer | `evidence/reviews/workspace-openlayers-configuracao-acompanhamento-e-rev/**` |
| `STORY-0274` | `ISSUE-0384` | `EPIC-045` | `SPRINT-005` | Reviewer | `evidence/reviews/mascara-analitica-adaptativa-preview-correcao-area-uti/**` |
| `STORY-0280` | `ISSUE-0390` | `EPIC-046` | `SPRINT-005` | QA | `tests/geo/artifactset-imutavel-staging-e-publicacao-atomica/**`<br>`tools/quality/artifactset-imutavel-staging-e-publicacao-atomica/**`<br>`.github/workflows/artifactset-imutavel-staging-e-publicacao-atomica.yaml` |
| `STORY-0417` | `ISSUE-0527` | `EPIC-066` | `SPRINT-004` | Reviewer | `evidence/reviews/checkpoints-canonicos-manifests-de-compatibilidade-ret/**` |

## Onda 044

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0163` | `ISSUE-0273` | `EPIC-027` | `SPRINT-005` | Reviewer | `evidence/reviews/gateway-de-fontes-protecao-ssrf-estados-de-disponibili/**` |
| `STORY-0281` | `ISSUE-0391` | `EPIC-046` | `SPRINT-005` | Reviewer | `evidence/reviews/artifactset-imutavel-staging-e-publicacao-atomica/**` |
| `STORY-0282` | `ISSUE-0392` | `EPIC-047` | `SPRINT-005` | Arquiteto | `contracts/geo/matching-coarse-to-fine-tiles-reconciliacao-de-coorden/**`<br>`docs/02-architecture/design-reviews/matching-coarse-to-fine-tiles-reconciliacao-de-coorden/**` |
| `STORY-0289` | `ISSUE-0399` | `EPIC-048` | `SPRINT-005` | Arquiteto | `contracts/geo/extracao-opcional-de-metadados-marginais-com-confianca/**`<br>`docs/02-architecture/design-reviews/extracao-opcional-de-metadados-marginais-com-confianca/**` |
| `STORY-0316` | `ISSUE-0426` | `EPIC-052` | `SPRINT-006` | Arquiteto | `contracts/geo/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex/**`<br>`docs/02-architecture/design-reviews/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex/**` |
| `STORY-0418` | `ISSUE-0528` | `EPIC-067` | `SPRINT-004` | Arquiteto | `contracts/job/cancelamento-cooperativo-supervisao-de-subprocessos-co/**`<br>`docs/02-architecture/design-reviews/cancelamento-cooperativo-supervisao-de-subprocessos-co/**` |
| `STORY-0425` | `ISSUE-0535` | `EPIC-068` | `SPRINT-004` | Arquiteto | `contracts/job/concorrencia-escalonamento-e-isolamento/**`<br>`docs/02-architecture/design-reviews/concorrencia-escalonamento-e-isolamento/**` |

## Onda 045

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0283` | `ISSUE-0393` | `EPIC-047` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/matching-coarse-to-fine-tiles-reconciliacao-de-coorden/**` |
| `STORY-0284` | `ISSUE-0394` | `EPIC-047` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/matching-coarse-to-fine-tiles-reconciliacao-de-coorden/**` |
| `STORY-0285` | `ISSUE-0395` | `EPIC-047` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/matching-coarse-to-fine-tiles-reconciliacao-de-coorden/**` |
| `STORY-0286` | `ISSUE-0396` | `EPIC-047` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/matching-coarse-to-fine-tiles-reconciliacao-de-coorden/**` |
| `STORY-0290` | `ISSUE-0400` | `EPIC-048` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/extracao-opcional-de-metadados-marginais-com-confianca/**` |
| `STORY-0291` | `ISSUE-0401` | `EPIC-048` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/extracao-opcional-de-metadados-marginais-com-confianca/**` |
| `STORY-0292` | `ISSUE-0402` | `EPIC-048` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/extracao-opcional-de-metadados-marginais-com-confianca/**` |
| `STORY-0293` | `ISSUE-0403` | `EPIC-048` | `SPRINT-005` | Geoprocessamento | `src/geo/dsgeorref_geo/extracao-opcional-de-metadados-marginais-com-confianca/**` |
| `STORY-0317` | `ISSUE-0427` | `EPIC-052` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex/**` |
| `STORY-0318` | `ISSUE-0428` | `EPIC-052` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex/**` |
| `STORY-0319` | `ISSUE-0429` | `EPIC-052` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex/**` |
| `STORY-0320` | `ISSUE-0430` | `EPIC-052` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex/**` |
| `STORY-0358` | `ISSUE-0468` | `EPIC-058` | `SPRINT-006` | Arquiteto | `contracts/geo/gateway-por-capacidades-adapters-stac-api-oficial-test/**`<br>`docs/02-architecture/design-reviews/gateway-por-capacidades-adapters-stac-api-oficial-test/**` |
| `STORY-0419` | `ISSUE-0529` | `EPIC-067` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/cancelamento-cooperativo-supervisao-de-subprocessos-co/**`<br>`src/backend/dsgeorref/adapters/cancelamento-cooperativo-supervisao-de-subprocessos-co/**` |
| `STORY-0420` | `ISSUE-0530` | `EPIC-067` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/cancelamento-cooperativo-supervisao-de-subprocessos-co/**`<br>`src/backend/dsgeorref/adapters/cancelamento-cooperativo-supervisao-de-subprocessos-co/**` |
| `STORY-0421` | `ISSUE-0531` | `EPIC-067` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/cancelamento-cooperativo-supervisao-de-subprocessos-co/**`<br>`src/backend/dsgeorref/adapters/cancelamento-cooperativo-supervisao-de-subprocessos-co/**` |
| `STORY-0422` | `ISSUE-0532` | `EPIC-067` | `SPRINT-004` | DevOps | `tests/job/cancelamento-cooperativo-supervisao-de-subprocessos-co/**`<br>`tools/quality/cancelamento-cooperativo-supervisao-de-subprocessos-co/**`<br>`.github/workflows/cancelamento-cooperativo-supervisao-de-subprocessos-co.yaml` |
| `STORY-0426` | `ISSUE-0536` | `EPIC-068` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/concorrencia-escalonamento-e-isolamento/**`<br>`src/backend/dsgeorref/adapters/concorrencia-escalonamento-e-isolamento/**` |
| `STORY-0427` | `ISSUE-0537` | `EPIC-068` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/concorrencia-escalonamento-e-isolamento/**`<br>`src/backend/dsgeorref/adapters/concorrencia-escalonamento-e-isolamento/**` |
| `STORY-0428` | `ISSUE-0538` | `EPIC-068` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/concorrencia-escalonamento-e-isolamento/**`<br>`src/backend/dsgeorref/adapters/concorrencia-escalonamento-e-isolamento/**` |
| `STORY-0429` | `ISSUE-0539` | `EPIC-068` | `SPRINT-004` | DevOps | `tests/job/concorrencia-escalonamento-e-isolamento/**`<br>`tools/quality/concorrencia-escalonamento-e-isolamento/**`<br>`.github/workflows/concorrencia-escalonamento-e-isolamento.yaml` |

## Onda 046

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0287` | `ISSUE-0397` | `EPIC-047` | `SPRINT-005` | QA | `tests/geo/matching-coarse-to-fine-tiles-reconciliacao-de-coorden/**`<br>`tools/quality/matching-coarse-to-fine-tiles-reconciliacao-de-coorden/**`<br>`.github/workflows/matching-coarse-to-fine-tiles-reconciliacao-de-coorden.yaml` |
| `STORY-0294` | `ISSUE-0404` | `EPIC-048` | `SPRINT-005` | QA | `tests/geo/extracao-opcional-de-metadados-marginais-com-confianca/**`<br>`tools/quality/extracao-opcional-de-metadados-marginais-com-confianca/**`<br>`.github/workflows/extracao-opcional-de-metadados-marginais-com-confianca.yaml` |
| `STORY-0321` | `ISSUE-0431` | `EPIC-052` | `SPRINT-006` | QA | `tests/geo/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex/**`<br>`tools/quality/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex/**`<br>`.github/workflows/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex.yaml` |
| `STORY-0359` | `ISSUE-0469` | `EPIC-058` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/gateway-por-capacidades-adapters-stac-api-oficial-test/**` |
| `STORY-0360` | `ISSUE-0470` | `EPIC-058` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/gateway-por-capacidades-adapters-stac-api-oficial-test/**` |
| `STORY-0361` | `ISSUE-0471` | `EPIC-058` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/gateway-por-capacidades-adapters-stac-api-oficial-test/**` |
| `STORY-0362` | `ISSUE-0472` | `EPIC-058` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/gateway-por-capacidades-adapters-stac-api-oficial-test/**` |
| `STORY-0423` | `ISSUE-0533` | `EPIC-067` | `SPRINT-004` | QA | `tests/job/cancelamento-cooperativo-supervisao-de-subprocessos-co/**`<br>`tools/quality/cancelamento-cooperativo-supervisao-de-subprocessos-co/**`<br>`.github/workflows/cancelamento-cooperativo-supervisao-de-subprocessos-co.yaml` |
| `STORY-0430` | `ISSUE-0540` | `EPIC-068` | `SPRINT-004` | QA | `tests/job/concorrencia-escalonamento-e-isolamento/**`<br>`tools/quality/concorrencia-escalonamento-e-isolamento/**`<br>`.github/workflows/concorrencia-escalonamento-e-isolamento.yaml` |

## Onda 047

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0288` | `ISSUE-0398` | `EPIC-047` | `SPRINT-005` | Reviewer | `evidence/reviews/matching-coarse-to-fine-tiles-reconciliacao-de-coorden/**` |
| `STORY-0295` | `ISSUE-0405` | `EPIC-048` | `SPRINT-005` | Reviewer | `evidence/reviews/extracao-opcional-de-metadados-marginais-com-confianca/**` |
| `STORY-0322` | `ISSUE-0432` | `EPIC-052` | `SPRINT-006` | Reviewer | `evidence/reviews/selecao-de-gcps-por-cobertura-qualidade-diversidade-ex/**` |
| `STORY-0363` | `ISSUE-0473` | `EPIC-058` | `SPRINT-006` | QA | `tests/geo/gateway-por-capacidades-adapters-stac-api-oficial-test/**`<br>`tools/quality/gateway-por-capacidades-adapters-stac-api-oficial-test/**`<br>`.github/workflows/gateway-por-capacidades-adapters-stac-api-oficial-test.yaml` |
| `STORY-0424` | `ISSUE-0534` | `EPIC-067` | `SPRINT-004` | Reviewer | `evidence/reviews/cancelamento-cooperativo-supervisao-de-subprocessos-co/**` |
| `STORY-0431` | `ISSUE-0541` | `EPIC-068` | `SPRINT-004` | Reviewer | `evidence/reviews/concorrencia-escalonamento-e-isolamento/**` |

## Onda 048

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0232` | `ISSUE-0342` | `EPIC-039` | `SPRINT-011` | DevOps | `tests/ops/instrumentacao-opentelemetry-correlation-ids-metricas/**`<br>`tools/quality/instrumentacao-opentelemetry-correlation-ids-metricas/**`<br>`.github/workflows/instrumentacao-opentelemetry-correlation-ids-metricas.yaml` |
| `STORY-0302` | `ISSUE-0412` | `EPIC-050` | `SPRINT-006` | Arquiteto | `contracts/geo/registry-de-matchers-classicos-ia-escalonamento-explic/**`<br>`docs/02-architecture/design-reviews/registry-de-matchers-classicos-ia-escalonamento-explic/**` |
| `STORY-0323` | `ISSUE-0433` | `EPIC-053` | `SPRINT-006` | Arquiteto | `contracts/geo/grafo-de-referencias-verificadas-componentes-desconect/**`<br>`docs/02-architecture/design-reviews/grafo-de-referencias-verificadas-componentes-desconect/**` |
| `STORY-0364` | `ISSUE-0474` | `EPIC-058` | `SPRINT-006` | Reviewer | `evidence/reviews/gateway-por-capacidades-adapters-stac-api-oficial-test/**` |
| `STORY-0391` | `ISSUE-0501` | `EPIC-063` | `SPRINT-006` | Arquiteto | `contracts/geo/modelo-tipado-versionado-de-gcps-lifecycle-provenienci/**`<br>`docs/02-architecture/design-reviews/modelo-tipado-versionado-de-gcps-lifecycle-provenienci/**` |
| `STORY-0432` | `ISSUE-0542` | `EPIC-069` | `SPRINT-004` | Arquiteto | `contracts/job/observabilidade-slos-e-diagnostico-do-scheduler/**`<br>`docs/02-architecture/design-reviews/observabilidade-slos-e-diagnostico-do-scheduler/**` |

## Onda 049

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0234` | `ISSUE-0344` | `EPIC-039` | `SPRINT-011` | DevOps | `tests/ops/instrumentacao-opentelemetry-correlation-ids-metricas/**`<br>`tools/quality/instrumentacao-opentelemetry-correlation-ids-metricas/**`<br>`.github/workflows/instrumentacao-opentelemetry-correlation-ids-metricas.yaml` |
| `STORY-0235` | `ISSUE-0345` | `EPIC-039` | `SPRINT-011` | QA | `tests/ops/instrumentacao-opentelemetry-correlation-ids-metricas/**`<br>`tools/quality/instrumentacao-opentelemetry-correlation-ids-metricas/**`<br>`.github/workflows/instrumentacao-opentelemetry-correlation-ids-metricas.yaml` |
| `STORY-0304` | `ISSUE-0414` | `EPIC-050` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-de-matchers-classicos-ia-escalonamento-explic/**` |
| `STORY-0305` | `ISSUE-0415` | `EPIC-050` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-de-matchers-classicos-ia-escalonamento-explic/**` |
| `STORY-0306` | `ISSUE-0416` | `EPIC-050` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-de-matchers-classicos-ia-escalonamento-explic/**` |
| `STORY-0324` | `ISSUE-0434` | `EPIC-053` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/grafo-de-referencias-verificadas-componentes-desconect/**` |
| `STORY-0325` | `ISSUE-0435` | `EPIC-053` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/grafo-de-referencias-verificadas-componentes-desconect/**` |
| `STORY-0326` | `ISSUE-0436` | `EPIC-053` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/grafo-de-referencias-verificadas-componentes-desconect/**` |
| `STORY-0327` | `ISSUE-0437` | `EPIC-053` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/grafo-de-referencias-verificadas-componentes-desconect/**` |
| `STORY-0365` | `ISSUE-0475` | `EPIC-059` | `SPRINT-006` | Arquiteto | `contracts/geo/busca-espaciotemporal-guiada-ranking-explicavel-incert/**`<br>`docs/02-architecture/design-reviews/busca-espaciotemporal-guiada-ranking-explicavel-incert/**` |
| `STORY-0392` | `ISSUE-0502` | `EPIC-063` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/modelo-tipado-versionado-de-gcps-lifecycle-provenienci/**` |
| `STORY-0393` | `ISSUE-0503` | `EPIC-063` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/modelo-tipado-versionado-de-gcps-lifecycle-provenienci/**` |
| `STORY-0394` | `ISSUE-0504` | `EPIC-063` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/modelo-tipado-versionado-de-gcps-lifecycle-provenienci/**` |
| `STORY-0395` | `ISSUE-0505` | `EPIC-063` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/modelo-tipado-versionado-de-gcps-lifecycle-provenienci/**` |
| `STORY-0433` | `ISSUE-0543` | `EPIC-069` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/observabilidade-slos-e-diagnostico-do-scheduler/**`<br>`src/backend/dsgeorref/adapters/observabilidade-slos-e-diagnostico-do-scheduler/**` |
| `STORY-0434` | `ISSUE-0544` | `EPIC-069` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/observabilidade-slos-e-diagnostico-do-scheduler/**`<br>`src/backend/dsgeorref/adapters/observabilidade-slos-e-diagnostico-do-scheduler/**` |
| `STORY-0435` | `ISSUE-0545` | `EPIC-069` | `SPRINT-004` | Backend | `src/backend/dsgeorref/application/observabilidade-slos-e-diagnostico-do-scheduler/**`<br>`src/backend/dsgeorref/adapters/observabilidade-slos-e-diagnostico-do-scheduler/**` |
| `STORY-0436` | `ISSUE-0546` | `EPIC-069` | `SPRINT-004` | DevOps | `tests/job/observabilidade-slos-e-diagnostico-do-scheduler/**`<br>`tools/quality/observabilidade-slos-e-diagnostico-do-scheduler/**`<br>`.github/workflows/observabilidade-slos-e-diagnostico-do-scheduler.yaml` |
| `STORY-0516` | `ISSUE-0626` | `EPIC-083` | `SPRINT-011` | DevOps | `tests/ops/modos-offline-restricted-connected-egress-enforcement/**`<br>`tools/quality/modos-offline-restricted-connected-egress-enforcement/**`<br>`.github/workflows/modos-offline-restricted-connected-egress-enforcement.yaml` |
| `STORY-0745` | `ISSUE-0855` | `EPIC-039` | `SPRINT-011` | DevOps | `tests/ops/instrumentacao-opentelemetry-correlation-ids-metricas/aie-artlayout-parte-1/**`<br>`tools/quality/instrumentacao-opentelemetry-correlation-ids-metricas/aie-artlayout-parte-1/**`<br>`.github/workflows/instrumentacao-opentelemetry-correlation-ids-metricas-aie-artlayout-pa.yaml` |
| `STORY-0746` | `ISSUE-0856` | `EPIC-039` | `SPRINT-011` | DevOps | `tests/ops/instrumentacao-opentelemetry-correlation-ids-metricas/artlayout-met-worker-parte-2/**`<br>`tools/quality/instrumentacao-opentelemetry-correlation-ids-metricas/artlayout-met-worker-parte-2/**`<br>`.github/workflows/instrumentacao-opentelemetry-correlation-ids-metricas-artlayout-met-wo.yaml` |
| `STORY-0750` | `ISSUE-0860` | `EPIC-050` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-de-matchers-classicos-ia-escalonamento-explic/ai-aie-parte-1/**` |
| `STORY-0751` | `ISSUE-0861` | `EPIC-050` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-de-matchers-classicos-ia-escalonamento-explic/aie-epic-sch-parte-2/**` |

## Onda 050

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0233` | `ISSUE-0343` | `EPIC-039` | `SPRINT-011` | DevOps | `tests/ops/instrumentacao-opentelemetry-correlation-ids-metricas/consolidacao/**`<br>`tools/quality/instrumentacao-opentelemetry-correlation-ids-metricas/consolidacao/**`<br>`.github/workflows/instrumentacao-opentelemetry-correlation-ids-metricas-consolidacao.yaml` |
| `STORY-0303` | `ISSUE-0413` | `EPIC-050` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/registry-de-matchers-classicos-ia-escalonamento-explic/consolidacao/**` |
| `STORY-0328` | `ISSUE-0438` | `EPIC-053` | `SPRINT-006` | QA | `tests/geo/grafo-de-referencias-verificadas-componentes-desconect/**`<br>`tools/quality/grafo-de-referencias-verificadas-componentes-desconect/**`<br>`.github/workflows/grafo-de-referencias-verificadas-componentes-desconect.yaml` |
| `STORY-0366` | `ISSUE-0476` | `EPIC-059` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-espaciotemporal-guiada-ranking-explicavel-incert/**` |
| `STORY-0367` | `ISSUE-0477` | `EPIC-059` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-espaciotemporal-guiada-ranking-explicavel-incert/**` |
| `STORY-0368` | `ISSUE-0478` | `EPIC-059` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-espaciotemporal-guiada-ranking-explicavel-incert/**` |
| `STORY-0369` | `ISSUE-0479` | `EPIC-059` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/busca-espaciotemporal-guiada-ranking-explicavel-incert/**` |
| `STORY-0396` | `ISSUE-0506` | `EPIC-063` | `SPRINT-006` | QA | `tests/geo/modelo-tipado-versionado-de-gcps-lifecycle-provenienci/**`<br>`tools/quality/modelo-tipado-versionado-de-gcps-lifecycle-provenienci/**`<br>`.github/workflows/modelo-tipado-versionado-de-gcps-lifecycle-provenienci.yaml` |
| `STORY-0437` | `ISSUE-0547` | `EPIC-069` | `SPRINT-004` | QA | `tests/job/observabilidade-slos-e-diagnostico-do-scheduler/**`<br>`tools/quality/observabilidade-slos-e-diagnostico-do-scheduler/**`<br>`.github/workflows/observabilidade-slos-e-diagnostico-do-scheduler.yaml` |
| `STORY-0517` | `ISSUE-0627` | `EPIC-083` | `SPRINT-011` | DevOps | `tests/ops/modos-offline-restricted-connected-egress-enforcement/**`<br>`tools/quality/modos-offline-restricted-connected-egress-enforcement/**`<br>`.github/workflows/modos-offline-restricted-connected-egress-enforcement.yaml` |
| `STORY-0518` | `ISSUE-0628` | `EPIC-083` | `SPRINT-011` | DevOps | `tests/ops/modos-offline-restricted-connected-egress-enforcement/**`<br>`tools/quality/modos-offline-restricted-connected-egress-enforcement/**`<br>`.github/workflows/modos-offline-restricted-connected-egress-enforcement.yaml` |
| `STORY-0519` | `ISSUE-0629` | `EPIC-083` | `SPRINT-011` | QA | `tests/ops/modos-offline-restricted-connected-egress-enforcement/**`<br>`tools/quality/modos-offline-restricted-connected-egress-enforcement/**`<br>`.github/workflows/modos-offline-restricted-connected-egress-enforcement.yaml` |

## Onda 051

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0236` | `ISSUE-0346` | `EPIC-039` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/instrumentacao-opentelemetry-correlation-ids-metricas/**`<br>`tests/security/instrumentacao-opentelemetry-correlation-ids-metricas/**` |
| `STORY-0307` | `ISSUE-0417` | `EPIC-050` | `SPRINT-006` | QA | `tests/geo/registry-de-matchers-classicos-ia-escalonamento-explic/**`<br>`tools/quality/registry-de-matchers-classicos-ia-escalonamento-explic/**`<br>`.github/workflows/registry-de-matchers-classicos-ia-escalonamento-explic.yaml` |
| `STORY-0329` | `ISSUE-0439` | `EPIC-053` | `SPRINT-006` | Reviewer | `evidence/reviews/grafo-de-referencias-verificadas-componentes-desconect/**` |
| `STORY-0370` | `ISSUE-0480` | `EPIC-059` | `SPRINT-006` | QA | `tests/geo/busca-espaciotemporal-guiada-ranking-explicavel-incert/**`<br>`tools/quality/busca-espaciotemporal-guiada-ranking-explicavel-incert/**`<br>`.github/workflows/busca-espaciotemporal-guiada-ranking-explicavel-incert.yaml` |
| `STORY-0397` | `ISSUE-0507` | `EPIC-063` | `SPRINT-006` | Reviewer | `evidence/reviews/modelo-tipado-versionado-de-gcps-lifecycle-provenienci/**` |
| `STORY-0438` | `ISSUE-0548` | `EPIC-069` | `SPRINT-004` | Reviewer | `evidence/reviews/observabilidade-slos-e-diagnostico-do-scheduler/**` |
| `STORY-0520` | `ISSUE-0630` | `EPIC-083` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/modos-offline-restricted-connected-egress-enforcement/**`<br>`tests/security/modos-offline-restricted-connected-egress-enforcement/**` |

## Onda 052

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0220` | `ISSUE-0330` | `EPIC-037` | `SPRINT-010` | Arquiteto | `contracts/rep/persistencia-e-exportacao-escalavel-de-resultados-por/**`<br>`docs/02-architecture/design-reviews/persistencia-e-exportacao-escalavel-de-resultados-por/**` |
| `STORY-0237` | `ISSUE-0347` | `EPIC-039` | `SPRINT-011` | Reviewer | `evidence/reviews/instrumentacao-opentelemetry-correlation-ids-metricas/**` |
| `STORY-0308` | `ISSUE-0418` | `EPIC-050` | `SPRINT-006` | Reviewer | `evidence/reviews/registry-de-matchers-classicos-ia-escalonamento-explic/**` |
| `STORY-0330` | `ISSUE-0440` | `EPIC-054` | `SPRINT-006` | Arquiteto | `contracts/geo/componentes-provisorios-multimodais-scores-versionados/**`<br>`docs/02-architecture/design-reviews/componentes-provisorios-multimodais-scores-versionados/**` |
| `STORY-0344` | `ISSUE-0454` | `EPIC-056` | `SPRINT-006` | Arquiteto | `contracts/geo/maquina-de-estados-de-arestas-evidencia-direta-lineage/**`<br>`docs/02-architecture/design-reviews/maquina-de-estados-de-arestas-evidencia-direta-lineage/**` |
| `STORY-0371` | `ISSUE-0481` | `EPIC-059` | `SPRINT-006` | Reviewer | `evidence/reviews/busca-espaciotemporal-guiada-ranking-explicavel-incert/**` |
| `STORY-0521` | `ISSUE-0631` | `EPIC-083` | `SPRINT-011` | Reviewer | `evidence/reviews/modos-offline-restricted-connected-egress-enforcement/**` |
| `STORY-0570` | `ISSUE-0680` | `EPIC-093` | `SPRINT-007` | Arquiteto | `contracts/geo/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos/**`<br>`docs/02-architecture/design-reviews/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos/**` |

## Onda 053

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0197` | `ISSUE-0307` | `EPIC-033` | `SPRINT-009` | Product Owner | `docs/01-product/capabilities/assistente-guiado-recomendacao-explicavel-consentiment/**` |
| `STORY-0222` | `ISSUE-0332` | `EPIC-037` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/persistencia-e-exportacao-escalavel-de-resultados-por/**`<br>`src/backend/dsgeorref/adapters/persistencia-e-exportacao-escalavel-de-resultados-por/**` |
| `STORY-0223` | `ISSUE-0333` | `EPIC-037` | `SPRINT-010` | Frontend | `src/frontend/src/features/persistencia-e-exportacao-escalavel-de-resultados-por/**` |
| `STORY-0238` | `ISSUE-0348` | `EPIC-040` | `SPRINT-011` | DevOps | `tests/ops/benchmark-limites-e-orcamento-de-recursos/**`<br>`tools/quality/benchmark-limites-e-orcamento-de-recursos/**`<br>`.github/workflows/benchmark-limites-e-orcamento-de-recursos.yaml` |
| `STORY-0331` | `ISSUE-0441` | `EPIC-054` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/componentes-provisorios-multimodais-scores-versionados/**` |
| `STORY-0332` | `ISSUE-0442` | `EPIC-054` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/componentes-provisorios-multimodais-scores-versionados/**` |
| `STORY-0333` | `ISSUE-0443` | `EPIC-054` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/componentes-provisorios-multimodais-scores-versionados/**` |
| `STORY-0334` | `ISSUE-0444` | `EPIC-054` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/componentes-provisorios-multimodais-scores-versionados/**` |
| `STORY-0345` | `ISSUE-0455` | `EPIC-056` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/maquina-de-estados-de-arestas-evidencia-direta-lineage/**` |
| `STORY-0346` | `ISSUE-0456` | `EPIC-056` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/maquina-de-estados-de-arestas-evidencia-direta-lineage/**` |
| `STORY-0347` | `ISSUE-0457` | `EPIC-056` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/maquina-de-estados-de-arestas-evidencia-direta-lineage/**` |
| `STORY-0348` | `ISSUE-0458` | `EPIC-056` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/maquina-de-estados-de-arestas-evidencia-direta-lineage/**` |
| `STORY-0372` | `ISSUE-0482` | `EPIC-060` | `SPRINT-006` | Arquiteto | `contracts/geo/policy-de-aquisicao-no-processingplan-preview-consenti/**`<br>`docs/02-architecture/design-reviews/policy-de-aquisicao-no-processingplan-preview-consenti/**` |
| `STORY-0545` | `ISSUE-0655` | `EPIC-088` | `SPRINT-011` | IA | `src/ai/dsgeorref_ai/namespace-experimental-labs-registry-separado-modelpac/**` |
| `STORY-0571` | `ISSUE-0681` | `EPIC-093` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos/**` |
| `STORY-0572` | `ISSUE-0682` | `EPIC-093` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos/**` |
| `STORY-0573` | `ISSUE-0683` | `EPIC-093` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos/**` |
| `STORY-0574` | `ISSUE-0684` | `EPIC-093` | `SPRINT-007` | Geoprocessamento | `src/geo/dsgeorref_geo/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos/**` |
| `STORY-0743` | `ISSUE-0853` | `EPIC-037` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/persistencia-e-exportacao-escalavel-de-resultados-por/bex-epic-msk-parte-1/**`<br>`src/backend/dsgeorref/adapters/persistencia-e-exportacao-escalavel-de-resultados-por/bex-epic-msk-parte-1/**` |
| `STORY-0744` | `ISSUE-0854` | `EPIC-037` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/persistencia-e-exportacao-escalavel-de-resultados-por/scl-scm-sdr-parte-2/**`<br>`src/backend/dsgeorref/adapters/persistencia-e-exportacao-escalavel-de-resultados-por/scl-scm-sdr-parte-2/**` |

## Onda 054

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0198` | `ISSUE-0308` | `EPIC-033` | `SPRINT-009` | Frontend | `src/frontend/src/features/assistente-guiado-recomendacao-explicavel-consentiment/**` |
| `STORY-0199` | `ISSUE-0309` | `EPIC-033` | `SPRINT-009` | Frontend | `src/frontend/src/features/assistente-guiado-recomendacao-explicavel-consentiment/**` |
| `STORY-0200` | `ISSUE-0310` | `EPIC-033` | `SPRINT-009` | Frontend | `src/frontend/src/features/assistente-guiado-recomendacao-explicavel-consentiment/**` |
| `STORY-0221` | `ISSUE-0331` | `EPIC-037` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/persistencia-e-exportacao-escalavel-de-resultados-por/consolidacao/**`<br>`src/backend/dsgeorref/adapters/persistencia-e-exportacao-escalavel-de-resultados-por/consolidacao/**` |
| `STORY-0239` | `ISSUE-0349` | `EPIC-040` | `SPRINT-011` | DevOps | `tests/ops/benchmark-limites-e-orcamento-de-recursos/**`<br>`tools/quality/benchmark-limites-e-orcamento-de-recursos/**`<br>`.github/workflows/benchmark-limites-e-orcamento-de-recursos.yaml` |
| `STORY-0240` | `ISSUE-0350` | `EPIC-040` | `SPRINT-011` | DevOps | `tests/ops/benchmark-limites-e-orcamento-de-recursos/**`<br>`tools/quality/benchmark-limites-e-orcamento-de-recursos/**`<br>`.github/workflows/benchmark-limites-e-orcamento-de-recursos.yaml` |
| `STORY-0241` | `ISSUE-0351` | `EPIC-040` | `SPRINT-011` | QA | `tests/ops/benchmark-limites-e-orcamento-de-recursos/**`<br>`tools/quality/benchmark-limites-e-orcamento-de-recursos/**`<br>`.github/workflows/benchmark-limites-e-orcamento-de-recursos.yaml` |
| `STORY-0335` | `ISSUE-0445` | `EPIC-054` | `SPRINT-006` | QA | `tests/geo/componentes-provisorios-multimodais-scores-versionados/**`<br>`tools/quality/componentes-provisorios-multimodais-scores-versionados/**`<br>`.github/workflows/componentes-provisorios-multimodais-scores-versionados.yaml` |
| `STORY-0349` | `ISSUE-0459` | `EPIC-056` | `SPRINT-006` | QA | `tests/geo/maquina-de-estados-de-arestas-evidencia-direta-lineage/**`<br>`tools/quality/maquina-de-estados-de-arestas-evidencia-direta-lineage/**`<br>`.github/workflows/maquina-de-estados-de-arestas-evidencia-direta-lineage.yaml` |
| `STORY-0373` | `ISSUE-0483` | `EPIC-060` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/policy-de-aquisicao-no-processingplan-preview-consenti/**` |
| `STORY-0374` | `ISSUE-0484` | `EPIC-060` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/policy-de-aquisicao-no-processingplan-preview-consenti/**` |
| `STORY-0375` | `ISSUE-0485` | `EPIC-060` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/policy-de-aquisicao-no-processingplan-preview-consenti/**` |
| `STORY-0376` | `ISSUE-0486` | `EPIC-060` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/policy-de-aquisicao-no-processingplan-preview-consenti/**` |
| `STORY-0546` | `ISSUE-0656` | `EPIC-088` | `SPRINT-011` | IA | `src/ai/dsgeorref_ai/namespace-experimental-labs-registry-separado-modelpac/**` |
| `STORY-0575` | `ISSUE-0685` | `EPIC-093` | `SPRINT-007` | QA | `tests/geo/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos/**`<br>`tools/quality/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos/**`<br>`.github/workflows/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos.yaml` |

## Onda 055

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0201` | `ISSUE-0311` | `EPIC-033` | `SPRINT-009` | QA | `tests/web/assistente-guiado-recomendacao-explicavel-consentiment/**`<br>`tools/quality/assistente-guiado-recomendacao-explicavel-consentiment/**`<br>`.github/workflows/assistente-guiado-recomendacao-explicavel-consentiment.yaml` |
| `STORY-0224` | `ISSUE-0334` | `EPIC-037` | `SPRINT-010` | QA | `tests/rep/persistencia-e-exportacao-escalavel-de-resultados-por/**`<br>`tools/quality/persistencia-e-exportacao-escalavel-de-resultados-por/**`<br>`.github/workflows/persistencia-e-exportacao-escalavel-de-resultados-por.yaml` |
| `STORY-0242` | `ISSUE-0352` | `EPIC-040` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/benchmark-limites-e-orcamento-de-recursos/**`<br>`tests/security/benchmark-limites-e-orcamento-de-recursos/**` |
| `STORY-0336` | `ISSUE-0446` | `EPIC-054` | `SPRINT-006` | Reviewer | `evidence/reviews/componentes-provisorios-multimodais-scores-versionados/**` |
| `STORY-0350` | `ISSUE-0460` | `EPIC-056` | `SPRINT-006` | Reviewer | `evidence/reviews/maquina-de-estados-de-arestas-evidencia-direta-lineage/**` |
| `STORY-0377` | `ISSUE-0487` | `EPIC-060` | `SPRINT-006` | QA | `tests/geo/policy-de-aquisicao-no-processingplan-preview-consenti/**`<br>`tools/quality/policy-de-aquisicao-no-processingplan-preview-consenti/**`<br>`.github/workflows/policy-de-aquisicao-no-processingplan-preview-consenti.yaml` |
| `STORY-0547` | `ISSUE-0657` | `EPIC-088` | `SPRINT-011` | QA | `tests/lab/namespace-experimental-labs-registry-separado-modelpac/**`<br>`tools/quality/namespace-experimental-labs-registry-separado-modelpac/**`<br>`.github/workflows/namespace-experimental-labs-registry-separado-modelpac.yaml` |
| `STORY-0576` | `ISSUE-0686` | `EPIC-093` | `SPRINT-007` | Reviewer | `evidence/reviews/contratos-de-crs-espacos-de-coordenadas-ordem-de-eixos/**` |

## Onda 056

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0202` | `ISSUE-0312` | `EPIC-033` | `SPRINT-009` | Reviewer | `evidence/reviews/assistente-guiado-recomendacao-explicavel-consentiment/**` |
| `STORY-0225` | `ISSUE-0335` | `EPIC-037` | `SPRINT-010` | Reviewer | `evidence/reviews/persistencia-e-exportacao-escalavel-de-resultados-por/**` |
| `STORY-0243` | `ISSUE-0353` | `EPIC-040` | `SPRINT-011` | Reviewer | `evidence/reviews/benchmark-limites-e-orcamento-de-recursos/**` |
| `STORY-0337` | `ISSUE-0447` | `EPIC-055` | `SPRINT-006` | Arquiteto | `contracts/geo/recuperacao-progressiva-de-vizinhos-com-candidate-budg/**`<br>`docs/02-architecture/design-reviews/recuperacao-progressiva-de-vizinhos-com-candidate-budg/**` |
| `STORY-0351` | `ISSUE-0461` | `EPIC-057` | `SPRINT-006` | Arquiteto | `contracts/geo/resultados-por-componente-sucesso-parcial-explicito-re/**`<br>`docs/02-architecture/design-reviews/resultados-por-componente-sucesso-parcial-explicito-re/**` |
| `STORY-0378` | `ISSUE-0488` | `EPIC-060` | `SPRINT-006` | Reviewer | `evidence/reviews/policy-de-aquisicao-no-processingplan-preview-consenti/**` |
| `STORY-0548` | `ISSUE-0658` | `EPIC-088` | `SPRINT-011` | Reviewer | `evidence/reviews/namespace-experimental-labs-registry-separado-modelpac/**` |

## Onda 057

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0215` | `ISSUE-0325` | `EPIC-036` | `SPRINT-009` | Product Owner | `docs/01-product/capabilities/central-aprender-exemplos-visuais-projeto-demonstrativ/**` |
| `STORY-0226` | `ISSUE-0336` | `EPIC-038` | `SPRINT-010` | Arquiteto | `contracts/rep/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**`<br>`docs/02-architecture/design-reviews/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**` |
| `STORY-0338` | `ISSUE-0448` | `EPIC-055` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/recuperacao-progressiva-de-vizinhos-com-candidate-budg/**` |
| `STORY-0339` | `ISSUE-0449` | `EPIC-055` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/recuperacao-progressiva-de-vizinhos-com-candidate-budg/**` |
| `STORY-0340` | `ISSUE-0450` | `EPIC-055` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/recuperacao-progressiva-de-vizinhos-com-candidate-budg/**` |
| `STORY-0341` | `ISSUE-0451` | `EPIC-055` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/recuperacao-progressiva-de-vizinhos-com-candidate-budg/**` |
| `STORY-0352` | `ISSUE-0462` | `EPIC-057` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/resultados-por-componente-sucesso-parcial-explicito-re/**` |
| `STORY-0353` | `ISSUE-0463` | `EPIC-057` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/resultados-por-componente-sucesso-parcial-explicito-re/**` |
| `STORY-0354` | `ISSUE-0464` | `EPIC-057` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/resultados-por-componente-sucesso-parcial-explicito-re/**` |
| `STORY-0355` | `ISSUE-0465` | `EPIC-057` | `SPRINT-006` | Geoprocessamento | `src/geo/dsgeorref_geo/resultados-por-componente-sucesso-parcial-explicito-re/**` |
| `STORY-0522` | `ISSUE-0632` | `EPIC-084` | `SPRINT-009` | Product Owner | `docs/01-product/capabilities/ux-guiada-de-ia-explicacao-do-plano-capacidades-instal/**` |

## Onda 058

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0216` | `ISSUE-0326` | `EPIC-036` | `SPRINT-009` | Frontend | `src/frontend/src/features/central-aprender-exemplos-visuais-projeto-demonstrativ/**` |
| `STORY-0217` | `ISSUE-0327` | `EPIC-036` | `SPRINT-009` | Frontend | `src/frontend/src/features/central-aprender-exemplos-visuais-projeto-demonstrativ/**` |
| `STORY-0227` | `ISSUE-0337` | `EPIC-038` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**`<br>`src/backend/dsgeorref/adapters/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**` |
| `STORY-0228` | `ISSUE-0338` | `EPIC-038` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**`<br>`src/backend/dsgeorref/adapters/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**` |
| `STORY-0229` | `ISSUE-0339` | `EPIC-038` | `SPRINT-010` | Frontend | `src/frontend/src/features/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**` |
| `STORY-0342` | `ISSUE-0452` | `EPIC-055` | `SPRINT-006` | QA | `tests/geo/recuperacao-progressiva-de-vizinhos-com-candidate-budg/**`<br>`tools/quality/recuperacao-progressiva-de-vizinhos-com-candidate-budg/**`<br>`.github/workflows/recuperacao-progressiva-de-vizinhos-com-candidate-budg.yaml` |
| `STORY-0356` | `ISSUE-0466` | `EPIC-057` | `SPRINT-006` | QA | `tests/geo/resultados-por-componente-sucesso-parcial-explicito-re/**`<br>`tools/quality/resultados-por-componente-sucesso-parcial-explicito-re/**`<br>`.github/workflows/resultados-por-componente-sucesso-parcial-explicito-re.yaml` |
| `STORY-0523` | `ISSUE-0633` | `EPIC-084` | `SPRINT-009` | Frontend | `src/frontend/src/features/ux-guiada-de-ia-explicacao-do-plano-capacidades-instal/**` |
| `STORY-0524` | `ISSUE-0634` | `EPIC-084` | `SPRINT-009` | Frontend | `src/frontend/src/features/ux-guiada-de-ia-explicacao-do-plano-capacidades-instal/**` |
| `STORY-0525` | `ISSUE-0635` | `EPIC-084` | `SPRINT-009` | Frontend | `src/frontend/src/features/ux-guiada-de-ia-explicacao-do-plano-capacidades-instal/**` |

## Onda 059

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0218` | `ISSUE-0328` | `EPIC-036` | `SPRINT-009` | QA | `tests/edu/central-aprender-exemplos-visuais-projeto-demonstrativ/**`<br>`tools/quality/central-aprender-exemplos-visuais-projeto-demonstrativ/**`<br>`.github/workflows/central-aprender-exemplos-visuais-projeto-demonstrativ.yaml` |
| `STORY-0230` | `ISSUE-0340` | `EPIC-038` | `SPRINT-010` | QA | `tests/rep/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**`<br>`tools/quality/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**`<br>`.github/workflows/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag.yaml` |
| `STORY-0343` | `ISSUE-0453` | `EPIC-055` | `SPRINT-006` | Reviewer | `evidence/reviews/recuperacao-progressiva-de-vizinhos-com-candidate-budg/**` |
| `STORY-0357` | `ISSUE-0467` | `EPIC-057` | `SPRINT-006` | Reviewer | `evidence/reviews/resultados-por-componente-sucesso-parcial-explicito-re/**` |
| `STORY-0526` | `ISSUE-0636` | `EPIC-084` | `SPRINT-009` | QA | `tests/web/ux-guiada-de-ia-explicacao-do-plano-capacidades-instal/**`<br>`tools/quality/ux-guiada-de-ia-explicacao-do-plano-capacidades-instal/**`<br>`.github/workflows/ux-guiada-de-ia-explicacao-do-plano-capacidades-instal.yaml` |

## Onda 060

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0203` | `ISSUE-0313` | `EPIC-034` | `SPRINT-009` | Product Owner | `docs/01-product/capabilities/painel-de-qualidade-do-lote-busca-server-side-filtros/**` |
| `STORY-0219` | `ISSUE-0329` | `EPIC-036` | `SPRINT-009` | Reviewer | `evidence/reviews/central-aprender-exemplos-visuais-projeto-demonstrativ/**` |
| `STORY-0231` | `ISSUE-0341` | `EPIC-038` | `SPRINT-010` | Reviewer | `evidence/reviews/metricas-heatmap-amostrado-e-diagnostico-denso-do-imag/**` |
| `STORY-0527` | `ISSUE-0637` | `EPIC-084` | `SPRINT-009` | Reviewer | `evidence/reviews/ux-guiada-de-ia-explicacao-do-plano-capacidades-instal/**` |

## Onda 061

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0205` | `ISSUE-0315` | `EPIC-034` | `SPRINT-009` | Frontend | `src/frontend/src/features/painel-de-qualidade-do-lote-busca-server-side-filtros/**` |
| `STORY-0206` | `ISSUE-0316` | `EPIC-034` | `SPRINT-009` | Frontend | `src/frontend/src/features/painel-de-qualidade-do-lote-busca-server-side-filtros/**` |
| `STORY-0741` | `ISSUE-0851` | `EPIC-034` | `SPRINT-009` | Frontend | `src/frontend/src/features/painel-de-qualidade-do-lote-busca-server-side-filtros/bat-bex-parte-1/**` |
| `STORY-0742` | `ISSUE-0852` | `EPIC-034` | `SPRINT-009` | Frontend | `src/frontend/src/features/painel-de-qualidade-do-lote-busca-server-side-filtros/requirements-epic-qual-scl-parte-2/**` |

## Onda 062

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0204` | `ISSUE-0314` | `EPIC-034` | `SPRINT-009` | Frontend | `src/frontend/src/features/painel-de-qualidade-do-lote-busca-server-side-filtros/consolidacao/**` |

## Onda 063

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0207` | `ISSUE-0317` | `EPIC-034` | `SPRINT-009` | QA | `tests/web/painel-de-qualidade-do-lote-busca-server-side-filtros/**`<br>`tools/quality/painel-de-qualidade-do-lote-busca-server-side-filtros/**`<br>`.github/workflows/painel-de-qualidade-do-lote-busca-server-side-filtros.yaml` |

## Onda 064

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0208` | `ISSUE-0318` | `EPIC-034` | `SPRINT-009` | Reviewer | `evidence/reviews/painel-de-qualidade-do-lote-busca-server-side-filtros/**` |

## Onda 065

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0209` | `ISSUE-0319` | `EPIC-035` | `SPRINT-009` | Product Owner | `docs/01-product/capabilities/workflow-de-revisao-com-gates-revisaveis-hard-gates-im/**` |
| `STORY-0539` | `ISSUE-0649` | `EPIC-087` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/baseline-operacional-vertical-privado-com-escopo-da-de/**` |

## Onda 066

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0210` | `ISSUE-0320` | `EPIC-035` | `SPRINT-009` | Arquiteto | `contracts/rev/workflow-de-revisao-com-gates-revisaveis-hard-gates-im/**`<br>`docs/02-architecture/design-reviews/workflow-de-revisao-com-gates-revisaveis-hard-gates-im/**` |
| `STORY-0211` | `ISSUE-0321` | `EPIC-035` | `SPRINT-009` | Frontend | `src/frontend/src/features/workflow-de-revisao-com-gates-revisaveis-hard-gates-im/**` |
| `STORY-0212` | `ISSUE-0322` | `EPIC-035` | `SPRINT-009` | Backend | `src/backend/dsgeorref/application/workflow-de-revisao-com-gates-revisaveis-hard-gates-im/**`<br>`src/backend/dsgeorref/adapters/workflow-de-revisao-com-gates-revisaveis-hard-gates-im/**` |
| `STORY-0540` | `ISSUE-0650` | `EPIC-087` | `SPRINT-012` | DevOps | `tests/rel/baseline-operacional-vertical-privado-com-escopo-da-de/**`<br>`tools/quality/baseline-operacional-vertical-privado-com-escopo-da-de/**`<br>`.github/workflows/baseline-operacional-vertical-privado-com-escopo-da-de.yaml` |
| `STORY-0541` | `ISSUE-0651` | `EPIC-087` | `SPRINT-012` | DevOps | `tests/rel/baseline-operacional-vertical-privado-com-escopo-da-de/**`<br>`tools/quality/baseline-operacional-vertical-privado-com-escopo-da-de/**`<br>`.github/workflows/baseline-operacional-vertical-privado-com-escopo-da-de.yaml` |
| `STORY-0542` | `ISSUE-0652` | `EPIC-087` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/baseline-operacional-vertical-privado-com-escopo-da-de/**`<br>`tests/security/baseline-operacional-vertical-privado-com-escopo-da-de/**` |

## Onda 067

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0213` | `ISSUE-0323` | `EPIC-035` | `SPRINT-009` | QA | `tests/rev/workflow-de-revisao-com-gates-revisaveis-hard-gates-im/**`<br>`tools/quality/workflow-de-revisao-com-gates-revisaveis-hard-gates-im/**`<br>`.github/workflows/workflow-de-revisao-com-gates-revisaveis-hard-gates-im.yaml` |
| `STORY-0543` | `ISSUE-0653` | `EPIC-087` | `SPRINT-012` | QA | `tests/rel/baseline-operacional-vertical-privado-com-escopo-da-de/**`<br>`tools/quality/baseline-operacional-vertical-privado-com-escopo-da-de/**`<br>`.github/workflows/baseline-operacional-vertical-privado-com-escopo-da-de.yaml` |

## Onda 068

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0214` | `ISSUE-0324` | `EPIC-035` | `SPRINT-009` | Reviewer | `evidence/reviews/workflow-de-revisao-com-gates-revisaveis-hard-gates-im/**` |
| `STORY-0544` | `ISSUE-0654` | `EPIC-087` | `SPRINT-012` | Reviewer | `evidence/reviews/baseline-operacional-vertical-privado-com-escopo-da-de/**` |

## Onda 069

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0385` | `ISSUE-0495` | `EPIC-062` | `SPRINT-009` | Product Owner | `docs/01-product/capabilities/workspace-visual-assistido-correctionsets-nova-tentati/**` |

## Onda 070

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0386` | `ISSUE-0496` | `EPIC-062` | `SPRINT-009` | Arquiteto | `contracts/rev/workspace-visual-assistido-correctionsets-nova-tentati/**`<br>`docs/02-architecture/design-reviews/workspace-visual-assistido-correctionsets-nova-tentati/**` |
| `STORY-0387` | `ISSUE-0497` | `EPIC-062` | `SPRINT-009` | Frontend | `src/frontend/src/features/workspace-visual-assistido-correctionsets-nova-tentati/**` |
| `STORY-0388` | `ISSUE-0498` | `EPIC-062` | `SPRINT-009` | Backend | `src/backend/dsgeorref/application/workspace-visual-assistido-correctionsets-nova-tentati/**`<br>`src/backend/dsgeorref/adapters/workspace-visual-assistido-correctionsets-nova-tentati/**` |

## Onda 071

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0389` | `ISSUE-0499` | `EPIC-062` | `SPRINT-009` | QA | `tests/rev/workspace-visual-assistido-correctionsets-nova-tentati/**`<br>`tools/quality/workspace-visual-assistido-correctionsets-nova-tentati/**`<br>`.github/workflows/workspace-visual-assistido-correctionsets-nova-tentati.yaml` |

## Onda 072

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0390` | `ISSUE-0500` | `EPIC-062` | `SPRINT-009` | Reviewer | `evidence/reviews/workspace-visual-assistido-correctionsets-nova-tentati/**` |

## Onda 073

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0296` | `ISSUE-0406` | `EPIC-049` | `SPRINT-010` | Arquiteto | `contracts/dat/lineage-normalizado-manifestos-e-bundle-de-reproducao/**`<br>`docs/02-architecture/design-reviews/lineage-normalizado-manifestos-e-bundle-de-reproducao/**` |
| `STORY-0398` | `ISSUE-0508` | `EPIC-064` | `SPRINT-009` | Product Owner | `docs/01-product/capabilities/fila-de-revisao-explicavel-filtros-priorizacao-impacto/**` |

## Onda 074

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0297` | `ISSUE-0407` | `EPIC-049` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/lineage-normalizado-manifestos-e-bundle-de-reproducao/**`<br>`src/backend/dsgeorref/adapters/lineage-normalizado-manifestos-e-bundle-de-reproducao/**` |
| `STORY-0298` | `ISSUE-0408` | `EPIC-049` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/lineage-normalizado-manifestos-e-bundle-de-reproducao/**`<br>`src/backend/dsgeorref/adapters/lineage-normalizado-manifestos-e-bundle-de-reproducao/**` |
| `STORY-0299` | `ISSUE-0409` | `EPIC-049` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/lineage-normalizado-manifestos-e-bundle-de-reproducao/**`<br>`src/backend/dsgeorref/adapters/lineage-normalizado-manifestos-e-bundle-de-reproducao/**` |
| `STORY-0399` | `ISSUE-0509` | `EPIC-064` | `SPRINT-009` | Frontend | `src/frontend/src/features/fila-de-revisao-explicavel-filtros-priorizacao-impacto/**` |
| `STORY-0400` | `ISSUE-0510` | `EPIC-064` | `SPRINT-009` | Frontend | `src/frontend/src/features/fila-de-revisao-explicavel-filtros-priorizacao-impacto/**` |
| `STORY-0401` | `ISSUE-0511` | `EPIC-064` | `SPRINT-009` | Frontend | `src/frontend/src/features/fila-de-revisao-explicavel-filtros-priorizacao-impacto/**` |

## Onda 075

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0300` | `ISSUE-0410` | `EPIC-049` | `SPRINT-010` | Security | `src/backend/dsgeorref/security/lineage-normalizado-manifestos-e-bundle-de-reproducao/**`<br>`tests/security/lineage-normalizado-manifestos-e-bundle-de-reproducao/**` |
| `STORY-0402` | `ISSUE-0512` | `EPIC-064` | `SPRINT-009` | QA | `tests/web/fila-de-revisao-explicavel-filtros-priorizacao-impacto/**`<br>`tools/quality/fila-de-revisao-explicavel-filtros-priorizacao-impacto/**`<br>`.github/workflows/fila-de-revisao-explicavel-filtros-priorizacao-impacto.yaml` |

## Onda 076

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0301` | `ISSUE-0411` | `EPIC-049` | `SPRINT-010` | Reviewer | `evidence/reviews/lineage-normalizado-manifestos-e-bundle-de-reproducao/**` |
| `STORY-0403` | `ISSUE-0513` | `EPIC-064` | `SPRINT-009` | Reviewer | `evidence/reviews/fila-de-revisao-explicavel-filtros-priorizacao-impacto/**` |

## Onda 077

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0379` | `ISSUE-0489` | `EPIC-061` | `SPRINT-010` | Arquiteto | `contracts/dat/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**`<br>`docs/02-architecture/design-reviews/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**` |
| `STORY-0439` | `ISSUE-0549` | `EPIC-070` | `SPRINT-010` | Arquiteto | `contracts/rep/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**`<br>`docs/02-architecture/design-reviews/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**` |
| `STORY-0445` | `ISSUE-0555` | `EPIC-071` | `SPRINT-011` | Arquiteto | `contracts/dat/backupset-coordenado-manifests-checksums-watermark-e-p/**`<br>`docs/02-architecture/design-reviews/backupset-coordenado-manifests-checksums-watermark-e-p/**` |
| `STORY-0469` | `ISSUE-0579` | `EPIC-075` | `SPRINT-011` | DevOps | `tests/ops/canal-append-only-de-auditoria-particionamento-digests/**`<br>`tools/quality/canal-append-only-de-auditoria-particionamento-digests/**`<br>`.github/workflows/canal-append-only-de-auditoria-particionamento-digests.yaml` |

## Onda 078

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0380` | `ISSUE-0490` | `EPIC-061` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**`<br>`src/backend/dsgeorref/adapters/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**` |
| `STORY-0381` | `ISSUE-0491` | `EPIC-061` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**`<br>`src/backend/dsgeorref/adapters/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**` |
| `STORY-0382` | `ISSUE-0492` | `EPIC-061` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**`<br>`src/backend/dsgeorref/adapters/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**` |
| `STORY-0440` | `ISSUE-0550` | `EPIC-070` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**`<br>`src/backend/dsgeorref/adapters/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**` |
| `STORY-0441` | `ISSUE-0551` | `EPIC-070` | `SPRINT-010` | Backend | `src/backend/dsgeorref/application/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**`<br>`src/backend/dsgeorref/adapters/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**` |
| `STORY-0442` | `ISSUE-0552` | `EPIC-070` | `SPRINT-010` | Frontend | `src/frontend/src/features/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**` |
| `STORY-0446` | `ISSUE-0556` | `EPIC-071` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/backupset-coordenado-manifests-checksums-watermark-e-p/**`<br>`src/backend/dsgeorref/adapters/backupset-coordenado-manifests-checksums-watermark-e-p/**` |
| `STORY-0447` | `ISSUE-0557` | `EPIC-071` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/backupset-coordenado-manifests-checksums-watermark-e-p/**`<br>`src/backend/dsgeorref/adapters/backupset-coordenado-manifests-checksums-watermark-e-p/**` |
| `STORY-0448` | `ISSUE-0558` | `EPIC-071` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/backupset-coordenado-manifests-checksums-watermark-e-p/**`<br>`src/backend/dsgeorref/adapters/backupset-coordenado-manifests-checksums-watermark-e-p/**` |
| `STORY-0470` | `ISSUE-0580` | `EPIC-075` | `SPRINT-011` | DevOps | `tests/ops/canal-append-only-de-auditoria-particionamento-digests/**`<br>`tools/quality/canal-append-only-de-auditoria-particionamento-digests/**`<br>`.github/workflows/canal-append-only-de-auditoria-particionamento-digests.yaml` |
| `STORY-0471` | `ISSUE-0581` | `EPIC-075` | `SPRINT-011` | DevOps | `tests/ops/canal-append-only-de-auditoria-particionamento-digests/**`<br>`tools/quality/canal-append-only-de-auditoria-particionamento-digests/**`<br>`.github/workflows/canal-append-only-de-auditoria-particionamento-digests.yaml` |
| `STORY-0472` | `ISSUE-0582` | `EPIC-075` | `SPRINT-011` | QA | `tests/ops/canal-append-only-de-auditoria-particionamento-digests/**`<br>`tools/quality/canal-append-only-de-auditoria-particionamento-digests/**`<br>`.github/workflows/canal-append-only-de-auditoria-particionamento-digests.yaml` |

## Onda 079

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0383` | `ISSUE-0493` | `EPIC-061` | `SPRINT-010` | Security | `src/backend/dsgeorref/security/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**`<br>`tests/security/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**` |
| `STORY-0443` | `ISSUE-0553` | `EPIC-070` | `SPRINT-010` | QA | `tests/rep/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**`<br>`tools/quality/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**`<br>`.github/workflows/snapshots-imutaveis-regra-de-resultado-vigente-e-compa.yaml` |
| `STORY-0449` | `ISSUE-0559` | `EPIC-071` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/backupset-coordenado-manifests-checksums-watermark-e-p/**`<br>`tests/security/backupset-coordenado-manifests-checksums-watermark-e-p/**` |
| `STORY-0473` | `ISSUE-0583` | `EPIC-075` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/canal-append-only-de-auditoria-particionamento-digests/**`<br>`tests/security/canal-append-only-de-auditoria-particionamento-digests/**` |

## Onda 080

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0384` | `ISSUE-0494` | `EPIC-061` | `SPRINT-010` | Reviewer | `evidence/reviews/cache-enderecado-por-conteudo-deduplicacao-quotas-rete/**` |
| `STORY-0444` | `ISSUE-0554` | `EPIC-070` | `SPRINT-010` | Reviewer | `evidence/reviews/snapshots-imutaveis-regra-de-resultado-vigente-e-compa/**` |
| `STORY-0450` | `ISSUE-0560` | `EPIC-071` | `SPRINT-011` | Reviewer | `evidence/reviews/backupset-coordenado-manifests-checksums-watermark-e-p/**` |
| `STORY-0474` | `ISSUE-0584` | `EPIC-075` | `SPRINT-011` | Reviewer | `evidence/reviews/canal-append-only-de-auditoria-particionamento-digests/**` |

## Onda 081

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0451` | `ISSUE-0561` | `EPIC-072` | `SPRINT-011` | DevOps | `tests/ops/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**`<br>`tools/quality/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**`<br>`.github/workflows/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e.yaml` |
| `STORY-0457` | `ISSUE-0567` | `EPIC-073` | `SPRINT-011` | Arquiteto | `contracts/dat/retentionpolicy-por-classe-estado-dependencia-holds-e/**`<br>`docs/02-architecture/design-reviews/retentionpolicy-por-classe-estado-dependencia-holds-e/**` |
| `STORY-0475` | `ISSUE-0585` | `EPIC-076` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/catalogo-de-campos-redaction-centralizada-testes-de-va/**`<br>`tests/security/catalogo-de-campos-redaction-centralizada-testes-de-va/**` |

## Onda 082

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0452` | `ISSUE-0562` | `EPIC-072` | `SPRINT-011` | DevOps | `tests/ops/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**`<br>`tools/quality/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**`<br>`.github/workflows/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e.yaml` |
| `STORY-0453` | `ISSUE-0563` | `EPIC-072` | `SPRINT-011` | DevOps | `tests/ops/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**`<br>`tools/quality/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**`<br>`.github/workflows/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e.yaml` |
| `STORY-0454` | `ISSUE-0564` | `EPIC-072` | `SPRINT-011` | QA | `tests/ops/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**`<br>`tools/quality/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**`<br>`.github/workflows/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e.yaml` |
| `STORY-0458` | `ISSUE-0568` | `EPIC-073` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/retentionpolicy-por-classe-estado-dependencia-holds-e/**`<br>`src/backend/dsgeorref/adapters/retentionpolicy-por-classe-estado-dependencia-holds-e/**` |
| `STORY-0459` | `ISSUE-0569` | `EPIC-073` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/retentionpolicy-por-classe-estado-dependencia-holds-e/**`<br>`src/backend/dsgeorref/adapters/retentionpolicy-por-classe-estado-dependencia-holds-e/**` |
| `STORY-0460` | `ISSUE-0570` | `EPIC-073` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/retentionpolicy-por-classe-estado-dependencia-holds-e/**`<br>`src/backend/dsgeorref/adapters/retentionpolicy-por-classe-estado-dependencia-holds-e/**` |
| `STORY-0476` | `ISSUE-0586` | `EPIC-076` | `SPRINT-011` | Arquiteto | `contracts/sec/catalogo-de-campos-redaction-centralizada-testes-de-va/**`<br>`docs/02-architecture/design-reviews/catalogo-de-campos-redaction-centralizada-testes-de-va/**` |
| `STORY-0477` | `ISSUE-0587` | `EPIC-076` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/catalogo-de-campos-redaction-centralizada-testes-de-va/**`<br>`src/backend/dsgeorref/adapters/catalogo-de-campos-redaction-centralizada-testes-de-va/**` |
| `STORY-0478` | `ISSUE-0588` | `EPIC-076` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/catalogo-de-campos-redaction-centralizada-testes-de-va/**`<br>`tests/security/catalogo-de-campos-redaction-centralizada-testes-de-va/**` |

## Onda 083

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0455` | `ISSUE-0565` | `EPIC-072` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**`<br>`tests/security/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**` |
| `STORY-0461` | `ISSUE-0571` | `EPIC-073` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/retentionpolicy-por-classe-estado-dependencia-holds-e/**`<br>`tests/security/retentionpolicy-por-classe-estado-dependencia-holds-e/**` |
| `STORY-0479` | `ISSUE-0589` | `EPIC-076` | `SPRINT-011` | DevOps | `tests/sec/catalogo-de-campos-redaction-centralizada-testes-de-va/**`<br>`tools/quality/catalogo-de-campos-redaction-centralizada-testes-de-va/**`<br>`.github/workflows/catalogo-de-campos-redaction-centralizada-testes-de-va.yaml` |

## Onda 084

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0456` | `ISSUE-0566` | `EPIC-072` | `SPRINT-011` | Reviewer | `evidence/reviews/restore-drills-isolados-evidencias-rpo-rto-e-runbook-e/**` |
| `STORY-0462` | `ISSUE-0572` | `EPIC-073` | `SPRINT-011` | Reviewer | `evidence/reviews/retentionpolicy-por-classe-estado-dependencia-holds-e/**` |
| `STORY-0480` | `ISSUE-0590` | `EPIC-076` | `SPRINT-011` | Reviewer | `evidence/reviews/catalogo-de-campos-redaction-centralizada-testes-de-va/**` |

## Onda 085

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0463` | `ISSUE-0573` | `EPIC-074` | `SPRINT-011` | Arquiteto | `contracts/dat/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**`<br>`docs/02-architecture/design-reviews/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**` |
| `STORY-0481` | `ISSUE-0591` | `EPIC-077` | `SPRINT-011` | DevOps | `tests/ops/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**`<br>`tools/quality/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**`<br>`.github/workflows/budgets-de-cardinalidade-sampling-retencao-por-sinal-e.yaml` |
| `STORY-0505` | `ISSUE-0615` | `EPIC-081` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/orquestrador-de-upgrade-preflight-migrations-explicita/**` |
| `STORY-0549` | `ISSUE-0659` | `EPIC-089` | `SPRINT-012` | Tech Lead | `src/backend/dsgeorref/application/release-train-internal-alpha-beta-1-0-automacao-de-evi/**` |

## Onda 086

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0464` | `ISSUE-0574` | `EPIC-074` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**`<br>`src/backend/dsgeorref/adapters/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**` |
| `STORY-0465` | `ISSUE-0575` | `EPIC-074` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**`<br>`src/backend/dsgeorref/adapters/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**` |
| `STORY-0466` | `ISSUE-0576` | `EPIC-074` | `SPRINT-011` | Backend | `src/backend/dsgeorref/application/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**`<br>`src/backend/dsgeorref/adapters/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**` |
| `STORY-0482` | `ISSUE-0592` | `EPIC-077` | `SPRINT-011` | DevOps | `tests/ops/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**`<br>`tools/quality/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**`<br>`.github/workflows/budgets-de-cardinalidade-sampling-retencao-por-sinal-e.yaml` |
| `STORY-0483` | `ISSUE-0593` | `EPIC-077` | `SPRINT-011` | DevOps | `tests/ops/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**`<br>`tools/quality/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**`<br>`.github/workflows/budgets-de-cardinalidade-sampling-retencao-por-sinal-e.yaml` |
| `STORY-0484` | `ISSUE-0594` | `EPIC-077` | `SPRINT-011` | QA | `tests/ops/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**`<br>`tools/quality/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**`<br>`.github/workflows/budgets-de-cardinalidade-sampling-retencao-por-sinal-e.yaml` |
| `STORY-0506` | `ISSUE-0616` | `EPIC-081` | `SPRINT-012` | DevOps | `tests/rel/orquestrador-de-upgrade-preflight-migrations-explicita/**`<br>`tools/quality/orquestrador-de-upgrade-preflight-migrations-explicita/**`<br>`.github/workflows/orquestrador-de-upgrade-preflight-migrations-explicita.yaml` |
| `STORY-0507` | `ISSUE-0617` | `EPIC-081` | `SPRINT-012` | DevOps | `tests/rel/orquestrador-de-upgrade-preflight-migrations-explicita/**`<br>`tools/quality/orquestrador-de-upgrade-preflight-migrations-explicita/**`<br>`.github/workflows/orquestrador-de-upgrade-preflight-migrations-explicita.yaml` |
| `STORY-0508` | `ISSUE-0618` | `EPIC-081` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/orquestrador-de-upgrade-preflight-migrations-explicita/**`<br>`tests/security/orquestrador-de-upgrade-preflight-migrations-explicita/**` |
| `STORY-0550` | `ISSUE-0660` | `EPIC-089` | `SPRINT-012` | DevOps | `tests/rel/release-train-internal-alpha-beta-1-0-automacao-de-evi/**`<br>`tools/quality/release-train-internal-alpha-beta-1-0-automacao-de-evi/**`<br>`.github/workflows/release-train-internal-alpha-beta-1-0-automacao-de-evi.yaml` |
| `STORY-0551` | `ISSUE-0661` | `EPIC-089` | `SPRINT-012` | DevOps | `tests/rel/release-train-internal-alpha-beta-1-0-automacao-de-evi/**`<br>`tools/quality/release-train-internal-alpha-beta-1-0-automacao-de-evi/**`<br>`.github/workflows/release-train-internal-alpha-beta-1-0-automacao-de-evi.yaml` |
| `STORY-0552` | `ISSUE-0662` | `EPIC-089` | `SPRINT-012` | Security | `src/backend/dsgeorref/security/release-train-internal-alpha-beta-1-0-automacao-de-evi/**`<br>`tests/security/release-train-internal-alpha-beta-1-0-automacao-de-evi/**` |

## Onda 087

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0467` | `ISSUE-0577` | `EPIC-074` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**`<br>`tests/security/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**` |
| `STORY-0485` | `ISSUE-0595` | `EPIC-077` | `SPRINT-011` | Security | `src/backend/dsgeorref/security/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**`<br>`tests/security/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**` |
| `STORY-0509` | `ISSUE-0619` | `EPIC-081` | `SPRINT-012` | QA | `tests/rel/orquestrador-de-upgrade-preflight-migrations-explicita/**`<br>`tools/quality/orquestrador-de-upgrade-preflight-migrations-explicita/**`<br>`.github/workflows/orquestrador-de-upgrade-preflight-migrations-explicita.yaml` |
| `STORY-0553` | `ISSUE-0663` | `EPIC-089` | `SPRINT-012` | QA | `tests/rel/release-train-internal-alpha-beta-1-0-automacao-de-evi/**`<br>`tools/quality/release-train-internal-alpha-beta-1-0-automacao-de-evi/**`<br>`.github/workflows/release-train-internal-alpha-beta-1-0-automacao-de-evi.yaml` |

## Onda 088

| História | Issue | Épico | Sprint | Papel | Write scope |
|---|---|---|---|---|---|
| `STORY-0468` | `ISSUE-0578` | `EPIC-074` | `SPRINT-011` | Reviewer | `evidence/reviews/gc-reference-aware-tombstone-quarentena-periodo-de-gra/**` |
| `STORY-0486` | `ISSUE-0596` | `EPIC-077` | `SPRINT-011` | Reviewer | `evidence/reviews/budgets-de-cardinalidade-sampling-retencao-por-sinal-e/**` |
| `STORY-0510` | `ISSUE-0620` | `EPIC-081` | `SPRINT-012` | Reviewer | `evidence/reviews/orquestrador-de-upgrade-preflight-migrations-explicita/**` |
| `STORY-0554` | `ISSUE-0664` | `EPIC-089` | `SPRINT-012` | Reviewer | `evidence/reviews/release-train-internal-alpha-beta-1-0-automacao-de-evi/**` |
