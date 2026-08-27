# Design Review — contrato da fundação CLI/API/Web

## Escopo e decisão

`STORY-0011` congela o contrato mínimo que antecede a materialização do monorepo
de `EPIC-003`. A topologia permanece um monólito modular single-instance. CLI e
HTTP API são adapters sobre os mesmos application services; a Web consome a API
por contrato OpenAPI e, portanto, alcança o mesmo núcleo sem duplicar regra de
negócio. Esta entrega não implementa runtime, endpoint ou interface.

O contrato público `monorepo-foundation-contract` pertence a `BC-001`, versão
`1.0.0`, e registra explicitamente `REQ-TOP-001` e os quatro critérios:
`AC-ISSUE-0121-01`, `AC-ISSUE-0121-02`, `AC-ISSUE-0121-03` e
`AC-ISSUE-0121-04`.

## Autoridades e compatibilidade

Application services são a única autoridade semântica das três superfícies.
PostgreSQL/PostGIS é autoritativo para estado, o filesystem gerenciado para
binários publicados, RabbitMQ é somente transporte e telemetria é derivada.
Nenhuma interface pode acessar diretamente um store autoritativo.

O OpenAPI `3.1.0` versão `2.6.0` e o `OPERATION_CATALOG.json` versão `2.0.0`
permanecem congelados e não são alterados. O contrato desta história usa SemVer,
rejeita propriedades desconhecidas e exige nova major com revisão do Arquiteto
para mudança incompatível. Schema, exemplo, manifest e registro de ownership são
versionados no mesmo candidate.

## Estados de erro e fail-closed

Ausência de mapeamento semântico produz `SEMANTIC_MAPPING_MISSING`; versão não
suportada produz `CONTRACT_VERSION_UNSUPPORTED`; tentativa de criar outra
autoridade produz `AUTHORITY_VIOLATION`. Todos bloqueiam publicação. Fallback
silencioso, lógica local substituta e degradação para acesso direto são
proibidos. A validação negativa muta esses invariantes e exige rejeição do schema.

## Limite da ISSUE-0121

Materialização de CLI, API, Web, workspace, automação e integração pertence às
histórias downstream já existentes. `STORY-0012` e `STORY-0013` tornam-se apenas
elegíveis para revisão independente após este candidate; não são liberadas nem
implementadas aqui. Não há migration ou rollback operacional; rollback
contratual ocorre por revert antes do consumo ou por nova versão compatível.

## Evidência e gate independente

`cli_api_semantic_contract` prova que as três superfícies preservam a mesma
autoridade, o caminho Web→HTTP API→application services e as versões das fontes
congeladas. `test_epic_003_contrato` prova identidade, requisito, ownership,
grafo, TaskEnvelope e gate. O implementador entrega o estado
`READY_FOR_INDEPENDENT_REVIEW`; somente Reviewer distinto pode aprovar o mesmo
commit e liberar dependentes. Autoaprovação permanece proibida.

Risco residual para o próximo macro-passo: a equivalência de resultados em
runtime só poderá ser demonstrada pelas histórias de materialização e automação;
esta entrega congela o contrato verificável sem publicar claim de execução.
