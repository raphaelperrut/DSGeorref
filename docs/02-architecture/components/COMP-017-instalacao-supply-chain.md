# COMP-017 — Instalação + Supply Chain

- **Camada:** Capacidades transversais
- **ADRs owners:** ADR-034, ADR-026
- **Tecnologias principais:** OCI, Compose, SBOM

## Responsabilidade

OCI/Compose, TLS, secrets, SBOM, assinaturas, upgrades e rollback.

## Boundaries de contrato

- Nenhuma dependência de runtime declarada.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-015`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
