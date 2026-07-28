# AP-004 — PostgreSQL/PostGIS physical conventions

- **Status:** `Accepted`
- **Owner ADR:** ADR-018

## Convenções iniciais

- poucos schemas por responsabilidade (`identity`, `core`, `jobs`, `artifacts`, `audit`) sem schema por projeto;
- migrations Alembic pequenas, monotônicas e executadas pelo UpgradeController;
- dados de referência com IDs estáveis e upsert idempotente;
- indexes, constraints e particionamento são propostos por migration/benchmark, não por novo DP.
