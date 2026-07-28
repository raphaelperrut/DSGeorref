# SAR-130 — Rastreabilidade e consistência

A cadeia normativa é:

`requisito → ADR/profile/benchmark → módulo/contrato → épico → história/issue → TaskEnvelope → teste/evidência → sprint gate`.

Arquivos machine-readable:

- `docs/01-product/REQUIREMENT_INDEX.csv`
- `docs/06-delivery/TRACEABILITY_MATRIX.csv`
- `docs/06-delivery/STORY_INDEX.csv`
- `.codex/tasks/TASK-*.json`
- `contracts/http/OPERATION_CATALOG.json`
- `docs/07-assurance/SAR_CONSISTENCY_REPORT.json`

O validador bloqueia sequência quebrada, referência ausente, ciclo, seção obrigatória vazia, ID obsoleto, decisão aberta não classificada, contrato HTTP divergente e requisito sem história.

## Rastreabilidade DDD

A cadeia canônica agora inclui `Requisito → Bounded Context → Épico → História/Issue → TaskEnvelope → Package → Contrato → ADR`. As matrizes `REQUIREMENT_CONTEXT_MAP.csv`, `ADR_CONTEXT_MAP.csv`, `TECHNICAL_MODULE_CONTEXT_MAP.csv` e `CONTEXT_CONTRACT_OWNERSHIP.csv` devem permanecer consistentes.
