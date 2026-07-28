# COMP-003 — HTTP API

- **Camada:** Interfaces e superfícies
- **ADRs owners:** ADR-002, ADR-028
- **Tecnologias principais:** FastAPI, Pydantic, OpenAPI

## Responsabilidade

Comandos e consultas REST, OpenAPI, SSE e polling de reconciliação.

## Boundaries de contrato

- Produz `adapta contratos` para `domain`.
- Produz `federação opcional` para `oidc`.
- Consome `REST/SSE/polling` de `web`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-002`, `BC-003`, `BC-004`, `BC-005`, `BC-006`, `BC-007`, `BC-008`, `BC-009`, `BC-010`, `BC-011`, `BC-012`, `BC-013`, `BC-014`, `BC-015`, `BC-016`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
