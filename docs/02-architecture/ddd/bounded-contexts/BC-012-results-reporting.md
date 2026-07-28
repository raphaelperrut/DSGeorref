# BC-012 — Resultados, Diagnósticos e Exportação

- **Classificação DDD:** `Supporting`
- **Papel estratégico:** `Entrega de valor`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-030, EPIC-037, EPIC-057, EPIC-070`

## Missão

Consolidar snapshots de resultado, diagnósticos, comparações, relatórios de lote e exports sem recalcular a verdade científica.

## Linguagem ubíqua local

- `resultado vigente`
- `snapshot`
- `diagnóstico`
- `comparação`
- `export`

## Aggregates e raízes

- `ResultSnapshot`
- `BatchResult`
- `FailureDiagnostic`
- `ResultComparison`
- `ExportRequest`

## Comandos

- `RegistrarResultado`
- `SelecionarResultadoVigente`
- `CompararResultados`
- `SolicitarExport`
- `ConcluirExport`

## Eventos de domínio

- `ResultRecorded`
- `CurrentResultChanged`
- `ResultsCompared`
- `ExportRequested`
- `ExportCompleted`

## Relações

- **Upstream:** BC-006, BC-007, BC-008, BC-010, BC-011, BC-013.
- **Downstream:** BC-016, BC-014.
- As relações normativas e os padrões de integração estão em `../DDD-040-CONTEXT-MAP.md`.

## Autoridade

O contexto é o único owner do significado, invariantes e transições de seus aggregates. Outros contextos recebem IDs, snapshots, eventos ou DTOs publicados; nunca importam entidades internas.

## Proibições

- não compartilhar ORM models, state machines ou repositories entre contexts;
- não acessar tabelas de outro contexto;
- não publicar evento antes do commit autoritativo;
- não usar UI, API, broker, filesystem ou banco como substituto do modelo de domínio;
- não criar módulo `common`, `utils` ou `shared-domain` para escapar do boundary.

## Contratos

Contratos públicos são registrados em `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`. Mudança breaking exige ADR ou versão nova do contrato, migration e rollback quando aplicável.
