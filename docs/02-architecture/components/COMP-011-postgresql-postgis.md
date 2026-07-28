# COMP-011 — PostgreSQL/PostGIS

- **Camada:** Persistência e transporte
- **ADRs owners:** ADR-018, ADR-026
- **Tecnologias principais:** PostgreSQL, PostGIS

## Responsabilidade

System of record para estado, geometrias, jobs, audit, lineage e outbox.

## Boundaries de contrato

- Consome `UoW/system of record` de `domain`.
- Consome `estado/checkpoints/outbox` de `workers`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-002`, `BC-003`, `BC-004`, `BC-005`, `BC-006`, `BC-007`, `BC-008`, `BC-009`, `BC-010`, `BC-011`, `BC-012`, `BC-013`, `BC-014`, `BC-015`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
