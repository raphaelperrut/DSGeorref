# SAR-010 — Contexto do sistema

## Sistema de interesse

DSGeorref é uma aplicação greenfield, single-instance e unificada para georreferenciamento controlado de imagens raster, com CLI, API REST, Web e workers sobre o mesmo núcleo de domínio.

## Atores

- Operador geoespacial: cria projetos, seleciona assets, executa e interpreta resultados.
- Revisor: trata casos revisáveis por CorrectionSets imutáveis.
- Administrador: opera identidade, roots, recursos, providers, backup e upgrade.
- Mantenedor científico: calibra profiles, corpora e promoção de modelos.
- Sistemas externos: OIDC opcional, providers STAC/APIs oficiais e registry de artifacts/modelpacks governados.

## Trust boundaries

- Browser ↔ ingress TLS ↔ API.
- API/workers ↔ PostgreSQL/PostGIS e filesystem gerenciado.
- Scheduler/outbox ↔ RabbitMQ ↔ workers.
- Gateway de providers ↔ egress allowlisted.
- Import de ModelPack ↔ verificação de assinatura/licença/digest.

## Invariantes

- PostgreSQL é autoritativo para estado; broker, logs, cache e frontend não são.
- ArtifactSet só se torna vigente após publicação atômica e validação.
- Homografia projetiva é o modelo final canônico; SGV é fail-closed.
- IA é opcional, classic-first e não contorna o SGV.
