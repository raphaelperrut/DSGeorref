# COMP-005 — Pipeline geoespacial

- **Camada:** Núcleo de domínio e processamento
- **ADRs owners:** ADR-044, ADR-041, ADR-049, ADR-050
- **Tecnologias principais:** GDAL/PROJ/GEOS, OpenCV, RootSIFT, FLANN, USAC_MAGSAC

## Responsabilidade

Matching coarse-to-fine, homografia projetiva, GCPs, grafo e mosaico relativo.

## Boundaries de contrato

- Produz `submete candidatos` para `sgv`.
- Produz `escalona quando elegível` para `ai`.
- Produz `gateway governado` para `providers`.
- Consome `orquestra ProcessingPlan` de `domain`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-005`, `BC-006`, `BC-008`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
