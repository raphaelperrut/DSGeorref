# COMP-015 — OIDC opcional

- **Camada:** Integrações externas
- **ADRs owners:** ADR-028
- **Tecnologias principais:** OIDC

## Responsabilidade

Federação opcional mantendo contas locais e autorização da instância.

## Boundaries de contrato

- Consome `federação opcional` de `api`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-002`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
