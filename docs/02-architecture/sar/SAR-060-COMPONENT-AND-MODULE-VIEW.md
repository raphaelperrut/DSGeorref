# SAR-060 — Visão de componentes e módulos

- 18 componentes arquiteturais: `docs/02-architecture/COMPONENT_INDEX.csv`.
- 18 módulos implementáveis: `docs/02-architecture/MODULE_INDEX.csv`.
- Cada módulo declara responsabilidade exclusiva, interfaces fornecidas/consumidas, autoridade, dependências proibidas, contratos e qualidades.
- Regras de dependência: `docs/02-architecture/DEPENDENCY_RULES.md`.
- Layout planejado: `docs/02-architecture/MONOREPO_LAYOUT.md`.

Nenhuma seção `Boundaries` permanece vazia.

## Distinção DDD

Módulos e componentes desta visão são unidades técnicas. Bounded contexts são unidades semânticas e estão no catálogo DDD. Um módulo técnico pode servir vários contexts, mas não pode fundi-los em um único modelo.
