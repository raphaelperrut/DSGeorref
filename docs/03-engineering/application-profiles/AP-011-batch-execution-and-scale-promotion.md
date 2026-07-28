# AP-011 — Batch execution and scale promotion profile

- **Status:** `Accepted`
- **Owner ADRs:** ADR-036 e ADR-039

## Aplicação

`BatchRun` agrega `ImageRun`, attempts e components com sucesso parcial explícito. Preflight, chunking, fairness, retry técnico, checkpoints, cancelamento, progresso e reporting aplicam as ADRs canônicas sem criar nova fonte de verdade.

A promoção de escala segue degraus `1 → 10 → 40 → até 300`, com fault injection, budgets de recursos, verificação de resume/idempotency, ausência de starvation, consistência do relatório e evidência de que falhas parciais não contaminam sucessos independentes.
