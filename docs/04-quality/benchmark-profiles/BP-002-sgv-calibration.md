# BP-002 — Calibração do SGV

- **Status:** `Obrigatório antes da promoção`
- **Owner ADR:** ADR-046

## Perguntas de calibração

Definir estratos e thresholds para residual distributions, coverage, conditioning, Jacobiano e plausibilidade; medir margens de accepted/needs_review/rejected; manter espaços/unidades explícitos.

## Gate de evidência

- desenvolvimento, calibração e holdout cego separados;
- falso aceite crítico como budget bloqueante;
- intervalos de confiança e análise de sensibilidade;
- replay e equivalência entre ambientes;
- SGVProfile/conjunto de evidências imutáveis, canary e rollback.

A composição e os valores quantitativos pertencem ao benchmark; hard gates e classes de métricas permanecem nas ADRs canônicas.
