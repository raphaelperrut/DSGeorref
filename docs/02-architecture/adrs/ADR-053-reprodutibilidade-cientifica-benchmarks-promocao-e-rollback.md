# ADR-053 — Reprodutibilidade científica, benchmarks, promoção e rollback

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-053`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-006` — Georreferenciamento, `BC-007` — Verificação Geométrica e Qualidade, `BC-008` — Mosaico Relativo, `BC-009` — Recuperação Assistida por IA e Governança de Modelos

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- Corpora são versionados, estratificados e separados em desenvolvimento, validação e holdout cego.
- DeterminismProfile inventaria seeds, RNGs, kernels e níveis de equivalência.
- Promoção é multidimensional; ganho em uma métrica não compensa falso aceite ou quebra de invariante.
- Bundles, profiles e ModelPacks promovidos são imutáveis e suportam shadow, canary e rollback.

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

`ADR-009`, `ADR-042`, `ADR-044`, `ADR-046`, `ADR-049`, `ADR-051`, `ADR-052`

## Gate de mudança

Mudança que altere a autoridade, tecnologia estrutural, formato público, trust boundary, modelo de consistência ou direção de dependências deste boundary exige ADR substituta. Ajustes compatíveis e reversíveis seguem profiles, contratos e issues.

## Verificação de conformidade

- validators devem confirmar referência a IDs existentes e sequência contínua;
- histórias e TaskEnvelopes devem listar esta ADR quando modificarem o boundary;
- contratos, migrations, testes e evidence aplicáveis devem ser versionados no mesmo commit candidato;
- nenhuma decisão aberta pode ser completada por inferência do implementador.

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-AIE-010`, `REQ-PRM-001`, `REQ-PRM-002`, `REQ-PRM-003`, `REQ-PRM-005`, `REQ-PRM-007`, `REQ-PRM-008`, `REQ-PRM-009`, `REQ-PRM-010`, `REQ-SCL-001`, `REQ-SCL-002`, `REQ-SCM-001`, `REQ-SCM-003`, `REQ-SCP-001`, `REQ-SDR-001`, `REQ-SDR-002`, `REQ-SDR-003`, `REQ-SDR-004`, `REQ-SRG-001`, `REQ-SRG-002`, `REQ-SRG-003`, `REQ-SRG-004`, `REQ-SRP-001`, `REQ-SRP-003`, `REQ-SRP-004`, `REQ-TST-001`
- **Épicos relacionados:** `EPIC-002`, `EPIC-004`, `EPIC-005`, `EPIC-006`, `EPIC-014`, `EPIC-018`, `EPIC-019`, `EPIC-021`, `EPIC-022`, `EPIC-023`, `EPIC-024`, `EPIC-028`, `EPIC-034`, `EPIC-037`, `EPIC-039`, `EPIC-040`, `EPIC-041`, `EPIC-043`, `EPIC-049`, `EPIC-050`, `EPIC-073`, `EPIC-076`, `EPIC-082`, `EPIC-092`, `EPIC-104`, `EPIC-105`, `EPIC-110`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`


## Especificações normativas — Fase E

Este boundary é concretizado por `SPEC-003`. Texto, schemas, exemplos e validadores dessas especificações são obrigatórios. Divergência bloqueia implementação e exige reconciliação pelo Arquiteto.
