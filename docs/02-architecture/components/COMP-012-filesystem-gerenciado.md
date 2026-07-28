# COMP-012 — Filesystem gerenciado

- **Camada:** Persistência e transporte
- **ADRs owners:** ADR-018, ADR-041, ADR-027
- **Tecnologias principais:** Managed roots, SHA-256, COG

## Responsabilidade

Originais e ArtifactSets imutáveis, publicação atômica e checksums.

## Boundaries de contrato

- Consome `ArtifactSets/inputs` de `domain`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-013`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
