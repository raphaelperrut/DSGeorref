# AP-010 — Governed AI escalation profile

- **Status:** `Accepted`
- **Owner ADRs:** ADR-051, ADR-046 e ADR-053

## Aplicação

Após falha clássica elegível e tipada, a execução preserva a baseline checkpointada e aplica uma escada neural bounded: modo normal curto e sweep de recuperação ampliado somente quando policy e budget permitirem. ModelPacks são assinados, pinados, opt-in e capability-aware; ausência de GPU produz fallback funcional para a baseline, não erro arquitetural.

Artifacts/checkpoints só são reutilizados quando compatíveis. Todo resultado neural passa pelo SGV independente. UX expõe motivo, modelo, custo e limitações. Promoção usa shadow, canary, corpus estratificado e rollback.
