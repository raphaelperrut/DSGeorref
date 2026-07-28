# SAR-160 — Fase B Requirements Review

- **Baseline:** `2.6.0`
- **Estado:** `APPROVED`

A Fase B verifica a cadeia sprint → issue → critério de aceite → requisito → ADR. A matriz canônica é `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`. Critérios sem requisito direto são controles derivados de ADR e não podem introduzir comportamento de produto.

## Invariantes

- todo critério possui ID estável;
- todo critério possui ao menos uma ADR governante;
- requisito de produto sem história é proibido;
- requisito expresso apenas por nome de teste é proibido;
- dependências de épico e história devem ser acíclicas;
- nenhuma dependência pode retroceder entre sprints;
- requisito impossível ou conflito normativo bloqueia o estado `Ready`.
