# BP-001 — Classical matching calibration

- **Status:** `Required before promotion`
- **Owner ADR:** ADR-044

## Perguntas de benchmark

Calibrar por estrato: preparação fotométrica; níveis/tiles/overlap; quotas de keypoints; epsilon e persistência RootSIFT float32; FLANN trees/checks; ratio/mutual/uniqueness; priors suaves; pruning; budgets de CPU/RAM/I/O.

## Evidência de saída

- recall FLANN versus BF oracle;
- falso aceite/falso rejeite;
- coverage e condicionamento;
- tempo, RAM e disco;
- estabilidade entre ambientes;
- ClassicalMatchingProfile imutável, digest, corpus e rollback.

Nenhum threshold será aprovado por preferência abstrata do Owner. O profile promovido é resultado do corpus, holdout e scientific gate.
