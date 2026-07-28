# ADR-043 — Stack geoespacial nativa, ABI e isolamento

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-043`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-006` — Georreferenciamento, `BC-007` — Verificação Geométrica e Qualidade

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- Rasterio é adapter raster primário; GDAL isolado cobre capacidades não expostas.
- pyproj representa CRS/transformers; Shapely representa geometrias; OpenCV cobre visão.
- Drivers e VSI usam allowlist; arquivos externos são tratados como hostis.
- A imagem OCI fixa uma stack GDAL/PROJ/GEOS/OpenCV coerente e passa smoke ABI.

## Invariantes

- nenhuma implementação pode criar uma segunda autoridade para este boundary;
- parâmetros quantitativos permanecem em Application Profiles ou Benchmark Profiles;
- detalhes locais e reversíveis pertencem a issues, contratos ou código;
- contradição entre esta ADR e outro artifact interrompe a execução até reconciliação pelo Arquiteto.

## Alternativas consideradas

- manter a decisão agregada em uma ADR ampla: rejeitado por ocultar drivers, trade-offs e owners independentes;
- delegar a escolha à implementação: rejeitado por permitir divergência entre agentes e superfícies;
- transformar parâmetros reversíveis em ADR: rejeitado; profiles e benchmarks continuam sendo os owners desses valores.

## Racional da seleção

A opção selecionada reduz ambiguidade, limita o espaço de inferência dos agentes, permite auditoria independente e mantém um único owner normativo para uma decisão material.

## Consequências e trade-offs

- aumenta o número de ADRs e a disciplina de rastreabilidade;
- reduz o tamanho de cada contexto decisório e o risco de implementações redundantes;
- mudanças futuras precisam identificar exatamente qual boundary será substituído;
- integração entre decisões ocorre somente pelas dependências declaradas abaixo.

## Dependências arquiteturais

`ADR-009`, `ADR-042`

## Gate de mudança

Mudança que altere a autoridade, tecnologia estrutural, formato público, trust boundary, modelo de consistência ou direção de dependências deste boundary exige ADR substituta. Ajustes compatíveis e reversíveis seguem profiles, contratos e issues.

## Verificação de conformidade

- validators devem confirmar referência a IDs existentes e sequência contínua;
- histórias e TaskEnvelopes devem listar esta ADR quando modificarem o boundary;
- contratos, migrations, testes e evidence aplicáveis devem ser versionados no mesmo commit candidato;
- nenhuma decisão aberta pode ser completada por inferência do implementador.

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-ACC-001`, `REQ-DBSCHEMA-003`, `REQ-GOV-001`, `REQ-HOM-001`, `REQ-NATIVE-003`, `REQ-NATIVE-007`, `REQ-NATIVE-010`, `REQ-PRJ-001`
- **Épicos relacionados:** `EPIC-002`, `EPIC-008`, `EPIC-009`, `EPIC-010`, `EPIC-012`, `EPIC-021`, `EPIC-022`, `EPIC-023`, `EPIC-024`, `EPIC-026`, `EPIC-110`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`


## Especificações normativas — Fase E

Este boundary é concretizado por `SPEC-005`. Texto, schemas, exemplos e validadores dessas especificações são obrigatórios. Divergência bloqueia implementação e exige reconciliação pelo Arquiteto.
