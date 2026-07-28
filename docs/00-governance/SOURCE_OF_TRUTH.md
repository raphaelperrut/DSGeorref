# Fonte de verdade

Precedência normativa:

1. PRD e escopo de produto
2. ADRs aceitas
3. contratos e schemas versionados
4. Application Profiles e Benchmark Profiles
5. sprint e épico
6. issue Ready e seu TaskEnvelope
7. implementação e testes
8. evidência de QA e decisão do Reviewer

Uma camada inferior não pode contradizer uma superior. Conflito material bloqueia a issue e retorna ao papel owner da camada superior.

A árvore ativa contém apenas fontes normativas e artefatos executáveis. O histórico de mudanças pertence ao Git.


## Software Architecture Repository

As views em `docs/02-architecture/sar/` são o índice arquitetural integrado. Elas não substituem ADRs ou contratos; conectam as fontes normativas e tornam inconsistências verificáveis.


## Architecture Review

O relatório da Fase A em `docs/07-assurance/PHASE-A-ARCHITECTURE-REVIEW-REPORT.md` aprova a arquitetura e registra ações de prontidão. Uma história não pode ser marcada `Ready` quando viola uma ação bloqueante do relatório.

## Domain-Driven Design

- contexts e classificação: `docs/02-architecture/ddd/BOUNDED_CONTEXT_INDEX.csv`;
- relações: `docs/02-architecture/ddd/CONTEXT_MAP.csv`;
- ownership de contratos: `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`;
- ownership de requisitos: `docs/07-assurance/REQUIREMENT_CONTEXT_MAP.csv`.
## CTO controls

Operational claims and investment gates are owned by `contracts/operations/cto-control-catalog.yaml`, the Phase G report and the production gate matrix. No issue may override them.
