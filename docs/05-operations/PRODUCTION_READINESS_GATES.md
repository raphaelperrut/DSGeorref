# Gates de prontidão para produção — Fase G

- **G-CTO-01 — Autorização e orçamento**: owner `Product Owner`; bloqueia `implementation`; evidência: ImplementationAuthorizationRecord + budget BRL + TCO 12 meses.
- **G-CTO-02 — Capacidade e escala**: owner `Tech Lead`; bloqueia `production`; evidência: BP-001/BP-004 em classes suportadas e lotes 40/100/300.
- **G-CTO-03 — Unit economics e GPU**: owner `Product Owner`; bloqueia `GPU/public production`; evidência: cost assessment validado; decisão CPU/GPU.
- **G-CTO-04 — Backup e restore**: owner `DevOps`; bloqueia `real data production`; evidência: restore drill com RPO/RTO atingidos.
- **G-CTO-05 — Migração e rollback**: owner `Tech Lead`; bloqueia `upgrade`; evidência: ensaio expand-migrate-contract e rollback/forward-fix.
- **G-CTO-06 — Segurança**: owner `Security`; bloqueia `network/public exposure`; evidência: threat review, supply-chain evidence e teste independente.
- **G-CTO-07 — LGPD e privacidade**: owner `Product Owner`; bloqueia `personal data/public operation`; evidência: ROPA, papéis, base/finalidade, retenção, direitos e incidente.
- **G-CTO-08 — Observabilidade e SLO**: owner `DevOps`; bloqueia `production`; evidência: dashboards, alertas e SLI medidos sem cardinalidade indevida.
- **G-CTO-09 — Release e rollback**: owner `Reviewer`; bloqueia `publication`; evidência: SBOM, assinatura, backup, smoke, rollback e release gate.
