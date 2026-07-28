# Reference Architecture — baseline consolidada

## Visão

DSGeorref é uma aplicação greenfield, single-instance e unificada. CLI, API, frontend e workers compartilham o mesmo núcleo de domínio e application services. PostgreSQL/PostGIS é o system of record; filesystem gerenciado armazena originals e artifacts; RabbitMQ transporta work units sem se tornar fonte de verdade.

## Boundaries canônicos

| Área | ADR |
|---|---|
| aplicação e superfícies | ADR-002 |
| persistência e artifacts | ADR-018 |
| identidade e proteção Web | ADR-028 |
| workers e transporte assíncrono | ADR-036 |
| instalação e deployment | ADR-034 |
| SGV e aceitação geométrica | ADR-046 |
| lote, scheduler e recursos | ADR-039 |
| pipeline e homografia | ADR-044 |
| providers e aquisição | ADR-047 |
| revisão e histórico | ADR-048 |
| backup e retenção | ADR-027 |
| observabilidade e audit | ADR-054 |
| IA e ModelPacks | ADR-051 |
| contrato geoespacial/raster | ADR-041 |
| mosaico relativo — grafo/âncoras | ADR-049 |
| mosaico relativo — qualidade/materialização | ADR-050 |
| reprodutibilidade/promoção | ADR-053 |
| compatibilidade e upgrades | ADR-026 |

## Fluxo principal

1. selecionar inputs por roots autorizados;
2. persistir snapshot e `ProcessingPlan`;
3. descobrir/adquirir referências autorizadas;
4. executar matching, homografia e SGV;
5. publicar `ArtifactSet` somente após aceitação;
6. agregar lote com sucesso parcial explícito;
7. encaminhar casos reviewable sem bloquear o lote;
8. preservar attempts, lineage, audit e evidência.

## Invariantes

- homografia projetiva é o modelo final canônico;
- SGV é fail-closed e não admite override de hard gate;
- original, attempt, CorrectionSet, ArtifactSet e snapshots são imutáveis;
- broker, logs e frontend nunca substituem PostgreSQL como estado autoritativo;
- CRS, datum, nodata, pixel semantics, hashes e lineage são sempre explícitos;
- nenhuma capacidade experimental ou de IA é apresentada como real sem evidence gate.

## Visão estratégica DDD

A arquitetura de runtime continua um monólito modular, mas suas fronteiras semânticas são os bounded contexts de `docs/02-architecture/ddd/`. Componentes técnicos implementam ou adaptam contexts; não possuem linguagem de negócio global. O core domain é formado por `BC-006`, `BC-007` e `BC-008`.
