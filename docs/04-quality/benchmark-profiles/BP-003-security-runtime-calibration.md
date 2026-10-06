# BP-003 — Security runtime calibration

- **Status:** `Required before production-like readiness`
- **Owner ADR:** ADR-028

Calibrar Argon2id, limites de concorrência, atraso progressivo, janelas, cooldowns, session idle/absolute timeout e thresholds de lockout sob hardware mínimo suportado e threat tests. A promoção deve demonstrar resistência a brute force e ausência de DoS operacional por consumo de memória/CPU.

## Baseline aprovado de execução — throttling

STORY-0767 / ISSUE-0874 / TASK-0770 estabelece os dois perfis abaixo, versão `1.0.0`, como baseline aprovado de execução para a calibração de throttling em TASK-0769, preservando o conteúdo e os SHA-256 do candidato `2e5b5ce79476f5961523ad622274ae63b079c007`:

- [BP-003-throttling-hardware-reference.yaml](BP-003-throttling-hardware-reference.yaml): hardware `reference_benchmark`, não `minimum_supported`; a aprovação do experimento não declara hardware mínimo suportado ou capacidade geral do produto.
- [BP-003-throttling-threat-workload.yaml](BP-003-throttling-threat-workload.yaml): números de carga e critérios do benchmark, não thresholds, janelas, cooldowns ou lockouts runtime.

A aplicabilidade permanece restrita ao recorte `post_auth_session` e às condições dos perfis. Este vínculo não executa o benchmark nem satisfaz o gate de produção em hardware mínimo suportado. A promoção dos valores finais de throttling continua pertencendo a TASK-0769 / [AP-003](../../03-engineering/application-profiles/AP-003-web-security-runtime-profile.md), após execução e revisão do benchmark.

Versões, digests e handoff são rastreados em `evidence/security/bp003-throttling-execution-baseline/`. Rejeição, alteração ou inaplicabilidade dos perfis invalida o handoff; uma substituição exige nova versão e revisão, sem fallback para hardware local ou defaults.
